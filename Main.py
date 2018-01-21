##########################################
###### Lab Control software for 910 ######
############### Tom Siday ################
##########################################

### start bokeh server BEFORE running this program -- (bokeh serve)
## Initial scan parameter values (reflected in the input box)

## The start time of 0 means the delay stage is at position 0 (home). +time is stage moving forwards, -time is stage moving back.
t_position = 0 # Set the delay stage to the default position (0),,
t_step = 66 # Default scan time step (time domain)
t_length = 10 # Default scan time length (ps)
t_wait = 1 # Time domain dwell time (s)
jog_XYZ = 0.5 # The translation jog step for XYZ axis of NanoMax600
jog_Theta = 0.5 # Rotation jog step for NanoMax600

##########################################################
### Callback (and loop) functions for the lab control. ###
##########################################################

# Starts live stream from lock in (callback for start button)
def call_lock_but_start(): 
	global playing
	if not playing:
		curdoc().add_periodic_callback(lock_plot_out, 50)
		playing = True

# Stops live stream from lock in (callback for stop button)	
def call_lock_but_stop():
	global playing
	if playing:
		curdoc().remove_periodic_callback(lock_plot_out)
		playing = False

# Loop to generate live stream from lockin -- just grabs the time and x-value
# TODO -- add options to change the stream 
def lock_plot_out():
	if playing:
		new_data = dict()

		out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
		new_data['x'] = lock_plot_line.data_source.data['x'] + [out['timestamp'][0]]
		new_data['y'] = lock_plot_line.data_source.data['y'] + [out['x'][0]]
		lock_plot_line.data_source.data = new_data
########

# Home Nanomax600 (XYZ axis) THIS IS BLOCKING
def call_xy_but_homeXYZ():
	global NanoMaxX, NanoMaxY, NanoMaxZ
	
	# Update notification bar
	txt_notifications.text='<font color="orange">Homing XYZ axis...</font>'
	
	# Home X,Y and Z axis
	NanoMaxX.move_home(True)
	NanoMaxY.move_home(True)
	NanoMaxZ.move_home(True)
	
	# Update notification bar
	txt_notifications.text='<font color="green">XYZ home complete.</font>'

	
# Home Nanomax600 (roll, pitch, yaw axis) THIS IS BLOCKING
def call_xy_but_homeThetaXYZ():
	global NanoMaxThetaX, NanoMaxThetaY, NanoMaxThetaZ
	
	# Update notification bar
	txt_notifications.text='<font color="orange">Homing rotation axis...</font>'
	
	# Home X,Y and Z axis
	NanoMaxThetaX.move_home(True)
	NanoMaxThetaY.move_home(True)
	NanoMaxThetaZ.move_home(True)
	
	# Update notification bar
	txt_notifications.text='<font color="green">Rotational axis home complete.</font>'

# Center Nanomax600 (XYZ axis) THIS IS BLOCKING
def call_xy_but_centerXYZ():
	global NanoMaxX, NanoMaxY, NanoMaxZ
	
	# Update notification bar
	txt_notifications.text='<font color="orange">Centering XYZ axis...</font>'
	
	# Home X,Y and Z axis
	NanoMaxX.move_to(2, blocking=True) # 2 mm is the center of translational motion
	NanoMaxY.move_to(2, blocking=True) 
	NanoMaxZ.move_to(2, blocking=True)
	
	# Update notification bar
	txt_notifications.text='<font color="green">XYZ center complete.</font>'

	
# Center Nanomax600 (roll, pitch, yaw axis) THIS IS BLOCKING
def call_xy_but_centerThetaXYZ():
	global NanoMaxThetaX, NanoMaxThetaY, NanoMaxThetaZ
	
	# Update notification bar
	txt_notifications.text='<font color="orange">Centering rotation axis...</font>'
	
	# Home X,Y and Z axis
	NanoMaxThetaX.move_to(3, blocking=True)
	NanoMaxThetaY.move_to(3, blocking=True)
	NanoMaxThetaZ.move_to(3, blocking=True)
	
	# Update notification bar
	txt_notifications.text='<font color="green">Rotational axis center complete.</font>'	
	
	
# Starts time domain scan with parameters set (callback for start button)
def call_t_but_start(): 
	global playing_time
	if not playing_time:
		playing_time = True
		curdoc().add_next_tick_callback(time_scan)

# Time Domain scan callback function		
def time_scan():
	global t_position
	if playing_time:
		if t_position <= (t_init+t_length):
			new_data = dict()
			t_pos_str = "1PA" + str(t_position*2.99792458e-04*0.5) + "\r" # -ve for time to go forwards Encode the position (and convert from time to millimeters) into a byte sring for the ESP301. Halved- edlay stage doubles distance
			print(t_pos_str) # Print the position being sent to the ESP301
			
			delay.write(t_pos_str.encode()) # Write the position to the ESP301 (after converting to a byte string)
			
			time.sleep(time_constant*5) # Wait for the filter to settle
			
			out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
			out['R'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y
			print(out) # 
			new_data['x'] = t_plot_line.data_source.data['x'] + [t_position*1e-3] # t_position*1e-3 for fs -> ps
			new_data['y'] = t_plot_line.data_source.data['y'] + [out['R'][0]]
			t_plot_line.data_source.data = new_data
		
			curdoc().add_next_tick_callback(time_scan)
			t_position = t_position + t_step # Set the next time step (in time, as it is converted above)
# Stops time domain scan  (callback for stop button)	
def call_t_but_stop():
	global playing_time
	if playing_time:
		playing_time = False
		curdoc().remove_next_tick_callback(time_scan)

# XY scan loop function
def xy_scan():
	global x_position, y_position
	new_data = dict()
	if x_position <= (x_start+x_length):
		NanoMaxX.move_to(x_position, blocking=true) # Move to the current x_position (blocking move)
		if y_position <= (y_start+y_length):
			NanoMaxY.move_to(y_position, blocking=true) # Move to the current y_position (blocking move)
			time.sleep(time_constant*5) # Wait for the filter to settle
			out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
			out['R'] = np.abs(out['x'] + 1j*out['y']) # Calculate the magnitude R from x and y
			print(out) # display the value
			new_data['z'] = xy_plot.data_source.data['z'] + [out['R'][0]]
			new_data['x'] = xy_plot.data_source.data['x'] + [x_position]
			new_data['y'] = xy_plot.data_source.data['y'] + [y_position]
			xy_plot.data_source.data = new_data
			
			curdoc().add_next_tick_callback(time_scan) # enable next iteration
			x_position = x_position + x_step # Set the next position step for the next step of this loop (x)
			y_position = y_position + y_step # Set the next position step for the next step of this loop (y)
			
	

	else:
		# Update notification bar
		txt_notifications.text='<font color="green">Scan complete.</font>'	
	new_data = dict()
	
	
# Callbacks for jog buttons		
def call_Xup():
	global NanoMaxX
	NanoMaxX.move_by(jog_XYZ)
def call_Xdown():
	global NanoMaxX
	NanoMaxX.move_by(-jog_XYZ)	
def call_Yup():
	global NanoMaxY
	NanoMaxY.move_by(jog_XYZ)
def call_Ydown():
	global NanoMaxY
	NanoMaxY.move_by(-jog_XYZ)
def call_Zup():
	global NanoMaxZ
	NanoMaxZ.move_by(jog_XYZ)
def call_Zdown():
	global NanoMaxZ
	NanoMaxZ.move_by(-jog_XYZ)	
def call_RotXup():
	global NanoMaxThetaX
	NanoMaxThetaX.move_by(jog_Theta)
def call_RotXdown():
	global NanoMaxThetaX
	NanoMaxThetaX.move_by(-jog_Theta)	
def call_RotYup():
	global NanoMaxThetaY
	NanoMaxThetaY.move_by(jog_Theta)
def call_RotYdown():
	global NanoMaxThetaY
	NanoMaxThetaY.move_by(-jog_Theta)
def call_RotZup():
	global NanoMaxThetaZ
	NanoMaxThetaZ.move_by(jog_Theta)
def call_RotZdown():
	global NanoMaxThetaZ
	NanoMaxThetaZ.move_by(-jog_Theta)

# Numerical position input
def call_posX(attrname, old, new):
	global NanoMaxX
	NanoMaxX.move_to(float(new))	
def call_posY(attrname, old, new):
	global NanoMaxY
	NanoMaxY.move_to(float(new))	
def call_posZ(attrname, old, new):
	global NanoMaxZ
	NanoMaxZ.move_to(float(new))
def call_posRotX(attrname, old, new):
	global NanoMaxThetaX
	NanoMaxThetaX.move_to(float(new))	
def call_posRotY(attrname, old, new):
	global NanoMaxThetaY
	NanoMaxThetaY.move_to(float(new))	
def call_posRotZ(attrname, old, new):
	global NanoMaxThetaZ
	NanoMaxThetaZ.move_to(float(new))	

# Shutdown connections to devices
def call_shutdown():
	# Disable APT interface (nanoMAX)
	core._cleanup()
	
####################################	
#### End of callback functions  ####
####################################
 
######################################################
### Connect to the Thorlabs BSC203s (6 axis stage) ###
######################################################
import thorlabs_apt as apt # This is from github -> qpit/thorlabs_apt
import thorlabs_apt.core as core # cor core.cleanup() (end communication)
import time
# display a list of connected APT controller serial numbers
print('APT devices: ', apt.list_available_devices())
## Initialise NanoMax600 Axis
# NanoMax Translate (motor)
NanoMaxX=apt.Motor(90838883)
NanoMaxY=apt.Motor(90838884)
NanoMaxZ=apt.Motor(90838885)
# NanoMax Rotate (motor)
NanoMaxThetaX=apt.Motor(90839317)
NanoMaxThetaY=apt.Motor(90839318)
NanoMaxThetaZ=apt.Motor(90839319)

#############################################################
### Initialise the ESP301 motion controller (delay stage) ###
#############################################################
import serial
# Initialise ESP301 serial connection
delay = serial.Serial('COM10', baudrate=921600, rtscts=True)
# Flush and reset serial buffers
delay.flush()
delay.reset_input_buffer()
delay.reset_output_buffer()
# Ask the ESP301 to identify the stage on axis 1? \r new line
delay.write(b"1ID?\r")
# Wait a second for the ESP301 to reply
time.sleep(1)
# Print out the stage in slot 1 (should be a GTS570)
print('Stage', delay.read(delay.in_waiting), 'Connected')

# playing is a variable which is sued to stop 'neverending' loops	TODO: The stop time takes lioger the longer the graph as been running? maybe something 'datay'			
playing = True

##############################################
### Initialise the Zurich instruments MFLI ###
##############################################
import zhinst.utils 
import numpy as np
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
				   ['/%s/demods/1/adcselect'       % (device), 8]] # Select the input for the external reference
# set the above settings on the MFLI
daq.set(exp_setting)
# Stop from any data streaming/being collected (needs to be done as prep for measurements)
daq.unsubscribe('*')
# Wait for demod filter to settle (10 * filter time constant)
time.sleep(10*time_constant)
# SYNC (make sure PC and MFLI agree with settings, etc...) - must be done after waiting for the demod filter to settle
daq.sync()

##############################
## Initialise Bokeh Server ###
##############################
from bokeh.client import push_session
from bokeh.plotting import show,figure, curdoc
from bokeh.layouts import column, row, layout
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Button, TextInput
# open a session to keep our local document in sync with server
session = push_session(curdoc())

##############################
### Gui content and layout ###
##############################

### Time domain tab ###

# Time domain plot
t_plot = figure(plot_width=600, plot_height=300) # Create the time domain plot window
t_plot_line = t_plot.line(x=[], y=[]) # Add empty line plot
# Frequency domain plot
t_frequency_plot = figure(plot_width=600, plot_height=300) # Create the spectrum plot window
t_frequency_plot.line(x=[], y=[]) # Add empty line plot
## Buttons and controls for time domain tab ##
t_but_start = Button(label='Start') # Start button
t_but_start.on_click(call_t_but_start) # Call function when pressed
t_but_stop = Button(label='S/top') # Stop NOW button
t_but_stop.on_click(call_t_but_stop) # Call the stop time scan callback function
t_in_starttime = TextInput(value= str(t_position), title="Scan start time (ps):") # Input the start time of the scan (in ps)
t_in_length = TextInput(value= str(t_length), title="Scan length (ps):") # Input the length of the scan (in ps)
t_in_stepsize = TextInput(value= str(t_step), title="Scan step size (fs):") # Input size of step (picoseconds). (If length/stepsize is not an integer, round)
t_in_wait = TextInput(value=str(t_wait), title="Wait time (s):")
## Time comain tab layout ##
t_control = layout([[ t_but_start, t_but_stop ], [ t_in_starttime, t_in_length ], [t_in_stepsize, t_in_wait]]) # Grid for widget layout
t_col = column([ t_plot, t_frequency_plot ]) # Put the plots above each other 
t_grid = row([t_control, t_col]) # Put widgets and plots in column
t_tab = Panel(child=t_grid, title="Time") # Create the time domain tab

### XY scan tab ###

# x-y color plot
#xy_plot = figure(plot_width=600, plot_height=300) # Create the color plot window
#data = {'x': [1,2,3,4], 'y':[1,2,3,4], 'z':[1,2,3,4]}
#xy_plot = HeatMap(data, x='x', y='y', values='z') # Add content (temp)
# Buttons and controls for time domain tab
xy_but_start = Button(label='Start') # Start button
xy_but_stop = Button(label='Stop') # Stop NOW button
xy_in_startposX = TextInput(value="0", title="Start position (x)")
# Input the end position of the scan along the X axis (in microns) 
xy_in_sizeX = TextInput(value="10", title="Scan size (x):") 
# Input size of step along x axis (microns). (If length/stepsize is not an integer, round (ceil). The true position data will be encoded still.
xy_in_stepsizeX = TextInput(value="66", title="Step size (x):") 
 # Input the start position of the scan along the Y axis (in microns)
xy_in_startposY = TextInput(value="0", title="Start position (y)")
# Input the end position of the scan along the Y axis (in microns)
xy_in_sizeY = TextInput(value="10", title="Scan size (y):") 
# Input size of step along x axis (microns). (If length/stepsize is not an integer, round (ceil). The true position data will be encoded still.
xy_in_stepsizeY = TextInput(value="66", title="Step size (y):") 

### NanoMax600 stage setup (home & center) ###

# Home translation axis
xy_but_homeXYZ = Button(label='Home XYZ')
xy_but_homeXYZ.on_click(call_xy_but_homeXYZ)
# Home rotation axis
xy_but_homeThetaXYZ = Button(label='Home Rotation') 
xy_but_homeThetaXYZ.on_click(call_xy_but_homeThetaXYZ)
# Center traslation axis ### Information --  centering is to the center of travel (2mm)
xy_but_centerXYZ = Button(label='Center XYZ')
xy_but_centerXYZ.on_click(call_xy_but_centerXYZ)
# Center rotation axis ### Information --  centering is to the center of travel (3 degrees)
xy_but_centerThetaXYZ = Button(label='Center Rotation')
xy_but_centerThetaXYZ.on_click(call_xy_but_centerThetaXYZ)

## XY scan tab layout ##
xy_control = layout([[ xy_but_start, xy_but_stop ], [ xy_in_startposX, xy_in_startposY ], [xy_in_sizeX, xy_in_sizeY], [xy_in_stepsizeX, xy_in_stepsizeY], [xy_but_homeXYZ, xy_but_homeThetaXYZ], [xy_but_centerXYZ, xy_but_centerThetaXYZ]]) # Grid for widget layout
xy_grid = row([xy_control]) # Put widgets and plots in column
xy_tab = Panel(child=xy_grid, title="Space") # Create the time domain tab

### Space/Time Tab ###

# x-t color plot
xt_plot = figure(plot_width=600, plot_height=300) # Create the color plot window
xt_plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5) # Add content (temp)
## Buttons and controls for time domain tab ##
xt_but_start = Button(label='Start') # Start button
xt_but_stop = Button(label='Stop') # Stop NOW button
# Input the start position of the scan along the X axis (in microns)
xt_in_startposX = TextInput(value="0", title="Start position (x)")
# Input the end position of the scan along the X axis (in microns) 
xt_in_sizeX = TextInput(value="10", title="Scan size (x):") 
# Input size of step along x axis (microns). (If length/stepsize is not an integer, round (ceil). The true position data will be encoded still.
xt_in_stepsizeX = TextInput(value="66", title="Step size (x):") 
 # Input the start position of the scan along the Y axis (in microns)
xt_in_startposY = TextInput(value="0", title="Start position (y)")
# Input the end position of the scan along the Y axis (in microns)
xt_in_sizeY = TextInput(value="10", title="Scan size (y):") 
# Input size of step along x axis (microns). (If length/stepsize is not an integer, round (ceil). The true position data will be encoded still.
xt_in_stepsizeY = TextInput(value="66", title="Step size (y):") 
## Space-time tab layout ##
xt_control = layout([[ xt_but_start, xt_but_stop ], [ xt_in_startposX, xt_in_startposY ], [xt_in_sizeX, xt_in_sizeY], [xt_in_stepsizeX, xt_in_stepsizeY]]) # Grid for widget layout
xt_grid = row([xt_control, xt_plot]) # Put widgets and plots in column
xt_tab = Panel(child=xt_grid, title="SpaceTime") # Create the time domain tab

### Lockin output tab ###

# plot shoing live lockin output
lock_plot = figure(plot_width=600, plot_height=300) # Create the color plot window
lock_plot_line = lock_plot.line(x=[], y=[]) # Add empty line plot
## Buttons and controls for lock-in tab ##
lock_but_start = Button(label='Start') # Start button
lock_but_start.on_click(call_lock_but_start) # Call function when pressed
lock_but_stop = Button(label='Stop') # Stop NOW button
lock_but_stop.on_click(call_lock_but_stop) # Call function when pressed
## Lockin tab layout ##
lock_row = row([ lock_but_start, lock_but_stop ]) # Put widgets and plots in column
lock_grid = column([ lock_plot, lock_row ]) # Put the plot above the buttons
lock_tab = Panel(child=lock_grid, title="SpaceTime") # Create the time domain tab

### Global controls ###

# Shutdown
but_shutdown = Button(label='Shutdown')
but_shutdown.on_click(call_shutdown)
# Notifications bar
txt_notifications = Div(text='<font color="green">Ready.</font>')

## Top bar layout ##
global_row=row([but_shutdown, txt_notifications])

# Width of jog buttons in browser
jog_button_width = 50 
## Global jog controls for XYZ axis ##
but_Xup = Button(label='+X')
but_Xup.on_click(call_Xup)
but_Xdown = Button(label='-X')
but_Xdown.on_click(call_Xdown)
but_Yup = Button(label='+Y')
but_Yup.on_click(call_Yup)
but_Ydown = Button(label='-Y')
but_Ydown.on_click(call_Ydown)
but_Zup = Button(label='+Z')
but_Zup.on_click(call_Zup)
but_Zdown = Button(label='-Z')
but_Zdown.on_click(call_Zdown)
## Global jog controls for rotation axis ##
but_RotXup = Button(label='+rX')
but_RotXup.on_click(call_RotXup)
but_RotXdown = Button(label='-rX')
but_RotXdown.on_click(call_RotXdown)
but_RotYup = Button(label='+rY')
but_RotYup.on_click(call_RotYup)
but_RotYdown = Button(label='-rY')
but_RotYdown.on_click(call_RotYdown)
but_RotZup = Button(label='+rZ')
but_RotZup.on_click(call_RotZup)
but_RotZdown = Button(label='-rZ')
but_RotZdown.on_click(call_RotZdown)
## Global position controls (numerical input)  for traslation axes ##
in_posX = TextInput(value="2", title="X position (0-4)")
in_posX.on_change('value', call_posX)
in_posY = TextInput(value="2", title="Y position (0-4)")
in_posY.on_change('value', call_posY)
in_posZ = TextInput(value="2", title="Z position (0-4)")
in_posZ.on_change('value', call_posZ)
## Global position controls (numerical input)  for rotation axes ##
in_posRotX = TextInput(value="3", title="Rot. X position (0-6)")
in_posRotX.on_change('value', call_posRotX)
in_posRotY = TextInput(value="3", title="Rot. Y position (0-6)")
in_posRotY.on_change('value', call_posRotY)
in_posRotZ = TextInput(value="3", title="Rot. Z position (0-6)")
in_posRotZ.on_change('value', call_posRotZ)

## Jog buttons layout ##
jog = layout([[but_Xup, but_Xdown, but_RotXup, but_RotXdown, in_posX, in_posRotX],[but_Yup, but_Ydown, but_RotYup, but_RotYdown, in_posY, in_posRotY],[but_Zup, but_Zdown, but_RotZup, but_RotZdown, in_posZ, in_posRotZ]]) 
jog_tab = Panel(child=jog, title="Jog Controls") # Create the time domain tab

# Make sure the lock-in stream isn't playing as soon as the window opens (TODO: I need to work out why this is needed)
playing =  False
playing_time = False

## Global layout ##
final_layout = column([Tabs(tabs=[ t_tab, xy_tab, xt_tab, lock_tab, jog_tab ]), global_row])

## Show the gui ##
session.show(final_layout)

## run forever ##
session.loop_until_closed() 

###############################################################################










#from bokeh.plotting import figure, curdoc

# create a plot and style its properties
#p = figure(toolbar_location=None)

# add a text renderer to our plot (no data yet)
#r = p.line(x=[], y=[])

#i = 0

#ds = r.data_source

# Create a callback function that activates when go is clicked
#def callback():
#	global i
#	global daq
#	global device
#	global demod_index
#	# BEST PRACTICE --- update .data in one step with a new dict
#	while (1==1):
#		new_data = dict()
#		out = daq.getSample('/%s/demods/%d/sample' % (device, demod_index))
#		new_data['x'] = ds.data['x'] + [out['timestamp'][0]]
#		new_data['y'] = ds.data['y'] + [out['x'][0]]
#		print(new_data)
#		ds.data = new_data
#		print(ds.data)

# add a button widget and configure with the call back
#button = Button(label="Press Me")
#button.on_click(callback)