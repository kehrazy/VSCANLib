import time
from enum import Enum
from vs_can_lib import *

version = VSCAN.get_api_version()
print("VSCAN-API Version {}.{}.{}".format(version.Major, version.Minor, version.SubMinor))

port = "192.168.254.254:2001"
can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)

can_bus.get_error_string(-1)

can_bus.write(frame_id=0xFF, data=[1, 2, 3, 4, 5, 8, 8, 8])

can_bus.flush()

time.sleep(0.5)  # Дождаться получения сообщения

mes = can_bus.read_mes()

parameters = Enum('parameters', [('MEM', 0), ('SPI', 1), ('I2C', 2), ('ADC', 3), ('SYS', 4), ('PIN', 5), ('WORD', 6)])
functions = Enum('functions' [('READ', 0), ('WRITE', 1), ('SET', 2), ('RESET',3)])

def form_send_id(func, param, addr):
    return int(f'{addr:02x}', 16) | (func + (param << 4) << addr.bit_length())

id = form_send_id(functions.READ.value, parameters.MEM.value , 0xdeadbeef)

mes = VSCAN.form_message(0x60, [0x00,0x00,0x00])
a = VSCAN.

print(mes)

status = can_bus.close()
if status < 0:
    print("<Error> Close: status = {}".format(status))
else:
    print("<Success> Close: status = {}".format(status))
