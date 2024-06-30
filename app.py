from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

MODBUS_HOST = '0.0.0.0'
MODBUS_PORT = 502
client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)

factory_status = {
    'temperature': 0,
    'pressure': 0,
    'humidity': 0
}

def read_modbus_data():
    global factory_status
    while True:
        try:
            temperature = client.read_holding_registers(1, 1).registers[0]
            pressure = client.read_holding_registers(2, 1).registers[0]
            humidity = client.read_holding_registers(3, 1).registers[0]

            factory_status = {
                'temperature': temperature,
                'pressure': pressure,
                'humidity': humidity
            }

            socketio.emit('update_status', factory_status)
        except ModbusException as e:
            print(f'Modbus Error: {e}')
        
        time.sleep(5)

@app.route('/')
def index():
    online = client.read_holding_registers(16, 1).registers[0]
    if online == 0:
        return render_template('warning.html')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(target=read_modbus_data)
    thread.daemon = True
    thread.start()
    
    socketio.run(app, debug=True, host='0.0.0.0')
