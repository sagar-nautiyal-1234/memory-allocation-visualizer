import tkinter as tk
from tkinter import ttk
from pages.allocation_tabs import show_allocation_tabs

def show_process_table(root, processes, memory_blocks):
    window = tk.Toplevel(root)
    window.title("Processes Table")
    window.geometry("700x500")
    window.minsize(500, 300)
    
    # Full-window light bg
    window.configure(bg="#E5F0FF")

    # Heading
    ttk.Label(window,
              text="Processes (Sorted by ID)",
              font=("Segoe UI", 12, "bold"),
              background="#E5F0FF").pack(pady=10)

    # Treeview
    tree = ttk.Treeview(
        window,
        columns=("ID", "Size", "Priority"),
        show="headings",
        selectmode="browse",
    )
    tree.heading("ID",       text="Process ID")
    tree.heading("Size",     text="Size")
    tree.heading("Priority", text="Priority")

    # --- Configure tags for coloring ---
    tree.tag_configure("high",   foreground="#10B981")
    tree.tag_configure("medium", foreground="#F59E0B")
    tree.tag_configure("low",    foreground="#EF4444")

    # Insert rows, tagging by p["priority"].lower()
    for p in processes:
        tag = p["priority"].lower()  # "high", "medium", or "low"
        tree.insert(
            "",
            "end",
            values=(
                p["id"],
                f'{p["size"]} KB',
                p["priority"].capitalize()
            ),
            tags=(tag,)
        )

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Proceed button
    ttk.Button(
        window,
        text="Proceed to Allocation",
        command=lambda: [
            window.destroy(),
            show_allocation_tabs(root, processes, memory_blocks)
        ]
    ).pack(pady=10)
