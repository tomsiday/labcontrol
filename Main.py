##########################################
###### Lab Control software for 910 ######
############### Tom Siday ################
##########################################
import matplotlib
matplotlib.use('Qt4Agg')

### start bokeh server BEFORE running this program -- (bokeh serve)
## Initial scan parameter values 

delay_position = 0 # Set the delay stage to the default position (0),,(THIS VAL CHANGES)
delay_pos_init = 0 # Initial delay stage position
delay_step = 5 # Default scan time step
delay_length = 100 # Default scan time length (steps)
t_wait = 1 # Time domain dwell time (s)
jog_XYZ = 0.5 # The translation jog step for XYZ axis of NanoMax600
jog_Theta = 0.5 # Rotation jog step for NanoMax600

XY_posX_init = 0
XY_posY_init = 0

XYStepX = 10 #um
XYStepY = 10 #um

XYLengthX = 100 #um
XYLengthY = 100 #um

XorR = 'x' # Display X or R

## Initial XT scan parameters

XT_pos_space_init = 0
XTStepSpace = 10
XTLengthSpace = 100

XT_pos_time_init = 0
XTStepTime = 10
XTLengthTime = 100

##################################################################
### Initialise the KLinGER MC4 motion controller (delay stage) ###
##################################################################
import visa # For GPIB communications

rm = visa.ResourceManager() # load up the pyvisa manager
print(rm.list_resources()) #print the availible devices  Klinger is 8 for now.
klinger = rm.open_resource('GPIB0::8::INSTR') # Open klinger for comms
# Se the EOL termination (otherwise  the klinger isnt happy)
klinger.write_termination = '\r'
klinger.read_termination = '\r'

##############################################
### Initialise the Zurich instruments MFLI ###
##############################################
import zhinst.utils 
import numpy as np
import time
# Serial number of our MFLI
device_id = 'dev3047'
# API level in the 17,06 release from ZI. (probably not a good idea to change this..) 
apilevel = 6 
# Create a session (daq) for communication with the MFLI. device is the serial number, and props is a load of useful info about the session
(daq, device, props) = zhinst.utils.create_api_session(device_id, apilevel, required_devtype='.*LI|.*IA|.*IS')
# check out api versions align (incase some nutter has updated the MFLI firmware)
print('PC and MFLI API version align?:', zhinst.utils.api_server_version_check(daq))
# Base config for MFLI -- disable everything
general_setting = [['/%s/demods/*/enable' % device, 0],
                       ['/%s/demods/*/trigger' % device, 0],
                       ['/%s/sigouts/*/enables/*' % device, 0],
                       ['/%s/scopes/*/enable' % device, 0]]
# Set this base config on the MFLI
daq.set(general_setting)
# SYNC (make sure PC and MFLI agree with settings, etc...)
daq.sync()
## Configure the MFLI for streaming data - these are all standard settings, availible in the MFLI manual (and in exp_setting below)
out_channel = 0
out_mixer_channel = zhinst.utils.default_output_mixer_channel(props)
in_channel = 0 # Signal in from preamp (+V)
demod_index = 0
osc_index = 0
demod_rate = 1e3
time_constant = 0.3
osc_frequency = 32369.665
# Initial settings for THz time domain experiments.
exp_setting = [['/%s/sigins/%d/ac'             % (device, in_channel), 0],
                   ['/%s/sigins/%d/ac'             % (device, in_channel), 1], # Set AC coupling (yes)
				   ['/%s/sigins/%d/imp50'          % (device, in_channel), 0], # Use 10Mohm impedance
				   ['/%s/sigins/%d/diff'           % (device, in_channel), 1], # Differential input
				   ['/%s/sigins/%d/float'           % (device, in_channel), 0], # Float off
                   ['/%s/sigins/%d/range'          % (device, in_channel), 0.03], # Range setting
                   ['/%s/demods/%d/enable'         % (device, demod_index), 1], # Enable demod 0
                   ['/%s/demods/%d/rate'           % (device, demod_index), demod_rate], # Set data transfer rate to PC \(dont really know why this matters)
                   ['/%s/demods/%d/adcselect'      % (device, demod_index), in_channel], # Set input channel for demod 0
                   ['/%s/demods/%d/order'          % (device, demod_index), 4], # Set filter order for demod 0 
                   ['/%s/demods/%d/timeconstant'   % (device, demod_index), time_constant], # Set filter time contstant
                   ['/%s/demods/%d/oscselect'      % (device, demod_index), osc_index], # Set oscillator for demod 0 (we only have 1)
                   ['/%s/demods/%d/harmonic'       % (device, demod_index), 1], # Set harmonic for mesurement
                   ['/%s/extrefs/0/enable'         % (device), 1], # Set external reference on/off (optical chopper)
					#['/%s/oscs/1/freq'         % (device), osc_frequency]]
['/%s/demods/1/adcselect'       % (device), 8]] # Select the input for the external reference
# set the above settings on the MFLI
daq.set(exp_setting)
# Stop from any data streaming/being collected (needs to be done as prep for measurements)
daq.unsubscribe('*')
# Wait for demod filter to settle (10 * filter time constant)
time.sleep(10*time_constant)
# SYNC (make sure PC and MFLI agree with settings, etc...) - must be done after waiting for the demod filter to settle
daq.sync()

########################################################################
### Initialise the ESP301 motion controller for aperture experiments ###
########################################################################
import serial
# Initialise ESP301 serial connection
XYscanner = serial.Serial('COM2', baudrate=921600, rtscts=True)
# Flush and reset serial buffers
XYscanner.flush()
XYscanner.reset_input_buffer()
XYscanner.reset_output_buffer()
# Ask the ESP301 to identify the stage on axis 1 \r new line
XYscanner.write(b"1ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a MFA-CC)
print('Stage', XYscanner.read(XYscanner.in_waiting), 'Connected (AX1)')

# Ask the ESP301 to identify the stage on axis 2 \r new line
XYscanner.write(b"2ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a MFA-CC)
print('Stage', XYscanner.read(XYscanner.in_waiting), 'Connected (AX2)')

# Ask the ESP301 to identify the stage on axis 3 \r new line
XYscanner.write(b"3ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a MFA-CC)
print('Stage', XYscanner.read(XYscanner.in_waiting), 'Connected (AX3)')

import sys
from PyQt4 import QtCore, QtGui
from Gui import Ui_MainWindow

import time 

import matplotlib.pyplot as plt
import numpy as np
import datetime

class Main(QtGui.QMainWindow,Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui= Ui_MainWindow()
		self.ui.setupUi(self)
		
		#Time domain tab
		self.ui.TStart.clicked.connect(self.startTScan)
		self.ui.TStop.clicked.connect(self.stop)
		self.ui.GoTScanStart.clicked.connect(self.UpdateTStart)
		self.ui.GoTScanLength.clicked.connect(self.UpdateTScanLength)		
		self.ui.GoTStep.clicked.connect(self.UpdateTStep)
		self.ui.GoTDwell.clicked.connect(self.UpdateTDwell)
		
		#XT scan (aperture) tab
		self.ui.XYStartBut.clicked.connect(self.startXYScan)
		self.ui.XYStopBut.clicked.connect(self.stop)
		self.ui.GoXYStartX.clicked.connect(self.UpdateXYStartX)
		self.ui.GoXYStartY.clicked.connect(self.UpdateXYStartY)
		self.ui.GoXYStepX.clicked.connect(self.UpdateXYStepX)
		self.ui.GoXYStepY.clicked.connect(self.UpdateXYStepY)
		self.ui.GoXYLengthX.clicked.connect(self.UpdateXYLengthX)
		self.ui.GoXYLengthY.clicked.connect(self.UpdateXYLengthY)
		self.ui.GoZPos.clicked.connect(self.UpdateZPos) # Set the sample stage position in Z
		self.ui.GoDelayPos.clicked.connect(self.UpdateDelayPos) # set position of delay stage
		
		self.ui.XTStartBut.clicked.connect(self.startXTScan) # Start the XT scan
		self.ui.XTStopBut.clicked.connect(self.stop) # Stop the XT scan
		self.ui.GoXTStartSpace.clicked.connect(self.UpdateXTStartSpace) # update XT scan start position (instant)
		self.ui.GoXTStepSpace.clicked.connect(self.UpdateXTStepSpace) # update XT scan step in space
		self.ui.GoXTLengthSpace.clicked.connect(self.UpdateXTLengthSpace) # set length of XT scan (space) on click
		self.ui.GoXTStartTime.clicked.connect(self.UpdateXTStartTime) # set XT scan time start (instant)
		self.ui.GoXTStepTime.clicked.connect(self.UpdateXTStepTime) # set XT time step
		self.ui.GoXTLengthTime.clicked.connect(self.UpdateXTLengthTime) # set XT time length
		
		
		self._generator = None
		self._timerId = None

	def UpdateXTStartSpace(self):
		global XT_pos_space_init
		XT_pos_space_init = self.ui.XTStartSpace.text()
		if self.ui.ScanAlongY.isChecked() == True:
			XYscanner.write(("2PA"+str(int(XT_pos_space_init)*1e-3) + "\r").encode())
		if self.ui.ScanAlongX.isChecked() == True:
			XYscanner.write(("1PA"+str(int(XT_pos_space_init)*1e-3) + "\r").encode())
		
		print("X axis start position " + XT_pos_space_init)
		
	def UpdateXTStepSpace(self): 
		global XTStepSpace
		XTStepSpace = self.ui.XTStepSpace.text()
		print("XT scan space step " + str(XTStepSpace) + " mm")
		
	def UpdateXTLengthSpace(self): 
		global XTLengthSpace
		XTLengthSpace = self.ui.XTLengthSpace.text()
		print("XT scan space length " + str(XTLengthSpace) + " mm")
		
	def UpdateXTStartTime(self): # Set and move delay stage to initial position.
		global XT_pos_time_init
		XT_pos_time_init = self.ui.XTStartTime.text()
		klinger.write("PW" + str(XT_pos_time_init))
		print("Delay stage initial position: " + str(XT_pos_time_init))		
		
	def UpdateXTStepTime(self):
		global XTStepTime
		XTStepTime = self.ui.XTStepTime.text()
		print("XT scan time step " + str(XTStepTime))
		
	def UpdateXTLengthTime(self): 
		global XTLengthTime
		XTLengthTime = self.ui.XTLengthTime.text()
		print("XT scan time length " + str(XTLengthTime))
		
	def startXTScan(self):  # Connect to Start-button clicked()
		self.stop()  # Stop any existing timer
		self._generator = self.XTScan()  # Start the loop
		self._timerId = self.startTimer(0)   # This is the idle timer
		
	def XTScan(self): # Loop to run the XT scan (including collect and plot data)
		
		xy = np.arange(float(XT_pos_space_init), float(XT_pos_space_init)+float(XTLengthSpace), float(XTStepSpace))
		t = np.arange(float(XT_pos_time_init), float(XT_pos_time_init)-float(XTLengthTime), -float(XTStepTime))
		
		print(xy)
		print(t)
		
		X, T, = np.mgrid[int(XT_pos_space_init):int(XT_pos_space_init)+int(XTLengthSpace):int(XTStepSpace), int(XT_pos_time_init):int(XT_pos_time_init)+int(XTLengthTime):int(XTStepTime)]

		Z = np.zeros((len(t), len(xy)))
		
		ax = self.ui.XTPlot.figure.add_subplot(111)
		
		for a in range(0, len(t)):
			
			klinger.write("PW" + str(t[a]))
			
			for b in range(0, len(xy)):
				
				if self.ui.ScanAlongY.isChecked() == True: # Scan changes y values (channel 2)
					
					XYscanner.write(("2PA"+str(xy[b]*1e-3) + "\r").encode()) # set y position
				
				if self.ui.ScanAlongX.isChecked() == True: # Scan changes x values (channel 2)
					
					XYscanner.write(("1PA"+str(xy[b]*1e-3) + "\r").encode()) # set x position
				
				time.sleep(t_wait)
				
				out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
				out['r'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y	
				
				if self.ui.XTLockinX.isChecked() == True: # Select whether the plot is X or magnitude
					Z[b,a] = out['x']
				if self.ui.XTLockinR.isChecked() == True:
					Z[b,a] = out['r']
				
				ax.clear()
				ax.pcolor(X,T,Z)
				
				ax.set_xlabel('X (microns)')
				ax.set_ylabel('time')
				
				self.ui.XTPlot.draw()
				self.ui.XTPlot.flush_events() # Flush the plot drawing - makes sure the plot updates.
				yield	
				
		print(Z)
		currenttime = datetime.datetime.now()
		filename = str(currenttime.hour) + str(currenttime.minute) + "-XTScan.txt"
		np.savetxt(filename, Z, delimiter=',')
		
	
	def startXYScan(self):  # Connect to Start-button clicked()
		self.stop()  # Stop any existing timer
		self._generator = self.XYScan()  # Start the loop
		self._timerId = self.startTimer(0)   # This is the idle timer	
	def XYScan(self): # Loop to run the XY scan (including collect and plot data)
		
		x = np.arange(float(XY_posX_init), float(XY_posX_init)+float(XYLengthX), float(XYStepX))
		y = np.arange(float(XY_posY_init), float(XY_posY_init)+float(XYLengthY), float(XYStepY))
		
		print(x)
		print(y)
		
		X, Y, = np.mgrid[int(XY_posX_init):int(XY_posX_init)+int(XYLengthX):int(XYStepX), int(XY_posY_init):int(XY_posY_init)+int(XYLengthY):int(XYStepY)]

		Z = np.zeros((len(y), len(x)))
		
		ax = self.ui.XYPlot.figure.add_subplot(111)

		
		for a in range(0, len(y)):
			
			XYscanner.write(("2PA"+str(y[a]*1e-3) + "\r").encode()) # set y position

			for b in range(0, len(x)):
				
				XYscanner.write(("1PA"+str(x[b]*1e-3) + "\r").encode()) # set x position
				
				time.sleep(t_wait)
				
				out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
				out['r'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y	
				
				if self.ui.XYLockinX.isChecked() == True: # Select whether the plot is X or magnitude
					Z[b,a] = out['x']
				if self.ui.XYLockinR.isChecked() == True:
					Z[b,a] = out['r']
					
				ax.clear()
				ax.pcolor(X,Y,Z)
				ax.set_xlabel('x (microns)')
				ax.set_ylabel('y (microns)')
				
				self.ui.XYPlot.draw()
				
				self.ui.XYPlot.flush_events() # Flush the plot drawing - makes sure the plot updates.
				
				yield
			
				
			
		print(Z)
		currenttime = datetime.datetime.now()
		filename = str(currenttime.hour) + str(currenttime.minute) + "-XYScan.txt"
		np.savetxt(filename, Z, delimiter=',')	
	
	def UpdateDelayPos(self): # Set and move delay stage
		DelayPos = self.ui.DelayPos.text()
		klinger.write("PW" + str(DelayPos))
		print("Delay stage initial position: " + str(delay_pos_init))				
	def UpdateZPos(self): # set sample stage position in microns
		global ZPos
		ZPos = self.ui.ZPos.text()
		XYscanner.write(("3PA"+str(int(ZPos)*1e-3) + "\r").encode())
		print("Z position set to " + ZPos + " microns")			
	def UpdateXYLengthY(self): 
		global XYLengthY
		XYLengthY = self.ui.XYLengthY.text()
		print("XY scan Y length " + str(XYLengthY) + " mm")		
	def UpdateXYLengthX(self): 
		global XYLengthX
		XYLengthX = self.ui.XYLengthX.text()
		print("XY scan X length " + str(XYLengthX) + " mm")	
	def UpdateXYStepX(self): 
		global XYStepX
		XYStepX = self.ui.XYStepX.text()
		print("XY scan X step " + str(XYStepX) + " mm")
	def UpdateXYStepY(self):
		global XYStepY
		XYStepY = self.ui.XYStepY.text()
		print("XY scan Y step " + str(XYStepY) + " mm")	
	def UpdateXYStartX(self):
		global XY_posX_init
		XY_posX_init = self.ui.XYStartX.text()
		XYscanner.write(("1PA"+str(int(XY_posX_init)*1e-3) + "\r").encode())
		print("X axis start position " + XY_posX_init)		
	def UpdateXYStartY(self):
		global XY_posY_init
		XY_posY_init = self.ui.XYStartY.text()
		XYscanner.write(("2PA"+str(int(XY_posY_init)*1e-3) + "\r").encode())
		print("Y axis start position " + XY_posY_init)			
	def UpdateTStart(self): # Set and move delay stage to initial position.
		global delay_pos_init
		delay_pos_init = self.ui.TScanStart.text()
		klinger.write("PW" + str(delay_pos_init))
		print("Delay stage initial position: " + str(delay_pos_init))
	def UpdateTScanLength(self): # Set time scan length (in steps)
		global delay_length
		delay_length = int(self.ui.TScanLength.text())
		print("Scan length " + str(delay_length) + " steps")	
	def UpdateTStep(self): # Set time scan length (in steps)
		global delay_step
		delay_step = int(self.ui.TStep.text())
		print("Scan step " + str(delay_step) + " steps")		
	def UpdateTDwell(self): # Set dwell time (seconds)
		global t_wait
		t_wait = float(self.ui.TDwell.text())
		print("Dwell time " + str(t_wait) + "s")	
		
	def TimeScan(self):
		
		X = np.arange(float(delay_pos_init), float(delay_pos_init)-float(delay_length), -float(delay_step))
		Y = np.zeros(len(X))
		
		ax = self.ui.TPlot.figure.add_subplot(211)
		ax2 = self.ui.TPlot.figure.add_subplot(212)

		for a in range(0, len(X)): # -, stage goes high to low.
			
			klinger.write("PW" + str(X[a])) # Send the position to the KLINGER
			
			time.sleep(t_wait) # wait for lock-in filter to settle 'integration time'
			
			out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
			out['r'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y
			
			if self.ui.TLockinX.isChecked() == True: # Select whether the plot is X or magnitude
				Y[a] = out['x']
			if self.ui.TLockinR.isChecked() == True:
				Y[a] = out['r']
			
			ax.clear()
			ax.plot(X[0:a+1], Y[0:a+1])
			
			ax.set_xlabel('Time')
			ax.set_ylabel('Lock-in output (V)')
			
			FFT = np.real(np.fft.fft(Y)) # Fourier transform

			ax2.clear()
			ax2.plot(X[0:a+1], FFT[0:a+1])
				
			ax2.set_xlabel('Arb')
			ax2.set_ylabel('Magnitude')
			
			self.ui.TPlot.draw()
			self.ui.TPlot.flush_events() # Flush the plot drawing - makes sure the plot updates.
			
			yield # check if stop button has been pressed.
		
		currenttime = datetime.datetime.now()
		filename = str(currenttime.hour) + str(currenttime.minute) + "-TWScan.txt"
		np.savetxt(filename, Y, delimiter=',')
	
	def startTScan(self):  # Connect to Start-button clicked()
		self.stop()  # Stop any existing timer
		self._generator = self.TimeScan()  # Start the loop
		self._timerId = self.startTimer(0)   # This is the idle timer
		
	def stop(self):  # Connect to Stop-button clicked()
		if self._timerId is not None:
			self.killTimer(self._timerId)
		self._generator = None
		self._timerId = None

	def timerEvent(self, event):
        # This is called every time the GUI is idle.
		if self._generator is None:
			return
		try:
			next(self._generator)  # Run the next iteration
		except StopIteration:
			self.stop()  # Iteration has finshed, kill the timer
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = Main()
	window.show()
	sys.exit(app.exec_())