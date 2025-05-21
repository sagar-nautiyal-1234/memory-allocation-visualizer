import tkinter as tk

class TooltipManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.tip = None

    def show_tooltip(self, event, text):
        if self.tip:
            self.hide_tooltip()
        x, y = event.x_root + 20, event.y_root + 20
        self.tip = tw = tk.Toplevel(self.canvas)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=text,
            background="#FEF3C7",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10),
            padx=8,
            pady=4
        )
        label.pack()

    def hide_tooltip(self):
        if self.tip:
            self.tip.destroy()
            self.tip = None
