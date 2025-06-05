import time
import random
import logging
import sys
print(">>> Script Started")
sys.stdout.flush()

# Configure logger
logger = logging.getLogger("CPUFixedPointBenchmark")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

def fixed_point_arithmetic(size):
    num = [1, 2, 3, 4]
    res = [0] * size
    j, k, l = 1, 2, 3
    ops_per_iteration = 0

    start = time.time()

    for i in range(size):
        j = (num[1] * (k - j) * (l - k)) % 1000                   # 1+1+1+1 = 4 ops
        k = (num[3] * k - (l - j) * k) % 1000                     # 1+1+1+1+1 = 5 ops
        l = ((l - k) * (num[2] + j)) % 1000                       # 1+1+1+1 = 4 ops
        res[(l - 2) % size] = j + k + l                  # 1+1+1+1+1 = 5 ops
        res[(k - 2) % size] = j * k * l                  # 1+1+1+1+1 = 5 ops
        ops_per_iteration += 23  # total ops this loop

    end = time.time()
    elapsed = end - start
    total_ops = ops_per_iteration * size
    mops = total_ops / elapsed / 1e6

    print(f"Fixed Point Arithmetic Benchmark:")
    sys.stdout.flush()
    print(f"Operations: {total_ops}")
    sys.stdout.flush()
    print(f"Time: {elapsed:.6f} seconds")
    sys.stdout.flush()
    print(f"MOPS: {mops:.2f}")
    sys.stdout.flush()

def branching_test(size):
    num = [0, 1, 2, 3]
    j = 1
    ops_per_iteration = 0

    start = time.time()

    for i in range(size):
        if j == 1:            # 1 op
            j = num[2]        # 1 + 1 = 2 ops
        else:
            j = num[3]        # 1 + 1 = 2 ops

        if j > 2:             # 1 op
            j = num[0]        # 1 + 1 = 2 ops
        else:
            j = num[1]        # 1 + 1 = 2 ops

        if j < 1:             # 1 op
            j = num[1]        # 1 + 1 = 2 ops
        else:
            j = num[0]        # 1 + 1 = 2 ops

        ops_per_iteration += 14

    end = time.time()
    elapsed = end - start
    total_ops = ops_per_iteration * size
    mops = total_ops / elapsed / 1e6

    print(f"Branching Benchmark:")
    sys.stdout.flush()
    print(f"Operations: {total_ops}")
    sys.stdout.flush()
    print(f"Time: {elapsed:.6f} seconds")
    sys.stdout.flush()
    print(f"MOPS: {mops:.2f}")
    sys.stdout.flush()

def array_access_test(size):
    a = list(range(size))
    b = [random.randint(0, size - 1) for _ in range(size)]
    c = [0] * size
    ops_per_iteration = 0

    start = time.time()

    for i in range(size):
        c[i] = a[b[i]]                  # 1+1+1 = 3 ops
        a[i], b[i] = b[i], a[i]         # 1+1+1+1 = 4 ops
        ops_per_iteration += 7

    end = time.time()
    elapsed = end - start
    total_ops = ops_per_iteration * size
    mops = total_ops / elapsed / 1e6

    print(f"Array Access Benchmark:")
    sys.stdout.flush()
    print(f"Operations: {total_ops}")
    sys.stdout.flush()
    print(f"Time: {elapsed:.6f} seconds")
    sys.stdout.flush()
    print(f"MOPS: {mops:.2f}")
    sys.stdout.flush()

# Run all benchmarks
def run_all(size=1000):
    fixed_point_arithmetic(size)
    branching_test(size)
    array_access_test(size)

if __name__ == "__main__":
    run_all(100000)