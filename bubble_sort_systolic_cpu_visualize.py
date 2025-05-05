import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

def generate_systolic_steps(arr):
    arr = arr.copy()
    n = len(arr)
    steps = []

    for phase in range(n):
        swaps = []
        if phase % 2 == 0:
            indices = range(0, n - 1, 2)  # Even phase
        else:
            indices = range(1, n - 1, 2)  # Odd phase

        for i in indices:
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps.append((i, i + 1))

        steps.append((arr.copy(), swaps))

    return steps

def animate_systolic_array_hwstyle(arr, save_gif=True, gif_name="plots/systolic_array_hw.gif"):
    steps = generate_systolic_steps(arr)
    n = len(arr)

    fig, ax = plt.subplots(figsize=(1.5 * n, 3))
    ax.set_xlim(-1, n)
    ax.set_ylim(-2, 3)
    ax.axis("off")

    # Draw PE boxes and labels
    pe_boxes = []
    pe_labels = []
    value_texts = []
    for i in range(n):
        box = patches.FancyBboxPatch((i - 0.4, 0), 0.8, 1.2,
                                     boxstyle="round,pad=0.05", edgecolor='black', facecolor='lightgrey', linewidth=2)
        ax.add_patch(box)
        pe_boxes.append(box)

        pe_label = ax.text(i, 1.4, f"PE{i}", ha='center', fontsize=10, fontweight='bold')
        pe_labels.append(pe_label)

        val_text = ax.text(i, 0.6, "", ha='center', fontsize=14, fontweight='bold')
        value_texts.append(val_text)

    # Clock label
    clock_text = ax.text(n // 2, -1.2, "", ha='center', fontsize=12, fontweight='bold')

    # Arrows for swaps
    arrows = []

    def init():
        for txt in value_texts:
            txt.set_text("")
        clock_text.set_text("")
        return value_texts + pe_labels + arrows

    def update(frame_idx):
        nonlocal arrows
        # Remove old arrows
        for arrow in arrows:
            arrow.remove()
        arrows.clear()

        values, swaps = steps[frame_idx]

        for i in range(n):
            value_texts[i].set_text(str(values[i]))

        for i, j in swaps:
            arrow = ax.annotate("",
                                xy=(j, 0.4), xytext=(i, 0.4),
                                arrowprops=dict(arrowstyle="->", color="red", lw=2))
            arrows.append(arrow)

        clock_text.set_text(f"Clock Cycle: {frame_idx}")
        return value_texts + pe_labels + arrows + [clock_text]

    ani = animation.FuncAnimation(fig, update, init_func=init,
                                  frames=len(steps), interval=800, blit=True)

    if save_gif:
        ani.save(gif_name, writer='pillow', fps=1)
        print(f"Saved animation as '{gif_name}'")

    plt.show()

if __name__ == "__main__":
    np.random.seed(0)
    data = np.random.randint(0, 100, size=10)
    print("Initial data:", data)
    animate_systolic_array_hwstyle(data)
