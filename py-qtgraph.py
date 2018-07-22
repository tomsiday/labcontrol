### Pyqt Graph plotting

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Point import Point # import a pointer mouse thing
import math
app = QtGui.QApplication([])


win = pg.GraphicsWindow(title="Time domain scan") # Open a graphics window for pyqtgraph
#win.showMaximized() # Open Window maximised

label = pg.LabelItem(justify='right') # create 'text box'
win.addItem(label) # add the 'text box' to the window

win.nextRow() # add a new row for plots 


pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots

p1 = win.addPlot() # add a plot with title
p1.setAutoVisible(y=True) # set auto range with only visible data
p1.setDownsampling(mode='peak') # downsampling reduces draw load

curve1 = p1.plot(pen='r') 

win.nextRow() # add a new row for plots 

label2 = pg.LabelItem(justify='right') # create 'text box'
win.addItem(label2) # add the 'text box' to the window

win.nextRow()

p2 = win.addPlot() # add a plot with title
p2.setAutoVisible(y=True) # set auto range with only visible data
p2.setDownsampling(mode='peak') # downsampling reduces draw load

curve2 = p2.plot(pen='g') 

def generateLines():
    global vLine, hLine, vLine2, hLine2
    vLine = pg.InfiniteLine(angle=90, movable=False, pen = 'w') # create infinite vertical line
    hLine = pg.InfiniteLine(angle=0, movable=False, pen = 'w') #  create infinite horizontal line
    p1.addItem(vLine, ignoreBounds=True) # add the vertical line
    p1.addItem(hLine, ignoreBounds=True) # add the horizontal line


    vLine2 = pg.InfiniteLine(angle=90, movable=False, pen='g') # create infinite vertical line
    hLine2 = pg.InfiniteLine(angle=0, movable=False, pen='g') #  create infinite horizontal line
    p2.addItem(vLine2, ignoreBounds=True) # add the vertical line
    p2.addItem(hLine2, ignoreBounds=True) # add the horizontal line

def mouseMovedTime(evt):
    if timer.isActive() is False: # do if scan is not running
        mousePoint = p1.vb.mapSceneToView(evt[0])
        label.setText("<span style='font-size: 12pt'>Cursor at: x=%0.3f,   <span style='color: red'>y1=%0.3f</span>" % (mousePoint.x(), mousePoint.y()))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())

proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMovedTime)

def mouseMovedFFT(evt):
    if timer.isActive() is False: # do if scan is not running
        mousePoint = p2.vb.mapSceneToView(evt[0])
        label2.setText("<span style='font-size: 12pt'>Cursor at: x=%0.3f,   <span style='color: red'>y1=%0.3f</span>" % (mousePoint.x(), mousePoint.y()))
        vLine2.setPos(mousePoint.x())
        hLine2.setPos(mousePoint.y())

proxy2 = pg.SignalProxy(p2.scene().sigMouseMoved, rateLimit=60, slot=mouseMovedFFT)


data1 = np.empty(1000) # create empty numpy array to be filled 
ptr1 = 0 # points to position on array

def update():
    global data1, ptr1
    if ptr1 < len(data1):
        data1[ptr1] = np.sin(np.radians(ptr1*10)) # generate a random number

        label.setText("<span style='font-size: 12pt'>Current sample: x=%0.3f,   <span style='color: red'>y=%0.3f</span>" % (ptr1, data1[ptr1]))
        label2.setText("<span style='font-size: 12pt'>Number of FFT points: %0.3f" % (ptr1))

        ptr1 += 1 # increase pointer

        curve1.setData(data1[:ptr1], pen = "r", clear = True) # update the plot (only new data)
        fft = np.abs(np.fft.fft(data1[:ptr1]))
        curve2.setData(fft, pen = "r", clear = True) # update the plot (only new data)

        p1.setRange(xRange=[0, ptr1+5]) # set the scale 
        p2.setRange(xRange=[0, ptr1+5]) # set the scale 

    else:
        timer.stop()
        generateLines()

timer = pg.QtCore.QTimer() # generate a timer object
timer.timeout.connect(update) # run 'update' everytime the timer ticks
timer.start(5) # timer ticks every X ms (50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()