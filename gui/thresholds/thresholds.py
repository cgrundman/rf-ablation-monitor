class ThresholdManager:
    def __init__(self):
        self.temperature_threshold = 60.0
        self.impedance_threshold = 300.0

    def get_threshold(self, threshold_type):
        if threshold_type == "imp":
            return self.impedance_threshold
        else:
            return self.temperature_threshold

    def increase_temperature(self, amount=1.0):
        self.temperature_threshold += amount

    def decrease_temperature(self, amount=1.0):
        self.temperature_threshold -= amount

    def reset_temperature(self):
        self.temperature_threshold = 60.0

    def increase_impedance(self, amount=10.0):
        self.impedance_threshold += amount

    def decrease_impedance(self, amount=10.0):
        self.impedance_threshold -= amount

    def reset_impedance(self):
        self.impedance_threshold = 300.0