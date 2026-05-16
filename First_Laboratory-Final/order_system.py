from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

# Task Distribution
if rank == 0:
    manager = Manager()
    shared_orders = manager.list()  # shared across all processes
    
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
    
    for w in range(1, size):
        comm.send(None, dest=w, tag=0)
    
    # Wait for all workers to finish
    comm.Barrier()
    
    print("\n[Master] All completed orders:")
    for completed in shared_orders:
        print(f"  Order #{completed['id']} — {completed['item']} "
              f"(handled by Worker {completed['worker']})")

else:
    # Workers receive and process orders
    while True:
        status = MPI.Status()
        order = comm.recv(source=0, status=status)
        
        if status.Get_tag() == 0:  # stop signal
            break

        # add delay 
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)

        result = {"id": order["id"], "item": order["item"], "worker": rank}
        shared_orders.append(result)  # write to shared memory
        
        print(f"[Worker {rank}] Processed order #{order['id']} "
              f"({order['item']}) in {delay:.2f}s")
        
    comm.Barrier()  # wait for all workers to finish