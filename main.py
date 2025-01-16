import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from utils.plotting import PlotManager

running = False

temp_thresh = 60.0
imp_thresh = 300.0

# Color Pallet
offwhite = "#f5fbfa"
blue = "#2872a2"
dark_gray = "#8c99a3"
light_gray = "#bec1c5"

def simulation():

    def update_data():
        global temp
        global imp
        if running and temp[-1] <= temp_thresh and imp[-1] <= imp_thresh:
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

            # Threshold Exceeded Notifications
            if temp[-1] > temp_thresh:
                temp_warn.config(text="Exceeded!", bg="#f00")
                start_stop_button.config(image=startButton, command=start_app)
            if imp[-1] > imp_thresh:
                imp_warn.config(text="Exceeded!", bg="#f00")
                start_stop_button.config(image=startButton, command=start_app)

            if temp[-1] <= temp_thresh and imp[-1] <= imp_thresh:  # Only continue updating if less than thresholds
                root.after(500, update_data)

        # High Level Notifications
        if len(temp) > 0:
            if temp[-1] > temp_thresh - 5.0 and temp[-1] <= temp_thresh:
                temp_warn.config(bg="#FFA500")

            if imp[-1] > imp_thresh - 40.0 and imp[-1] <= imp_thresh:
                imp_warn.config(bg="#FFA500")

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
    start_stop_button.config(image=stopButton, command=stop_app)
    simulation()

def stop_app():
    global running
    start_stop_button.config(image=startButton, command=start_app)
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
    start_stop_button.config(image=startButton, command=start_app)
    temp_warn.config(text="Warning!", bg=offwhite)
    imp_warn.config(text="Warning!", bg=offwhite)
    plot_data(temp, imp)

def close_app():
    root.quit()

def update_thresholds():
    global temp
    global imp
    temp_thresh_label.config(text=f"Threshold: {str(temp_thresh)}")
    imp_thresh_label.config(text=f"Threshold: {str(imp_thresh)}")
    plot_data(temp, imp)

def increase_temp_thresh():
    global temp_thresh
    temp_thresh += 1.0
    update_thresholds()

def decrease_temp_thresh():
    global temp_thresh
    temp_thresh -= 1.0
    update_thresholds()

def reset_temp_thresh():
    global temp_thresh
    temp_thresh = 60.0
    update_thresholds()

def increase_imp_thresh():
    global imp_thresh
    imp_thresh += 10.0
    update_thresholds()

def decrease_imp_thresh():
    global imp_thresh
    imp_thresh -= 10.0
    update_thresholds()

def reset_imp_thresh():
    global imp_thresh
    imp_thresh = 300.0
    update_thresholds()

def plot_data(temp, imp):
    # Update temperature plot
    x = [-50, 10, 10000]
    ax1.cla()
    ax1.set_xlim(int(min(len(temp) - 20, 0)), int(min(len(temp) - 1, 19)))
    ax1.set_ylim(34, int(temp_thresh + 3.0))
    ax1.fill_between(x, temp_thresh - 5.0, temp_thresh, color='#FFA500', alpha=0.5)
    ax1.axhline(y=temp_thresh,xmin=0,xmax=3,ls="--",c="r",lw=2)
    ax1.set_xticklabels([])
    ax1.grid()
    ax1.plot(temp[-20:], "-")
    canvas1.draw()
    # Update impedence plot
    ax2.cla()
    ax2.set_xlim(int(min(len(imp) - 20, 0)), int(min(len(imp) - 1, 19)))
    ax2.set_ylim(75, int(imp_thresh + 25.0))
    ax2.fill_between(x, imp_thresh - 40.0, imp_thresh, color='#FFA500', alpha=0.5)
    ax2.axhline(y=imp_thresh,xmin=0,xmax=3,ls="--",c="r",lw=2)
    ax2.set_xticklabels([])
    ax2.grid()
    ax2.plot(imp[-20:], "-")
    canvas2.draw()

# Initialize the tkinter Application
root = tk.Tk()
root.title("RF Ablation Simulator")
root.geometry("850x700")
root.configure(background=offwhite)

# Initialize the temperature
temp = []

# Initialize the impedence
imp = []

# Main Title Label
main_title = tk.Label(root, text="RF Ablation Simulation", bg=offwhite, font=("Helvetica", 36))
main_title.grid(row=0, column=0, columnspan=6, sticky='')

# Temperature Title Label
temp_title = tk.Label(root, text="Temperature", bg=offwhite, font=("Helvetica", 24))
temp_title.grid(row=1, column=0, columnspan=6, sticky='')

# Temperature Warning Label
temp_warn = tk.Label(root, text="Warning!", bg=offwhite, fg=offwhite, font=("Helvetica", 24))
temp_warn.grid(row=2, column=5, sticky='')

# Temperature Display
temp_label = tk.Label(root, text="37.0", bg=offwhite, font=("Helvetica", 36))
temp_label.grid(row=3, column=5, sticky='')

# Temperature Threshold
temp_thresh_label = tk.Label(root, text=f"Threshold: {str(temp_thresh)}", bg=offwhite, font=("Helvetica", 16))
temp_thresh_label.grid(row=4, column=5, sticky='')

# Temperature Threshold Buttons
temp_thresh_frame = tk.Frame(root)
temp_thresh_frame.grid(row=5, column=5, sticky='')

resetButtonBlue = tk.PhotoImage(file="images/reset_blue.png")
plus1Button = tk.PhotoImage(file="images/plus_1.png")
minus1Button = tk.PhotoImage(file="images/minus_1.png")

temp_thresh_up = tk.Button(temp_thresh_frame, image=plus1Button, border=0, command=increase_temp_thresh) # Threshold Increase
temp_thresh_reset = tk.Button(temp_thresh_frame, image=resetButtonBlue, border=0, command=reset_temp_thresh) # Threshold Reset
temp_thresh_down = tk.Button(temp_thresh_frame, image=minus1Button, border=0, command=decrease_temp_thresh) # Threshold Decrease

temp_thresh_down.pack(side="left")
temp_thresh_reset.pack(side="left")
temp_thresh_up.pack(side="left")

# Impedence Title Label
imp_title = tk.Label(root, text="Impedence", bg=offwhite, font=("Helvetica", 24))
imp_title.grid(row=6, column=0, columnspan=6, sticky='')

# Impedence Warning Label
imp_warn = tk.Label(root, text="Warning!", bg=offwhite, fg=offwhite, font=("Helvetica", 24))
imp_warn.grid(row=7, column=5, sticky='')

# Impedence Display
imp_label = tk.Label(root, text="100.0", bg=offwhite, font=("Helvetica", 36))
imp_label.grid(row=8, column=5, sticky='')

# Impedence Threshold Setting
imp_thresh_label = tk.Label(root, text=f"Threshold: {str(imp_thresh)}", bg=offwhite, font=("Helvetica", 16))
imp_thresh_label.grid(row=9, column=5, sticky='')

# Impedence Threshold Buttons
imp_thresh_frame = tk.Frame(root)
imp_thresh_frame.grid(row=10, column=5, sticky='')

plus10Button = tk.PhotoImage(file="images/plus_10.png")
minus10Button = tk.PhotoImage(file="images/minus_10.png")

imp_thresh_up = tk.Button(imp_thresh_frame, image=plus10Button, border=0, command=increase_imp_thresh) # Threshold Increase
imp_thresh_reset = tk.Button(imp_thresh_frame, image=resetButtonBlue, border=0, command=reset_imp_thresh) # Threshold Reset
imp_thresh_down = tk.Button(imp_thresh_frame, image=minus10Button, border=0, command=decrease_imp_thresh) # Threshold Decrease

imp_thresh_down.pack(side="left")
imp_thresh_reset.pack(side="left")
imp_thresh_up.pack(side="left")

# Temperature Graph
figure1, ax1 = plt.subplots()
figure1.set_figwidth(6)
figure1.set_figheight(2.5)
figure1.patch.set_facecolor(offwhite)
canvas1 = FigureCanvasTkAgg(figure1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(row=2, column=0, rowspan=4, columnspan=5, sticky='')

# Impedence Graph
figure2, ax2 = plt.subplots()
figure2.set_figwidth(6)
figure2.set_figheight(2.5)
figure2.patch.set_facecolor(offwhite)
canvas2 = FigureCanvasTkAgg(figure2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(row=7, column=0, rowspan=4, columnspan=5, sticky='')

# Plot initial data
plot_data(temp, imp)

# Start/Stop button
startButton = tk.PhotoImage(file="images/start_button_active.png")
stopButton = tk.PhotoImage(file="images/stop_button_active.png")
start_stop_button = tk.Button(root, image=startButton, text="Stop", border=0, command=stop_app, font=("Helvetica", 14))
start_stop_button.grid(row=11, column=2, columnspan=1, sticky='')

# Reset button
resetButton = tk.PhotoImage(file="images/reset_button.png")
reset_button = tk.Button(root, image=resetButton, text="Reset", border=0, command=reset_app, font=("Helvetica", 14))
reset_button.grid(row=11, column=3, columnspan=1, sticky='')

# Close button
closeButton = tk.PhotoImage(file="images/close_button.png")
close_button = tk.Button(root, image=closeButton, text="Close", border=0, command=close_app, font=("Helvetica", 14))
close_button.grid(row=11, column=4, columnspan=1, sticky='')

# Run the tkinter main loop
root.mainloop()