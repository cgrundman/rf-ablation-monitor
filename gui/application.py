import tkinter as tk
# from gui.thresholds import ThresholdManager
# from gui.simulation import Simulation
# from utils.plotting import PlotManager
from gui.styles import Styles

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RF Ablation Simulator")
        self.root.geometry("850x700")
        self.root.configure(background=Styles.OFFWHITE)

        # Initialize components
        # self.threshold_manager = ThresholdManager()
        # self.simulation = Simulation(self.root, self.threshold_manager)
        # self.plot_manager = PlotManager(self.root, self.threshold_manager)

        # Layout UI
        self.create_layout()

    def create_layout(self):
        # Main Title
        main_title = tk.Label(self.root, text="RF Ablation Simulation", bg=Styles.OFFWHITE, font=("Helvetica", 36))
        main_title.grid(row=0, column=0, columnspan=6, sticky='')

        # Temperature and Impedance Threshold Management
        # self.simulation.create_temperature_controls()
        # self.simulation.create_impedance_controls()

        # Graphs
        # self.plot_manager.create_temperature_plot()
        # self.plot_manager.create_impedance_plot()

        # Buttons
        # self.simulation.create_control_buttons()

    def run(self):
        self.root.mainloop()
