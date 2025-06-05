import time
import random
import math
import gc
from decimal import Decimal, getcontext
import sys
import logging

sys.setrecursionlimit(1_000_000)


import time


def benchmark(func, runs=10, unit="s"):
    """
    Benchmarks a function over multiple runs and outputs the execution time.

    Parameters:
    - func: The function to benchmark.
    - runs (int): The number of times to run the benchmark (default is 10).
    - unit (str): The time unit to display the result in. Options are "s" (seconds),
                  "ms" (milliseconds), "us" (microseconds). Default is "s".
    """
    # Dictionary to map time unit to a multiplier
    time_unit_multipliers = {
        "s": 1,  # seconds
        "ms": 1000,  # milliseconds
        "us": 1_000_000,  # microseconds
    }

    # Ensure the unit is valid
    if unit not in time_unit_multipliers:
        raise ValueError("Invalid time unit. Choose from 's', 'ms', or 'us'.")

    total_time = 0

    for i in range(runs):
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()

        duration = end_time - start_time
        # Convert the duration to the desired unit
        duration_in_unit = duration * time_unit_multipliers[unit]

        total_time += duration_in_unit
        print(f"Run {i+1}: {duration_in_unit:.3f} {unit}")

    total_time_in_unit = total_time
    print(f"Total execution time for {runs} runs: {total_time_in_unit:.3f} {unit}")


def generate_random_numbers():
    return [random.randint(0, 100) for _ in range(1000)]


def calculate_pi(precision):
    getcontext().prec = precision

    # Chudnovsky algorithm
    C = 426880 * Decimal(10005).sqrt()
    M = 1
    L = 13591409
    X = 1
    K = 6
    S = L
    for i in range(1, precision):
        M = (K**3 - 16 * K) * M // i**3
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12

    pi = C / S
    return str(pi)


def iterative_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def recursive_sum(n):
    if n == 1:
        return 1
    else:
        return n + recursive_sum(n - 1)


print("Benchmarking iterative sum:")
benchmark(lambda: iterative_sum(10000), runs=10, unit="ms")

print("\nBenchmarking recursive sum:")
benchmark(lambda: recursive_sum(10000), runs=10, unit="ms")

print("\nBenchmarking the digits of PI:")
benchmark(lambda: calculate_pi(500), runs=10, unit="s")
