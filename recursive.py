def recursive_search(numbers, target):
    if not numbers:
        return False
    elif numbers[0] == target:
        return True
    else:
        return recursive_search(numbers[1:], target)

numbers = [1, 3, 5, 7, 9]
target = int(input("Enter a number to search for: "))
found = recursive_search(numbers, target)
if found:
    print("The number is in the list.")
else:
    print("The number is not in the list.")
