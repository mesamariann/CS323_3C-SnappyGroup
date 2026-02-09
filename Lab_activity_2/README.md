# Lab Activity 2: Exploring Multithreading and Multiprocessing in Python

This lab compares **multithreading** and **multiprocessing** in Python by computing grades for multiple subjects concurrently. Below are the results, analysis, and explanations.

---

## Recorded Results

| Method         | Execution Order              | GWA Output                                  | Execution Time |
|----------------|------------------------------|---------------------------------------------|----------------|
| Multithreading | 1 → 8 → 7 → 6 → 5 → 4 → 3 → 2 | 1.50, 1.75, 2.00, 2.25, 2.50, 2.50, 2.75, 3.00 | 0.1032 sec |
| Multiprocessing| 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 | 1.50, 1.75, 2.00, 2.25, 2.50, 2.50, 2.75, 3.00 | 0.4029 sec |

---
## Output Table Discussion
The outputs may appear in different orders for threads and processes because of how the operating system schedules them. In multithreading, all threads share the same memory space, but the OS decides which thread runs at any given moment, so threads may complete in a non-deterministic order, causing shuffled outputs. In multiprocessing, each process runs independently with its own memory space, and the OS schedules them across CPU cores, so even if processes are started sequentially, their execution happens in parallel, resulting in outputs appearing out of order. To optimize the code for faster execution, unnecessary delays like `time.sleep()` can be reduced, and for CPU-bound tasks, the number of processes can be matched to the available CPU cores. For I/O-bound tasks, multithreading is more efficient because context switching is lighter than creating new processes. For better readability, results can be collected in a shared list and sorted before printing, or a separate “printer” function or process can handle displaying outputs in the correct order. Structuring the code with clear functions for computation and output also improves clarity and maintainability.

##  Group Lab Questions and Answers

### 1. Which approach demonstrates true parallelism in Python?

**Answer:**  
Multiprocessing achieves true parallelism by running separate processes on multiple CPU cores, each with its own memory and interpreter. Multithreading is limited by Python’s **Global Interpreter Lock (GIL)**, so threads cannot run Python code simultaneously.

---

### 2. Compare execution times between multithreading and multiprocessing

**Answer:**  
- Multiprocessing has higher overhead due to creating separate processes, but it excels at CPU-bound tasks.  
- Multithreading is lighter and better for I/O-bound tasks, though it cannot speed up CPU-heavy work because of the GIL.  

**Observed results:**  
- Multithreading: **0.103 seconds**  
- Multiprocessing: **0.403 seconds**  

In this activity, the task mostly involved waiting (simulated with `time.sleep`), which benefits from concurrency. Therefore, multithreading performed faster, while multiprocessing took longer despite true parallelism.

---

### 3. Can Python handle true parallelism using threads? Why or why not?

**Answer:**  
No. Python threads cannot achieve true parallelism for CPU-bound tasks because the **GIL** allows only one thread to run Python bytecode at a time. Threads are suitable for concurrency and I/O-bound tasks but cannot execute CPU-bound tasks in parallel.

---

### 4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?

**Answer:**  
- Multiprocessing distributes tasks across multiple CPU cores, making it faster for large CPU-bound workloads.  
- Multithreading is limited by the GIL, so it may not speed up CPU-heavy tasks but can still handle I/O-bound tasks efficiently.

---

### 5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?

**Answer:**  
- **CPU-bound tasks:** Multiprocessing (bypasses GIL, uses all CPU cores).  
- **I/O-bound tasks:** Multithreading (threads can wait for input/output efficiently with low overhead).

---

### 6. How did your group apply creative coding or algorithmic solutions in this lab?

**Answer:**  
In this activity, we used both multithreading and multiprocessing to calculate grades for multiple subjects at the same time. We wrote a function that handles each subject’s grade processing and made sure that when different threads or processes add their results to a shared list, they don’t interfere with each other by using locks. For multiprocessing, we used a special shared list from Python’s Manager to safely share data between processes. For multithreading, we used a threading lock to protect the shared list. This way, we were able to run the tasks concurrently and safely collect the results. Our code helped us see the difference between how threads and processes work in Python and compare their speeds.  



   
