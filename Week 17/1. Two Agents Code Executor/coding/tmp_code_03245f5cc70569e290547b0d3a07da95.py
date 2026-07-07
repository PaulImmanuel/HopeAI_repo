import math

# The word is ALGEbRA
word = "ALGEbRA"

# Calculate total number of letters
n = len(word)

# Count occurrences of each character
from collections import Counter
char_counts = Counter(word)

# Calculate the denominator for repeated characters
denominator = 1
for count in char_counts.values():
    denominator *= math.factorial(count)

# Calculate the total number of unique permutations
result = math.factorial(n) // denominator

print(f"The word is: {word}")
print(f"Total number of letters: {n}")
print(f"Letter counts: {char_counts}")
print(f"The final count of unique permutations is: {result}")