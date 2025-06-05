import numpy as np
import pyperf


def ram_speed_test():
    a = np.random.rand(100_000_000)
    b = np.random.rand(100_000_000)
    _ = a + b


runner = pyperf.Runner()
runner.bench_func("RAM array addition", ram_speed_test)
