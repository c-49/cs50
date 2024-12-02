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

    // For each row
    for (int i = 0; i < height; i++)
    {
        // Print leading spaces
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }

        // Print left-side hashes
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        // Print the middle gap
        printf("  ");

        // Print right-side hashes
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        // Move to next line
        printf("\n");
    }
}
