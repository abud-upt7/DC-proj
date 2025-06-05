import pyperf


def cpu_heavy_task():
    x = 0
    for i in range(1_000_000):
        x += i * i


runner = pyperf.Runner()
runner.bench_func("CPU heavy computation", cpu_heavy_task)
