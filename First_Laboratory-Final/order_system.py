from mpi4py import MPI
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
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

    # Collect results from workers
    completed = []
    for _ in range(num_orders):
        result = comm.recv(source=MPI.ANY_SOURCE, tag=2)
        completed.append(result)

    print("\n[Master] Final completed orders:")
    for entry in sorted(completed, key=lambda x: x["id"]):
        print(f"  Order #{entry['id']} | {entry['item']:10s} "
              f"| Worker {entry['worker']} | {entry['delay']:.2f}s")

else:
    while True:
        status = MPI.Status()
        order = comm.recv(source=0, status=status)

        if status.Get_tag() == 0:
            break

        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)

        print(f"[Worker {rank}] Processed Order #{order['id']} ({order['item']}) in {delay:.2f}s")

        # Send result back to master
        result = {
            "id":     order["id"],
            "item":   order["item"],
            "worker": rank,
            "delay":  delay
        }
        comm.send(result, dest=0, tag=2)