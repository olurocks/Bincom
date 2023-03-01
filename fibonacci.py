# Initialize variables for the first two numbers in the sequence
a = 0
b = 1

# Initialize a variable to keep track of the sum
sum = 0

# Loop through the first 50 numbers in the sequence
for i in range(50):
    # Add the current number to the sum
    sum += a
    
    # Calculate the next number in the sequence
    c = a + b
    
    # Update the values of a and b for the next iteration
    a = b
    b = c

# Print the sum
print(f"Sum of the first 50 Fibonacci numbers:{sum}")
