class Simulation:
    def __init__(self, threshold_manager, plot_manager, update_ui_callback):
        """
        Initializes the simulation with a threshold manager, plot manager, 
        and a callback to update the UI.

        Args:
            threshold_manager (ThresholdManager): Manages thresholds for temperature and impedance.
            plot_manager (PlotManager): Handles plotting of simulation data.
            update_ui_callback (callable): A function to update the UI when data changes.
        """
        self.threshold_manager = threshold_manager
        self.plot_manager = plot_manager
        self.update_ui_callback = update_ui_callback

        self.running = False
        self.temp = [37.0]  # Initial temperature
        self.imp = [100.0]  # Initial impedance

    def start(self):
        """Starts the simulation."""
        if not self.running:
            self.running = True
            self.update_data()

    def stop(self):
        """Stops the simulation."""
        self.running = False

    def reset(self):
        """Resets the simulation to its initial state."""
        self.stop()
        self.temp = [37.0]
        self.imp = [100.0]
        self.threshold_manager.reset_thresholds()
        self.plot_manager.update_plots(self.temp, self.imp)
        self.update_ui_callback()

    def update_data(self):
        """Updates the simulation data and continues if running."""
        if self.running:
            # Update temperature
            self.temp.append(self.temp[-1] + 0.1)  # Increment temperature
            self.temp[-1] = round(self.temp[-1], 2)

            # Update impedance
            self.imp.append(self.imp[-1] + 0.9)  # Increment impedance
            self.imp[-1] = round(self.imp[-1], 2)

            # Check thresholds
            temp_exceeded = self.temp[-1] > self.threshold_manager.temp_thresh
            imp_exceeded = self.imp[-1] > self.threshold_manager.imp_thresh

            if temp_exceeded or imp_exceeded:
                self.stop()

            # Update UI
            self.update_ui_callback()

            # Update the plots
            self.plot_manager.update_plots(self.temp, self.imp)

            # Schedule the next update
            if not temp_exceeded and not imp_exceeded:
                self.plot_manager.root.after(500, self.update_data)
