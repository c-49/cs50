from math import pow

def get_length(number):
    length = 0
    while number > 0:
        number = number // 10  # Use integer division in Python
        length += 1
    return length

def check_luhn(number):
    sum = 0
    alternate = False

    while number > 0:
        digit = number % 10

        if alternate:
            digit *= 2
            if digit > 9:
                digit = (digit % 10) + (digit // 10)

        sum += digit
        alternate = not alternate
        number = number // 10

    return (sum % 10 == 0)

def get_first_digits(number, n):
    while number >= pow(10, n):
        number = number // 10
    return number

# Main program
try:
    # Get card number
    number = int(input("Number: "))

    # Get length of number
    length = get_length(number)

    # Get first digits
    first_two = get_first_digits(number, 2)
    first_one = get_first_digits(number, 1)

    # Check Luhn's Algorithm
    is_valid = check_luhn(number)

    # If checksum is invalid, print INVALID
    if not is_valid:
        print("INVALID")

    # Check card type based on length and starting digits
    elif length == 15 and (first_two == 34 or first_two == 37):
        print("AMEX")
    elif length == 16 and (51 <= first_two <= 55):
        print("MASTERCARD")
    elif (length == 13 or length == 16) and first_one == 4:
        print("VISA")
    else:
        print("INVALID")

except ValueError:
    print("INVALID")
