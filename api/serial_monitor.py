import glob
import sys

from serial import Serial, SerialException

def filter_ports(ports):
    return list(filter(lambda port : "usbmodem" in port, ports))
def list_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    return result

class SerialMonitor:
    def __init__(self, port='COM4', noSerial=False):
        self.noSerial = noSerial
        if not self.noSerial:
            self.arduino = Serial(port=port, baudrate=9600, timeout=.1)
            print("Starting monitor")


    def write(self, data):

        if not self.noSerial:
            print("REAL Serial: ", data)
            self.arduino.write(bytes(data, 'utf-8'))
        else:
            print("PRETENDING Serial: ", data)

    def fire(self):
        print("Firing")
        self.write('f')

    def stop_firing(self):
        print("Ceasefire")
        self.write('c')

    def left(self):
        print("Left")
        self.write('l')

    def right(self):
        print("Right")
        self.write('r')

    def stop(self):
        print("Halting Motor")
        self.write('h')
