# Get height (1-8)
while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= 8:
            break
    except ValueError:
        continue

# For each row
for i in range(height):
    # Print leading spaces
    print(" " * (height - i - 1), end="")

    # Print left-side hashes
    print("#" * (i + 1), end="")

    # Print the middle gap
    print("  ", end="")

    # Print right-side hashes
    print("#" * (i + 1))
