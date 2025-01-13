import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


running = False

def simulation():

    def update_data():
        global temp
        global imp
        if running and temp[-1] <= 60.0 and imp[-1] <= 300.0:
            # Update the temperature
            temp.append(temp[-1])
            temp[-1] += 1 # .1
            temp[-1] = round(temp[-1], 2)
            temp_label.config(text=str(temp[-1]))
            # Update the impedence
            imp.append(imp[-1])
            imp[-1] += 9 # .9
            imp[-1] = round(imp[-1], 2)
            imp_label.config(text=str(imp[-1]))
            plot_data(temp, imp)

            if temp[-1] <= 60.0 and imp[-1] <= 300.0:  # Only continue updating if less than thresholds
                root.after(1, update_data)

        # if not running:
        #     root.after(200, update_data)

        # TODO Alarms
        # if temp[-1] > 60.0 or imp[-1] > 300.0:  # Reset the app when temp reaches 60
        #     reset_app()

    # Set Initial temperature and impedence
    global temp
    global imp
    if len(temp) == 0:
        # Reset temp
        temp = [37.0]
        # Reset imp
        imp = [100.0] 
    update_data()

def start_app():
    global running
    running = True
    start_button.config(state=tk.DISABLED)  # Disable button while simulating
    stop_button.config(state=tk.NORMAL)  # Disable button while simulating
    simulation()

def stop_app():
    global running
    start_button.config(state=tk.NORMAL)  # Disable button while simulating
    stop_button.config(state=tk.DISABLED)  # Disable button while simulating
    running = False

def reset_app():
    """Reset the temperature, impedence, and app state to the initial setup."""
    global running
    running = False
    global temp
    temp = []
    temp_label.config(text="37.0")
    global imp
    imp = []
    imp_label.config(text="100.0")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    plot_data(temp, imp)

def close_app():
    root.quit()

def plot_data(temp, imp):
    # Update temperature plot
    ax1.cla()
    ax1.axhline(y=60,xmin=0,xmax=3,ls="--",c="r",zorder=0)
    ax1.set_xlim(0, 20)
    ax1.set_ylim(34, 63)
    ax1.set_xticks([])
    ax1.plot(temp[-20:], "-")
    canvas1.draw()
    # Update impedence plot
    ax2.cla()
    ax2.axhline(y=300,xmin=0,xmax=3,ls="--",c="r",zorder=0)
    ax2.set_xlim(0, 20)
    ax2.set_ylim(75, 325)
    ax2.set_xticks([])
    ax2.plot(imp[-20:], "-")
    canvas2.draw()

# Initialize the tkinter Application
root = tk.Tk()
root.title("RF Ablation Simulator")
root.geometry("700x450")

# Initialize the temperature
# temp = [37.0]
temp = []

# Initialize the impedence
# imp = [100.0]
imp = []

# Temperature Title Label
temp_title = tk.Label(root, text="Temperature", font=("Helvetica", 24))
temp_title.grid(row=0, column=0, columnspan=6, sticky='')

# Temperature Display
temp_label = tk.Label(root, text="37.0", font=("Helvetica", 24))
temp_label.grid(row=1, column=5, columnspan=1, sticky='')

# Impedence Title Label
imp_title = tk.Label(root, text="Impedence", font=("Helvetica", 24))
imp_title.grid(row=2, column=0, columnspan=6, sticky='')

# Impedence Display
imp_label = tk.Label(root, text="100.0", font=("Helvetica", 24))
imp_label.grid(row=3, column=5, columnspan=2, sticky='')

# Temperature Graph
figure1, ax1 = plt.subplots()
figure1.set_figwidth(6)
figure1.set_figheight(1.5)
canvas1 = FigureCanvasTkAgg(figure1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(row=1, column=0, columnspan=5, sticky='')

# Impedence Graph
figure2, ax2 = plt.subplots()
figure2.set_figwidth(6)
figure2.set_figheight(1.5)
canvas2 = FigureCanvasTkAgg(figure2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(row=3, column=0, columnspan=5, sticky='')

# Plot initial data
plot_data(temp, imp)

# Start button
start_button = tk.Button(root, text="Start", command=start_app, font=("Helvetica", 14))
start_button.grid(row=4, column=1, columnspan=1, sticky='')

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_app, font=("Helvetica", 14))
stop_button.grid(row=4, column=2, columnspan=1, sticky='')
stop_button.config(state=tk.DISABLED)  # Disable button initially

# Reset button
reset_button = tk.Button(root, text="Reset", command=reset_app, font=("Helvetica", 14))
reset_button.grid(row=4, column=3, columnspan=1, sticky='')

# Close button
close_button = tk.Button(root, text="Close", command=close_app, font=("Helvetica", 14))
close_button.grid(row=4, column=4, columnspan=1, sticky='')

# Run the tkinter main loop
root.mainloop()