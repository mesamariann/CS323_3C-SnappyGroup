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


# Sequential Linear Search
def sequential_search(data, target):
    for i, value in enumerate(data):
        if value == target:
            return i
    return -1

# Parallel Search
def search_worker(sub_data, target, offset, q):
    for i, value in enumerate(sub_data):
        if value == target:
            q.put(i + offset)
            return
    q.put(-1)


def parallel_search(data, target):
    num_processes = 4
    chunk_size = len(data) // num_processes
    
    processes = []
    q = Queue()
    
    for i in range(num_processes):
        start_idx = i * chunk_size
        # Handle the remainder for the last process
        end_idx = len(data) if i == num_processes - 1 else (i + 1) * chunk_size
        sub_data = data[start_idx:end_idx]
        
        p = Process(target=search_worker, args=(sub_data, target, start_idx, q))
        processes.append(p)
        p.start()
        
    results = []
    for _ in range(num_processes):
        res = q.get()
        if res != -1:
            results.append(res)
            
    for p in processes:
        p.join()
        
    return min(results) if results else -1


# Testing
def run_test(size):
    print(f"\nTesting size: {size}")

    data = generate_data(size)
    target = data[len(data)//2]

    start = time.time()
    sequential_sort(data.copy())
    print("Sequential Sort:", time.time() - start)

    start = time.time()
    parallel_sort(data.copy())
    print("Parallel Sort:", time.time() - start)

    start = time.time()
    sequential_search(data, target)
    print("Sequential Search:", time.time() - start)

    start = time.time()
    parallel_search(data, target)
    print("Parallel Search:", time.time() - start)


if __name__ == "__main__":
    run_test(1000)       
    run_test(100000)     
    run_test(1000000)     
