import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

    # Get user's stocks and shares
    holdings = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    # Initialize lists for stock data
    stocks = []
    total_value = 0

    # Get current price for each stock and add to list
    for holding in holdings:
        stock = lookup(holding["symbol"])

        # Calculate total value for this stock
        total = stock["price"] * holding["total_shares"]
        total_value += total

        # Add stock data to list
        stocks.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": holding["total_shares"],
            "price": stock["price"],
            "total": total
        })

    # Get user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Calculate grand total (stocks + cash)
    grand_total = cash + total_value

    # Render template with all data
    return render_template("index.html",
        stocks=stocks,
        cash=cash,
        grand_total=grand_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate symbol
        if not symbol:
            return apology("must provide symbol", 400)

        # Validate shares
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive", 400)
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        # Look up stock
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        # Calculate total cost
        total_cost = stock["price"] * shares

        # Check if user can afford the purchase
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if total_cost > user_cash:
            return apology("can't afford", 400)

        # Add transaction to database
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], stock["symbol"], shares, stock["price"])

        # Update user's cash
        db.execute("""
            UPDATE users
            SET cash = cash - ?
            WHERE id = ?
        """, total_cost, session["user_id"])

        # Flash a success message
        flash(f"Bought {shares} shares of {stock['symbol']} for {usd(total_cost)}!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Look up quote
        stock = lookup(symbol)

        # Ensure valid symbol
        if stock is None:
            return apology("invalid symbol", 400)

        # Display quote
        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        if not confirmation:
            return apology("must confirm password", 400)

        # Ensure passwords match
        if password != confirmation:
            return apology("passwords must match", 400)

        # Add the user to the database and handle duplicate username
        try:
            id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password)
            )
        except ValueError:
            return apology("username already exists", 400)

        # Log the user in
        session["user_id"] = id

        # Redirect to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate symbol
        if not symbol:
            return apology("must provide symbol", 400)

        # Validate shares
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive", 400)
        except (ValueError, TypeError):
            return apology("shares must be a positive integer", 400)

        # Query database for user's shares of this stock
        holdings = db.execute("""
            SELECT SUM(shares) as total_shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, session["user_id"], symbol)

        # Check if user owns the stock
        if not holdings:
            return apology("symbol not found in portfolio", 400)

        user_shares = holdings[0]["total_shares"]

        # Check if user has enough shares
        if shares > user_shares:
            return apology("too many shares", 400)

        # Look up stock's current price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        # Calculate sale proceeds
        proceeds = stock["price"] * shares

        # Record the sale (negative number of shares represents a sale)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], symbol, -shares, stock["price"])

        # Update user's cash
        db.execute("""
            UPDATE users
            SET cash = cash + ?
            WHERE id = ?
        """, proceeds, session["user_id"])

        # Flash success message
        flash(f"Sold {shares} shares of {symbol} for {usd(proceeds)}!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get user's stocks for the select menu
        stocks = db.execute("""
            SELECT symbol, SUM(shares) as total_shares
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING total_shares > 0
        """, session["user_id"])

        return render_template("sell.html", stocks=stocks)
