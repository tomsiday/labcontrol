### Pyqt Graph plotting

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Point import Point # import a pointer mouse thing

app = QtGui.QApplication([])


win = pg.GraphicsWindow(title="Basic plotting examples") # Open a graphics window for pyqtgraph
win.showMaximized() # Open Window maximised

label = pg.LabelItem(justify='right') # create 'text box'
win.addItem(label) # add the 'text box' to the window

win.nextRow() # add a new row for plots 


pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots

p1 = win.addPlot() # add a plot with title
p1.setAutoVisible(y=True) # set auto range with only visible data
p1.setDownsampling(mode='peak') # downsampling reduces draw load
p1.setClipToView(True) # dont know
p1.setRange(xRange=[0, 100]) # set the initial plot range
p1.setLimits(xMin=0) # set the maximum of the plot (is this needed?)
curve1 = p1.plot(pen='r') 
 
data1 = np.empty(100) # create empty numpy array to be filled 
ptr1 = 0 # points to position on array

# Add a crosshair
vLine = pg.InfiniteLine(angle=90, movable=False) # create infinite vertical line
hLine = pg.InfiniteLine(angle=0, movable=False) #  create infinite horizontal line
p1.addItem(vLine, ignoreBounds=True) # add the vertical line
p1.addItem(hLine, ignoreBounds=True) # add the horizontal line

vb = p1.vb

def mouseMoved(evt): # callback for moved mouse
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple, so need to de-tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > 0 and index < len(data1):
            label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>" % (mousePoint.x(), data1[index]))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())



proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)

def update1():
    global data1, ptr1
    data1[ptr1] = np.random.normal() # generate a random number
    ptr1 += 1 # increase pointer
    if ptr1 >= data1.shape[0]: # is the pointer number larger than the length of the array?
        tmp = data1 # put the data in a temp. array
        data1 = np.empty(data1.shape[0] * 2) # generate an empty array with double the length of the current array
        data1[:tmp.shape[0]] = tmp # fill the new array with the old data
    curve1.setData(data1[:ptr1]) # update the plot (only new data)
    #curve1.setPos(0, ptr1)

win.nextRow() # add a new row for plots 

p2 = win.addPlot(title="Basic array plotting") # add a plot

# update all the plots (if there are more than one, otherwise this is not needed)
def update():
    update1()

timer = pg.QtCore.QTimer() # generate a timer object
timer.timeout.connect(update) # run 'update' everytime the timer ticks
timer.start(50) # timer ticks every X ms (50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()