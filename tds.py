# -*- coding: utf-8 -*-
"""Lab Control software for 910.

TIME DOMAIN SCAN
"""
###############################################################################
# Imports
## standard library imports
import sys, datetime, time, math, argparse, configparser, os, numpy as np
### Communication
import visa, serial
### Plotting
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.Point import Point
import pyqtgraph.console

## Import ESP 301 functions
from esp301 import *

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
    timer.stop() # stop the timer

def quit():
    klinger.close()
    sr830.close()
    app.closeAllWindows()

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

# callback for when the mouse is moved after the scan is complete (move cursor and set the text)
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
    metafile.write("#  Initial value : %s\n" % Tstart)
    metafile.write("#  Scan length   : %s\n" % Tlength)
    metafile.write("#  Step size     : %s\n" % Tstep)
    metafile.write("# Time\n")
    metafile.write("#  Date       : %s\n" % datetime.date.today())
    metafile.write("#  Start time : %s\n" % starttime.strftime("%H:%M:%S"))
    metafile.close()
    datafile = open(datafilename, 'w')

def start(): 
    
    global dataTD, dataFFT, ptr, TDCurve, FFTCurve, timer
    
    dataTD = np.zeros(len(stage)) # create empty numpy array to be filled 
    dataFFT = np.zeros(len(stage)) 

    ptr = 0 # points to position on array

    TDCurve = TD.plot(dataTD)
    FFTCurve = FFT.plot(dataFFT)
    
    update()

    timer = pg.QtCore.QTimer() # generate a timer object
    timer.timeout.connect(update) # run 'update' everytime the timer ticks
    timer.start(Tdwell*1e3) # timer ticks every X ms (50)

def restart():
    global dataTD, dataFFT, ptr, TDCurve, FFTCurve, timer
    
    TD.clear()
    FFT.clear()
    fileSetup()
    start()

def update():
    global dataTD, ptr, datafile
    
    if ptr < len(dataTD):
         
        dataTD[ptr] = sr830.query('OUTR ? 1') # generate a random number
        TDCursorPos.setText("<span style='font-size: 12pt'>Current sample: x=%0.3f,   <span style='color: red'>y=%0.3f</span>" % (ptr, dataTD[ptr]))
        FFTCursorPos.setText("<span style='font-size: 12pt'>Number of FFT points: %0.3f" % (ptr))

        # write data into file
        datafile.write("%d, %e\n" % (stage[ptr], dataTD[ptr]))
        datafile.flush()
        ptr += 1 # increase pointer

        TDCurve.setData(stage[:ptr], dataTD[:ptr], pen = "r", clear = True) # update the plot (only new data)
        dataFFT = np.abs(np.fft.fft(dataTD[:ptr])) # do an FFT of the data measured up till now
        FFTCurve.setData(dataFFT, pen = "r", clear = True) # update the plot (only new data)
 
        klinger.write("PW" + str(stage[ptr]))
    
    else: # What to do then the scan finishes 
        
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
        
        generateLines() # run the crosshair generate function

        if CloseOnFinish == True:
            app.closeAllWindows()

##################################################################
#  Initialise the KLinGER MC4 motion controller (delay stage)    #
##################################################################
rm = visa.ResourceManager()  # load up the pyvisa manager
# print(rm.list_resources()) #print the available devices KLINGER IS GPIB::8
klinger = rm.open_resource('GPIB0::8::INSTR')  # 'open' Klinger stage
# Sets required EOL termination
klinger.write_termination = '\r'
klinger.read_termination = '\r'

########################################################
#  Initialise the Stanford instrumetnts SR830 (Lockin) #
########################################################
sr830 = rm.open_resource('GPIB0::6::INSTR')  # 'open' sr830

# parser for config file (scan parameters)
config = configparser.ConfigParser()
config.read('scan.conf')

Tstart = int(config['TWScan']['start'])
Tlength = int(config['TWScan']['length'])
Tstep = int(config['TWScan']['step'])
Tdwell = int(config['TWScan']['dwell'])

# Parser for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-q', help = 'Specify to close the program once the scan is finished. If not specified, the scan will finish and a terminal will open for control', action='store_true')
parser.add_argument('-x', help = 'Horisontal position of sample ("x" position).', action='store')
parser.add_argument('-y', help = 'Vertical position of sample along optical axis ("y" position).', action='store')
parser.add_argument('-z', help = 'Position of sample along optical axis ("z" position).', action='store')
args = parser.parse_args()

app = QtGui.QApplication([])
screen= app.desktop().availableGeometry() # get size of screen not already occupied (e.g. by the 0.0windows bar)

win = pg.GraphicsWindow() # Open a graphics window for pyqtgraph
win.setWindowTitle("Time Domain Spectroscopy")

TitleBar = 30 # title bar thickness (would be good to be able to get this peice of information automatically)
ConsoleWidth = 300
win.setGeometry(0, TitleBar, screen.width()-ConsoleWidth, screen.height()-TitleBar)
win.show()

NotificationText = pg.LabelItem(justify='left')
ScanParameterText = "<span style='font-size: 12pt'><span style='color: white'>Start: %0.0f, Length: %0.0f, Step: %0.0f, Dwell:, %0.0f" % (Tstart, Tlength, Tstep, Tdwell)

if args.q:
    CloseOnFinish = True
    NotificationText.setText("<span style='font-size: 12pt'><span style='color: green'>The program will close when the scan is finished. Data will be saved. " + ScanParameterText)
else:
    CloseOnFinish = False
    NotificationText.setText("<span style='font-size: 12pt'><span style='color: green'>The program will not close automatically. Data will be saved. " + ScanParameterText)

if args.x is not None:
    xgo(int(args.x))

if args.y is not None:
    ygo(int(args.y))

if args.z is not None:
    zgo(int(args.z))

StagePositionText = pg.LabelItem(justify = 'left')
StagePositionText.setText("<span style='font-size: 12pt'><span style='color: green'>x: " + str(args.x) + " y: " + str(args.y) + " z: " + str(args.z))

TDCursorPos = pg.LabelItem() # create 'text box' to show the position of the cursor/current TD sample 
FFTCursorPos = pg.LabelItem() # create 'text box' to show the position of the cursor/number of FFT points

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
win.addItem(NotificationText)
win.nextRow()
win.addItem(StagePositionText)
console=pg.console.ConsoleWidget(namespace={'tgo': tgo, 'stop': stop, 'restart': restart, 'quit': quit, 'xgo':xgo, 'ygo':ygo, 'zgo':zgo}) # add a console to enter commands after the scan is complete
console.setWindowTitle('Console')
console.setGeometry(screen.width()-ConsoleWidth, TitleBar, ConsoleWidth, screen.height()-TitleBar)
console.show()

proxy = pg.SignalProxy(TD.scene().sigMouseMoved, rateLimit=60, slot=mouseMovedTD)
proxy2 = pg.SignalProxy(FFT.scene().sigMouseMoved, rateLimit=60, slot=mouseMovedFFT)

# array with positions of time delay stage

stage = np.arange(Tstart, Tstart-Tlength-Tstep, -Tstep) # the extra Tstep is to account for the final time position, as python is zero indexed

fileSetup()
start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
