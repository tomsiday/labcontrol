"""
Lab Control software for 910.

Measuring the scattering of indium tip, multiple harmonics

"""
###############################################################################
# Imports
## standard library imports
import sys, datetime, time, math, argparse, configparser, os, numpy as np
### Communication
import visa, serial
## Ni DAQ
import nidaqmx
### Plotting
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.Point import Point
import pyqtgraph.console

# Third party imports
import zhinst.utils

from genFuncs import *

def tgo(tPosition):
    klinger.write("PW" + str(tPosition))
    print("Moving delay stage to " + str(tPosition))

def xgo(xPosition):
    print("Moving sample to x = " + str(xPosition))

def ygo(yPosition):
    print("Moving sample to y = " + str(yPosition))

def zgo(zPosition):
    print("Moving sample to z = " + str(zPosition))

def stop():
    
    global demod1Line
    timer.stop() # stop the timer
    klinger.clear() ## needed otherwse the klinger complains (TODO: work out why)  

    demod1Line = genLines(demod1) # run the crosshair generate function
def quit():
    
    klinger.clear() ## needed otherwse the klinger complains (TODO: work out why)  
    klinger.close()
    app.closeAllWindows()


def fileSetup():

    global metafile, datafile, metafilename

    # get time for filename
    starttime = datetime.datetime.now()
    
    print(
            "► TimeScan start : %s ◄               "
             % starttime.strftime("%H:%M:%S"), end='\n', flush=True
             )
    
    # generate filename string
    dateNow = starttime.strftime("%Y%m%d")
    timeNow = starttime.strftime("%H%M")
    
    if os.path.isdir(dateNow) is False: # check for today's folder. if it doesnt exist, make it
        os.mkdir(dateNow)

    metafilename = (dateNow + '/' + timeNow + "-TWScan-metadata.txt")
    datafilename = (dateNow + '/' + timeNow + "-TWScan.txt")
    metafile = open(metafilename, 'w')

    #metafile.write("# Sample initial position\n")
    #metafile.write("#  X   : %f\n" % XYscanner.position(1))
    #metafile.write("#  Y   : %f\n" % XYscanner.position(2))
    #metafile.write("#  Z   : %f\n" % XYscanner.position(3))
    metafile.write("# Delay line\n")
    metafile.write("#  Initial value : %s\n" % CP.Tstart)
    metafile.write("#  Scan length   : %s\n" % CP.Tlength)
    metafile.write("#  Step size     : %s\n" % CP.Tstep)
    metafile.write("# Time\n")
    metafile.write("#  Date       : %s\n" % datetime.date.today())
    metafile.write("#  Start time : %s\n" % starttime.strftime("%H:%M:%S"))
    metafile.close()
    datafile = open(datafilename, 'w')

def start(): 
    
    global datademod1, dataFFT, ptr, demod1Curve, FFTCurve, timer
    
    datademod1 = np.zeros(len(stage)) # create empty numpy array to be filled 
    dataFFT = np.zeros(len(stage)) 

    ptr = 0 # points to position on array

    demod1Curve = demod1.plot(datademod1)
    FFTCurve = FFT.plot(dataFFT)
     
    proxy = pg.SignalProxy(demod1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
    proxy2 = pg.SignalProxy(FFT.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

    timer = pg.QtCore.QTimer() # generate a timer object
    timer.timeout.connect(update) # run 'update' everytime the timer ticks
    timer.start(CP.Tdwell*1e3) # timer ticks every X ms (50)

    
def restart():
    global datademod1, dataFFT, ptr, demod1Curve, FFTCurve, timer
    
    demod1.clear()
    FFT.clear()
    fileSetup()
    start()

def update():
    global datademod1, ptr, datafile, demod1Line
    
    if ptr < len(datademod1):
         
        
        demod1CursorPos.setText("<span style='font-size: 12pt'>Current sample: x=%0.3f,   <span style='color: red'>y=%0.3f</span>" % (ptr, datademod1[ptr]))
        FFTCursorPos.setText("<span style='font-size: 12pt'>Number of FFT points: %0.3f" % (ptr))
        
        out = MFLI.daq.getSample('/%s/demods/%d/sample' % (MFLI.device, MFLI.demod_0)) # Grab a sample from the MFLI
            
        out['r'] = np.abs(out['x'] + 1j*out['y']) # calculate magnitude from 
            
        if CP.RX == 'X' or 'x':
            datademod1[ptr] = out['x']
        if CP.RX == 'R' or 'r':
            datademod1[ptr] = out['r']
       
       # write data into file
        datafile.write("%d, %e\n" % (stage[ptr], datademod1[ptr]))
        datafile.flush()
        ptr += 1 # increase pointer

        demod1Curve.setData(stage[:ptr], datademod1[:ptr], pen = "r", clear = True) # update the plot (only new data)
        dataFFT = np.abs(np.fft.fft(datademod1[:ptr])) # do an FFT of the data measured up till now
        FFTCurve.setData(dataFFT, pen = "r", clear = True) # update the plot (only new data)
        
        klinger.move(stage[ptr])

    else: # What to do then the scan finishes 
       

        klinger.clear() ## needed otherwse the klinger complains (TODO: work out why)  
        datafile.close()
        metafile = open(metafilename, 'a')
        metafile.write(
                "#  Finish time: %s\n"
                % datetime.datetime.now().strftime("%H:%M:%S")
                )
        metafile.close()
        print(
                "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b► Finished : %s ◄"
                % datetime.datetime.now().strftime("%H:%M:%S"), end='\n'
                )
        
        timer.stop() # stop the timer
        
        demod1Line = genLines(demod1) # run the crosshair generate function

        if CloseOnFinish == True:
            app.closeAllWindows()


CP = ConfigParser()
CL = CLineParser()

rm = visa.ResourceManager()  # load up the pyvisa manager
klinger = klinger(rm)


MFLI = MFLI()
MFLI.set(CP)

app = QtGui.QApplication([])
screen= app.desktop().availableGeometry() # get size of screen not already occupied (e.g. by the 0.0windows bar)

win = pg.GraphicsWindow() # Open a graphics window for pyqtgraph
win.setWindowTitle("Time Domain Spectroscopy")

TitleBar = 30 # title bar thickness (would be good to be able to get this peice of information automatically)
ConsoleWidth = 300
win.setGeometry(0, TitleBar, screen.width()-ConsoleWidth, screen.height()-TitleBar)
win.show()

NotificationText = pg.LabelItem(justify='left')
ScanParameterText = "<span style='font-size: 12pt'><span style='color: white'>Start: %0.0f, Length: %0.0f, Step: %0.0f, Dwell:, %0.1f" % (CP.Tstart, CP.Tlength, CP.Tstep, CP.Tdwell)

if CL.q:
    CloseOnFinish = True
    NotificationText.setText("<span style='font-size: 12pt'><span style='color: green'>The program will close when the scan is finished. Data will be saved. " + ScanParameterText)
else:
    CloseOnFinish = False
    NotificationText.setText("<span style='font-size: 12pt'><span style='color: green'>The program will not close automatically. Data will be saved. " + ScanParameterText)

if CL.x is not None:
    xgo(int(CL.x))

if CL.y is not None:
    ygo(int(CL.y))

if CL.z is not None:
    zgo(int(CL.z))

StagePositionText = pg.LabelItem(justify = 'left')
StagePositionText.setText("<span style='font-size: 12pt'><span style='color: green'>x: " + str(CL.x) + " y: " + str(CL.y) + " z: " + str(CL.z))

demod1CursorPos = pg.LabelItem() # create 'text box' to show the position of the cursor/current TD sample 
FFTCursorPos = pg.LabelItem() # create 'text box' to show the position of the cursor/number of FFT points

win.addItem(demod1CursorPos) 
win.nextRow() # add new plot row

demod1 = win.addPlot() # add a plot with title
demod1.setAutoVisible(y=True) # set auto range with only visible data
demod1.setDownsampling(mode='peak') # downsampling reduces draw load

demod2 = win.addPlot() # add a plot with title
demod2.setAutoVisible(y=True) # set auto range with only visible data
demod2.setDownsampling(mode='peak') # downsampling reduces draw load

demod3 = win.addPlot() # add a plot with title
demod3.setAutoVisible(y=True) # set auto range with only visible data
demod3.setDownsampling(mode='peak') # downsampling reduces draw load

win.nextRow()
win.addItem(FFTCursorPos)
win.nextRow()

FFT = win.addPlot() # add/ a plot with title
FFT.setAutoVisible(y=True) # set auto range with only visible data
FFT.setDownsampling(mode='peak') # downsampling reduces draw load

win.nextRow()
win.addItem(NotificationText)
win.nextRow()
win.addItem(StagePositionText)
console=pg.console.ConsoleWidget(namespace={'tgo': tgo, 'stop': stop, 'restart': restart, 'quit': quit, 'xgo':xgo, 'ygo':ygo, 'zgo':zgo}) # add a console to enter commands after the scan is complete
console.setWindowTitle('Console')
console.setGeometry(screen.width()-ConsoleWidth, TitleBar, ConsoleWidth, screen.height()-TitleBar)
console.show()



# array with positions of time delay stage

stage = np.arange(CP.Tstart, CP.Tstart-CP.Tlength-CP.Tstep, -CP.Tstep) # the extra Tstep is to account for the final time position, as python is zero indexed

fileSetup()
start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
