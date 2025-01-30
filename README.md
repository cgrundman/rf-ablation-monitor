# RF Ablation Monitor

Code for a GUI monitoring and an RF Ablation device in operation. Python GUI built on Tkinter/Matplotlib.

## Download Instructions

## Run Locally

Clone the project:

```bash
  git clone https://github.com/cgrundman/rf-ablation-monitor
```

Go to the project directory:

```bash
  cd local/path/rf-ablation-monitor
```

In the terminal:

```bash
  python main.py
```

## Cardiac Arrhythmia

Cardiac Arrhythmia is a condition where the heart beat takes an irregular step. It is caused by fatty tissue present in the heart.

Heart beats are triggered by electrical signal from the sinus nerve. The signal travels through the heart and triggers contractions in the different chamber of the heart to pump blood through the body.

<img src="https://www.mayoclinic.org/-/media/kcms/gbs/patient-consumer/images/2013/08/26/10/42/typical-heartbeat_1709751_3881158-001-1-72ppi-8col.jpg"/>

The signal originates from the Sinus node. From the sinus node, it travels through the Atrium (causing the Atriums to contract) to the Atrioventricular (AV) Node. The signal then continues through the vetricals causing contraction there. From here the signal travels back towards the Atriums, where there is a refractory period in the heart muscle preventing the signal from activating another contraction before dissipation.

The heartbeat can be further visualized by an ECG. PQ is contraction and relaxation of atriums, QRS is the contraction of the ventricals, and ST represents relaxation of the ventrical. 

<img src="https://ars.els-cdn.com/content/image/1-s2.0-S0213911121002466-gr1.jpg" width="250"/>

However when there is sufficient fatty tissue, the impedence of the tissue rises and delays signal propagation. If the delay lasts longer than the refractory period, the signal triggers another contraction of the ventricals. The ECG then shows another ventrical contraction after the first. The following image shows a normal heartbeat above, and a heartbeat with arrhythmia lies below.

<img src="https://www.saludsol.net/hchsnews/sites/default/files/inline-images/arritmias_arrhythmia.jpg"/>

## Radio Frequency (RF) Ablation

RF Ablation is one of the treatments for this condition. It is not the first option as it is an invasive procedure. The idea is to use a radio-frequency signal to generate heat. The heat is then applied to the heart tissue causing a lesion. Lesioned tissue has a lower impedance, thus hopefully the arrhythmia is cured. An image of the operation can be seen below:

<img src="https://i0.wp.com/thoracickey.com/wp-content/uploads/2021/06/f08-01-9780323793384.jpg?w=960"/>

The ablation electrode is inserted into the femoral vein in the leg and fed through the vein into the heart. There the controls are used for fine control and placement of the electrode. Modern imaging technology allow for path planning of the surgery beforehand. Here is an example of a typical ablation path:

<img src="https://cdn.ncbi.nlm.nih.gov/pmc/blobs/79e5/7252711/8c6cb91e5243/icrm-08-2868-g004.jpg" />

The relationship between impedence of the tissue and the temperature of the electrode is complex. Therefore the temperature of the electrode and the impedence of the system (electrode and tissue) are always monitored. This gui is an example of a monitor and interface for rf-ablation.

## GUI

The GUI simlates temperature and impedence values and plots the values on screen. Various settings can be adjusted to and tweeked for control of the procedue. The GUI is as seen below:

<img src="https://github.com/cgrundman/rf-ablation-monitor/blob/main/images/GUI_example.png" />

The GUI is split into 3 main sections. On the far left, there is a monitor for the impedence and temperature values. There are also the thresholds for max value in red and warning areas in orange. For Impedence, the ideal values are shaded in green. The vlaues them selves are plotted in blue and 20 values are plotted at a time (this is a constraint of Matplotlib, as more produce lag in the function of the device) and displayed numerically above the plot. 

The middle section displys and aloows for adjustment in the thresholds. There are buttons for increasing, decreasing, and resseting to default the threshold values. Unseen are the warning and Exceeded warnings above the threshold adjustments. If the values are in the orange regions in the plot, a warning message appears to warn the user. If the thresholds are exceeded, an exceeded message is displayed and the simulation is turned off. 

On the right are the controls. On the bottom, the on/off button for the simlutation apears as a toggle switch, and the reset and close buttons are both for the entire of the GUI. Above are the buttons for ablation (turning the electrode on and off) and the reposition button (normally these are controls to physically move the device, however this is simply resetting values after movement would occur)

All buttons were programed with svg and converted to png graphics. TKinter is simply using the image as the button. 

## License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)
