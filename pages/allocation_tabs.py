import tkinter as tk
from tkinter import ttk
from utils.memory_allocator import allocate_memory
from utils.tooltip import TooltipManager
from pages.comparison_summary import show_comparison_summary

def draw_block_diagram(canvas, allocation_visual, memory_blocks, tooltip_manager):
    canvas.delete("all")
    y_offset = 20
    box_height = 60
    spacing = 80
    total_width = 600

    for i, block in enumerate(memory_blocks):
        x = 20
        y = y_offset + i * spacing

        canvas.create_text(
            x, y, anchor="nw", text=f"Partition {i}", font=("Segoe UI", 10, "bold")
        )
        x += 100

        used = sum(p[1] for p in allocation_visual[i])
        free = block - used

        canvas.create_rectangle(
            x, y, x + total_width, y + box_height, outline="#D1D5DB", fill="white"
        )
        canvas.create_text(
            x + 5,
            y - 15,
            anchor="nw",
            text=f"Total: {block} KB | Used: {used} KB | Free: {free} KB ",
            font=("Segoe UI", 9),
        )

        px = x
        for pid, size, color in allocation_visual[i]:
            width = int((size / block) * total_width)
            rect = canvas.create_rectangle(
                px, y, px + width, y + box_height, fill=color, outline="gray"
            )
            if width >= 50:
                canvas.create_text(
                    px + width / 2,
                    y + box_height / 2,
                    text=f"P{pid}\n{size} KB",
                    fill="black",
                    font=("Segoe UI", 9),
                    justify="center",
                )
            else:
                canvas.tag_bind(
                    rect,
                    "<Enter>",
                    lambda e, p=pid, s=size: tooltip_manager.show_tooltip(
                        e, f"PID: {p}, Size: {s} KB"
                    ),
                )
                canvas.tag_bind(rect, "<Leave>", lambda e: tooltip_manager.hide_tooltip())
            px += width

        if free > 0:
            free_width = int((free / block) * total_width)
            rect = canvas.create_rectangle(
                px, y, px + free_width, y + box_height, fill="#E5E7EB", outline="gray"
            )
            if free_width >= 50:
                canvas.create_text(
                    px + free_width / 2,
                    y + box_height / 2,
                    text=f"Free\n{free} KB",
                    font=("Segoe UI", 9),
                    justify="center",
                )
            else:
                canvas.tag_bind(
                    rect,
                    "<Enter>",
                    lambda e, s=free: tooltip_manager.show_tooltip(
                        e, f"Free Space: {s} KB"
                    ),
                )
                canvas.tag_bind(rect, "<Leave>", lambda e: tooltip_manager.hide_tooltip())

def show_allocation_tabs(root, processes, memory_blocks):
    window = tk.Toplevel(root)
    window.configure(bg="#E5F0FF")
    window.title("Memory Allocation")
    window.geometry("1100x700")

    tab_control = ttk.Notebook(window)
    summary_data = {}

    for strategy in ["first_fit", "best_fit", "worst_fit", "next_fit"]:
        frame = ttk.Frame(tab_control)
        tab_control.add(frame, text=strategy.replace("_", " ").title())

        canvas_frame = ttk.Frame(frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", height=600)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        allocation, failures, allocation_visual, remaining, logs = allocate_memory(
            processes, memory_blocks, strategy
        )
        summary_data[strategy] = {
            "failures": len(failures),
            "fragmentation": sum(remaining),
            "fail_list": failures,
            "log": logs,
        }

        tooltip_manager = TooltipManager(canvas)
        draw_block_diagram(canvas, allocation_visual, memory_blocks, tooltip_manager)

        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    tab_control.pack(expand=True, fill="both")
    ttk.Button(
        window, text="View Summary", command=lambda: show_comparison_summary(root, summary_data, memory_blocks)
    ).pack(pady=10)