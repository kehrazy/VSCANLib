# -*- coding: utf-8 -*- #
import ctypes
import time
from enum import Enum
import string
from load_lib import vs_can_api

# port_ip = "10.7.6.70:2001"
port_ip = "192.168.254.254:2001"

# vs_can_api = ctypes.cdll.LoadLibrary(r"E:\WORK\Repository\Megapolis\PO_CAN_LIBRARY\Win64\vs_can_api.dll")

DWORD = ctypes.c_uint32

VSCAN_HANDLE = ctypes.c_int
VSCAN_STATUS = ctypes.c_int

VSCAN_FIRST_FOUND = 0

# Debug Mode
VSCAN_DEBUG_MODE_CONSOLE = 1  # define VSCAN_DEBUG_MODE_CONSOLE        (void*)1
VSCAN_DEBUG_MODE_FILE = 2  # define VSCAN_DEBUG_MODE_FILE               (void*)2
# Debug Level
VSCAN_DEBUG_NONE = 0  # define VSCAN_DEBUG_NONE                        (void*)0
VSCAN_DEBUG_LOW = -1  # define VSCAN_DEBUG_LOW                         (void*)-1
VSCAN_DEBUG_MID = 51  # define VSCAN_DEBUG_MID                         (void*)-51
VSCAN_DEBUG_HIGH = -101  # define VSCAN_DEBUG_HIGH                        (void*)-101

# Status / Errors
VSCAN_ERR_OK = 0
VSCAN_ERR_ERR = VSCAN_DEBUG_LOW
VSCAN_ERR_NO_DEVICE_FOUND = VSCAN_DEBUG_LOW - 1
VSCAN_ERR_SUBAPI = VSCAN_DEBUG_LOW - 2
VSCAN_ERR_NOT_ENOUGH_MEMORY = VSCAN_DEBUG_LOW - 3
VSCAN_ERR_NO_ELEMENT_FOUND = VSCAN_DEBUG_LOW - 4
VSCAN_ERR_INVALID_HANDLE = VSCAN_DEBUG_LOW - 5
VSCAN_ERR_IOCTL = VSCAN_DEBUG_LOW - 6
VSCAN_ERR_MUTEX = VSCAN_DEBUG_LOW - 7
VSCAN_ERR_CMD = VSCAN_DEBUG_LOW - 8
VSCAN_ERR_LISTEN_ONLY = VSCAN_DEBUG_LOW - 9
VSCAN_ERR_NOT_SUPPORTED = VSCAN_DEBUG_LOW - 10
VSCAN_ERR_GOTO_ERROR = VSCAN_DEBUG_HIGH  # Debug Level High

# Mode
VSCAN_MODE_NORMAL = 0
VSCAN_MODE_LISTEN_ONLY = 1
VSCAN_MODE_SELF_RECEPTION = 2

# Speed
VSCAN_SPEED_1M = 8
VSCAN_SPEED_800K = 7
VSCAN_SPEED_500K = 6
VSCAN_SPEED_250K = 5
VSCAN_SPEED_125K = 4
VSCAN_SPEED_100K = 3
VSCAN_SPEED_50K = 2
VSCAN_SPEED_20K = 1
# // generally not possible with the TJA1050
# //#define VSCAN_SPEED_10K               (void*)0

# Device Types
VSCAN_HWTYPE_UNKNOWN = 0
VSCAN_HWTYPE_SERIAL = 1
VSCAN_HWTYPE_USB = 2
VSCAN_HWTYPE_NET = 3
VSCAN_HWTYPE_BUS = 4

VSCAN_IOCTL_OFF = 0
VSCAN_IOCTL_ON = 1

# Timestamp
VSCAN_TIMESTAMP_OFF = VSCAN_IOCTL_OFF
VSCAN_TIMESTAMP_ON = VSCAN_IOCTL_ON

# Filter Mode
VSCAN_FILTER_MODE_SINGLE = 1
VSCAN_FILTER_MODE_DUAL = 2

# Ioctls
VSCAN_IOCTL_SET_DEBUG = 1
VSCAN_IOCTL_GET_HWPARAM = 2
VSCAN_IOCTL_SET_SPEED = 3
VSCAN_IOCTL_SET_BTR = 4
VSCAN_IOCTL_GET_FLAGS = 5
VSCAN_IOCTL_SET_ACC_CODE_MASK = 6
VSCAN_IOCTL_SET_TIMESTAMP = 7
VSCAN_IOCTL_SET_DEBUG_MODE = 8
VSCAN_IOCTL_SET_BLOCKING_READ = 9
VSCAN_IOCTL_SET_FILTER_MODE = 10
VSCAN_IOCTL_GET_API_VERSION = 11
VSCAN_IOCTL_SET_FILTER = 12

# Bits for VSCAN_IOCTL_GET_FLAGS
VSCAN_IOCTL_FLAG_RX_FIFO_FULL = (1 << 0)
VSCAN_IOCTL_FLAG_TX_FIFO_FULL = (1 << 1)
VSCAN_IOCTL_FLAG_ERR_WARNING = (1 << 2)
VSCAN_IOCTL_FLAG_DATA_OVERRUN = (1 << 3)
VSCAN_IOCTL_FLAG_UNUSED = (1 << 4)
VSCAN_IOCTL_FLAG_ERR_PASSIVE = (1 << 5)
VSCAN_IOCTL_FLAG_ARBIT_LOST = (1 << 6)
VSCAN_IOCTL_FLAG_BUS_ERROR = (1 << 7)
VSCAN_IOCTL_FLAG_API_RX_FIFO_FULL = (1 << 16)

# Masks for VSCAN_IOCTL_SET_ACC_CODE_MASK
VSCAN_IOCTL_ACC_CODE_ALL = 0x00000000
VSCAN_IOCTL_ACC_MASK_ALL = 0xFFFFFFFF

# Flags
VSCAN_FLAGS_STANDARD = (1 << 0)
VSCAN_FLAGS_EXTENDED = (1 << 1)
VSCAN_FLAGS_REMOTE = (1 << 2)
VSCAN_FLAGS_TIMESTAMP = (1 << 3)


# Hardware Parameter Structure
class VSCAN_HWPARAM(ctypes.Structure):
    _fields_ = [("SerialNr", ctypes.c_uint32), ("HwVersion", ctypes.c_uint8), ("SwVersion", ctypes.c_uint8),
                ("HwType", ctypes.c_uint8)]


'''
// Hardware Parameter Structure
typedef struct
{
    UINT32 SerialNr;
    UINT8 HwVersion;
    UINT8 SwVersion;
    UINT8 HwType;
} VSCAN_HWPARAM;
'''


# Message Structure
class VSCAN_MSG(ctypes.Structure):
    _fields_ = [("Id", ctypes.c_uint32), ("Size", ctypes.c_uint8), ("Data", ctypes.c_uint8 * 8),
                ("Flags", ctypes.c_uint8), ("Timestamp", ctypes.c_uint16)]

    def __repr__(self):  # Print CAN message content
        return (
            "Id = {:08X}, Size = {}, Flags = {}, Timestamp = {}, Data = [{}]".format(
                self.Id, self.Size, self.Flags, self.Timestamp, ", ".join("{:02X}".format(num) for num in self.Data)
            )
        )


'''
// Message Structure
typedef struct
{
    UINT32 Id;
    UINT8 Size;
    UINT8 Data[8];
    UINT8 Flags;
    UINT16 Timestamp;
} VSCAN_MSG;
'''


class VSCAN_BTR(ctypes.Structure):
    _fields_ = [("Btr0", ctypes.c_uint8), ("Btr1", ctypes.c_uint8)]


'''
// Bit Timing Register Structure
typedef struct
{
    UINT8 Btr0;
    UINT8 Btr1;
} VSCAN_BTR;
'''


# Acceptance Code and Mask Structure
class VSCAN_CODE_MASK(ctypes.Structure):
    _fields_ = [("Code", ctypes.c_uint32), ("Mask", ctypes.c_uint32)]


'''
// Acceptance Code and Mask Structure
typedef struct
{
    UINT32 Code;
    UINT32 Mask;
} VSCAN_CODE_MASK;
'''


# API Version Structure
class VSCAN_API_VERSION(ctypes.Structure):
    _fields_ = [("Major", ctypes.c_int8), ("Minor", ctypes.c_int8), ("SubMinor", ctypes.c_int8)]


'''
// API Version Structure
typedef struct
{
    UINT8 Major;
    UINT8 Minor;
    UINT8 SubMinor;
} VSCAN_API_VERSION;
'''


# Filter Structure
# <received_can_id> & Mask == Id & Mask
class VSCAN_FILTER(ctypes.Structure):
    _fields_ = [("Size", ctypes.c_int8), ("Id", ctypes.c_int32), ("Mask", ctypes.c_int32), ("Extended", ctypes.c_int8)]


'''
// Filter Structure
// <received_can_id> & Mask == Id & Mask
typedef struct
{
    UINT8 Size;
    UINT32 Id;
    UINT32 Mask;
    UINT8 Extended;
} VSCAN_FILTER;
'''

# // If the function succeeds, the return value is greater zero (handle)
# // If the function fails, the return value is one of VSCAN_STATUS
VSCAN_Open = vs_can_api.VSCAN_Open
VSCAN_Open.argtypes = [ctypes.c_char_p, ctypes.c_uint32]
VSCAN_Open.restype = VSCAN_HANDLE
# // If the function succeeds, the return value is greater zero (handle)
# // If the function fails, the return value is one of VSCAN_STATUS
# VSCAN_HANDLE VSCAN_Open(CHAR *SerialNrORComPortORNet, DWORD Mode);
# // The return value is one of VSCAN_STATUS

VSCAN_Close = vs_can_api.VSCAN_Close
VSCAN_Close.argtypes = [VSCAN_HANDLE]
VSCAN_Close.restype = VSCAN_STATUS
# // The return value is one of VSCAN_STATUS
# VSCAN_STATUS VSCAN_Close(VSCAN_HANDLE Handle);
# // The return value is one of VSCAN_STATUS

# // The return value is one of VSCAN_STATUS
VSCAN_Ioctl = vs_can_api.VSCAN_Ioctl
VSCAN_Ioctl.argtypes = [VSCAN_HANDLE, ctypes.c_uint32, ctypes.c_void_p]
VSCAN_Ioctl.restype = VSCAN_STATUS
# VSCAN_STATUS VSCAN_Ioctl(VSCAN_HANDLE Handle, DWORD Ioctl, VOID *Param);

# // The return value is one of VSCAN_STATUS
VSCAN_Flush = vs_can_api.VSCAN_Flush
VSCAN_Flush.argtypes = [VSCAN_HANDLE]
VSCAN_Flush.restype = VSCAN_STATUS
# VSCAN_STATUS VSCAN_Flush(VSCAN_HANDLE Handle);

# // The return value is one of VSCAN_STATUS
VSCAN_Write = vs_can_api.VSCAN_Write
VSCAN_Write.argtypes = [VSCAN_HANDLE, ctypes.POINTER(VSCAN_MSG), ctypes.c_uint32, ctypes.POINTER(DWORD)]
VSCAN_Write.restype = VSCAN_STATUS
# VSCAN_STATUS VSCAN_Write(VSCAN_HANDLE Handle, VSCAN_MSG *Buf, DWORD Size, DWORD *Written);

# // The return value is one of VSCAN_STATUS
VSCAN_Read = vs_can_api.VSCAN_Read
VSCAN_Read.argtypes = [VSCAN_HANDLE, ctypes.POINTER(VSCAN_MSG), ctypes.c_uint32, ctypes.POINTER(DWORD)]
VSCAN_Read.restype = VSCAN_STATUS
# VSCAN_STATUS VSCAN_Read(VSCAN_HANDLE Handle, VSCAN_MSG *Buf, DWORD Size, DWORD *Read);

# // The return value is one of VSCAN_STATUS
# don't implemented in Python
# ifdef WIN32
# VSCAN_STATUS VSCAN_SetRcvEvent(VSCAN_HANDLE Handle, HANDLE Event);
# else
# VSCAN_STATUS VSCAN_SetRcvEvent(VSCAN_HANDLE Handle, sem_t *Event);
##endif

# // No return value for this function
VSCAN_GET_ERROR_MAX_STRINGSIZE = 255
VSCAN_GetErrorString = vs_can_api.VSCAN_GetErrorString
VSCAN_GetErrorString.argtypes = [
    VSCAN_STATUS, ctypes.POINTER(ctypes.c_char * VSCAN_GET_ERROR_MAX_STRINGSIZE), ctypes.c_uint32
]
VSCAN_Read.restype = None


# VOID VSCAN_GetErrorString(VSCAN_STATUS Status, CHAR *String, DWORD MaxLen);


# Own VSCAN_Exception class
class VSCANException(Exception):
    pass

class VSCAN():
    def __init__(self, port_com, mode, can_speed):
        self.can_descr = self.open(port_com, mode)
        self.set_speed(can_speed)

    # Open CAN Device
    def open(self, port_com, mode):
        status = VSCAN_Open(ctypes.c_char_p(port_com.encode('utf-8')), mode)
        if status < 0:
            raise VSCANException(
                "<Error> Can't open CAN: status = {}({})".format(status, self.get_error_string(status)))

        print('CAN device opened.')
        return status

    # Close CAN device. Ur Cap.
    def close(self):
        status = VSCAN_ERR_OK  # VSCAN_Close(self.can_descr)
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> close: status = {}({})".format(status, self.get_error_string(status)))
        return status

    # Get API Version in VSCAN_API_VERSION structure (version.Major, version.Minor, version.SubMinor)
    @staticmethod
    def get_api_version():
        version = VSCAN_API_VERSION(0)
        p_version = ctypes.pointer(version)
        VSCAN_Ioctl(0, VSCAN_IOCTL_GET_API_VERSION, p_version)
        return version

    # Set CAN Speed
    def set_speed(self, can_speed):
        status = VSCAN_Ioctl(self.can_descr, VSCAN_IOCTL_SET_SPEED, can_speed)
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> set_speed: status = {}({})".format(status, self.get_error_string(status)))
        return

    # Write CAN message
    def write_mes(self, mes, flush=True):
        Written = DWORD(0)
        status = VSCAN_Write(self.can_descr, ctypes.pointer(mes), 1, ctypes.pointer(Written))
        print("can_write_mes status = {}, Written = {}".format(status, Written.value))
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> write_mes: status = {}({})".format(status, self.get_error_string(status)))
        if Written.value != 1:
            raise VSCANException(
                "<Error> write_mes: some thing wrong with trancieve Written.value ({}) != 1 ".format(Written.value)
            )

        if flush:
            self.flush()
        return Written.value

    def form_message(self, frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0):
        mes = VSCAN_MSG()
        mes.Id = frame_id
        if not data_size:
            data_size = len(data)
            if data_size > 8:
                raise VSCANException(f"<Error> Data size == {data_size} > 8. Not valid for CAN")
        mes.Size = data_size
        for i in range(data_size):
            mes.Data[i] = data[i]
        mes.Flags = flags
        mes.Timestamp = timestamp
        print(mes)
        return mes  # self.write_mes(mes, flush)

    # Write proxy. Can message forms inside function
    def write(self, frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0, flush=True):
        mes = VSCAN_MSG()
        mes.Id = frame_id
        if not data_size:
            data_size = len(data)
            if data_size > 8:
                raise VSCANException("<Error> Data size == {} > 8. Not valid for CAN".format(data_size))
        mes.Size = data_size
        for i in range(data_size):
            mes.Data[i] = data[i]
        mes.Flags = flags
        mes.Timestamp = timestamp
        mes = self.form_message(frame_id, data, data_size, flags, timestamp)
        print("CAN write MES: {}".format(mes))
        return self.write_mes(mes, flush)

    # Read message
    def read_mes(self):
        mes = VSCAN_MSG()
        Readed = DWORD(0)
        status = VSCAN_Read(self.can_descr, ctypes.pointer(mes), 1, ctypes.pointer(Readed))
        if status is None:  # Todo WTF? It return None in success
            status = 0

        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> read_mes: status = {}({})".format(status, self.get_error_string(status)))

        if Readed.value == 0:
            mes = None
        elif Readed.value != 1:
            raise VSCANException("<Error> read_mes: some thing wrong Readed.value ({}) != 1 != 0".format(Readed.value))
        return mes

    # Read proxy, message in dict
    def read(self):
        mes = self.read_mes()
        if mes != None:
            return {"": mes.Id, "Data": list(mes.Data)[:mes.Size]}
        return mes

    def flush(self):
        status = VSCAN_Flush(self.can_descr)
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> read_mes: status = {}({})".format(status, self.get_error_string(status)))
        return status

    @staticmethod
    def get_error_string(status):
        # Form error string by status code
        string_buf = (ctypes.c_char * VSCAN_GET_ERROR_MAX_STRINGSIZE)()
        p_string_buf = ctypes.pointer(string_buf)
        VSCAN_GetErrorString(status, p_string_buf, VSCAN_GET_ERROR_MAX_STRINGSIZE)
        return string_buf.value

    # ToDo Not tested!!! U can read number of messages by using this function
    def read_mes_s(self):
        test_mes = (VSCAN_MSG * 5)()
        Readed = DWORD(0)
        status = VSCAN_Read(self.can_descr, ctypes.pointer(test_mes[0]), 1, ctypes.pointer(Readed))
        mes = test_mes[0]
        print("status = {}, Readed = {}".format(status, Readed.value))
        return mes

    def write_test_many(self):
        """
        class VSCAN_MSG(ctypes.Structure):
            _fields_ = [("Id", ctypes.c_uint32),
                        ("Size", ctypes.c_uint8),
                        ("Data", ctypes.c_uint8 * 8),
                        ("Flags", ctypes.c_uint8),
                        ("Timestamp", ctypes.c_uint16)]
        """
        Written = DWORD(0)
        test_mes = (VSCAN_MSG * 5)()
        test_mes[0].Id = 0xFF
        test_mes[0].Size = 0x8
        for i in range(8):
            test_mes[0].Data[i] = i
        test_mes[0].Flags = VSCAN_FLAGS_STANDARD
        test_mes[0].Timestamp = 0xFF
        status = VSCAN_Write(self.can_descr, ctypes.pointer(test_mes[0]), 1, ctypes.pointer(Written))
        print("status = {}, Written = {}".format(status, Written.value))
        return status



# test for VSCAN.get_error_string
def test_get_error_string():
    for i in range(-20, 10):  # noqa: WPS432
        print("error_code = {}. Error string = {}".format(i, VSCAN.get_error_string(i)))


def can_self_test():
    # test_get_error_string()

    version = VSCAN.get_api_version()
    print("VSCAN-API Version {}.{}.{}".format(version.Major, version.Minor, version.SubMinor))

    port = port_ip
    can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)

    # Write some messages
    can_bus.write(frame_id=0xFF, data=[1, 2, 3, 4, 5, 8])  # noqa: WPS432

    time.sleep(0.5)  # Дождаться получения сообщения

    mes = can_bus.read_mes()
    print(mes)

    # Write some messages
    can_bus.write(frame_id=0xFF, data=[1, 2, 3])  # noqa: WPS432

    time.sleep(0.5)  # Дождаться получения сообщения

    mes = can_bus.read()
    print(mes)

    status = can_bus.close()
    if status < 0:
        print("<Error> Close: status = {}".format(status))
    else:
        print("<Success> Close: status = {}".format(status))


def test_data_transmit():
    version = VSCAN.get_api_version()
    print("VSCAN-API Version {}.{}.{}".format(version.Major, version.Minor, version.SubMinor))

    port = port_ip
    can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)

    counter = 0

    TEST_LENGTH = 1000
    for i in range(0, TEST_LENGTH):
        DLC = (i % 8 + 1) & 0xFF
        Id = (i % 8 + i % 0xFF) & 0xFF
        aData = []
        for j in range(0, DLC):
            if i < 255:
                tmp_val = i
            elif ((i > 255) and (i < 512)):
                tmp_val = 255 - i
            else:
                tmp_val = i % 2 + i % 255
            aData.append((tmp_val + j) & 0xFF)
        # def write(self, frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0):
        can_bus.write(frame_id=Id, data=aData, data_size=DLC)
        time.sleep(0.1)  # Дождаться получения сообщения
        if counter % 10 == 0:
            print(counter)
        counter += 1

    status = can_bus.close()
    if status < 0:
        print("<Error> Close: status = {}".format(status))
    else:
        print("<Success> Close: status = {}".format(status))


if __name__ == "__main__":
    test_data_transmit()