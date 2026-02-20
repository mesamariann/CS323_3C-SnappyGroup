import time
import threading
from queue import Queue




class PrintOrder:
    def __init__(self, order_id):
        self.order_id = order_id



def edit_and_format(order, edit_time):
    print(f"[Editing] Order {order.order_id} - START")
    time.sleep(edit_time)
    print(f"[Editing] Order {order.order_id} - DONE")


def print_document(order, print_time):
    print(f"[Printing] Order {order.order_id} - START")
    time.sleep(print_time)
    print(f"[Printing] Order {order.order_id} - DONE")


def finishing(order, finish_time):
    print(f"[Finishing] Order {order.order_id}")
    time.sleep(finish_time)


def payment(order, payment_time):
    print(f"[Payment] Order {order.order_id} completed\n")
    time.sleep(payment_time)

    # Sequential Implementation

def run_sequential(num_orders, edit_time, print_time, finish_time, payment_time):
    print("\n===== SEQUENTIAL EXECUTION =====\n")
    start = time.time()

    orders = [PrintOrder(i) for i in range(num_orders)]

    for order in orders:
        edit_and_format(order, edit_time)
        print_document(order, print_time)
        finishing(order, finish_time)
        payment(order, payment_time)

    end = time.time()
    return end - start

# Parallel Implementation

def run_parallel(num_orders, edit_time, print_time, finish_time, payment_time):
    print("\n===== PARALLEL EXECUTION =====\n")

    input_queue = Queue()
    ready_to_print_queue = Queue()
    printer_lock = threading.Lock()

    for i in range(num_orders):
        input_queue.put(PrintOrder(i))

    input_queue.put(None)

    def editing_worker():
        while True:
            order = input_queue.get()
            if order is None:
                ready_to_print_queue.put(None)
                break

            edit_and_format(order, edit_time)
            ready_to_print_queue.put(order)

    def printing_worker():
        while True:
            order = ready_to_print_queue.get()
            if order is None:
                break

            with printer_lock:
                print_document(order, print_time)

            finishing(order, finish_time)
            payment(order, payment_time)

            start = time.time()

    thread_edit = threading.Thread(target=editing_worker)
    thread_print = threading.Thread(target=printing_worker)

    thread_edit.start()
    thread_print.start()

    thread_edit.join()
    thread_print.join()

    end = time.time()
    return end - start

def main():
    print("=== Alrose Printing Service Simulation ===")

    num_orders = int(input("Enter number of orders: "))
    edit_time = float(input("Enter editing time per order (seconds): "))
    print_time = float(input("Enter printing time per order (seconds): "))
    finish_time = float(input("Enter finishing time per order (seconds): "))
    payment_time = float(input("Enter payment time per order (seconds): "))

    seq_time = run_sequential(num_orders, edit_time, print_time, finish_time, payment_time)
    print(f"\nSequential Time: {seq_time:.2f} seconds")

    par_time = run_parallel(num_orders, edit_time, print_time, finish_time, payment_time)
    print(f"\nParallel Time: {par_time:.2f} seconds")

    speedup = seq_time / par_time
    print(f"\nSpeedup Achieved: {speedup:.2f}x")


if __name__ == "__main__":
    main()