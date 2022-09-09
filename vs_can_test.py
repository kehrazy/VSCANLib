import time

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

print(mes)

status = can_bus.close()
if status < 0:
    print("<Error> Close: status = {}".format(status))
else:
    print("<Success> Close: status = {}".format(status))
