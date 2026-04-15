import random
import time
from multiprocessing import Process, Queue


def generate_data(n):
    data = [random.randint(1, 1000000) for _ in range(n)]
    return data

# Sequential Merge Sort
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sequential_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = sequential_sort(data[:mid])
    right = sequential_sort(data[mid:])

    return merge(left, right)
