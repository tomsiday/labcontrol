##########################################
###### Lab Control software for 910 ######
############### Tom Siday ################
##########################################

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

XYStepX = 0.1 #mm
XYStepY = 0.1 #mm

XYLengthX = 1 #mm
XYLengthY = 1 #mm

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
                   ['/%s/sigins/%d/ac'             % (device, in_channel), 0], # Set AC coupling (no)
				   ['/%s/sigins/%d/imp50'          % (device, in_channel), 0], # Use 10Mohm impedance
				   ['/%s/sigins/%d/diff'           % (device, in_channel), 1], # Differential input
				   ['/%s/sigins/%d/float'           % (device, in_channel), 0], # Float off
                   ['/%s/sigins/%d/range'          % (device, in_channel), 0.3], # Range setting
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
XYscanner = serial.Serial('COM14', baudrate=921600, rtscts=True)
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
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import time 
import numpy as np

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

		self._generator = None
		self._timerId = None
	
	def startXYScan(self):  # Connect to Start-button clicked()
		self.stop()  # Stop any existing timer
		self._generator = self.XYScan()  # Start the loop
		self._timerId = self.startTimer(0)   # This is the idle timer
	
	def XYScan(self):
		
		xgrid = self.ui.XYPlot.GLGridItem()
		ygrid = self.ui.XYPlot.GLGridItem()
		zgrid = self.ui.XYPlot.GLGridItem()
		self.ui.XYPlot.view.addItem(xgrid)
		self.ui.XYPlot.view.addItem(ygrid)
		self.ui.XYPlot.view.addItem(zgrid)

		data = dict([('xpos',[]), ('ypos',[]), ('R',[])])
		for y in range(int(XY_posY_init), int(XY_posY_init)+int(XYLengthY), int(XYStepY)):
			
			XYscanner.write(("2PA"+str(int(y)*1e-3) + "\r").encode()) # set y position

			for x in range(int(XY_posX_init), int(XY_posX_init)+int(XYLengthX), int(XYStepX)):
				
				XYscanner.write(("1PA"+str(int(x)*1e-3) + "\r").encode()) # set x position
				
				time.sleep(1)
				
				out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
				out['R'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y
			
				data['xpos'] =  data['xpos'] + [x] # add sample stage x pos to dict
				data['ypos'] =  data['ypos'] + [y] # add sample stage y pos to dict
				data['R'] =  data['R'] + [out['x'][0]] # add magnitude to data dict
				
				print(data)
				
				#self.ui.XYPlot.image(data)
				yield
	
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
		t_wait = int(self.ui.TDwell.text())
		print("Dwell time " + str(t_wait) + "s")	
		
	def TimeScan(self):
		data = dict([('delay',[]),('R',[])])#, ('fft',[])]) # create empty dictionary with keys
		for a in range(int(delay_pos_init),int(delay_pos_init)-int(delay_length),-int(delay_step)): # -, stage goes high to low.
			
			klinger.write("PW" + str(a)) # Send the position to the KLINGER
			print("Delay stage at " + str(a) + " steps")
			
			time.sleep(t_wait) # wait for lock-in filter to settle 'integration time'
			
			out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
			out['R'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y
			
			data['delay'] =  data['delay'] + [a] # add delay stage position to data dict
			data['R'] =  data['R'] + [out['x'][0]] # add magnitude to data dict
			
			print(data)
			
			#self.ui.TPlot.sigTransformChanged.clear()
			self.ui.TPlot.plot(data['delay'], data['R']) # plot time domain (stage position)
			
			
			#data['fft'] = np.real(np.fft.fft(data['R'])) #fourier transform
			
			#self.ui.TFFTPlot.plot.clear()
			#self.ui.TFFTPlot.plot(data['delay'], data['fft'])
			#print(out) # print current lock-in values
			
			yield # check if stop button has been pressed.

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