##########################################
###### Lab Control software for 910 ######
############### Tom Siday ################
##########################################

# Import matplotlib for plotting
import matplotlib
# Qt4Agg allows matplotlib to be used in a qt4 window.
matplotlib.use('Qt4Agg')

### Initial values ###
#	Position values in microns
#	Time in units of delay stage position
# TODO : add times in picoseconds (input and plot) 

XorR = 'x' # Choose between 'x' and 'r' (magnitude) lockin output.

## Initial time scan parameter values  ##
delay_position = 0 # Set the delay stage to the default position (0),,(THIS VAL CHANGES)
delay_pos_init = 0 # Initial delay stage position
delay_step = 5 # Default scan time step
delay_length = 100 # Default scan time length (steps)
t_wait = 1 # Time domain dwell time (s)
jog_XYZ = 0.5 # The translation jog step for XYZ axis of NanoMax600
jog_Theta = 0.5 # Rotation jog step for NanoMax600

## Initial XY scan values ##
XY_posX_init = 0 # Starting position (x-axis)
XY_posY_init = 0 # Starting position (y-axis)
XYStepX = 10 # position step (x-axis)
XYStepY = 10 # position step (y-axis)
XYLengthX = 100 # Scan length (x-axis)
XYLengthY = 100 # scan length (y-axis)

## Initial XT scan parameters
XT_pos_space_init = 0 # Starting position (space-axis)
XTStepSpace = 10 # Step size (space)
XTLengthSpace = 100 # Scan length (space)
XT_pos_time_init = 0 # start time (delay stage)
XTStepTime = 10 # step size (time)
XTLengthTime = 100 # scan length (time)

##################################################################
### Initialise the KLinGER MC4 motion controller (delay stage) ###
##################################################################
import visa # For GPIB communications

rm = visa.ResourceManager() # load up the pyvisa manager
print(rm.list_resources()) #print the available devices KLINGER IS GPIB::8 (for now).
klinger = rm.open_resource('GPIB0::8::INSTR') # 'open' Klinger stage

klinger.write_termination = '\r' # Set the EOL termination (otherwise the Klinger stage won't communicate nicely)
klinger.read_termination = '\r'

##############################################
### Initialise the Zurich instruments MFLI ###
##############################################
import zhinst.utils # import the Zurich instruments python library
import numpy as np # import numpy python library
import time # for time.sleep

device_id = 'dev3047' # Serial number of our MFLI

apilevel = 6 # API level in the 17,06 release from ZI. (probably not a good idea to change this..) 

# Create a session (daq) for communication with the MFLI. device is the serial number, and props is a load of useful info about the session
(daq, device, props) = zhinst.utils.create_api_session(device_id, apilevel, required_devtype='.*LI|.*IA|.*IS')

# check out API versions align (in case the MFLI firmware, or PC library is updated above 17.06)
# If this is False, both should be changed to the same version (preferably kept at 17.06 unless new features are required)
print('PC and MFLI API version align?:', zhinst.utils.api_server_version_check(daq))

# Base config for MFLI -- disable everything
general_setting = [['/%s/demods/*/enable' % device, 0],
                       ['/%s/demods/*/trigger' % device, 0],
                       ['/%s/sigouts/*/enables/*' % device, 0],
                       ['/%s/scopes/*/enable' % device, 0]]

# Set this base config on the MFLI
daq.set(general_setting)

# SYNC (make sure PC and MFLI have communicated settings, etc...)
daq.sync()

## Configure the MFLI for streaming data - these are all standard settings, available in the MFLI manual (and in exp_setting below)
out_channel = 0 
out_mixer_channel = zhinst.utils.default_output_mixer_channel(props)
in_channel = 0 # Signal in from preamp (+V)
demod_index = 0 # which demodulator to use
osc_index = 0 # which oscillator ot use
demod_rate = 1e3 # data transfer rate for the selected demodulator
time_constant = 0.3 # Lock-in time constant, t_c (seconds)
osc_frequency = 32369.665 # frequency set for oscillator (if not using external reference)
# Initial settings for THz time domain experiments.
exp_setting = [['/%s/sigins/%d/ac'             % (device, in_channel), 1], # Set AC coupling (yes)
				   ['/%s/sigins/%d/imp50'          % (device, in_channel), 0], # Use 10Mohm impedance
				   ['/%s/sigins/%d/diff'           % (device, in_channel), 1], # Differential input
				   ['/%s/sigins/%d/float'           % (device, in_channel), 0], # Float off
                   ['/%s/sigins/%d/range'          % (device, in_channel), 0.03], # Range setting
                   ['/%s/demods/%d/enable'         % (device, demod_index), 1], # Enable demod 0
                   ['/%s/demods/%d/rate'           % (device, demod_index), demod_rate], # Set data transfer rate to PC \(dont really know why this matters)
                   ['/%s/demods/%d/adcselect'      % (device, demod_index), in_channel], # Set input channel for demod 0
                   ['/%s/demods/%d/order'          % (device, demod_index), 4], # Set filter order for demod 0 
                   ['/%s/demods/%d/timeconstant'   % (device, demod_index), time_constant], # Set filter time constant
                   ['/%s/demods/%d/oscselect'      % (device, demod_index), osc_index], # Set oscillator for demod 0 (we only have 1)
                   ['/%s/demods/%d/harmonic'       % (device, demod_index), 1], # Set harmonic for measurement
                   ['/%s/extrefs/0/enable'         % (device), 1], # Set external reference on/off (optical chopper)
					#['/%s/oscs/1/freq'         % (device), osc_frequency]] # set oscillator frequency
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
import serial # python library for serial connections
# Initialise ESP301 serial connection
XYscanner = serial.Serial('COM10', baudrate=921600, rtscts=True)

# Flush and reset serial buffers (why not..)
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

################################################################################################
###### Gui display, callback functions (including run loops, e.g. the xy and time scans.) ######
################################################################################################

import sys # python library of system specific parameters and functions
from PyQt4 import QtCore, QtGui # import pyqt4, the GUI interface.
from Gui import Ui_MainWindow # Gui is the python file containing this interface.
import matplotlib.pyplot as plt # matplotlib pyplot for plotting in program.
import datetime # gives us date and time (for saving files mainly)

class Main(QtGui.QMainWindow,Ui_MainWindow): # PyQt4 GUI window class.
	def __init__(self):
		QtGui.QMainWindow.__init__(self) # set up the GUI (all standard commands for creating pyqt guis)
		self.ui= Ui_MainWindow()
		self.ui.setupUi(self)
		
		## List of commands (functions) to run when various GUI interactions are made (such as clicking buttons, etc..)
		# Time domain (TDS) tab
		self.ui.TStart.clicked.connect(self.startTScan) # start button
		self.ui.TStop.clicked.connect(self.stop) # stop button
		self.ui.GoTScanStart.clicked.connect(self.UpdateTStart) # set start time button
		self.ui.GoTScanLength.clicked.connect(self.UpdateTScanLength) # set scan length button
		self.ui.GoTStep.clicked.connect(self.UpdateTStep) # set scan step button
		self.ui.GoTDwell.clicked.connect(self.UpdateTDwell) #  set dwell time button
		
		# XY scan (aperture) tab
		self.ui.XYStartBut.clicked.connect(self.startXYScan) # start button
		self.ui.XYStopBut.clicked.connect(self.stop) # stop button
		self.ui.GoXYStartX.clicked.connect(self.UpdateXYStartX) # set start (x) button
		self.ui.GoXYStartY.clicked.connect(self.UpdateXYStartY) # set start (y) button
		self.ui.GoXYStepX.clicked.connect(self.UpdateXYStepX) # set step (x) button
		self.ui.GoXYStepY.clicked.connect(self.UpdateXYStepY) # set step (y) button
		self.ui.GoXYLengthX.clicked.connect(self.UpdateXYLengthX) # set scan length (x) button
		self.ui.GoXYLengthY.clicked.connect(self.UpdateXYLengthY) # set scan length (y) button
		
		# Global controls
		self.ui.GoZPos.clicked.connect(self.UpdateZPos) # Set the sample stage position in Z
		self.ui.GoDelayPos.clicked.connect(self.UpdateDelayPos) # set position of delay stage
		
		# XT scan (aperture) tab
		self.ui.XTStartBut.clicked.connect(self.startXTScan) # Start the XT scan button
		self.ui.XTStopBut.clicked.connect(self.stop) # Stop the XT scan button
		self.ui.GoXTStartSpace.clicked.connect(self.UpdateXTStartSpace) # update XT scan start position (instant) button
		self.ui.GoXTStepSpace.clicked.connect(self.UpdateXTStepSpace) # update XT scan step in space button
		self.ui.GoXTLengthSpace.clicked.connect(self.UpdateXTLengthSpace) # set length of XT scan (space) button
		self.ui.GoXTStartTime.clicked.connect(self.UpdateXTStartTime) # set XT scan time start (instant) button
		self.ui.GoXTStepTime.clicked.connect(self.UpdateXTStepTime) # set XT time step button
		self.ui.GoXTLengthTime.clicked.connect(self.UpdateXTLengthTime) # set XT time  button
		
		
		self._generator = None # these make it possible to not make the gui freeze during the whole scan
		self._timerId = None

	def UpdateXTStartSpace(self): # set the start position(space) for XT scan
		global XT_pos_space_init # global means we can edit the global variable from within this loop
		XT_pos_space_init = self.ui.XTStartSpace.text() # set variable to the value in the box (will complain if empty)
		if self.ui.ScanAlongY.isChecked() == True: # check for which scan axis used (x or y) (is y?)
			XYscanner.write(("2PA"+str(int(XT_pos_space_init)*1e-3) + "\r").encode()) # move stage to start position (y)
		if self.ui.ScanAlongX.isChecked() == True: # (is x?)
			XYscanner.write(("1PA"+str(int(XT_pos_space_init)*1e-3) + "\r").encode()) # move stage to start position (x)
		
		print("X axis start position " + XT_pos_space_init) # display confirmation the position has been set
		
	def UpdateXTStepSpace(self): # set the XT scan step (space)
		global XTStepSpace # import global variable
		XTStepSpace = self.ui.XTStepSpace.text() # set from input box
		print("XT scan space step " + str(XTStepSpace) + " mm") # print confirmation of parameter set
		
	def UpdateXTLengthSpace(self): # set the XT scan length (space)
		global XTLengthSpace # import global variable
		XTLengthSpace = self.ui.XTLengthSpace.text() # set from input box
		print("XT scan space length " + str(XTLengthSpace) + " mm") # print confirmation of parameter set
		
	def UpdateXTStartTime(self): # Set and move delay stage to initial position for XT scan
		global XT_pos_time_init # import global variable
		XT_pos_time_init = self.ui.XTStartTime.text() # set from input box
		klinger.write("PW" + str(XT_pos_time_init)) # write to delay stage (move stage now)
		print("Delay stage initial position: " + str(XT_pos_time_init)) # print confirmation of parameter change and movement
		
	def UpdateXTStepTime(self): # Set the XT scan set (time)
		global XTStepTime # import global variable
		XTStepTime = self.ui.XTStepTime.text() # set from input box
		print("XT scan time step " + str(XTStepTime)) # confirm change of parameter
		
	def UpdateXTLengthTime(self): # set the XT scan length (time)
		global XTLengthTime # import global variable
		XTLengthTime = self.ui.XTLengthTime.text() # set from input box
		print("XT scan time length " + str(XTLengthTime)) # print confirmation of parameter change
		
	def startXTScan(self):  # start the xt scan
		self.stop()  # Stop any existing timer
		self._generator = self.XTScan()  # Start the loop (the XT scan loop)
		self._timerId = self.startTimer(0)   # This is the idle timer (this triggers the repeat timer for the loop)
		
	def XTScan(self): # Loop to run the XT scan (including collect and plot data)
		
		# create arrays with the values of each step of scan in time (t) and space (xy)
		xy = np.arange(float(XT_pos_space_init), float(XT_pos_space_init)+float(XTLengthSpace), float(XTStepSpace))
		t = np.arange(float(XT_pos_time_init), float(XT_pos_time_init)-float(XTLengthTime), -float(XTStepTime))
		
		print(xy) # print the values in the terminal
		print(t)
		
		# create a meshgrid for the scan (a grid of values for the plotter) (see numpy/pyplot docs for details
		X, T, = np.mgrid[int(XT_pos_space_init):int(XT_pos_space_init)+int(XTLengthSpace):int(XTStepSpace), int(XT_pos_time_init):int(XT_pos_time_init)+int(XTLengthTime):int(XTStepTime)]
		
		# initialise an empty array where the measured values will be placed.
		Z = np.zeros((len(xy), len(t)))
		
		ax = self.ui.XTPlot.figure.add_subplot(111) # create axis for color plot
		
		for a in range(0, len(t)): # loop across number of time samples
			
			klinger.write("PW" + str(t[a])) # set klinger (delay) position
			
			for b in range(0, len(xy)): # loop across number of position samples
				
				# check if to move along x or y axis (space)
				if self.ui.ScanAlongY.isChecked() == True: # Scan changes y values (channel 2)
					
					XYscanner.write(("2PA"+str(xy[b]*1e-3) + "\r").encode()) # set y position (1e-3 to convert microns to mm)
				
				if self.ui.ScanAlongX.isChecked() == True: # Scan changes x values (channel 2)
					
					XYscanner.write(("1PA"+str(xy[b]*1e-3) + "\r").encode()) # set x position (1e-3 to convert microns to mm)
				
				time.sleep(t_wait) # wait for the selected dwell time to let lock-in demod settle
				
				out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index)) # grab a bunch of data from the MFLI
				
				out['r'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y (in MFLI dataset) adn add it to the MFLI dataset
				
				if self.ui.XTLockinX.isChecked() == True: # decide if we want magnitude or x shown on plot (and saved)
					Z[b,a] = out['x'] # put the lockin value into the data array
				if self.ui.XTLockinR.isChecked() == True:
					Z[b,a] = out['r'] # put the lock-in value into the data array
				
				ax.clear() # clear the axis (might help for speed)
				ax.pcolor(X,T,Z) # colour plot
				
				ax.set_xlabel('X (microns)') # draw axis labels
				ax.set_ylabel('time') # draw axis labels
				
				self.ui.XTPlot.draw() # draw the plot
				self.ui.XTPlot.flush_events() # Flush the plot drawing - makes sure the plot updates (it can sometimes skip a loop if this isnt done)
				
				# TODO: find an efficient way to do this plotting (doesn't really matter at this update rate (~1s))
				yield # is the timer/generator still running (i.e. has stop been pressed) this stops the app from locking up
				
		print(Z) # print the final dataset
		currenttime = datetime.datetime.now() # grab the time for the filename
		filename = str(currenttime.hour) + str(currenttime.minute) + "-XTScan.txt" # generate the filename string
		np.savetxt(filename, Z, delimiter=',') # save the data (Z only for now)
		# TODO: add the x and y values, and experiment parameters in a separate file or header
		
	
	def startXYScan(self):  # Connect to Start-button clicked()
		self.stop()  # Stop any existing timer
		self._generator = self.XYScan()  # Start the loop
		self._timerId = self.startTimer(0)   # This is the idle timer	
	
	def XYScan(self): # Loop to run the XY scan (including collect and plot data)
		
		# create arrays with the scan positions in x and y
		x = np.arange(float(XY_posX_init), float(XY_posX_init)+float(XYLengthX), float(XYStepX))
		y = np.arange(float(XY_posY_init), float(XY_posY_init)+float(XYLengthY), float(XYStepY))
		
		print(x) # print the arrays
		print(y)
		
		# create meshgrid for plotting (check numpy/pyplot docs for details)
		X, Y, = np.mgrid[int(XY_posX_init):int(XY_posX_init)+int(XYLengthX):int(XYStepX), int(XY_posY_init):int(XY_posY_init)+int(XYLengthY):int(XYStepY)]
		
		Z = np.zeros((len(y), len(x))) # initialize empty array for lock-in data
		
		ax = self.ui.XYPlot.figure.add_subplot(111) # add plot in the correct window of the XY scan tab

		
		for a in range(0, len(y)): # loop over length of scan
			
			XYscanner.write(("1PA"+str(x[0]*1e-3) + "\r").encode()) # set x position back to start of scan
			time.sleep(t_wait) # wait for stage to move
			XYscanner.write(("2PA"+str(y[a]*1e-3) + "\r").encode()) # set y position
			time.sleep(t_wait) # wait for stage to move

			for b in range(0, len(x)): # loop over length of scan
				
				XYscanner.write(("1PA"+str(x[b]*1e-3) + "\r").encode()) # set x position
				
				time.sleep(t_wait) # wait for lockin filter to settle
				
				out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index)) # grab data from the MFLI
				out['r'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y	and add to MFLI dataset
				
				if self.ui.XYLockinX.isChecked() == True: # Select whether the plot is X or magnitude
					Z[b,a] = out['x']
				if self.ui.XYLockinR.isChecked() == True:
					Z[b,a] = out['r']
					
				ax.clear() # clear plot (may help with speed)
				ax.pcolor(X,Y,Z) # color plot
				ax.set_xlabel('x (microns)') # draw axis labels
				ax.set_ylabel('y (microns)')
				
				self.ui.XYPlot.draw() # draw the plot
				
				self.ui.XYPlot.flush_events() # Flush the plot drawing - makes sure the plot updates.
				
				yield # has the stop button been pressed?
			
				
			
		print(Z # print the final dataset
		currenttime = datetime.datetime.now() # get time for filename
		filename = str(currenttime.hour) + str(currenttime.minute) + "-XYScan.txt" # generate filename string
		np.savetxt(filename, Z, delimiter=',')	# save data (no x,y)
	
	def UpdateDelayPos(self): # Set and move delay stage (global control)
		DelayPos = self.ui.DelayPos.text() # get the value in box - don't need global variable for this
		klinger.write("PW" + str(DelayPos)) # move the delay stage
		print("Delay stage initial position: " + str(delay_pos_init)) # print stage move confirmation
	def UpdateZPos(self): # set sample stage position in microns along beam axis (z)
		global ZPos # import global variable
		ZPos = self.ui.ZPos.text() # set from input box
		XYscanner.write(("3PA"+str(int(ZPos)*1e-3) + "\r").encode()) # move sample stage (z)
		print("Z position set to " + ZPos + " microns") # print stage move confirmation
	def UpdateXYLengthY(self):  # set length of xy scan in Y
		global XYLengthY # import global variable
		XYLengthY = self.ui.XYLengthY.text() # get value from input box
		print("XY scan Y length " + str(XYLengthY) + " mm") # print confirmation of parameter set
	def UpdateXYLengthX(self): # set length of XY scan in X
		global XYLengthX # import global variable
		XYLengthX = self.ui.XYLengthX.text() # get value from input box
		print("XY scan X length " + str(XYLengthX) + " mm")	# print confirmation of parameter set
	def UpdateXYStepX(self): # set XY scan step in X
		global XYStepX # import global variable
		XYStepX = self.ui.XYStepX.text() # get value from input box
		print("XY scan X step " + str(XYStepX) + " mm") # print confirmation of parameter set
	def UpdateXYStepY(self): # set XY scan step in Y
		global XYStepY # import global variable
		XYStepY = self.ui.XYStepY.text() # get value from input box
		print("XY scan Y step " + str(XYStepY) + " mm")	# print confirmation of parameter set
	def UpdateXYStartX(self): # set and go to xy scan start position (x)
		global XY_posX_init # import global variable
		XY_posX_init = self.ui.XYStartX.text() # get value from input box
		XYscanner.write(("1PA"+str(int(XY_posX_init)*1e-3) + "\r").encode()) # move the sample to this position (x)
		print("X axis start position " + XY_posX_init) # print confirmation of parameter set and move
	def UpdateXYStartY(self): # set and go to xy scan start position (y)
		global XY_posY_init # import global variable
		XY_posY_init = self.ui.XYStartY.text() # get value form input box
		XYscanner.write(("2PA"+str(int(XY_posY_init)*1e-3) + "\r").encode()) # move sample to position (y)
		print("Y axis start position " + XY_posY_init) # print confirmation of parameter set and stage move
	
	def UpdateTStart(self): # Set and move delay stage to initial position.
		global delay_pos_init # import global variable
		delay_pos_init = self.ui.TScanStart.text() # get value from input box
		klinger.write("PW" + str(delay_pos_init)) # move the delay stage to this position
		print("Delay stage initial position: " + str(delay_pos_init)) # print confirmation of parameter set and move
	def UpdateTScanLength(self): # Set time scan length (in steps)
		global delay_length # import global variable
		delay_length = int(self.ui.TScanLength.text()) # get value from input box
		print("Scan length " + str(delay_length) + " steps") # print confirmation of parameter set
	def UpdateTStep(self): # Set time scan length (in steps)
		global delay_step # import global variable
		delay_step = int(self.ui.TStep.text()) # get value from input box
		print("Scan step " + str(delay_step) + " steps") # print confirmation of parameter set	
	def UpdateTDwell(self): # Set dwell time (seconds)
		global t_wait # import global variable
		t_wait = float(self.ui.TDwell.text()) # get value from input box
		print("Dwell time " + str(t_wait) + "s") # print confirmation of parameter set
		# TODO: add setting the dwell time for XY and XT scan
		
	def TimeScan(self): # loop for time scan
		
		# create array of delay stage values
		X = np.arange(float(delay_pos_init), float(delay_pos_init)-float(delay_length), -float(delay_step))
		# initialise array of zeros for output data
		Y = np.zeros(len(X))
		
		ax = self.ui.TPlot.figure.add_subplot(211) # subplot for time domain scan
		ax2 = self.ui.TPlot.figure.add_subplot(212) # subplot for live Fourier transform

		for a in range(0, len(X)): # loop with length = number of points in scan
			
			klinger.write("PW" + str(X[a])) # Send the position to the KLINGER. it references the previously created array for position to send
			
			time.sleep(t_wait) # wait for lock-in filter to settle 'integration time'
			
			out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index)) # get data from MFLI
			out['r'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y
			
			if self.ui.TLockinX.isChecked() == True: # Select whether the plot is X or magnitude
				Y[a] = out['x']
			if self.ui.TLockinR.isChecked() == True:
				Y[a] = out['r']
			
			ax.clear()  # clear plot (may add speed)
			ax.plot(X[0:a+1], Y[0:a+1]) # plot line plot
			
			ax.set_xlabel('Time') # draw axis labels
			ax.set_ylabel('Lock-in output (V)')
			
			FFT = np.real(np.fft.fft(Y)) # Fourier transform of current dataset (live)

			ax2.clear() # clear plot (may add speed)
			ax2.plot(X[0:a+1], FFT[0:a+1]) # plot the FFT
				
			ax2.set_xlabel('Arb') # draw axis labels
			ax2.set_ylabel('Magnitude')
			
			self.ui.TPlot.draw() # draw plots
			self.ui.TPlot.flush_events() # Flush the plot drawing - makes sure the plot updates.
			
			yield # check if stop button has been pressed.
		
		currenttime = datetime.datetime.now() # get time for filename
		filename = str(currenttime.hour) + str(currenttime.minute) + "-TWScan.txt" # generate filename string
		np.savetxt(filename, Y, delimiter=',') # save file 
	
	def startTScan(self):  # Connect to Start-button clicked() START the time domain scan
		self.stop()  # Stop any existing timer
		self._generator = self.TimeScan()  # Start the loop
		self._timerId = self.startTimer(0)   # This is the idle timer
	def stop(self):  # Connect to Stop-button clicked() this STOPS all running scans
		if self._timerId is not None: # kill timer if there is one
			self.killTimer(self._timerId)
		self._generator = None # disable any generator/timers.
		self._timerId = None

	def timerEvent(self, event):
        # This is called every time the GUI is idle.
		if self._generator is None: # exits if no generator
			return
		try:
			next(self._generator)  # Run the next iteration
		except StopIteration:
			self.stop()  # Iteration has finished, kill the timer
if __name__ == "__main__": # open up the GUI windows (all standard pyqt commands)
	app = QtGui.QApplication(sys.argv)
	window = Main()
	window.show()
	sys.exit(app.exec_())