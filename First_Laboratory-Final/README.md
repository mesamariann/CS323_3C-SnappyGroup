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
> Orders were distributed by the master process using comm.send(), where each order was assigned to a worker process based on the available ranks. The distribution used a cycle-like approach so the tasks could be shared among workers instead of being handled by only one process.

2. **What happens if there are more orders than workers?**
> If there are more orders than workers, some workers receive and process more than one order. This still works because the orders are assigned one by one until all orders are handled.

3. **How did processing delays affect order completion?**
> The processing delays made some workers finish earlier or later depending on how long their assigned task took. Because of this, the completed orders did not always appear in the same order as they were originally assigned.

4. **How did you implement shared memory, and where was it initialized?**
> Shared memory was implemented using a shared list where completed orders were stored after processing. It was initialized in the master process before collecting the results from the workers.

5. **What issues occurred when multiple workers wrote to shared memory?**
> When multiple workers wrote to shared memory at the same time, the results could become inconsistent or appear in an unpredictable order. This showed why synchronization was needed when several processes access the same data.

6. **How did you ensure consistent results?**
> Consistent results were ensured by using a Lock() so only one process could write to the shared list at a time. This helped prevent race conditions and made sure the final list of completed orders was complete and reliable.

## Galendez

## Panandigan
