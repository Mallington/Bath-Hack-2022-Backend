import multiprocessing
import threading
import time
from flask import Flask, request
from serial_monitor import list_ports, SerialMonitor, filter_ports
from cheap_vison_algo import PersonDestroyer

noSerial = False
videoNumber =0
print("Listing possible ports")
ports = filter_ports(list_ports())
print(ports)

standalone = False

if len(ports) ==0 and not noSerial:
    assert "Serial port not found"

serialMonitor = SerialMonitor(port=None, noSerial=True) if noSerial else SerialMonitor(ports[0])


visonPerson = PersonDestroyer(serialMonitor, videoNumber)


app = Flask(__name__)






print("done")
print(__name__)
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/fire', methods=['GET'])
def search():
    print("Firing")
    serialMonitor.fire()
    time.sleep(1)
    serialMonitor.stop_firing()

    return "I have fired"



threading.Thread(target=serialMonitor.worker, daemon=True).start()

# threading.Thread(target=visonPerson.start, daemon=False).start()

if standalone:
    visonPerson.start(showImg=True)
else:
    thread = threading.Thread(target=visonPerson.start, daemon=True).start()

