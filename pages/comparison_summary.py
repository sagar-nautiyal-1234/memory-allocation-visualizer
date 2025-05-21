import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import data_generator

def show_comparison_summary(root, data, memory_blocks):
    window = tk.Toplevel(root)
    window.configure(bg="#E5F0FF")
    window.title("Comparison Summary")
    window.geometry("1000x600")

    notebook = ttk.Notebook(window)
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)
    notebook.add(tab1, text="Failures (%)")
    notebook.add(tab2, text="Fragmentation (%)")
    notebook.add(tab3, text="Summary Table")
    notebook.add(tab4, text="Logs")
    notebook.pack(expand=True, fill="both")

    strategies = list(data.keys())

    total_processes = data_generator.number_of_processes
    total_memory = sum(memory_blocks) if memory_blocks else 0
    failures = [round((data[s]["failures"] / total_processes) * 100, 2) if total_processes > 0 else 0 for s in strategies]
    fragmentations = [round((data[s]["fragmentation"] / total_memory) * 100, 2) if total_memory > 0 else 0 for s in strategies]

    # Failures bar chart
    fig1, ax1 = plt.subplots()
    ax1.bar([s.replace("_", " ").title() for s in strategies], failures, color="#EF4444")
    ax1.set_title("Process Allocation Failures (%)")
    ax1.set_ylabel("Failures (%)")
    fig1.tight_layout()
    FigureCanvasTkAgg(fig1, master=tab1).get_tk_widget().pack(fill="both", expand=True)

    # Fragmentation bar chart
    fig2, ax2 = plt.subplots()
    ax2.bar([s.replace("_", " ").title() for s in strategies], fragmentations, color="#60A5FA")
    ax2.set_title("Memory Fragmentation (%)")
    ax2.set_ylabel("Fragmentation (%)")
    fig2.tight_layout()
    FigureCanvasTkAgg(fig2, master=tab2).get_tk_widget().pack(fill="both", expand=True)

    # Table
    # Summary Table with algorithm names, percentages, and absolute fragmentation
    # Summary Table with Algorithm name, % failures, % fragmentation, and absolute fragmentation
    tree = ttk.Treeview(tab3, columns=("Algorithm","Failures (%)","Fragmentation (%)","Fragmentation (abs)"), show="headings")
    # Summary Table with Algorithm name, % failures, % fragmentation, and absolute fragmentation
    tree.heading("Algorithm", text="Algorithm")
    tree.heading("Algorithm", text="Algorithm")
    tree.heading("Failures (%)", text="Failures (%)")
    tree.heading("Fragmentation (%)", text="Fragmentation (%)")
    tree.heading("Fragmentation (abs)", text="Fragmentation (in KB)")
    
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)            # center cell contents
        tree.heading(col, anchor=tk.CENTER)    

    for i, s in enumerate(strategies):
        name = s.replace('_', ' ').title()
        frag_abs = data[s]['fragmentation']
        tree.insert('', 'end', values=(name, failures[i], fragmentations[i], f'{frag_abs} KB'))
    tree.pack(fill="both", expand=True)

    for i, s in enumerate(strategies):
        name = s.replace("_", " ").title()
        frag_abs = data[s]["fragmentation"]
        frag_abs = data[s]["fragmentation"]

    # Logs: separate sub-tabs for each strategy with scrollbar
    logs_notebook = ttk.Notebook(tab4)
    logs_notebook.pack(expand=True, fill='both')
    for s in strategies:
        title = s.replace('_', ' ').title()
        frame = ttk.Frame(logs_notebook)
        logs_notebook.add(frame, text=title)
        text_widget = tk.Text(frame)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        text_widget.pack(side='left', fill='both', expand=True)
        for entry in data[s].get('log', []):
            text_widget.insert(tk.END, entry + '\n')
        text_widget.config(state=tk.DISABLED)
