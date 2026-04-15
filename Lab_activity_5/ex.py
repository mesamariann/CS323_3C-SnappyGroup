import random

def generate_data(n):
    data = [random.randint(1, 1000000) for _ in range(n)]
    return data

if __name__ == "__main__":
    print("Parallel vs Sequential Algorithms")

def merge(left, right):
    
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(data):
    
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def sequential_search_merge(data, target):
    sorted_data = merge_sort(data)
    index = binary_search(sorted_data, target)
    return index


def choose_dataset():
    print("\nChoose dataset size:")
    print("1 - Small (1,000)")
    print("2 - Medium (100,000)")
    print("3 - Large (1,000,000)")

    choice = input("Enter choice: ")

    if choice == "1":
        n = 1000
    elif choice == "2":
        n = 100000
    elif choice == "3":
        n = 1000000
    else:
        print("Invalid choice, defaulting to small")
        n = 1000

    data = generate_data(n)

    print("\nSpecial case:")
    print("1 - Normal random")
    print("2 - Already sorted")
    print("3 - Reverse sorted")

    case = input("Enter choice: ")

    if case == "2":
        data = sorted(data)
    elif case == "3":
        data = sorted(data, reverse=True)

    return data


# main menu
def menu():
    print("\nSelect operation:")
    print("1 - Sequential Search (Merge Sort + Binary Search)")
    print("2 - Parallel Search (not implemented)")
    print("3 - Sequential Sort (not implemented)")
    print("4 - Parallel Sort (not implemented)")

    return input("Enter choice: ")


if __name__ == "__main__":
    print("Parallel vs Sequential Algorithms")

    data = choose_dataset()
    choice = menu()

    target = data[random.randint(0, len(data) - 1)]

    start = time.time()

    if choice == "1":
        index = sequential_search_merge(data, target)

        if index != -1:
            print("Found", target, "at index", index)
        else:
            print("Not found")

    elif choice == "2":
        print("Parallel search not implemented yet")

    elif choice == "3":
        print("Sequential sort not implemented yet")

    elif choice == "4":
        print("Parallel sort not implemented yet")

    else:
        print("Invalid option")

    end = time.time()

    print("Execution time:", end - start)
