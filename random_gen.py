import random

# Generate a random 4-digit binary number
binary_num = ''.join([str(random.randint(0, 1)) for i in range(4)])

# Convert binary to decimal
decimal_num = int(binary_num, 2)

# Print the results
print("Binary number:", binary_num)
print("Decimal equivalent:", decimal_num)
