### 1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.

**Answer:**
Task Parallelism and Data Parallelism differ in how concurrent workloads are structured and executed. Task Parallelism involves running different operations at the same time on the same data, while Data Parallelism applies the same operation concurrently to multiple data elements.

In this Third Laboratory Activity, Part A demonstrates Task Parallelism by executing separate deduction computations (SSS, PhilHealth, Pag-IBIG, and withholding tax) simultaneously for a single employee. Each task operates on the same salary value, and the workload is divided by deduction type.

Part B demonstrates Data Parallelism by applying one payroll computation function to multiple employees in parallel. In this case, the workload is divided by employee records, allowing each employee’s payroll to be processed independently.

---

### 2. Explain how concurrent.futures managed execution, including submit(),map(), and Future objects. Discuss the purpose of with when creating an Executor.

**Answer:**
The concurrent.futures module helps run tasks at the same time using something called Executors. Executors are objects that manage and control worker threads or processes, deciding how tasks are started and run in parallel.

The submit() method sends a function to the executor to run and gives back a Future object. A Future is like a placeholder for a result that is not ready yet. You can call .result() on it to get the answer once the task is done.

The map() method runs the same function on many inputs at the same time. It is easier to use than submit() when you want to work with a list of items, like employee records.

The with statement is used when creating an Executor to make sure everything is cleaned up properly. When the block of code ends, the executor shuts down automatically. This helps avoid memory problems and makes sure all threads or processes are closed correctly

---

### 3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur?

**Answer:**
ThreadPoolExecutor uses multiple threads within a single Python process, but execution is limited by Python’s Global Interpreter Lock (GIL), which allows only one thread to execute Python bytecode at a time. Because the payroll deduction computations in this laboratory are CPU-bound, true parallel execution across multiple CPU cores does not occur. Although tasks appear to run concurrently, the operating system time-slices the threads, resulting in limited performance gains.

Therefore, ThreadPoolExecutor does not achieve true parallelism in this scenario and is more suitable for I/O-bound tasks.

---

### 4. Explain why ProcessPoolExecutor enables true parallelism, including memory space separation and GIL behavior.

**Answer:**
ProcessPoolExecutor uses separate processes instead of threads. Each process has its own memory and its own Python interpreter. This means every process has its own Global Interpreter Lock (GIL).

Because the processes are separate and each has its own GIL, they can run at the same time on different CPU cores. This makes true parallel processing possible for CPU-heavy tasks, like large salary calculations. The operating system handles each process separately, allowing the computer to use multiple cores fully.

---

### 5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why?

**Answer:**
In this activity, Part A uses ThreadPoolExecutor to calculate different deductions for one employee at the same time. This works fine for a few employees, but Python threads are limited by the GIL, so CPU-heavy tasks can’t run fully in parallel. If we had 10,000 employees, threads would be slow because they can’t use all CPU cores effectively.

Part B uses ProcessPoolExecutor to compute payroll for each employee in separate processes. Each process runs independently on a CPU core, allowing true parallelism. This makes it much faster and scalable for thousands of employees.

For lots of employees, ProcessPoolExecutor is faster because it can do many calculations at the same time. For a few employees or tasks that just read/write files or wait for something, ThreadPoolExecutor works fine.

---

### 6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.

**Answer:**
In a big company, such as a bank, payroll has to handle thousands of employees. For each person, the system needs to calculate their gross pay, subtract deductions like taxes, insurance, and retirement contributions, determine their net salary, create their payslip, and update their payroll information in the HR database.

Task Parallelism: For one employee, different payroll tasks like calculating deductions, creating the payslip, and saving the record to the database can be done at the same time. Each task works on its own, so running them together speeds up the process. ThreadPoolExecutor is a good choice here because many of these tasks involve waiting for files or databases, and they can run at the same time even if they don’t use much CPU.

Data Parallelism: When processing payroll for 10,000 employees, the same steps calculating gross salary, deductions, and net pay can be done for all employees at the same time. Each employee’s payroll can run in its own process using ProcessPoolExecutor. This lets multiple CPU cores work in parallel, making it much faster to complete a large payroll batch.
