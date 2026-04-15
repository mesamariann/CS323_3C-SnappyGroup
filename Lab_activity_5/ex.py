import random

def generate_data(n):
    data = [random.randint(1, 1000000) for _ in range(n)]
    return data

if __name__ == "__main__":
    print("Parallel vs Sequential Algorithms")
