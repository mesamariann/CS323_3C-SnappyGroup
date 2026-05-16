import sys
sys.stdout.reconfigure(encoding='utf-8')

from mpi4py import MPI
from multiprocessing import Lock
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Master process (rank 0) generates orders and distributes them to workers
if rank == 0:
    lock = Lock()

    items = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard",
             "Mouse", "Headset", "Webcam"]
    num_orders = random.randint(5, 8)
    orders = [{"id": i + 1, "item": items[i % len(items)]}
              for i in range(num_orders)]

    print(f"[Master] Generated {num_orders} orders\n")

    num_workers = size - 1
    for i, order in enumerate(orders):
        target_worker = (i % num_workers) + 1
        comm.send(order, dest=target_worker, tag=1)
        print(f"[Master] Sent Order #{order['id']} ({order['item']}) -> Worker {target_worker}")

    for w in range(1, size):
        comm.send(None, dest=w, tag=0)

    # Collect results with Lock — only one write at a time
    completed = []
    for _ in range(num_orders):
        result = comm.recv(source=MPI.ANY_SOURCE, tag=2)
        with lock:
            completed.append(result)
            print(f"[Master] [LOCKED] Stored Order #{result['id']} "
                  f"from Worker {result['worker']}")

    print("\n[Master] Consistent and complete final list:")
    for entry in sorted(completed, key=lambda x: x["id"]):
        print(f"  Order #{entry['id']} | {entry['item']:10s} "
              f"| Worker {entry['worker']} | {entry['delay']:.2f}s")

else:
    while True:
        status = MPI.Status()
        order = comm.recv(source=0, status=status)

        if status.Get_tag() == 0:
            break

        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)

        print(f"[Worker {rank}] Processed Order #{order['id']} ({order['item']}) in {delay:.2f}s")

        result = {
            "id":     order["id"],
            "item":   order["item"],
            "worker": rank,
            "delay":  delay
        }
        comm.send(result, dest=0, tag=2)