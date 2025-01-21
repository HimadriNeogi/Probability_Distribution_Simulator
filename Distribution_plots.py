import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import mode
import seaborn as sns

# Create the main application window
root = tk.Tk()
root.title("Distribution Simulator")
root.geometry("1200x750")
root.configure(bg="#e8f0f2")

# Heading Frame for the project title
heading_frame = tk.Frame(root, bg="#37474f", relief="raised", bd=4)  #Add a border width of 4 pixels to give 3D effect
heading_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10)) #sticky="ew" stretches the frame horizontally (East-West) to fill the width of its grid cell

# Project Title Label
title_label = tk.Label(
    heading_frame,
    text="PROBABILITY DISTRIBUTION SIMULATOR",
    font=("Helvetica", 30, "bold"),  
    fg="white",  #White text for contrast
    bg="#37474f",  #Charcoal Grey background
    relief="flat",
    padx=10,  #Add padding around the text
)
title_label.pack(pady=20)  #Add spacing within the frame

def update_parameters(event):
    """Updates parameter input fields based on the selected distribution."""
    dist = distribution_var.get()
    if dist == "Binomial Distribution":
        param1_label.config(text="n (trials)")
        param2_label.config(text="p (probability)")
        param1_entry.grid()
        param2_entry.grid()
        param2_label.grid()
    elif dist == "Poisson Distribution":
        param1_label.config(text="λ (average number of occurences)")
        param2_entry.grid_remove()
        param2_label.grid_remove()
    elif dist == "Geometric Distribution":
        param1_label.config(text="p (probability)")
        param2_entry.grid_remove()
        param2_label.grid_remove()
    elif dist == "Uniform Distribution":
        param1_label.config(text="a (low)")
        param2_label.config(text="b (high)")
        param1_entry.grid()
        param2_entry.grid()
        param2_label.grid()
    elif dist == "Normal Distribution":
        param1_label.config(text="μ (mean)")
        param2_label.config(text="σ (standard deviation)")
        param1_entry.grid()
        param2_entry.grid()
        param2_label.grid()
    elif dist == "Exponential Distribution":
        param1_label.config(text="1/λ (scale)")
        param2_entry.grid_remove()
        param2_label.grid_remove()

def plot_distribution():
    """Plots the selected distribution with the chosen visualization type."""
    ax.clear()
    dist = distribution_var.get()
    plot_type = plot_type_var.get()
    try:
        param1 = float(param1_entry.get())
        param2 = float(param2_entry.get()) if param2_entry.winfo_ismapped() else None
        size = int(size_entry.get())
    except ValueError:
        result_label.config(text="Please enter valid numeric parameters.", fg="red")
        return

    # Generate data for each distribution
    if dist == "Binomial Distribution":
        data = np.random.binomial(n=int(param1), p=param2, size=size)
    elif dist == "Poisson Distribution":
        data = np.random.poisson(lam=param1, size=size)
    elif dist == "Geometric Distribution":
        data = np.random.geometric(p=param1, size=size)
    elif dist == "Uniform Distribution":
        data = np.random.uniform(low=param1, high=param2, size=size)
    elif dist == "Normal Distribution":
        data = np.random.normal(loc=param1, scale=param2, size=size)
    elif dist == "Exponential Distribution":
        data = np.random.exponential(scale=param1, size=size)
    else:
        raise ValueError(f"Unknown distribution!", fg="red")

    # Plot based on selected type
    if plot_type == "Histogram":
        ax.hist(data, bins=25, color='skyblue', edgecolor='black')
    elif plot_type == "CDF":
        sorted_data = np.sort(data)
        cdf = np.arange(len(sorted_data)) / float(len(sorted_data))
        ax.plot(sorted_data, cdf, color='skyblue', label="CDF")
        ax.legend()
    
    ax.set_title(f"{dist} Distribution ({plot_type})")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency" if plot_type == "Histogram" else "Probability")
    canvas.draw()
    result_label.config(text="Plot generated successfully!", fg="green")

    # Calculate statistics
    mean_val = np.mean(data)
    median_val = np.median(data)
    variance_val = np.var(data)
    std_dev_val = np.std(data)

    # Update statistics labels
    mean_label.config(text=f"Mean: {mean_val:.3f}")
    median_label.config(text=f"Median: {median_val:.3f}")
    variance_label.config(text=f"Variance: {variance_val:.3f}")
    std_dev_label.config(text=f"Standard Deviation: {std_dev_val:.3f}")

def export_plot():
    """Exports the current plot as an image file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
    )
    if file_path:
        fig.savefig(file_path)
        result_label.config(text="Plot exported successfully!", fg="green")

# Main layout frames
plot_frame = tk.Frame(root, bg="#f8f8f8")
plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

input_frame = tk.Frame(root, bg="#f5f5f5", bd=2, relief="solid")
input_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Configure column and row weights
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# Left frame: Matplotlib figure setup
fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Parent Frame for Center Alignment
right_parent_frame = tk.Frame(root, bg="#f8f8f8")  
right_parent_frame.grid(row=1, column=1, sticky="nsew")
root.grid_columnconfigure(1, weight=1)  

# Center-align the Input Frame inside the Parent Frame
input_frame = tk.Frame(right_parent_frame, bg="#f5f5f5", bd=2, relief="solid")
input_frame.pack(expand=True, padx=50, pady=50) 

# Right frame: Input fields and controls
distribution_var = tk.StringVar(value="Binomial Distribution")
distribution_label = tk.Label(input_frame, text="Select Distribution:", font=("Helventica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
distribution_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Configure the dropdown menu font size
root.option_add("*TCombobox*Listbox*Font", ("Helventica", 16))

# Increase font size of Combobox options
style = ttk.Style()
style.configure("TCombobox", font=("Helventica", 16))

distribution_dropdown = ttk.Combobox(
    input_frame, textvariable=distribution_var, state="readonly", font=("Helventica", 16), style="TCombobox"
)
distribution_dropdown['values'] = (
    "Binomial Distribution",
    "Poisson Distribution",
    "Geometric Distribution",
    "Uniform Distribution",
    "Normal Distribution",
    "Exponential Distribution"
)
distribution_dropdown.bind("<<ComboboxSelected>>", update_parameters)
distribution_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Parameter inputs
param1_label = tk.Label(input_frame, text="Parameter 1:", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
param1_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
param1_entry = tk.Entry(input_frame, font=("Helvetica", 16))
param1_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

param2_label = tk.Label(input_frame, text="Parameter 2:", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
param2_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
param2_entry = tk.Entry(input_frame, font=("Helvetica", 16))
param2_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

size_label = tk.Label(input_frame, text="Sample Size:", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
size_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
size_entry = tk.Entry(input_frame, font=("Helvetica", 16))
size_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

plot_type_var = tk.StringVar(value="Histogram")
plot_type_label = tk.Label(input_frame, text="Plot Type:", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
plot_type_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
plot_type_dropdown = ttk.Combobox(input_frame, textvariable=plot_type_var, state="readonly", font=("Helvetica", 16))
plot_type_dropdown['values'] = ("Histogram", "CDF")
plot_type_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

result_label = tk.Label(input_frame, text="", font=("Helvetica", 16), bg="#f5f5f5", fg="#37474f")
result_label.grid(row=5, column=0, columnspan=2, pady=5)

plot_button = tk.Button(input_frame, text="Plot Distribution", command=plot_distribution, font=("Helvetica", 18, "bold"), bg="#00796a", fg="#ffffff")
plot_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")

export_button = tk.Button(input_frame, text="Export Plot", command=export_plot, font=("Helvetica", 18, "bold"), bg="#0288cf", fg="white")
export_button.grid(row=12, column=0, columnspan=2, pady=0, sticky="nsew")

# Statistics labels
mean_label = tk.Label(input_frame, text="Mean: N/A", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
mean_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=5, pady=5)

median_label = tk.Label(input_frame, text="Median: N/A", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
median_label.grid(row=9, column=0, columnspan=2, sticky="w", padx=5, pady=5)

variance_label = tk.Label(input_frame, text="Variance: N/A", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
variance_label.grid(row=10, column=0, columnspan=2, sticky="w", padx=5, pady=5)

std_dev_label = tk.Label(input_frame, text="Standard Deviation: N/A", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#37474f")
std_dev_label.grid(row=11, column=0, columnspan=2, sticky="w", padx=5, pady=5)
update_parameters(None)
root.mainloop()