# filename: permutation.py

import math

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

def calculate_permutations(word):
    # Calculate the total number of permutations
    total_permutations = 1
    for char in word:
        total_permutations *= factorial(len(word) - word.count(char))

    return math.isclose(total_permutations, int(total_permutations)) and int(total_permutations) or math.inf

word = "ALGEbRA"
print(calculate_permutations(word))