
from tkinter import ttk

def apply_theme_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Set root window background
    root.configure(bg="#E5F0FF")

    # General colors
    fluent_blue = "#0078D4"
    fluent_hover = "#005A9E"
    text_color = "#212121"
    border_color = "#D0D0D0"
    highlight_color = "#D6EBFF"

    # Button style - pill like
    style.configure("TButton",
                    font=("Segoe UI", 10, "bold"),
                    foreground="white",
                    background=fluent_blue,
                    borderwidth=0,
                    padding=10,
                    relief="flat")
    style.map("TButton",
              background=[("active", fluent_hover)],
              foreground=[("active", "white")])

    # Label style
    style.configure("TLabel",
                    font=("Segoe UI", 10),
                    foreground=text_color,
                    background="#E5F0FF")

    # Frame style (all pages bluish)
    style.configure("TFrame",
                    background="#E5F0FF")

    # Entry style
    style.configure("TEntry",
                    padding=5,
                    relief="flat",
                    borderwidth=1,
                    bordercolor=border_color,
                    font=("Segoe UI", 10),
                    fieldbackground="#FFFFFF",
                    background="#FFFFFF",
                    foreground=text_color)

    # Treeview style
    style.configure("Treeview",
                    font=("Segoe UI", 10),
                    rowheight=28,
                    fieldbackground="#FFFFFF",
                    background="#FFFFFF",
                    foreground=text_color,
                    bordercolor=border_color,
                    relief="flat")
    style.map("Treeview",
              background=[("selected", highlight_color)],
              foreground=[("selected", text_color)])

    style.configure("Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#F3F3F3",
                    foreground=text_color,
                    borderwidth=1,
                    relief="flat")

    # Notebook (Tabs) style
    style.configure("TNotebook",
                    background="#E5F0FF",
                    borderwidth=0)
    style.configure("TNotebook.Tab",
                    font=("Segoe UI", 10, "bold"),
                    background="#E5F0FF",
                    padding=[10,5])
    style.map("TNotebook.Tab",
              background=[("selected", fluent_blue)],
              foreground=[("selected", "white")])

