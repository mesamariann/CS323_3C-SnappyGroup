from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Task deduction functions
def compute_sss(salary):
    return salary * 0.045

def compute_philhealth(salary):
    return salary * 0.025

def compute_pagibig(salary):
    return salary * 0.02

def compute_tax(salary):
    return salary * 0.10


# PART A – TASK PARALLELISM
def task_parallelism(employee):
    name, salary = employee

    print("\nPART A – TASK PARALLELISM")
    print("Employee Name:", name)
    print("Gross Salary:", salary)

    with ThreadPoolExecutor(max_workers=4) as executor:
        deductions = {
            "SSS": executor.submit(compute_sss, salary),
            "PhilHealth": executor.submit(compute_philhealth, salary),
            "Pag-IBIG": executor.submit(compute_pagibig, salary),
            "Tax": executor.submit(compute_tax, salary),
        }

        total = 0
        for label, future in deductions.items():
            amount = future.result()
            total += amount
            print(label, ":", amount)

        print("Total Deduction:", total)


# PART B – DATA PARALLELISM
def compute_payroll(employee):
    name, salary = employee
    total = salary * (0.045 + 0.025 + 0.02 + 0.10)
    net = salary - total
    return name, salary, total, net


def data_parallelism(employees):
    print("\nPART B – DATA PARALLELISM")

    with ProcessPoolExecutor() as executor:
        results = executor.map(compute_payroll, employees)

        for name, salary, total, net in results:
            print("\nEmployee Name:", name)
            print("Gross Salary:", salary)
            print("Total Deduction:", total)
            print("Net Salary:", net)


# MAIN
if __name__ == "__main__":
    employees = [
        ("Alice", 25000),
        ("Bob", 32000),
        ("Charlie", 28000),
        ("Diana", 40000),
        ("Edward", 35000)
    ]

    task_parallelism(employees[0])
    data_parallelism(employees)