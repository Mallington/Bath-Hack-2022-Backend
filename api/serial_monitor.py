import glob
import sys
import time

from serial import Serial, SerialException
import multiprocessing
import threading, queue

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

        self.last_halt = time.time()
        self.q = queue.Queue()
        self.port = port

    def worker(self):
        if not self.noSerial:
            self.arduino = Serial(port=self.port, baudrate=9600, timeout=.1)
            print("Starting monitor")
            while True:
                print("get")
                data_raw = self.q.get()
                print("nbo")
                self.arduino.write(data_raw)
                print(f'Finished {data_raw}')
                self.q.task_done()

    def write(self, data):

        if not self.noSerial:
            print("REAL Serial: ", data)
            self.q.put(bytes(data, 'utf-8'))
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
