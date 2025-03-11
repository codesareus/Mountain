import matplotlib.pyplot as plt
import numpy as np

class DraggableLine:
    def __init__(self, line):
        self.line = line
        self.press = None
        self.cid_press = line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes: return
        contains, _ = self.line.contains(event)
        if contains:
            self.press = (event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.line.axes: return
        if self.line.get_linestyle() == '-':  # Horizontal line
            self.line.set_ydata([event.ydata, event.ydata])
        else:  # Vertical line
            self.line.set_xdata([event.xdata, event.xdata])
        self.line.figure.canvas.draw()

    def on_release(self, event):
        self.press = None

# Create a figure
fig, ax = plt.subplots()

x=[1,2,3,4,5,6,8,10,20]
y=[1,2,3,4,5,6,8,10,20]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.plot(x, y)

# Add a draggable vertical and horizontal line
h_line = ax.axhline(y=5, color='r', lw=2, linestyle='-')
v_line = ax.axvline(x=5, color='b', lw=2, linestyle='--')

# Make them draggable
DraggableLine(h_line)
DraggableLine(v_line)

plt.show()
