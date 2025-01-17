import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.styles.styles import Styles

class PlotManager:
    def __init__(self, root, threshold_manager):
        self.root = root
        self.threshold_manager = threshold_manager
        self.temp_plot = None
        self.imp_plot = None
        self.create_temperature_plot()
        self.create_impedance_plot()

    def create_temperature_plot(self):
        # Create temperature graph
        self.figure1, self.ax1 = plt.subplots()
        self.figure1.set_figwidth(6)
        self.figure1.set_figheight(2.5)
        self.figure1.patch.set_facecolor(Styles.OFFWHITE)
        self.ax1.set_xlim(int(0), int(19))
        self.ax1.set_ylim(34, 63.0)
        self.ax1.set_xticklabels([])
        self.ax1.grid()
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.root)
        canvas_widget1 = self.canvas1.get_tk_widget()
        canvas_widget1.grid(row=2, column=0, rowspan=4, columnspan=5, sticky='')

    def create_impedance_plot(self):
        # Create impedance graph
        self.figure2, self.ax2 = plt.subplots()
        self.figure2.set_figwidth(6)
        self.figure2.set_figheight(2.5)
        self.figure2.patch.set_facecolor(Styles.OFFWHITE)
        self.ax2.set_xlim(int(0), int(19))
        self.ax2.set_ylim(75, 325)
        self.ax2.set_xticklabels([])
        self.ax2.grid()
        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.root)
        canvas_widget2 = self.canvas2.get_tk_widget()
        canvas_widget2.grid(row=7, column=0, rowspan=4, columnspan=5, sticky='')

    def update_plots(self, temp, imp, temp_thresh, imp_thresh):
        # Logic to update Matplotlib plots

        # Update temperature plot
        x = [-50, 10, 10000]
        self.ax1.cla()
        self.ax1.set_xlim(int(min(len(temp) - 20, 0)), int(min(len(temp) - 1, 19)))
        self.ax1.set_ylim(34, int(temp_thresh + 3.0))
        self.ax1.fill_between(x, temp_thresh - 5.0, temp_thresh, color='#FFA500', alpha=0.5)
        self.ax1.axhline(y=temp_thresh,xmin=0,xmax=3,ls="--",c="r",lw=2)
        self.ax1.set_xticklabels([])
        self.ax1.grid()
        self.ax1.plot(temp[-20:], "-")
        self.canvas1.draw()
        # Update impedence plot
        self.ax2.cla()
        self.ax2.set_xlim(int(min(len(imp) - 20, 0)), int(min(len(imp) - 1, 19)))
        self.ax2.set_ylim(75, int(imp_thresh + 25.0))
        self.ax2.fill_between(x, imp_thresh - 40.0, imp_thresh, color='#FFA500', alpha=0.5)
        self.ax2.axhline(y=imp_thresh,xmin=0,xmax=3,ls="--",c="r",lw=2)
        self.ax2.set_xticklabels([])
        self.ax2.grid()
        self.ax2.plot(imp[-20:], "-")
        self.canvas2.draw()
