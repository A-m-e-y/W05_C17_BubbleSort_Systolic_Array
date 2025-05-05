import time
import random
import csv

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def benchmark_bubble_sort():
    sizes = [10, 100, 1000, 10000]  # Increase upper limit as needed
    results = []

    for size in sizes:
        run_times = []
        print(f"\nRunning bubble sort for size = {size}")

        for run in range(100):
            data = [random.randint(0, 10000) for _ in range(size)]
            start_time = time.time()
            bubble_sort(data)
            end_time = time.time()
            duration = end_time - start_time
            run_times.append(duration)

        # Exclude first 2 runs
        avg_time = sum(run_times[2:]) / (len(run_times) - 2)
        print(f"Average execution time (98 runs): {avg_time:.6f} sec")
        results.append(("python_pure", avg_time))

    # Write to CSV
    with open("bubble_sort_benchmark.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["backend", "exe time"])
        writer.writerows(results)

if __name__ == "__main__":
    benchmark_bubble_sort()
