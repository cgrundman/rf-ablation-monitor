import tkinter as tk

def simulation():
    def update_temp():
        nonlocal temp
        if temp <= 60.0:
            temp += .1
            temp = round(temp, 2)
            temp_label.config(text=str(temp))
            if temp <= 60.0:  # Only continue updating if less than or equal to 60
                root.after(50, update_temp)
        if temp > 60.0:  # Reset the app when temp reaches 60
            reset_app()

    def update_imp():
        nonlocal imp
        if imp <= 300.0:
            imp += .5
            imp = round(imp, 2)
            imp_label.config(text=str(imp))
            if imp <= 300.0:  # Only continue updating if less than or equal to 300
                root.after(50, update_temp)
        # if imp > 300.0:  # Reset the app when impedence reaches 300
        #     reset_app()

    start_button.config(state=tk.DISABLED)  # Disable button while simulating
    temp = 37.0 # Reset temp
    imp = 100.0 # Reset imp
    update_temp()
    update_imp()

def reset_app():
    """Reset the temper and app state to the initial setup."""
    global temp
    temp = 37.0
    temp_label.config(text="37.0")
    global imp
    imp = 100.0
    imp_label.config(text="100.0")
    start_button.config(state=tk.NORMAL)

# Initialize the tkinter Application
root = tk.Tk()
root.title("RF Ablation Simulator")
root.geometry("300x250")

# Temperature Title Label
temp_title = tk.Label(root, text="Temperature", font=("Helvetica", 24))
temp_title.grid(row=0, column=0, columnspan=2, sticky='')

# Temperature Display
temp_label = tk.Label(root, text="37.0", font=("Helvetica", 24))
temp_label.grid(row=1, column=0, columnspan=2, sticky='')

# Impedence Title Label
imp_title = tk.Label(root, text="Impedence", font=("Helvetica", 24))
imp_title.grid(row=2, column=0, columnspan=2, sticky='')

# Impedence Display
imp_label = tk.Label(root, text="100.0", font=("Helvetica", 24))
imp_label.grid(row=3, column=0, columnspan=2, sticky='')

# Start button
start_button = tk.Button(root, text="Start", command=simulation, font=("Helvetica", 14))
start_button.grid(row=4, column=0, columnspan=2, sticky='')

# Initialize the temp
temp = 37.0

# Initialize the imp
imp = 100.0

# Run the tkinter main loop
root.mainloop()