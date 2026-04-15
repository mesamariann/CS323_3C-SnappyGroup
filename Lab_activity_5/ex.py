import random
import time
from multiprocessing import Process, Queue
from concurrent.futures import ProcessPoolExecutor

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
def search_chunk(chunk_data, target, offset):
    for i, value in enumerate(chunk_data):
        if value == target:
            return offset + i
    return None

def parallel_search(data, target, num_workers=4):
    n = len(data)
    chunk_size = (n + num_workers - 1) // num_workers
    chunks = [
        (data[i : i + chunk_size], target, i) 
        for i in range(0, n, chunk_size)
    ]
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(search_chunk, *c) for c in chunks]
        for future in futures:
            result = future.result()
            if result is not None:
                return result
    return -1

if __name__ == "__main__":
    N = 1000000
    data = generate_data(N)
    target = data[random.randint(0, N-1)]
    
    print(f"--- Testing Search (Target: {target}) ---")
    start_search = time.time()
    idx = parallel_search(data, target)
    end_search = time.time()
    print(f"Parallel Search Result Index: {idx}")
    print(f"Search Time: {end_search - start_search:.4f}s\n")

    print(f"--- Testing Sort (N={N}) ---")
    start_sort = time.time()
    sorted_res = parallel_sort(data)
    end_sort = time.time()
    print(f"Sort Time: {end_sort - start_sort:.4f}s")
    print(f"Is Sorted: {sorted_res == sorted(data)}")
