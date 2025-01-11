import tkinter as tk

class RFAblationMonitor:
    def __init__(self, root):
        bg_color = '#4c4c4c'
        self.plt_color = '#5a5a5a'

        self.root = root
        self.root.title("RF Ablation Monitor")
        self.root.configure(bg=bg_color)
        
        # Temperature
        self.label1 = tk.Label(self.root, text=f"Temperature", font=('Helvetica', 24), bg=bg_color)
        self.label1.grid(row=0, column=0, columnspan=2)

        # Impedence
        self.label2 = tk.Label(self.root, text=f"Impedence", font=('Helvetica', 24), bg=bg_color)
        self.label2.grid(row=2, column=0, columnspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = RFAblationMonitor(root)
    root.mainloop()