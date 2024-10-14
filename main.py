import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt


def draw_divider(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x = width / 3
    canvas.create_line(x, 0, x, height, fill="black", width=2)


def create_components(canvas):
    mode_label = tk.Label(canvas, text="Number of modes:", bg="white", fg="black", font=("Arial", 10, "bold"), bd=2, relief="solid")
    mode_label.place(x=90, y=50)

    mode_entry_block = tk.Entry(canvas, bg="white", fg="black", font=("Arial", 14, "bold"), bd=2, relief="solid")
    mode_entry_block.place(x=105, y=80, width=90, height=30)

    samples_label = tk.Label(canvas, text="Number of samples:", bg="white", fg="black", font=("Arial", 10, "bold"), bd=2, relief="solid")
    samples_label.place(x=82, y=190)

    samples_entry_block = tk.Entry(canvas, bg="white", fg="black", font=("Arial", 14, "bold"), bd=2, relief="solid")
    samples_entry_block.place(x=105, y=220, width=90, height=30)

    generate_button = tk.Button(canvas, text="GENERATE", bg="red", fg="black", font=("Arial", 10, "bold"), bd=2, relief="solid", command=lambda: generate_and_plot(samples_entry_block.get(), mode_entry_block.get()))
    generate_button.place(x=105, y=350, width=90, height=30)

    refresh_button = tk.Button(canvas, text="REFRESH", bg="green", fg="black", font=("Arial", 10, "bold"), bd=2, relief="solid", command=lambda: reset_interface(samples_entry_block, mode_entry_block, canvas))
    refresh_button.place(x=105, y=450, width=90, height=30)


def generateGaussianModes(numModes, numSamples):
    rng = np.random.default_rng()
    rangeFirst = -1
    rangeLast = 1

    xSamples = []
    ySamples = []
    sampleLabels = []
    mode_centers = []

    for label in [0, 1]:
        for mode in range(numModes):
            mu_x = rng.uniform(rangeFirst, rangeLast)
            mu_y = rng.uniform(rangeFirst, rangeLast)
            sigma_x = rng.uniform(0.1, 1)
            sigma_y = rng.uniform(0.1, 1)

            x_samples = rng.normal(mu_x, sigma_x, numSamples)
            y_samples = rng.normal(mu_y, sigma_y, numSamples)

            xSamples.extend(x_samples)
            ySamples.extend(y_samples)
            sampleLabels.extend([label] * numSamples)

            mode_centers.append((mu_x, mu_y, label))

    return np.array(xSamples), np.array(ySamples), np.array(sampleLabels), mode_centers


def plot_samples(x, y, labels, mode_centers, point_size=10):
    figure = Figure(figsize=(5, 5))
    ax = figure.add_subplot(111)

    ax.scatter(x[labels == 0], y[labels == 0], color='blue', label='Class 0', s=point_size)
    ax.scatter(x[labels == 1], y[labels == 1], color='red', label='Class 1', s=point_size)

    square_size = 0.1

    for (mu_x, mu_y, label) in mode_centers:
        color = 'blue' if label == 0 else 'red'
        ax.add_patch(plt.Rectangle((mu_x - square_size / 2, mu_y - square_size / 2), square_size, square_size, color=color, alpha=0.5))

    ax.scatter([], [], color='blue', marker='s', label='Class 0 Mode', s=50)
    ax.scatter([], [], color='red', marker='s', label='Class 1 Mode', s=50)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    ax.set_title('Generated Data Samples')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    ax.legend()

    return figure


def generate_and_plot(num_samples, num_modes):
    try:
        numModes = int(num_modes)
        numSamples = int(num_samples)

        if numModes < 1 or numModes > 10:
            raise ValueError("Please enter a number of modes between 1 and 10.")

        if numSamples < 1 or numSamples > 100:
            raise ValueError("Please enter a number of samples between 1 and 100.")

        x, y, labels, mode_centers = generateGaussianModes(numModes, numSamples)

        figure = plot_samples(x, y, labels, mode_centers)

        canvas_plot = FigureCanvasTkAgg(figure, master=canvas)
        canvas_plot.get_tk_widget().place(x=320, y=20, width=580, height=560)
        canvas_plot.draw()

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


def reset_interface(samples_entry, modes_entry, canvas):
    samples_entry.delete(0, tk.END)
    modes_entry.delete(0, tk.END)

    for widget in canvas.winfo_children():
        widget.destroy()

    create_components(canvas)
    draw_divider(canvas)


root = tk.Tk()
root.geometry("902x600")
root.title("Data Generator and Visualizer")
root.maxsize(902, 600)
root.minsize(902, 600)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<Configure>", lambda event: draw_divider(canvas))

create_components(canvas)

root.mainloop()
