import time
import torch
import csv

def systolic_bubble_sort_torch(tensor):
    tensor = tensor.clone()
    n = tensor.shape[0]

    for _ in range(n):
        # Even phase
        even_idx = torch.arange(0, n - 1, 2, device=tensor.device)
        left = tensor[even_idx]
        right = tensor[even_idx + 1]
        mask = left > right
        tensor[even_idx[mask]] = right[mask]
        tensor[even_idx[mask] + 1] = left[mask]

        # Odd phase
        odd_idx = torch.arange(1, n - 1, 2, device=tensor.device)
        left = tensor[odd_idx]
        right = tensor[odd_idx + 1]
        mask = left > right
        tensor[odd_idx[mask]] = right[mask]
        tensor[odd_idx[mask] + 1] = left[mask]

    return tensor

def benchmark_torch_systolic_sort():
    sizes = [10, 100, 1000, 10000]
    results = []

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    for size in sizes:
        run_times = []
        print(f"\nRunning PyTorch systolic sort on GPU for size = {size}")

        for run in range(25):
            data = torch.randint(0, 10000, (size,), device=device)

            # Time only the sorting
            start_time = time.time()
            sorted_tensor = systolic_bubble_sort_torch(data)
            end_time = time.time()
            run_times.append(end_time - start_time)

            # Check correctness (excluded from timing)
            if not torch.all(sorted_tensor[:-1] <= sorted_tensor[1:]):
                raise ValueError(f"Sort failed on run {run} for size {size}")

        avg_time = sum(run_times[2:]) / (len(run_times) - 2)
        print(f"Average execution time ({len(run_times) - 2} runs): {avg_time:.6f} sec")
        results.append(("torch_systolic_gpu", avg_time))

    # Append to CSV
    with open("bubble_sort_benchmark.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

if __name__ == "__main__":
    benchmark_torch_systolic_sort()
