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
        self.ablating = False
        self.idxs = [0] # Set initial index
        self.temp = [37.0] # Initial temperature
        self.imp = [100.0] # Initial impedance

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
        self.end_ablate()
        self.idxs = [0]
        self.temp = [37.0]
        self.imp = [100.0]
        self.threshold_manager.reset_temperature()
        self.threshold_manager.reset_impedance()
        self.plot_manager.update_plots(
            self.idxs,
            self.temp, 
            self.imp, 
            self.threshold_manager.get_threshold("temp"), 
            self.threshold_manager.get_threshold("imp")
        )
        self.update_ui_callback()

    def ablate(self):
        """Starts ablation."""
        if not self.ablating:
            self.ablating = True
    
    def end_ablate(self):
        """Ends ablation."""
        self.ablating = False

    def update_data(self):
        """Updates the simulation data and continues if running."""
        if self.running:
            # Update x-values
            self.idxs.append(self.idxs[-1] + 1)

            # Update temperature
            steady_state = 37.0
            if self.ablating:
                self.temp.append(self.temp[-1] + 0.5) # Increment temperature
            else:
                self.temp.append(self.temp[-1] + 0.01*min(steady_state - self.temp[-1], 2))
            self.temp[-1] = round(self.temp[-1], 2)

            # Update impedance
            if self.ablating:
                self.imp.append(self.imp[-1] + 9)  # Increment impedance
            else:
                self.imp.append(self.imp[-1])
            self.imp[-1] = round(self.imp[-1], 2)

            # Check thresholds
            temp_exceeded = self.temp[-1] > self.threshold_manager.temperature_threshold
            imp_exceeded = self.imp[-1] > self.threshold_manager.impedance_threshold

            if temp_exceeded or imp_exceeded:
                self.stop()

            # Update UI
            self.update_ui_callback()

            # Update the plots
            self.plot_manager.update_plots(
                self.idxs,
                self.temp, 
                self.imp, 
                self.threshold_manager.temperature_threshold, 
                self.threshold_manager.impedance_threshold
            )

            # Schedule the next update
            if not temp_exceeded and not imp_exceeded:
                self.plot_manager.root.after(50, self.update_data)
