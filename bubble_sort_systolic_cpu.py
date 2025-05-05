import time
import numpy as np
import csv

def systolic_bubble_sort_numpy(arr):
    arr = arr.copy()
    n = arr.shape[0]

    for _ in range(n):
        # Even phase
        even_idx = np.arange(0, n - 1, 2)
        left = arr[even_idx]
        right = arr[even_idx + 1]
        mask = left > right
        arr[even_idx[mask]], arr[even_idx[mask] + 1] = right[mask], left[mask]

        # Odd phase
        odd_idx = np.arange(1, n - 1, 2)
        left = arr[odd_idx]
        right = arr[odd_idx + 1]
        mask = left > right
        arr[odd_idx[mask]], arr[odd_idx[mask] + 1] = right[mask], left[mask]

    return arr


def benchmark_numpy_systolic_sort():
    sizes = [10, 100, 1000, 10000]
    results = []

    for size in sizes:
        run_times = []
        print(f"\nRunning NumPy systolic sort for size = {size}")

        for run in range(25):
            data = np.random.randint(0, 10000, size=size)

            # Benchmark only the sorting logic
            start_time = time.time()
            sorted_arr = systolic_bubble_sort_numpy(data)
            end_time = time.time()

            run_times.append(end_time - start_time)

            # ✔️ Due diligence check (excluded from timing)
            if not np.all(np.diff(sorted_arr) >= 0):
                print(f"sorted array: {sorted_arr}")
                raise ValueError(f"Sort failed on run {run} for size {size}")

        # Compute average excluding first 2 warmup runs
        avg_time = sum(run_times[2:]) / (len(run_times) - 2)
        print(f"Average execution time ({len(run_times) - 2} runs): {avg_time:.6f} sec")
        results.append(("numpy_systolic", avg_time))

    # Append to CSV
    with open("bubble_sort_benchmark.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

if __name__ == "__main__":
    benchmark_numpy_systolic_sort()
