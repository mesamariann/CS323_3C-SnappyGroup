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