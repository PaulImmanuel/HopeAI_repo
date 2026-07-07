# filename: calculate_permutations.py

def factorial(n):
    """Calculate n!"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def count_unique_permutations(word):
    """Count the number of unique permutations of a word."""
    # Convert to lowercase and count the frequency of each character
    char_freq = {}
    for char in word.lower():
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1

    # Calculate the total number of permutations using the formula n! / (k1! * k2! * ... * km!)
    permutation_count = factorial(len(word))
    for freq in char_freq.values():
        permutation_count //= factorial(freq)

    return permutation_count

# Test with 'ALGEBRA'
word = "algebra"
print(count_unique_permutations(word))