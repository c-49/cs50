import math

def count_letters(text):
    return sum(1 for char in text if char.isalpha())

def count_words(text):
    # Start at 1 because last word won't have space after it
    return 1 + sum(1 for char in text if char == ' ')

def count_sentences(text):
    return sum(1 for char in text if char in '.!?')

# Get input text from user
text = input("Text: ")

# Count letters, words, and sentences
letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

# Calculate averages per 100 words
L = letters / words * 100
S = sentences / words * 100

# Calculate Coleman-Liau index
index = 0.0588 * L - 0.296 * S - 15.8

# Round to nearest integer
grade = round(index)

# Print grade level
if grade >= 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {grade}")
