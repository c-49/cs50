#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Points assigned to each letter
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int score = 0;
    // Loop through each character in the word
    for (int i = 0; i < strlen(word); i++)
    {
        if (isalpha(word[i]))  // Check if it's a letter
        {
            // Convert to uppercase and find position in alphabet (A=0, B=1, etc.)
            int letter_index = toupper(word[i]) - 'A';
            // Add corresponding score from POINTS array
            score += POINTS[letter_index];
        }
    }
    return score;
}
