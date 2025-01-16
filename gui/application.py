import tkinter as tk
from gui.simulation.simulation import Simulation
from gui.thresholds.thresholds import ThresholdManager
from utils.plotting import PlotManager

class Application:
    def __init__(self, root):
        """
        Initializes the main application.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("RF Ablation Simulator")
        self.root.geometry("850x700")
        self.root.configure(background="#f5fbfa")  # Offwhite background

        # Initialize Managers
        self.threshold_manager = ThresholdManager()
        self.plot_manager = PlotManager(self.root, self.threshold_manager)
        self.simulation = Simulation(self.threshold_manager, self.plot_manager, self.update_ui)

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        """Sets up the UI components for the application."""
        # Main Title
        tk.Label(
            self.root, text="RF Ablation Simulation", bg="#f5fbfa", font=("Helvetica", 36)
        ).grid(row=0, column=0, columnspan=6, sticky="")

        # Temperature Section
        self.create_section("Temperature", row_start=1, threshold_type="temp")

        # Impedance Section
        self.create_section("Impedance", row_start=6, threshold_type="imp")

        # Control Buttons
        self.create_control_buttons()

    def create_section(self, title, row_start, threshold_type):
        """
        Creates a section for temperature or impedance display and controls.

        Args:
            title (str): Title of the section.
            row_start (int): Starting row for the section.
            threshold_type (str): Either 'temp' or 'imp' for respective thresholds.
        """
        bg_color = "#f5fbfa"

        # Section Title
        tk.Label(
            self.root, text=title, bg=bg_color, font=("Helvetica", 24)
        ).grid(row=row_start, column=0, columnspan=6, sticky="")

        # Warning Label
        setattr(
            self,
            f"{threshold_type}_warn_label",
            tk.Label(self.root, text="Warning!", bg=bg_color, fg=bg_color, font=("Helvetica", 24)),
        )
        getattr(self, f"{threshold_type}_warn_label").grid(row=row_start + 1, column=5, sticky="")

        # Value Display
        setattr(
            self,
            f"{threshold_type}_value_label",
            tk.Label(self.root, text="0.0", bg=bg_color, font=("Helvetica", 36)),
        )
        getattr(self, f"{threshold_type}_value_label").grid(row=row_start + 2, column=5, sticky="")

        # Threshold Display
        setattr(
            self,
            f"{threshold_type}_threshold_label",
            tk.Label(
                self.root,
                text=f"Threshold: {self.threshold_manager.get_threshold(threshold_type)}",
                bg=bg_color,
                font=("Helvetica", 16),
            ),
        )
        getattr(self, f"{threshold_type}_threshold_label").grid(row=row_start + 3, column=5, sticky="")

        # Threshold Control Buttons
        threshold_frame = tk.Frame(self.root, bg=bg_color)
        threshold_frame.grid(row=row_start + 4, column=5, sticky="")

        plus_button = tk.PhotoImage(file=f"images/plus_{'1' if threshold_type == 'temp' else '10'}.png")
        minus_button = tk.PhotoImage(file=f"images/minus_{'1' if threshold_type == 'temp' else '10'}.png")
        reset_button = tk.PhotoImage(file="images/reset_blue.png")

        tk.Button(
            threshold_frame,
            image=minus_button,
            border=0,
            command=lambda: self.update_threshold(threshold_type, "decrease"),
        ).pack(side="left")
        tk.Button(
            threshold_frame,
            image=reset_button,
            border=0,
            command=lambda: self.update_threshold(threshold_type, "reset"),
        ).pack(side="left")
        tk.Button(
            threshold_frame,
            image=plus_button,
            border=0,
            command=lambda: self.update_threshold(threshold_type, "increase"),
        ).pack(side="left")

        # Keep references to the images to prevent garbage collection
        setattr(self, f"{threshold_type}_plus_img", plus_button)
        setattr(self, f"{threshold_type}_minus_img", minus_button)
        setattr(self, f"{threshold_type}_reset_img", reset_button)

    def create_control_buttons(self):
        """Creates Start/Stop, Reset, and Close buttons."""
        start_button_img = tk.PhotoImage(file="images/start_button_active.png")
        stop_button_img = tk.PhotoImage(file="images/stop_button_active.png")
        reset_button_img = tk.PhotoImage(file="images/reset_button.png")
        close_button_img = tk.PhotoImage(file="images/close_button.png")

        self.start_stop_button = tk.Button(
            self.root,
            image=start_button_img,
            text="Start",
            border=0,
            command=self.simulation.start,
            font=("Helvetica", 14),
        )
        self.start_stop_button.grid(row=11, column=2, columnspan=1, sticky="")

        tk.Button(
            self.root,
            image=reset_button_img,
            text="Reset",
            border=0,
            command=self.simulation.reset,
            font=("Helvetica", 14),
        ).grid(row=11, column=3, columnspan=1, sticky="")

        tk.Button(
            self.root,
            image=close_button_img,
            text="Close",
            border=0,
            command=self.root.quit,
            font=("Helvetica", 14),
        ).grid(row=11, column=4, columnspan=1, sticky="")

        # Keep references to the images to prevent garbage collection
        self.start_img = start_button_img
        self.stop_img = stop_button_img
        self.reset_img = reset_button_img
        self.close_img = close_button_img

    def update_ui(self):
        """Updates the UI elements based on the current simulation state."""
        # Update temperature and impedance values
        self.temp_value_label.config(text=str(self.simulation.temp[-1]))
        self.imp_value_label.config(text=str(self.simulation.imp[-1]))

        # Update threshold warnings
        temp_exceeded = self.simulation.temp[-1] > self.threshold_manager.get_threshold("temp")
        imp_exceeded = self.simulation.imp[-1] > self.threshold_manager.get_threshold("imp")

        self.temp_warn_label.config(bg="#f00" if temp_exceeded else "#f5fbfa")
        self.imp_warn_label.config(bg="#f00" if imp_exceeded else "#f5fbfa")

        # Update threshold labels
        self.temp_threshold_label.config(
            text=f"Threshold: {self.threshold_manager.get_threshold("temp")}"
        )
        self.imp_threshold_label.config(
            text=f"Threshold: {self.threshold_manager.get_threshold("imp")}"
        )

    def update_threshold(self, threshold_type, action):
        """Updates the threshold value based on user input."""
        if threshold_type == "temp":
            if action == "increase":
                self.threshold_manager.increase_temperature()
            elif action == "decrease":
                self.threshold_manager.decrease_temperature()
            elif action == "reset":
                self.threshold_manager.reset_temperature()
        elif threshold_type == "imp":
            if action == "increase":
                self.threshold_manager.increase_impedance()
            elif action == "decrease":
                self.threshold_manager.decrease_impedance()
            elif action == "reset":
                self.threshold_manager.reset_impedance()

        # Update the UI after changing thresholds
        self.update_ui()
