import pyqtgraph as pg
import zhinst.utils
import configparser
import time
import argparse

class genLines:

    def __init__(self, plot):
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen = 'w') # create infinite vertical line
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen = 'w') #  create infinite horizontal line
        plot.addItem(self.hLine, ignoreBounds=True) # add the horizontal line
        plot.addItem(self.vLine, ignoreBounds=True) # add vertical line

# callback for when the mouse is moved after the scan is complete (move cursor and set the text)
class mouseMoved:
   
    def __init__(self, evt, timer):

        if timer.isActive() is False: # do if scan is not running
            mousePoint = demod1.vb.mapSceneToView(evt[0]) # get the mouse position
            demod1CursorPos.setText("<span style='font-size: 12pt'>Cursor at: x=%0.3f,   <span style='color: red'>y1=%0.3f</span>" % (mousePoint.x(), mousePoint.y())) # set the numerical display
            demod1Line.vLine.setPos(mousePoint.x()) # move the vertical line
            demod1Line.hLine.setPos(mousePoint.y()) # move the horisontal line


##############################################
### Initialise the Zurich instruments MFLI ###
##############################################

class MFLI:


    def __init__(self): 
        
        self.demod_0 = 0 # make it a bit easier to know which demodulator i'm using
        self.demod_1 = 1
        self.demod_2 = 2
        
        device_id = 'dev3047' # Serial number of our MFLI
        apilevel = 6

        (self.daq, self.device, self.props) = zhinst.utils.create_api_session(device_id,
                                                            apilevel,
                                                            required_devtype='.*LI|.*IA|.*IS') # Create API session
    def set(self, CP): # CP is config parser
     # Stop from any data streaming/being collected (needs to be done as prep for measurements)
        self.daq.unsubscribe('*')
    
       # Experimental settings
        exp_setting = [['/%s/demods/%d/timeconstant' % (self.device, self.demod_0), CP.TC], # Set filter time constant
                        ['/%s/demods/%d/timeconstant' % (self.device, self.demod_1), CP.TC], # Set filter time constant
                        ['/%s/demods/%d/timeconstant' % (self.device, self.demod_2), CP.TC], # Set filter time constant
                        ['/%s/demods/%d/harmonic' % (self.device, self.demod_0), CP.nD0], # Set harmonic for measurement
                        ['/%s/demods/%d/harmonic' % (self.device, self.demod_1), CP.nD1], # Set harmonic for measurement
                        ['/%s/demods/%d/harmonic' % (self.device, self.demod_2), CP.nD2]] # Set harmonic for measurement
    
        self.daq.set(exp_setting)
        # Wait for demod filter to settle (10 * filter time constant)

        self.daq.unsubscribe('*')

        time.sleep(10*CP.TC)
        # SYNC (make sure PC and MFLI agree with settings, etc...)
        # must be done after waiting for the demod filter to settle
        self.daq.sync()
		
# parser for config file (scan parameters) this is a class so the returned values match the style of the command line parser (i.e. class (dot notation))
class ConfigParser():
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('scan.conf')

        self.Tstart = int(config['TWScan']['start'])
        self.Tlength = int(config['TWScan']['length'])
        self.Tstep = int(config['TWScan']['step'])
        self.RX = config['TWScan']['RX']
        self.TC = float(config['TWScan']['TC'])
        self.nD0 = int(config['TWScan']['nD0'])
        self.nD1 = int(config['TWScan']['nD1'])
        self.nD2 = int(config['TWScan']['nD2'])

        # Calculate dwell time from time constant
        if self.TC == 0.3:
            self.Tdwell = 1

        elif self.TC == 0.1:
            self.Tdwell = 0.5

        else:
            self.Tdwell = 3*self.TC

def CLineParser():
    # Parser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', help = 'Specify to close the program once the scan is finished. If not specified, the scan will finish and a terminal will open for control', action='store_true')
    parser.add_argument('-x', help = 'Horisontal position of sample ("x" position).', action='store')
    parser.add_argument('-y', help = 'Vertical position of sample along optical axis ("y" position).', action='store')
    parser.add_argument('-z', help = 'Position of sample along optical axis ("z" position).', action='store')
    args = parser.parse_args()
    return args

class klinger:
    
    def __init__(self, rm):
        self.klinger = rm.open_resource('GPIB0::8::INSTR')  # 'open' Klinger stage
        # Sets required EOL termination
        
        self.klinger.write_termination = '\r'
        self.klinger.read_termination = '\r'
        
        self.klinger.timeout = 30000 # make the timeout large for long stage moves

    def move(self, pos):
        
        self.klinger.write("PW" + str(pos))

        klingerPos = float(self.klinger.query('DW').strip("W=+")) # request position (will only be provided when movement is complete) Strip formatting and generate position as float
                        
        if int(klingerPos) != pos:
            print("Position error") 
