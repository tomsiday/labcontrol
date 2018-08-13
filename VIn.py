import nidaqmx # For NI DAQ-6211 IO
import pyqtgraph as pg # Plotting library
from pyqtgraph.Qt import QtCore, QtGui # Qt required for plotting library
import numpy as np # numpy
import math # simple functions like sin, cos ..

win = pg.GraphicsWindow() #Open a window for the plot
win.setWindowTitle('Stream of data from the DAQ input') # Window title

p1 = win.addPlot() # add a plot
p2 = win.addPlot()
# Use automatic downsampling and clipping to reduce the drawing load
p1.setDownsampling(mode='peak')
p1.setClipToView(True)
p1.setRange(xRange=[-100, 0])
p1.setLimits(xMax=0)
curve1 = p1.plot()

p2.setDownsampling(mode='peak')
p2.setClipToView(True)
p2.setRange(xRange=[-100, 0])
p2.setLimits(xMax=0)
curve2 = p2.plot()

data1 = np.empty(100)
output = np.empty(100)
ptr1 = 0

def plot_update():
    
    global data1, output, ptr1
    with nidaqmx.Task() as task:
        
        output[ptr1] = math.sin(math.radians(ptr1))+1
        task.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=-5, max_val=5)
        task.write(output[ptr1])
    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai1", min_val=0, max_val=10, terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
        data1[ptr1]=task.read()
        print(task.read())
    ptr1 += 1
    
    if ptr1 >= data1.shape[0]:
        tmp = data1
        data1 = np.empty(data1.shape[0] * 2)
        data1[:tmp.shape[0]] = tmp
        
    if ptr1 >= output.shape[0]:
        tmp = output
        output = np.empty(data1.shape[0] * 2)
        output[:tmp.shape[0]] = tmp
    
    curve1.setData(data1[:ptr1])
    curve1.setPos(-ptr1, 0)

    curve2.setData(output[:ptr1])
    curve2.setPos(-ptr1, 0)


plot_update()
timer = pg.QtCore.QTimer()
timer.timeout.connect(plot_update)
timer.start(0)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
