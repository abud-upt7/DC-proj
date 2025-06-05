import os
import time

TEMP_DIR = r"D:\Faculta\AN 2 SEM 2\dc"
os.makedirs(TEMP_DIR, exist_ok=True)

def write_benchmark(file_path, file_size_bytes, buffer_size_bytes):
    buffer = bytearray(buffer_size_bytes)
    written = 0
    t0 = time.perf_counter()
    with open(file_path, "wb") as f:
        while written < file_size_bytes:
            write_size = min(buffer_size_bytes, file_size_bytes - written)
            f.write(buffer[:write_size])
            written += write_size
    t1 = time.perf_counter()
    mb_written = file_size_bytes / 1024 / 1024
    elapsed = t1 - t0
    return mb_written / elapsed  # MB/s

def run_fixed_file_size(file_size_mb, buffer_sizes_kb, repeats=5):
    results = []
    file_size_bytes = file_size_mb * 1024 * 1024
    for buffer_kb in buffer_sizes_kb:
        buffer_size_bytes = buffer_kb * 1024
        speeds = []
        for r in range(repeats):
            file_path = os.path.join(TEMP_DIR, f"fs_{buffer_kb}KB_{r}.dat")
            speed = write_benchmark(file_path, file_size_bytes, buffer_size_bytes)
            speeds.append(speed)
            os.remove(file_path)
        avg_speed = sum(speeds) / len(speeds)
        result_row = [buffer_kb] + speeds + [avg_speed]
        results.append(result_row)
    return results

def run_fixed_buffer_size(buffer_kb, file_sizes_mb, repeats=5):
    results = []
    buffer_size_bytes = buffer_kb * 1024
    for file_mb in file_sizes_mb:
        file_size_bytes = file_mb * 1024 * 1024
        speeds = []
        for r in range(repeats):
            file_path = os.path.join(TEMP_DIR, f"fb_{file_mb}MB_{r}.dat")
            speed = write_benchmark(file_path, file_size_bytes, buffer_size_bytes)
            speeds.append(speed)
            os.remove(file_path)
        avg_speed = sum(speeds) / len(speeds)
        result_row = [file_mb] + speeds + [avg_speed]
        results.append(result_row)
    return results

def save_to_csv(filename, header, data):
    with open(filename, "w", newline="") as f:
        f.write(",".join(header) + "\n")
        for row in data:
            f.write(",".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in row) + "\n")

def main():
    fs_file_size = 512
    fs_buffer_sizes = [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536]
    fb_buffer_size = 2
    fb_file_sizes = [1, 10, 100, 1024]
    repeats = 5

    # Fixed file size
    print("Running 'fs' (fixed file size) tests...")
    fs_header = ["Buffer Size (KB)"] + [f"Run {i+1} (MB/s)" for i in range(repeats)] + ["Average (MB/s)"]
    fs_results = run_fixed_file_size(fs_file_size, fs_buffer_sizes, repeats)
    save_to_csv("fs_results.csv", fs_header, fs_results)

    # Fixed buffer size
    print("Running 'fb' (fixed buffer size) tests...")
    fb_header = ["File Size (MB)"] + [f"Run {i+1} (MB/s)" for i in range(repeats)] + ["Average (MB/s)"]
    fb_results = run_fixed_buffer_size(fb_buffer_size, fb_file_sizes, repeats)
    save_to_csv("fb_results.csv", fb_header, fb_results)

    # Print summaries to screen
    print("\n--- Fixed File Size (fs) results ---")
    print(",".join(fs_header))
    for row in fs_results:
        print(",".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in row))

    print("\n--- Fixed Buffer Size (fb) results ---")
    print(",".join(fb_header))
    for row in fb_results:
        print(",".join(f"{x:.2f}" if isinstance(x, float) else str(x) for x in row))

    print("\nResults saved as fs_results.csv and fb_results.csv. Open them in Excel for graphs!")

if __name__ == "__main__":
    main()
