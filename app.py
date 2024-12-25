import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, get_time, check_password

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    portfolio = db.execute("SELECT * FROM portfolios WHERE user_id = ?", user_id)
    cash_left = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    # Getting the amount of cash the user has left to spend
    if cash_left and "cash" in cash_left[0]:
        cash_left = float(cash_left[0]["cash"])
    else:
        cash_left = 0.0

    total_amount = cash_left

    # Updating the current price and the overall stock value for each stock
    try:
        for stock in portfolio:
            symbol = stock["symbol"]
            stock_info = lookup(symbol)

            current_price = float(stock_info["price"])
            stock_value = current_price * stock["shares"]

            stock.update({"current_price": current_price, "stock_value": stock_value})
            total_amount += float(stock["stock_value"])
    except (ValueError, LookupError):
        return apology("Failed to update stock prices!")

    return render_template("index.html", portfolio=portfolio, cash_left=cash_left, total_amount=total_amount)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive number of shares", 400)

        # Look up quote
        quote = lookup(symbol)
        if quote is None:
            return apology("symbol not found", 400)

        # Calculate total cost
        shares = int(shares)
        cost = shares * quote["price"]

        # Check if user can afford
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cost > user_cash:
            return apology("can't afford", 400)

        # Update user's cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash - cost, user_id)

        # Add to portfolio
        db.execute(
            "INSERT INTO portfolios (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, quote["symbol"], shares, quote["price"]
        )

        flash("Bought!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM portfolios WHERE user_id = ? ORDER BY timestamp DESC", user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if quote is None:
            return apology("symbol not found", 400)

        return render_template("quoted.html", quote=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            # Check for empty fields
            if not username:
                return apology("must provide username", 400)
            if not password:
                return apology("must provide password", 400)
            if not confirmation:
                return apology("must provide confirmation", 400)

            # Check for password to be the same
            if password != confirmation:
                return apology("passwords do not match", 400)

            # Make sure the name isn't registered already
            existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(existing_user) != 0:
                return apology("username already exists", 400)

            # Hash password and insert new user
            hash = generate_password_hash(password)
            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

            if not result:
                return apology("registration error", 400)

            # Log them in
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

        except Exception as e:
            print(f"Registration error: {str(e)}")
            return apology("registration error", 400)

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive number of shares", 400)

        shares = int(shares)

        # Check user owns enough shares
        user_shares = db.execute(
            "SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?",
            user_id, symbol
        )

        if not user_shares or shares > user_shares[0]["shares"]:
            return apology("not enough shares", 400)

        # Look up current price
        quote = lookup(symbol)
        if quote is None:
            return apology("symbol not found", 400)

        # Calculate sale proceeds
        proceeds = shares * quote["price"]

        # Update user's cash
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            proceeds, user_id
        )

        # Update portfolio
        current_shares = user_shares[0]["shares"]
        if shares == current_shares:
            db.execute(
                "DELETE FROM portfolios WHERE user_id = ? AND symbol = ?",
                user_id, symbol
            )
        else:
            db.execute(
                "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
                current_shares - shares, user_id, symbol
            )

        flash("Sold!")
        return redirect("/")

    # GET request - display form
    symbols = db.execute(
        "SELECT symbol FROM portfolios WHERE user_id = ? GROUP BY symbol", user_id
    )
    return render_template("sell.html", symbols=symbols)
