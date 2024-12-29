#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>

// Function prototypes
int get_length(long number);
bool check_luhn(long number);
int get_first_digits(long number, int n);

int main(void)
{
    // Get card number
    long number = get_long("Number: ");

    // Get length of number
    int length = get_length(number);

    // Check if length is valid and get first digits
    int first_two = get_first_digits(number, 2);
    int first_one = get_first_digits(number, 1);

    // Check Luhn's Algorithm
    bool is_valid = check_luhn(number);

    // If checksum is invalid, print INVALID
    if (!is_valid)
    {
        printf("INVALID\n");
        return 0;
    }

    // Check card type based on length and starting digits
    if (length == 15 && (first_two == 34 || first_two == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && (first_two >= 51 && first_two <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && first_one == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

// Get length of number
int get_length(long number)
{
    int length = 0;
    while (number > 0)
    {
        number = number / 10;
        length++;
    }
    return length;
}

// Implement Luhn's Algorithm
bool check_luhn(long number)
{
    int sum = 0;
    bool alternate = false;

    while (number > 0)
    {
        int digit = number % 10;

        if (alternate)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit = (digit % 10) + (digit / 10);
            }
        }

        sum += digit;
        alternate = !alternate;
        number = number / 10;
    }

    return (sum % 10 == 0);
}

// Get first n digits of number
int get_first_digits(long number, int n)
{
    while (number >= pow(10, n))
    {
        number = number / 10;
    }
    return number;
}
