import tkinter as tk
from gui.simulation.simulation import Simulation
from gui.thresholds.thresholds import ThresholdManager
from utils.plotting import PlotManager
from gui.styles.styles import Styles

class Application:
    def __init__(self, root):
        """
        Initializes the main application.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("RF Ablation Simulator")
        self.root.geometry("1350x750")
        self.root.configure(background=Styles.OFFWHITE)  # Offwhite background
        
        # Running state variables
        self.simulation_running = False
        self.ablating = False

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
            self.root, text="RF Ablation Simulation", bg=Styles.OFFWHITE, font=("Helvetica", 36)
        ).grid(row=0, column=0, columnspan=10, sticky="")

        # Monitor Widget
        self.create_monitor()

        # Threshold Widget
        self.create_thresholds()

        # Control Buttons
        self.create_controls()

        # Application Buttons
        self.create_application_buttons()

    def create_monitor(self):
        # Temperature Section
        self.create_monitor_plot("Temperature", row_start=1, threshold_type="temp")

        # Impedance Section
        self.create_monitor_plot("Impedance", row_start=6, threshold_type="imp")

    def create_monitor_plot(self, title, row_start, threshold_type):
        """
        Creates a section for temperature or impedance display and controls.

        Args:
            title (str): Title of the section.
            row_start (int): Starting row for the section.
            threshold_type (str): Either 'temp' or 'imp' for respective thresholds.
        """

        # Section Title
        tk.Label(
            self.root, text=f"{title}:", bg=Styles.OFFWHITE, font=("Helvetica", 24)
        ).grid(row=row_start, column=0, columnspan=1, sticky="")

        # Warning Label
        setattr(
            self,
            f"{threshold_type}_warn_label",
            tk.Label(self.root, text="Warning!", bg=Styles.OFFWHITE, fg=Styles.OFFWHITE, font=("Helvetica", 24)),
        )
        getattr(self, f"{threshold_type}_warn_label").grid(row=row_start + 1, column=5, sticky="")

        # Value Display
        setattr(
            self,
            f"{threshold_type}_value_label",
            tk.Label(
                self.root, 
                text=f"{'37.0' if threshold_type == 'temp' else '100.0'}", 
                bg=Styles.OFFWHITE, 
                font=("Helvetica", 36)
            ),
        )
        getattr(self, f"{threshold_type}_value_label").grid(row=row_start, column=1, columnspan=1, sticky="")

    def create_thresholds(self):
        # Create Temperature Threshold
        self.create_threshold_section(row_start=1, threshold_type="temp")

        # Create Impedence Threshold
        self.create_threshold_section(row_start=6, threshold_type="imp")

    def create_threshold_section(self, row_start, threshold_type):
        # Threshold Control Buttons
        threshold_frame = tk.Frame(self.root, bg=Styles.OFFWHITE)
        threshold_frame.grid(row=row_start + 4, column=5, sticky="")

        # Threshold Display
        setattr(
            self,
            f"{threshold_type}_threshold_label",
            tk.Label(
                self.root,
                text=f"Threshold: {self.threshold_manager.get_threshold(threshold_type)}",
                bg=Styles.OFFWHITE,
                font=("Helvetica", 16),
            ),
        )
        getattr(self, f"{threshold_type}_threshold_label").grid(row=row_start + 3, column=5, sticky="")

        plus_button = tk.PhotoImage(file=f"images/plus_{'1' if threshold_type == 'temp' else '10'}.png")
        minus_button = tk.PhotoImage(file=f"images/minus_{'1' if threshold_type == 'temp' else '10'}.png")
        reset_button = tk.PhotoImage(file="images/reset_blue.png")

        tk.Button(
            threshold_frame,
            image=minus_button,
            border=0,
            bg=Styles.OFFWHITE,
            command=lambda: self.update_threshold(threshold_type, "decrease"),
        ).pack(side="left")
        tk.Button(
            threshold_frame,
            image=reset_button,
            border=0,
            bg=Styles.OFFWHITE,
            command=lambda: self.update_threshold(threshold_type, "reset"),
        ).pack(side="left")
        tk.Button(
            threshold_frame,
            image=plus_button,
            border=0,
            bg=Styles.OFFWHITE,
            command=lambda: self.update_threshold(threshold_type, "increase"),
        ).pack(side="left")

        # Keep references to the images to prevent garbage collection
        setattr(self, f"{threshold_type}_plus_img", plus_button)
        setattr(self, f"{threshold_type}_minus_img", minus_button)
        setattr(self, f"{threshold_type}_reset_img", reset_button)

    def create_controls(self):
        self.create_control_buttons()

    def create_control_buttons(self):
        device_button_pressed = tk.PhotoImage(file="images/button_pressed.png")
        device_button_unpressed = tk.PhotoImage(file="images/button_unpressed.png")

        tk.Label(
            self.root, text="Ablation", bg=Styles.OFFWHITE, font=("Helvetica", 24)
        ).grid(row=1, column=7, columnspan=3, sticky="")

        self.ablate_button = tk.Button(
            self.root,
            image=device_button_unpressed,
            border=0,
            bg=Styles.OFFWHITE,
            command=self.toggle_ablation
        )
        self.ablate_button.grid(row=2, column=7, columnspan=3, rowspan=4, sticky="")

        tk.Label(
            self.root, text="Postioning", bg=Styles.OFFWHITE, font=("Helvetica", 24)
        ).grid(row=6, column=7, columnspan=3, sticky="")

        self.positioning_button = tk.Button(
            self.root,
            image=device_button_pressed,
            border=0,
            bg=Styles.OFFWHITE,
            command=self.simulation.reposition
        )
        self.positioning_button.grid(row=7, column=7, columnspan=3, rowspan=4, sticky="")

        # Keep references to the images to prevent garbage collection
        self.device_button_pressed = device_button_pressed
        self.device_button_unpressed = device_button_unpressed

    def create_application_buttons(self):
        """Creates Start/Stop, Reset, and Close buttons."""
        start_button_img = tk.PhotoImage(file="images/start_button_active.png")
        stop_button_img = tk.PhotoImage(file="images/stop_button_active.png")
        reset_button_img = tk.PhotoImage(file="images/reset_button.png")
        close_button_img = tk.PhotoImage(file="images/close_button.png")
        on_img = tk.PhotoImage(file="images/on.png")
        off_img = tk.PhotoImage(file="images/off.png")

        self.app_button_frame = tk.Frame(self.root, bg=Styles.OFFWHITE)
        self.app_button_frame.grid(row=11, column=7, sticky="")

        self.off_img_label = tk.Label(
            self.app_button_frame, image=off_img, bg=Styles.OFFWHITE, font=("Helvetica", 24)
        ).pack(side="left")
        self.start_stop_button = tk.Button(
            self.app_button_frame,
            image=start_button_img,
            border=0,
            bg=Styles.OFFWHITE,
            command=self.toggle_simulation
        )
        self.start_stop_button.pack(side="left")
        self.on_img_label = tk.Label(
            self.app_button_frame, image=on_img, bg=Styles.OFFWHITE, font=("Helvetica", 24)
        ).pack(side="left")

        self.reset_button = tk.Button(
            self.root,
            image=reset_button_img,
            border=0,
            bg=Styles.OFFWHITE,
            command=self.reset_simulation
        )
        self.reset_button.grid(row=11, column=8, columnspan=1, sticky="")

        self.close_button = tk.Button(
            self.root,
            image=close_button_img,
            border=0,
            bg=Styles.OFFWHITE,
            command=self.root.quit
        )
        self.close_button.grid(row=11, column=9, columnspan=1, sticky="")

        self.root.grid_columnconfigure(7, minsize=300)
        self.root.grid_columnconfigure(8, minsize=150)
        self.root.grid_columnconfigure(9, minsize=150)

        # Keep references to the images to prevent garbage collection
        self.start_img = start_button_img
        self.stop_img = stop_button_img
        self.reset_img = reset_button_img
        self.close_img = close_button_img
        self.on_img = on_img
        self.off_img = off_img

    def update_ui(self):
        """Updates the UI elements based on the current simulation state."""
        # Update temperature and impedance values
        self.temp_value_label.config(text=str(self.simulation.temp[-1]))
        self.imp_value_label.config(text=str(self.simulation.imp[-1]))

        # Update threshold warnings
        temp_exceeded = self.simulation.temp[-1] > self.threshold_manager.get_threshold("temp")
        imp_exceeded = self.simulation.imp[-1] > self.threshold_manager.get_threshold("imp")
        temp_high = self.simulation.temp[-1] > self.threshold_manager.get_threshold("temp") - 5.0
        imp_high = self.simulation.imp[-1] > self.threshold_manager.get_threshold("imp") - 40.0

        if temp_exceeded:
            self.temp_warn_label.config(bg=Styles.WARNING_RED, text="Exceeded!")
        elif temp_high:
            self.temp_warn_label.config(bg=Styles.WARNING_ORANGE, text="Warning!")
        else:
            self.temp_warn_label.config(bg=Styles.OFFWHITE, text="Warning!")

        if imp_exceeded:
            self.imp_warn_label.config(bg=Styles.WARNING_RED, text="Exceeded!")
        elif imp_high:
            self.imp_warn_label.config(bg=Styles.WARNING_ORANGE, text="Warning!")
        else:
            self.imp_warn_label.config(bg=Styles.OFFWHITE, text="Warning!")

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

    def toggle_simulation(self):
        """Start or stop the simulation."""
        if self.simulation_running:
            # Stop simulation
            self.simulation_running = False
            self.start_stop_button.config(image=self.start_img)
            self.simulation.stop()
        else:
            # Start simulation
            self.simulation_running = True
            self.start_stop_button.config(image=self.stop_img)
            self.simulation.start()

    def reset_simulation(self):
        """Reset simulation to the initial state."""
        self.simulation_running = False
        self.start_stop_button.config(image=self.start_img)
        self.simulation.reset()

    def toggle_ablation(self):
        """Toggle ablation state."""
        if self.ablating:
            # Stop Ablating
            self.ablating = False
            self.ablate_button.config(image=self.device_button_unpressed)
            self.simulation.end_ablate()
        else:
            # Start ablating
            self.ablating = True
            self.ablate_button.config(image=self.device_button_pressed)
            self.simulation.ablate()
