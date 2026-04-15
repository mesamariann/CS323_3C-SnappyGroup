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

# Parallel Merge Sort
def sort_worker(data, q):
    q.put(sequential_sort(data))


def parallel_sort(data):
    num_processes = 4
    chunk_size = len(data) // num_processes

    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    processes = []
    q = Queue()

    for chunk in chunks:
        p = Process(target=sort_worker, args=(chunk, q))
        processes.append(p)
        p.start()

    sorted_chunks = [q.get() for _ in processes]

    for p in processes:
        p.join()

    while len(sorted_chunks) > 1:
        left = sorted_chunks.pop(0)
        right = sorted_chunks.pop(0)
        sorted_chunks.append(merge(left, right))

    return sorted_chunks[0]

