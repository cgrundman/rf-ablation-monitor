import tkinter as tk


def simulation():
    def update_data():
        nonlocal temp
        nonlocal imp
        if temp[-1] <= 60.0 and imp[-1] <= 300.0:
            # Update the temperature
            temp.append(temp[-1])
            temp[-1] += .1
            temp[-1] = round(temp[-1], 2)
            temp_label.config(text=str(temp[-1]))
            # Update the impedence
            print(len(temp))
            imp.append(imp[-1])
            imp[-1] += .9
            imp[-1] = round(imp[-1], 2)
            imp_label.config(text=str(imp[-1]))

            if temp[-1] <= 60.0 and imp[-1] <= 300.0:  # Only continue updating if less than thresholds
                root.after(50, update_data)
                
        if temp[-1] > 60.0 or imp[-1] > 300.0:  # Reset the app when temp reaches 60
            reset_app()

    start_button.config(state=tk.DISABLED)  # Disable button while simulating
    # Reset temp
    temp = [37.0]
    # Reset imp
    imp = [100.0] 
    update_data()

def reset_app():
    """Reset the temperature, impedence, and app state to the initial setup."""
    global temp
    temp = [37.0]
    temp_label.config(text=str(temp[-1]))
    global imp
    imp = [100.0]
    imp_label.config(text=str(imp[-1]))
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
start_button.grid(row=4, column=0, columnspan=1, sticky='')

# # Reset button
# reset_button = tk.Button(root, text="Reset", command=reset_app, font=("Helvetica", 14))
# reset_button.grid(row=4, column=1, columnspan=1, sticky='')

# Initialize the temperature
temp = [37.0]

# Initialize the impedence
imp = [100.0]

# Run the tkinter main loop
root.mainloop()