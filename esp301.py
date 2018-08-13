###############################################################################
# Newport ESP301 Motion controller
class ESP301:
    """ Newport ESP301 Motion controller class """
    def __init__(self, port="COM6", baudrate=921600):
        """ Initializes serial port, cleans buffers and prints port config """
        self.dev = serial.Serial(port, baudrate, rtscts=True, timeout=5)
        self.dev.flush()
        self.dev.reset_input_buffer()
        self.dev.reset_output_buffer()
        print("║   Port     : %5s     Baud rate: %8s           ║" % (self.dev.port, self.dev.baudrate))
        print("║   Byte size: %5s     Parity   : %8s           ║" % (self.dev.bytesize, self.dev.parity))
        print("║   Stop bits: %5s     RTS/CTS  : %8s           ║" % (self.dev.stopbits, self.dev.rtscts))
        print("║   Firmware : %10s                    ║" % self.firmware())

    def firmware(self):
        """gets firmware string"""
        self.dev.write(b"VE\r")
        return self.dev.readline(-1).decode('ascii').rstrip()

    def errormessage(self):
        """ gets error message """
        self.dev.write(b"TB?\r")
        return self.dev.readline(-1).decode('ascii').rstrip()

    def errorcode(self):
        """ gets error code """
        self.dev.write(b"TE?\r")
        return int(self.dev.readline(-1).decode('ascii').rstrip())

    def stagemodel(self, axis):
        """ gets stage model for the given channel """
        self.dev.write(b"%dID\r" % axis)
        return self.dev.readline(-1).decode('ascii').rstrip()

    def position(self, axis, pos=None, wait=False, verbose=False):
        """gets/sets position
           Arguments (channel int, position float, wait True/False) """
        self.verbose = verbose
        if pos:  # If position is given, then set position
            if self.verbose:
                print("Moving ch%d to %f" % (axis, pos))
            self.dev.write(b"%dPA%f\r" % (axis, pos))
            if wait:  # Wait or not for the motion to stop
                # Actual waiting is limited by serial timeout
                if self.verbose:
                    print("Waiting for ch%d to stop" % axis)
                self.dev.write(b"%dWS\r" % axis)
        self.dev.write(b"%dTP\r" % axis)
        return float(self.dev.readline(-1).decode('ascii').rstrip())

    def velocity(self, axis, vel=None):
        """ gets/sets velocity
            Arguments (channel int, velocity float) """
        if vel:  # If velocity is given, then set velocity
            self.dev.write(b"%dVA%f\r" % (axis, vel))
        self.dev.write(b"%dTV\r" % axis)
        return float(self.dev.readline(-1).decode('ascii').rstrip())
