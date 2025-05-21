import tkinter as tk
import sys
from tkinter import ttk
from utils.data_generator import generate_data
from pages.process_table import show_process_table
from utils import data_generator
from themes.style import apply_theme_styles

def launch_main_window():
    root = tk.Tk()
    root.title("Memory Allocation Simulator")
    root.geometry("400x250")
    root.minsize(300, 200)

    # Apply Fluent theme styles (widgets will float on top of canvas)
    apply_theme_styles(root)

    # Full-window Canvas for blob background
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Container frame (transparent) for your widgets
    frame = ttk.Frame(root, padding=20)
    # We’ll place it centered—canvas is underneath
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Redraw blobs on resize
    def draw_blobs(event=None):
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        # First blob
        canvas.create_oval(-0.5*w, -0.3*h, 1.1*w, 1.2*h,
                           fill="#A0CFFF", outline="")
        # Second blob
        canvas.create_oval(0.2*w, -0.4*h, 1.5*w, 1.3*h,
                           fill="#C0E0FF", outline="")
    canvas.bind("<Configure>", draw_blobs)

    # Widgets
    title_label = ttk.Label(frame, text="Memory Allocation Simulator",
                            font=("Segoe UI", 18, "bold"))
    title_label.pack(pady=(0, 10))

    ttk.Label(frame, text="Enter number of processes:").pack()
    process_entry = ttk.Entry(frame)
    process_entry.pack()

    error_label = ttk.Label(frame, text="", foreground="red")
    error_label.pack(pady=(5, 0))

    def start_simulation():
        try:
            process_count = int(process_entry.get())
            if process_count <= 0:
                raise ValueError
        except ValueError:
            error_label.config(text="Please enter a valid positive integer.")
            return

        data_generator.number_of_processes = process_count
        process_list, memory_blocks = generate_data()
        show_process_table(root, process_list, memory_blocks)

    ttk.Button(frame, text="Start Simulation",
               command=start_simulation).pack(pady=10)

    def on_closing():
        root.destroy()
        sys.exit(0)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()