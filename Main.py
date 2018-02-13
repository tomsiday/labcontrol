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

##################################################################
### Initialise the KLinGER MC4 motion controller (delay stage) ###
##################################################################
import visa # For GPIB communications

rm = visa.ResourceManager() # load up the pyvisa manager
print(rm.list_resources()) #print the availible devices  Klinger is 8 for now.
#klinger = rm.open_resource('GPIB0::8::INSTR') # Open klinger for comms
# Se the EOL termination (otherwise  the klinger isnt happy)
#klinger.write_termination = '\r'
#klinger.read_termination = '\r'

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
osc_index = 1
demod_rate = 1e3
time_constant = 0.3
osc_frequency = 32369.665
# Initial settings for THz time domain experiments.
exp_setting = [['/%s/sigins/%d/ac'             % (device, in_channel), 0],
                   ['/%s/sigins/%d/ac'             % (device, in_channel), 1], # Set AC coupling
				   ['/%s/sigins/%d/imp50'          % (device, in_channel), 0], # Use 10Mohm impedance
				   ['/%s/sigins/%d/diff'           % (device, in_channel), 1], # Differential input
				   ['/%s/sigins/%d/float'           % (device, in_channel), 1], # Float on
                   ['/%s/sigins/%d/range'          % (device, in_channel), 0.1], # Range setting
                   ['/%s/demods/%d/enable'         % (device, demod_index), 1], # Enable demod 0
                   ['/%s/demods/%d/rate'           % (device, demod_index), demod_rate], # Set data transfer rate to PC \(dont really know why this matters)
                   ['/%s/demods/%d/adcselect'      % (device, demod_index), in_channel], # Set input channel for demod 0
                   ['/%s/demods/%d/order'          % (device, demod_index), 1], # Set filter order for demod 0 
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
delay = serial.Serial('COM14', baudrate=921600, rtscts=True)
# Flush and reset serial buffers
delay.flush()
delay.reset_input_buffer()
delay.reset_output_buffer()
# Ask the ESP301 to identify the stage on axis 1 \r new line
delay.write(b"1ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a MFA-CC)
print('Stage', delay.read(delay.in_waiting), 'Connected (AX1)')

# Ask the ESP301 to identify the stage on axis 2 \r new line
delay.write(b"2ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a MFA-CC)
print('Stage', delay.read(delay.in_waiting), 'Connected (AX2)')

# Ask the ESP301 to identify the stage on axis 3 \r new line
delay.write(b"3ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a MFA-CC)
print('Stage', delay.read(delay.in_waiting), 'Connected (AX3)')

import sys
from PyQt4 import QtCore, QtGui
from Gui import Ui_MainWindow
from pyqtgraph import PlotWidget
from Callbacks import *

class Main(QtGui.QMainWindow,Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui= Ui_MainWindow()
		self.ui.setupUi(self)
	   
		self.ui.TStart.clicked.connect(helloworld)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = Main()
	window.show()
	sys.exit(app.exec_())