import math
from collections import Counter

def count_permutations_with_repetition(word):
    """
    Calculates the number of unique permutations for a given word
    with repeating characters.
    """
    n = len(word)
    
    # Calculate n!
    numerator = math.factorial(n)
    
    # Count occurrences of each character
    char_counts = Counter(word)
    
    denominator = 1
    # For each character that appears more than once,
    # multiply the denominator by the factorial of its count
    for count in char_counts.values():
        denominator *= math.factorial(count)
            
    return numerator // denominator

word = "ALGEBRA"
result = count_permutations_with_repetition(word.upper()) # Ensure case-insensitivity for counting

print(f"The number of unique permutations for the word '{word}' is: {result}")