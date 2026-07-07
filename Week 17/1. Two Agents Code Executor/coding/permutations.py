# filename: permutations.py
from math import factorial

def count_unique_permutations(word):
  """Counts the number of unique permutations of a word.

  Args:
    word: The word to count the permutations of.

  Returns:
    The number of unique permutations of the word.
  """

  # Create a dictionary to store the count of each letter in the word.
  letter_counts = {}
  for letter in word:
    if letter not in letter_counts:
      letter_counts[letter] = 0
    letter_counts[letter] += 1

  # Calculate the number of unique permutations of the word.
  num_permutations = factorial(len(word))
  for letter_count in letter_counts.values():
    num_permutations //= factorial(letter_count)

  return num_permutations


# Verify the output using the word 'ALGEBRA'.
word = 'ALGEBRA'
num_permutations = count_unique_permutations(word)
print(num_permutations)  # Output: 2520