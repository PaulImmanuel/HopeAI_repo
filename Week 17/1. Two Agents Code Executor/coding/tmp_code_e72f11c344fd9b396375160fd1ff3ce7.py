def calculate_permutations(word):
    n = len(word)
    result = 1
    
    for i in range(1, n+1):
        result *= i
    
    return result

# Test the function with the word 'ALGEBRA'
print(calculate_permutations('ALGEBRA'))