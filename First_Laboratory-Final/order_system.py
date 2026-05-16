from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 

# Task Distribution
if rank == 0:
    # Master generates orders
    items = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard",
             "Mouse", "Headset", "Webcam"]
    num_orders = random.randint(5, 8)
    orders = [{"id": i + 1, "item": items[i % len(items)]}
              for i in range(num_orders)]
    
    print(f"[Master] Generated {num_orders} orders: {orders}\n")
    
    num_workers = size - 1
    for i, order in enumerate(orders):
        target_worker = (i % num_workers) + 1 
        comm.send(order, dest=target_worker, tag=1)
    

    for w in range(1, size):
        comm.send(None, dest=w, tag=0)  

else:
    # Workers receive and process orders
    while True:
        status = MPI.Status()
        order = comm.recv(source=0, status=status)
        
        if status.Get_tag() == 0:  # stop signal
            break
        
        print(f"[Worker {rank}] Received order #{order['id']} — {order['item']}")