#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height (1-8)
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Loop through each row
    for (int row = 0; row < height; row++)
    {
        // Print spaces for left pyramid
        // We need (height - 1) - row spaces
        for (int space = 0; space < height - 1 - row; space++)
        {
            printf(" ");
        }

        // Print hashes for left pyramid
        // We need row + 1 hashes
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }

        // Print gap (always 2 spaces)
        printf("  ");

        // Print hashes for right pyramid
        // We need row + 1 hashes again
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }

        // Move to next line
        printf("\n");
    }
}
