# -*- coding: utf-8 -*- #
import ctypes
import time
from enum import Enum
import string
from load_lib import vs_can_api

# port_ip = "10.7.6.70:2001"
PORT_IP = "192.168.254.254:2001"

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
VSCAN_DEBUG_MID = -51  # define VSCAN_DEBUG_MID                         (void*)-51
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


# class that can't be modified.
class const(object):
    def __setattr__(self, key, value):
        pass  # constants can not be changed.


class VSCAN:
    def __init__(self, port_com, mode, can_speed):
        self.can_descr = self.open(port_com, mode)
        self.set_speed(can_speed)

    @staticmethod
    def print_version():
        """
        function to print the version of the VSCAN-API.
        """
        v = VSCAN.get_api_version()
        print(f"VSCAN-API Version {v.Major}.{v.Minor}.{v.SubMinor}")

    # > This class represents a VSCAN message
    class VSCANMessage:
        # > The `Parameters` class is an enumeration of the parameters that can be passed to the `get_data` function
        class Parameters(Enum):
            MEM = 0
            SPI = 1
            I2C = 2
            ADC = 3
            SYS = 4
            PIN = 5
            WORD = 6

        # > The `Functions` class is an enumeration of the functions that can be used in the `Function` class
        class Functions(Enum):
            READ = 0
            WRITE = 1
            SET = 2
            RESET = 3

        # возможные сочетания функций и параметров.
        ftp_dict: dict[Functions, list[Parameters]] = {Functions.READ: list(Parameters),
                                                       Functions.WRITE: [Parameters.MEM, Parameters.I2C,
                                                                         Parameters.SPI],
                                                       Functions.SET: [Parameters.PIN],
                                                       Functions.RESET: [Parameters.PIN]}
        i2c_response = 0

        expected_response_length: dict[Functions, dict[Parameters, int]] = {
            Functions.READ: {Parameters.MEM: 4,
                             Parameters.SPI: 2,
                             Parameters.I2C: i2c_response,
                             Parameters.ADC: 5},
            Functions.WRITE: {Parameters.MEM: 1,
                              Parameters.SPI: 2,
                              Parameters.I2C: 1,
                              },
            Functions.SET: {Parameters.PIN: 1}
        }

        def get_response_length(self):
            """
            returns the length of the response
            """
            return (self.expected_response_length[self.function])[self.parameter]

        @property
        def verify_message(self) -> bool:
            """
            > This function verifies the VSCAN message
            """
            if self.parameter not in self.ftp_dict[self.function]:
                raise VSCANException(f'<Error> verify_instruction: cant request {self.parameter} by {self.function}')

            # убедимся, что каждый байт инструкции - hex от 00 до FF.
            def is_hex(str_byte):
                return set(str_byte).issubset(string.hexdigits)

            for byte in self.message.split(' '):
                if not is_hex(byte) or len(byte) != 2:
                    raise VSCANException(f'<Error> Invalid request! {byte} is not a proper hex byte!')

            return True

        def form_message(self) -> str:
            if self.request:
                def form_instruction_byte(func, param):
                    # byte =    hex(function)         +              hex(parameter << 4)
                    return str(int(f'{func.value:X}') + int(f'{int(bin(param.value << 4), 2):X}'))  # переписать
                    # убедиться, что в первом байте два чара

                return str(
                    f'{form_instruction_byte(self.function, self.parameter).zfill(2)} {self.request}')  # переделать.

            # - Бэрримор, что у меня хлюпает в реквесте?
            # - [None, ''], сэр!
            # - [None, '']?! Что они там делают?!
            # - Хлюпают, сэр...
            raise VSCANException('<Error> form_data: invalid request!')

        def __init__(self, function: Functions, parameter: Parameters, request: str):
            """
            > This function takes in a function, parameter, and request and returns a message

            param function: The function you want to call
            type function: VSCANMessage.Functions
            param parameter: The parameter that the function is being called with
            type parameter: VSCANMessage.Parameters
            param request: The request that was sent to the server
            type request: str
            """
            self.function = function
            self.parameter = parameter
            self.request = request
            self.message = self.form_message()
            self.is_valid_message = self.verify_message

        def __str__(self):
            return (f"{'-' * 10}\n"
                    f'function: {self.function}\n'
                    f'parameter: {self.parameter}\n'
                    f'request: {self.request}\n'
                    f'message: {self.message}\n'
                    f'is_valid_message: {self.is_valid_message}\n')

        def __repr__(self):
            return self.message

    # > The VSCANId class is used to represent a VSCAN Message ID.
    class VSCANId:
        class Parameters:
            class RCI(Enum):
                RCI_FIRST = 1
                RCI_SECOND = 2

            class SID(Enum):
                REPLY = 0
                REQUEST = 1

            class Status(Enum):
                LCC = 2  # #define STATUS_LCC    	  NOC_LCC
                FID = 120  # функция ПМУ
                TEST = 121

            class LCC(Enum):
                EEC = 0  # исключительное событие
                NOC = 2  # нормальная операция
                NSC = 4  # сервис шины
                UDC = 5  # пользовательский канал
                TMC = 6  # тестирование и поддержка
                FMC = 7  # канал миграции

            class FID(Enum):
                MFC = 0  # Multicast Function Code ID
                IMA = 15  # Integral Modular Avionics
                TEST = 121
                UTDS = 126  # Upload Target or Download Source
                TTM = 127  # Temporary Test and Maintenance

            class ID_POS(Enum):
                RCI = 0
                SID = 2
                S_FID = 9
                P = 16
                L = 17
                S = 18
                R = 18
                C_FID = 19
                LCC = 26

            class MessageType(Enum):
                CLIENT = 1
                SERVER = 0

            class Privacy(const):
                value = 1

            class LocalBus(const):
                value = 1

        def __init__(self):
            def make_bit(count: int, value):
                return bytes(value.to_bytes(count, byteorder='little'))

            parameters = self.Parameters
            self.message_id = [None for _ in range(9)]  # list of the message id
            self.rci = self.message_id[0] = make_bit(2,
                                                     parameters.RCI.RCI_FIRST.value)  # rci. @doc: RCI_1 - 1, RCI_2 - 2
            self.sid = self.message_id[1] = make_bit(7, 1)  # вроде 1?
            self.server_fid = self.message_id[2] = make_bit(7, parameters.Status.TEST.value)  # 120 / 121 ?
            self.privacy = self.message_id[3] = make_bit(1, parameters.Privacy.value)
            self.local_bus = self.message_id[4] = make_bit(1, parameters.LocalBus.value)
            self.msg_type = self.message_id[5] = make_bit(1, parameters.MessageType.CLIENT.value)  # msg_type
            self.client_fid = self.message_id[6] = make_bit(7, parameters.FID.TEST.value)  # client_fid
            self.lcc = self.message_id[7] = make_bit(3, parameters.LCC.TMC.value)  # lcc
            self.empty = self.message_id[8] = ''  # ?

        def __str__(self):
            def fmt_string(prefix, bits):  # much python, very wow
                # message with spaces on the left, bytes formatted like {bits: something, width 50} | int: some bytes to integer form
                return (f'{prefix.ljust(15, " ")}|   '
                        f'bits: {str(bits):{int(50 - len(prefix.ljust(15, " ")))}} | '
                        f'int: {int.from_bytes(bits, "little")}\n')

            return (f"{'-' * 10}\n"
                    f"{fmt_string('RCI [0-1]', self.rci)}"
                    f"{fmt_string('SID [2-8]', self.sid)}"
                    f"{fmt_string('Server FID', self.server_fid)}"
                    f"{fmt_string('Privacy', self.privacy)}"
                    f"{fmt_string('Local Bus', self.local_bus)}"
                    f"{fmt_string('Message Type', self.msg_type)}"
                    f"{fmt_string('Client FID', self.client_fid)}"
                    f"{fmt_string('LCC', self.lcc)}\n"
                    f'ID: {self.message_id}\n')

    # Open CAN Device
    def open(self, port_com, mode):
        status = VSCAN_Open(ctypes.c_char_p(port_com.encode('utf-8')), mode)
        if status < 0:
            raise VSCANException(f"<Error> Can't open CAN: status = {status}({self.get_error_string(status)})")
        print('CAN device opened.')
        return status

    # Close CAN device. Ur Cap.
    def close(self):
        status = VSCAN_ERR_OK  # VSCAN_Close(self.can_descr)
        if status != VSCAN_ERR_OK:
            raise VSCANException(f"<Error> close: status = {status}({self.get_error_string(status)})")
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
            raise VSCANException(f"<Error> set_speed: status = {status}({self.get_error_string(status)})")
        # return - redundant?

    # Write CAN message
    def write_mes(self, mes, flush=True):
        written = DWORD(0)
        status = VSCAN_Write(self.can_descr, ctypes.pointer(mes), 1, ctypes.pointer(written))
        print(f"can_write_mes status = {status}, Written = {written.value}")
        if status != VSCAN_ERR_OK:
            raise VSCANException(f"<Error> write_mes: status = {status}({self.get_error_string(status)})")
        if written.value != 1:
            raise VSCANException(
                f"<Error> write_mes: some thing wrong with trancieved written.value ({written.value}) != 1 ")

        if flush:
            self.flush()
        return written.value

    @staticmethod
    def form_message(frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0):
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
                raise VSCANException(f"<Error> Data size == {data_size} > 8. Not valid for CAN")
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
        read = DWORD(0)
        status = VSCAN_Read(self.can_descr, ctypes.pointer(mes), 1, ctypes.pointer(read)) or 0  # fixes todo.
        # if status is None:  # Todo WTF? It return None in success
        #     status = 0

        if status != VSCAN_ERR_OK:
            raise VSCANException(f"<Error> read_mes: status = {status}({self.get_error_string(status)})")

        if read.value == 0:
            mes = None
        elif read.value != 1:
            raise VSCANException(f"<Error> read_mes: something wrong with Readed.value ({read.value}) != 1 != 0")
        return mes

    # Read proxy, message in dict
    def read(self):
        mes = self.read_mes()
        if mes is not None:
            return {"": mes.Id, "Data": list(mes.Data)[:mes.Size]}
        return mes

    def flush(self):
        status = VSCAN_Flush(self.can_descr)
        if status != VSCAN_ERR_OK:
            raise VSCANException(f"<Error> read_mes: status = {status}({self.get_error_string(status)})")
        return status

    @staticmethod
    def get_error_string(status):
        # form error string by status code
        string_buf = (ctypes.c_char * VSCAN_GET_ERROR_MAX_STRINGSIZE)()
        p_string_buf = ctypes.pointer(string_buf)
        VSCAN_GetErrorString(status, p_string_buf, VSCAN_GET_ERROR_MAX_STRINGSIZE)
        return string_buf.value

    # @todo: test this
    def read_mes_s(self):
        test_mes = (VSCAN_MSG * 5)()
        read = DWORD(0)
        status = VSCAN_Read(self.can_descr, ctypes.pointer(test_mes[0]), 1, ctypes.pointer(read))
        mes = test_mes[0]
        print(f"status = {status}, read = {read.value}")
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
        written = DWORD(0)
        test_mes = (VSCAN_MSG * 5)()
        test_mes[0].Id = 0xFF
        test_mes[0].Size = 0x8
        for i in range(8):
            test_mes[0].Data[i] = i
        test_mes[0].Flags = VSCAN_FLAGS_STANDARD
        test_mes[0].Timestamp = 0xFF
        status = VSCAN_Write(self.can_descr, ctypes.pointer(test_mes[0]), 1, ctypes.pointer(written))
        print("status = {status}, Written = {Written.value}")
        return status


# test for VSCAN.get_error_string
def test_get_error_string():
    for i in range(-20, 10):  # noqa: WPS432
        print(f"error_code = {i}. Error string = {VSCAN.get_error_string(i)}")


def can_self_test():
    # test_get_error_string()

    port = PORT_IP
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
    print(f'<{"Error" if status < 0 else "Success"}> Close: status = {status}')


def test_data_transmit():
    VSCAN.print_version()

    port = PORT_IP
    can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)

    counter = 0

    TEST_LENGTH = 1000
    for i in range(0, TEST_LENGTH):
        dlc = (i % 8 + 1) & 0xFF
        fid = (i % 8 + i % 0xFF) & 0xFF
        a_data = []
        for j in range(0, dlc):
            if i < 255:
                tmp_val = i
            elif (i > 255) and (i < 512):
                tmp_val = 255 - i
            else:
                tmp_val = i % 2 + i % 255
            a_data.append((tmp_val + j) & 0xFF)
        # def write(self, frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0):
        can_bus.write(frame_id=fid, data=a_data, data_size=dlc)
        time.sleep(0.1)  # Дождаться получения сообщения
        if counter % 10 == 0:
            print(counter)
        counter += 1

    status = can_bus.close()
    print(f'<{"Error" if status < 0 else "Success"}> Close: status = {status}')


def check_vscan_msg():
    VSCAN.print_version()
    port = PORT_IP
    can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)
    msg = VSCAN.VSCANMessage(VSCAN.VSCANMessage.Functions.WRITE, VSCAN.VSCANMessage.Parameters.MEM, 'DE AD BE EF')
    testid = VSCAN.VSCANId()
    can_bus.write(frame_id=testid, data=msg)
    time.sleep(0.5)  # Дождаться получения сообщения
    mes = can_bus.read_mes()
    print(mes)
    status = can_bus.close()
    if status < 0:
        print(f"<Error> Close: status = {status}")
    else:
        print(f"<Success> Close: status = {status}")


def check_vscan_id():
    VSCAN.print_version()
    some_id = VSCAN.VSCANId()
    print(some_id)


if __name__ == "__main__":
    check_vscan_msg()
