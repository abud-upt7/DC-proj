import os
import pyperf


def write_read_disk():
    size_mb = 100
    file_path = "test_file.bin"
    data = os.urandom(size_mb * 1024 * 1024)

    with open(file_path, "wb") as f:
        f.write(data)

    with open(file_path, "rb") as f:
        _ = f.read()

    os.remove(file_path)


runner = pyperf.Runner()
runner.bench_func("Disk Write and Read", write_read_disk)
