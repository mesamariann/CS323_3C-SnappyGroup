# Individual Reflections: Distributed Order Processing
## Galleros
1. **How did you distribute orders among worker processes?**
> Orders were distributed evenly by the master process (rank 0) to workers
using comm.send(). Each order was assigned using
(order_index % num_workers) + 1 to cycle through available workers.

2. **What happens if there are more orders than workers?**
> Workers receive multiple orders sequentially. A worker finishes
one order and receives the next, so no order is skipped or lost.

3. **How did processing delays affect order completion?**
> Workers with shorter delays finished earlier, causing results to
arrive at master out of original order. This is visible in the
output where Order #2 was stored before Order #1.

4. **How did you implement shared memory, and where was it initialized?**
> A Python list (completed) was initialized in the master process.
Workers sent results back to master via MPI messages using tag=2,
and master appended each result to the list under a Lock().

5. **What issues occurred when multiple workers wrote to shared memory?**
> Without synchronization, concurrent writes could cause race conditions
resulting in lost entries or inconsistent ordering. This was observed
when running without Lock() where results arrived unpredictably.

6. **How did you ensure consistent results?**
> A Lock() was used as a context manager (with lock:) around each
append() call in the master process, ensuring only one result
was written at a time and producing a complete, consistent final list.

## Mesa

## Betonio
1. **How did you distribute orders among worker processes?**
> 

2. **What happens if there are more orders than workers?**
> 

3. **How did processing delays affect order completion?**
> 

4. **How did you implement shared memory, and where was it initialized?**
>

5. **What issues occurred when multiple workers wrote to shared memory?**
> 

6. **How did you ensure consistent results?**
> 

## Galendez

## Panandigan
