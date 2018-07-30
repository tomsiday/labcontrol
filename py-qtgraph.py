### Pyqt Graph plotting

from pyqtgraph.Qt import QtGui, QtCore # import Qt libaries
import numpy as np 
import pyqtgraph as pg
from pyqtgraph.Point import Point # import a pointer mouse thing
import pyqtgraph.console # so we have a console in which to enter commands
import math
import argparse

def generateLines():
    global vLineTD, hLineTD, vLineFFT, hLineFFT
    vLineTD = pg.InfiniteLine(angle=90, movable=False, pen = 'w') # create infinite vertical line
    hLineTD = pg.InfiniteLine(angle=0, movable=False, pen = 'w') #  create infinite horizontal line
    TD.addItem(hLineTD, ignoreBounds=True) # add the horizontal line
    TD.addItem(vLineTD, ignoreBounds=True) # add vertical line

    vLineFFT = pg.InfiniteLine(angle=90, movable=False, pen='g') # create infinite vertical line
    hLineFFT = pg.InfiniteLine(angle=0, movable=False, pen='g') #  create infinite horizontal line
    FFT.addItem(vLineFFT, ignoreBounds=True) # add the vertical line
    FFT.addItem(hLineFFT, ignoreBounds=True) # add the horizontal line

def mouseMovedTD(evt):
    if timer.isActive() is False: # do if scan is not running
        mousePoint = TD.vb.mapSceneToView(evt[0]) # get the mouse position
        TDCursorPos.setText("<span style='font-size: 12pt'>Cursor at: x=%0.3f,   <span style='color: red'>y1=%0.3f</span>" % (mousePoint.x(), mousePoint.y())) # set the numerical display
        vLineTD.setPos(mousePoint.x()) # move the vertical line
        hLineTD.setPos(mousePoint.y()) # move the horisontal line

def mouseMovedFFT(evt):
    if timer.isActive() is False: # do if scan is not running
        mousePoint = FFT.vb.mapSceneToView(evt[0])
        FFTCursorPos.setText("<span style='font-size: 12pt'>Cursor at: x=%0.3f,   <span style='color: red'>y1=%0.3f</span>" % (mousePoint.x(), mousePoint.y()))
        vLineFFT.setPos(mousePoint.x())
        hLineFFT.setPos(mousePoint.y())

parser = argparse.ArgumentParser()
parser.add_argument('-q', help = 'Specify to close the program once the scan is finished', action='store_true')

args = parser.parse_args()

if args.q:
    CloseOnFinish = True
    print('The program will close when the scan is finished. Data will be saved')
else:
    CloseOnFinish = False
    print('The program will not close automatically')


print(CloseOnFinish)

quit()
app = QtGui.QApplication([])

win = pg.GraphicsWindow() # Open a graphics window for pyqtgraph
win.setWindowTitle("Time Domain Spectroscopy")
win.setGeometry(50,100,1000,500)
win.show()

TDCursorPos = pg.LabelItem() # create 'text box'
FFTCursorPos = pg.LabelItem() # create 'text box'

win.addItem(TDCursorPos)
win.nextRow() # add new plot row

TD = win.addPlot() # add a plot with title
TD.setAutoVisible(y=True) # set auto range with only visible data
TD.setDownsampling(mode='peak') # downsampling reduces draw load

win.nextRow()

win.addItem(FFTCursorPos)

win.nextRow()

FFT = win.addPlot() # add/ a plot with title
FFT.setAutoVisible(y=True) # set auto range with only visible data
FFT.setDownsampling(mode='peak') # downsampling reduces draw load
win.nextRow()

console=pg.console.ConsoleWidget()
console.setWindowTitle('Console')
console.setGeometry(1050,100,300,500)

proxy = pg.SignalProxy(TD.scene().sigMouseMoved, rateLimit=60, slot=mouseMovedTD)
proxy2 = pg.SignalProxy(FFT.scene().sigMouseMoved, rateLimit=60, slot=mouseMovedFFT)

dataTD = np.empty(100) # create empty numpy array to be filled 
dataFFT = np.empty(100) 

ptr = 0 # points to position on array

TDCurve = TD.plot(dataTD)
FFTCurve = FFT.plot(dataFFT)

def update():
    global dataTD, ptr
    if ptr < len(dataTD):
        dataTD[ptr] = np.sin(np.radians(ptr*10)) # generate a random number

        TDCursorPos.setText("<span style='font-size: 12pt'>Current sample: x=%0.3f,   <span style='color: red'>y=%0.3f</span>" % (ptr, dataTD[ptr]))
        FFTCursorPos.setText("<span style='font-size: 12pt'>Number of FFT points: %0.3f" % (ptr))

        ptr += 1 # increase pointer

        TDCurve.setData(dataTD[:ptr], pen = "r", clear = True) # update the plot (only new data)
        dataFFT = np.abs(np.fft.fft(dataTD[:ptr])) # do an FFT of the data measured up till now
        FFTCurve.setData(dataFFT, pen = "r", clear = True) # update the plot (only new data)

        #TD.setRange(xRange=[0, ptr+5]) # set the scale 
        #FFT.setRange(xRange=[0, ptr+5]) # set the scale 

    else: # TODO add a conf. file optin to close on exit, for sweeps

        timer.stop() # stop the timer
        generateLines() # run the crosshair generate function
        
        if CloseOnFinish == True:
            app.closeAllWindows()
        else: 
            console.show()    

timer = pg.QtCore.QTimer() # generate a timer object
timer.timeout.connect(update) # run 'update' everytime the timer ticks
timer.start(500) # timer ticks every X ms (50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
