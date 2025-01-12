import tkinter as tk

def simulation():
    def update_temp():
        nonlocal temp
        if temp <= 60.0:
            temp += .1
            temp = round(temp, 2)
            temper_label.config(text=str(temp))
            if temp <= 60.0:  # Only continue updating if less than or equal to 60
                root.after(50, update_temp)
        if temp > 60.0:  # Reset the app when temp reaches 60
            reset_app()

    start_button.config(state=tk.DISABLED)  # Disable button while simulating
    temp = 37.0  # Reset temp
    update_temp()

def reset_app():
    """Reset the temper and app state to the initial setup."""
    global temp
    temp = 37.0
    temper_label.config(text="37.0")
    start_button.config(state=tk.NORMAL)

# Initialize the tkinter Application
root = tk.Tk()
root.title("RF Ablation Simulator")
root.geometry("300x250")

# Temperature Title Label
temp_label = tk.Label(root, text="Temperature", font=("Helvetica", 24))
temp_label.grid(row=0, column=0, columnspan=2, sticky='')

# Temperature Display
temper_label = tk.Label(root, text="37.0", font=("Helvetica", 24))
temper_label.grid(row=1, column=0, columnspan=2, sticky='')

# Start button
start_button = tk.Button(root, text="Start", command=simulation, font=("Helvetica", 14))
start_button.grid(row=3, column=0, columnspan=2, sticky='')

# Initialize the temp
temp = 37.0

# Run the tkinter main loop
root.mainloop()