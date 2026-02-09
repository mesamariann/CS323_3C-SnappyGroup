from multiprocessing import Process, Manager, Lock
import time
import os


def print_header():
    print("=" * 50)
    print("         GWA Calculator with Multiprocessing")
    print("=" * 50)

def print_separator():
    print("-" * 50)

def process_subject(grade, subject_id, shared_results, lock):
    """
    Handles the computation for a single subject (PROCESS).
    """
    time.sleep(0.1)

    with lock:
        # Styled print with some design
        print(f"┌─ Process-{subject_id} ────────────────────────────────────┐")
        print(f"│ Subject {subject_id} processed → Grade: {grade:.2f}              │")
        print(f"└────────────────────────────────────────────────┘")
        shared_results.append(grade)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
    print_header()
    
    try:
        num_subjects = int(input("Enter number of subjects: "))
        if num_subjects <= 0:
            raise ValueError("Number of subjects must be positive.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    grades = []
    print_separator()
    for i in range(num_subjects):
        try:
            grade = float(input(f"Enter grade for subject {i + 1}: "))
            if not (0 <= grade <= 100):  
                raise ValueError("Grade must be between 0 and 100.")
            grades.append(grade)
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid grade.")
            return

    print_separator()
    print("Starting multiprocessing computation...")
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

        gwa = sum(results) / len(results) if results else 0

    end_time = time.time()

    print_separator()
    print("All subject processes completed.")
    print(f"Final GWA: {gwa:.2f}")
    print(f"Multiprocessing Execution Time: {end_time - start_time:.4f} seconds\n")
    print_separator()
    print("Thank you for using the GWA Calculator!")
    print("=" * 50)

if __name__ == "__main__":
    main()