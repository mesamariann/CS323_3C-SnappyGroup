# Galleros

# Galendez
In this activity, I learned the difference between sequential and parallel algorithms through actual implementation. The sequential approach was easier to understand because everything runs step by step. I used merge sort for sorting and binary search for searching, and I noticed that most of the execution time is spent on sorting rather than searching.

When testing different dataset sizes, the program became slower as the data increased, especially for large inputs. However, the behavior stayed consistent even with sorted or reverse sorted data because merge sort always divides the data the same way.

One challenge I encountered was making sure the data is sorted before applying binary search. I also had to be careful with how the index is returned since it is based on the sorted array.

Overall, I realized that sequential algorithms are simple and efficient for smaller datasets. Parallel algorithms may be faster for large data, but they also introduce more complexity and overhead, so they are not always the better choice.

# Mesa
When comparing sequential and parallel execution in our code, the main difference I observed is how the tasks are handled. Sequential execution follows a single flow, like in our recursive merge sort and linear search, which made it easier to implement and debug. In contrast, the parallel version splits the data into chunks and assigns them to multiple processes using `multiprocessing`, which makes the execution faster but also more complex. In terms of performance, sequential execution worked better for smaller datasets because it avoids the extra overhead, while parallel execution started to perform better as the dataset size increased, especially during sorting where chunks can be processed simultaneously.

One challenge I encountered during implementation was handling synchronization and merging, particularly in the parallel merge sort where sorted chunks needed to be combined correctly. Managing queues and ensuring all processes finished properly also added difficulty. I also realized that process creation and communication introduce overhead, which can actually slow things down for smaller inputs. From this, I learned that parallelism is most beneficial when the dataset is large enough to justify the added complexity and overhead, but for smaller datasets or simpler tasks like quick searches, sequential execution is still the more efficient and practical choice.

