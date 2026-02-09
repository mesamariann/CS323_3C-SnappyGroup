from multiprocessing import Process, Manager, Lock
import time

def process_subject(grade, subject_id, shared_results, lock):
    """
    Handles the computation for a single subject (PROCESS).
    """
    time.sleep(0.1)

    with lock:
        print(f"[Process-{subject_id}] Subject {subject_id} processed → Grade: {grade}")
        shared_results.append(grade)


def main():
    num_subjects = int(input("Enter number of subjects: "))
    grades = []

    for i in range(num_subjects):
        grade = float(input(f"Enter grade for subject {i + 1}: "))
        grades.append(grade)

    start_time = time.time()

    with Manager() as manager:
        results = manager.list()     
        lock = Lock()              
        processes = []

        for index, grade in enumerate(grades, start=1):
            process = Process(
                target=process_subject,
                args=(grade, index, results, lock)
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        gwa = sum(results) / len(results)

    end_time = time.time()

    print("\nAll subject processes completed.")
    print(f"Final GWA: {gwa:.2f}")
    print(f"Multiprocessing Execution Time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
