import csv
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
csv_file = "bubble_sort_benchmark.csv"
data = {"python_pure": [], "numpy_systolic": []}

with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        backend = row[0]
        exec_time = float(row[1])
        data[backend].append(exec_time)

# Define labels (array sizes)
sizes = [10, 100, 1000, 10000]
x = np.arange(len(sizes))  # X-axis positions

# Bar width and positions
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bars
bars1 = ax.bar(x - width/2, data["python_pure"], width, label="Pure Python", color='tab:blue')
bars2 = ax.bar(x + width/2, data["numpy_systolic"], width, label="NumPy Systolic", color='tab:orange')

# Log scale on Y-axis
ax.set_yscale("log")

# Axis labels and title
ax.set_xlabel("Array Size")
ax.set_ylabel("Execution Time (s, log scale)")
ax.set_title("Bubble Sort Execution Time Comparison")
ax.set_xticks(x)
ax.set_xticklabels([str(s) for s in sizes])
ax.legend()

# Annotate bars with formatted value
def annotate_bars(bars):
    for bar in bars:
        height = bar.get_height()
        if height < 0.001:
            # Convert to 10^-x format
            exponent = int(np.floor(np.log10(height)))
            base = height / (10 ** exponent)
            label = f'{base:.1f}×10^{exponent}'
        else:
            label = f'{height:.6f}'

        ax.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

annotate_bars(bars1)
annotate_bars(bars2)

plt.tight_layout()
plt.savefig("plots/bubble_sort_benchmark_plot.png", dpi=300)
plt.show()
