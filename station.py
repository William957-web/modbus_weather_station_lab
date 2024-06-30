from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import random
import threading
import time

online = 1

def update_registers(context):
    while True:
        slave_id = 0x00
        address = 0x01

        temperature = random.randint(20, 30)
        pressure = random.randint(1000, 1100)
        humidity = random.randint(30, 50)
        context[slave_id].setValues(3, address, [temperature])
        context[slave_id].setValues(3, address + 1, [pressure])
        context[slave_id].setValues(3, address + 2, [humidity])
        context[slave_id].setValues(3, address + 15, [online])

        time.sleep(5)

# Data storage
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

# Machine Configurations
identity = ModbusDeviceIdentification()
identity.VendorName = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'pymodbus Server'
identity.ModelName = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'

# Multi Threadings
update_thread = threading.Thread(target=update_registers, args=(context,))
update_thread.daemon = True
update_thread.start()

# Modbus TCP Server
StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))
