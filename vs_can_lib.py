# -*- coding: utf-8 -*- #
import ctypes
import time
import queue
from load_lib import vs_can_api

port_ip = "10.7.6.70:2001"
# port_ip = "192.168.254.254:2001"

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
VSCAN_MODE_NORMAL = 0  # Обычный режим
VSCAN_MODE_LISTEN_ONLY = 1  # Только просулшивание
VSCAN_MODE_SELF_RECEPTION = 2  # Сам послал сам принял

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
    def __init__(self, port_com, mode, can_speed, emulation=True, emulation_read_mes_queue=queue.Queue(),
                 emulation_write_machine=None):
        """

        :param port_com: IP-адресс:Port или имя виртуального COM-порта
        :param mode: Режим работы см. перечесление Mode
        :param can_speed: Скорость работы см. перечисление Speed
        :param emulation: Эмулировать чтения/записи
        :param emulation_read_mes: Очередь с сообщениями для чтения
        """
        self.emulation = emulation
        self.port_com = port_com
        self.mode = mode
        if emulation:  # Режим эмуляции
            self.mes_for_write = queue.Queue()
            self.mes_for_read = emulation_read_mes_queue
            self.emulation_write_machine = emulation_write_machine
            
            self.open = self.open_emu
            self.close = self.close_emu
            self.set_speed = self.set_speed_emu
            self.write_mes = self.write_mes_emu
            self.read_mes = self.read_mes_emu
            self.flush = self.flush_emu
            
            self.write_s = self.write_s_emu
            self.read_mes_s = self.read_mes_s_emu
            
            # ToDo
            # 1. Почему-то при проверке на закоротке при отправке сразу нескольких сообщений при чтении появляются лишние дублирующие сообщения
            # 2. На будущее реализовать вызов VSCAN_IOCTL_SET_KEEPALIVE, если потребуется делать сервер, чтобы востоянно поддерживать связь с NetCan
        
        self.can_descr = self.open(self.port_com, self.mode)
        self.set_speed(can_speed)
    
    def GetDescr(self):
        return self.can_descr
    
    # Open CAN Device
    def open(self, port_com, mode):
        status = VSCAN_Open(ctypes.c_char_p(port_com.encode('utf-8')), mode)
        if status < 0:
            raise VSCANException(
                "<Error> Can't open CAN: status = {}({})".format(status, self.get_error_string(status)))
        return status
    
    def open_emu(self, port_com, mode):
        """
        Виртуальная функция открытия NetCAN
        :param port_com:
        :param mode:
        :return:
        """
        print("open_emu port_com = {}, mode = {}".format(port_com, mode))
        return VSCAN_ERR_OK
    
    # Close CAN device. Ur Cap.
    def close(self):
        status = VSCAN_Close(self.can_descr)
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> close: status = {}({})".format(status, self.get_error_string(status)))
        return status
    
    def close_emu(self):
        """
        Виртуальная функция закрытия NetCAN
        :return:
        """
        print("close_emu")
        return VSCAN_ERR_OK
    
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
        return VSCAN_ERR_OK
    
    def set_speed_emu(self, can_speed):
        """
        Вирттуальная функция
        :return:
        """
        print("set_speed_emu can_speed = {}".format(can_speed))
        return VSCAN_ERR_OK
    
    # Write CAN message
    def write_mes(self, mes, flush=True):
        Written = DWORD(0)
        status = VSCAN_Write(self.can_descr, ctypes.pointer(mes), 1, ctypes.pointer(Written))
        # print("can_write_mes status = {}, Written = {}".format(status, Written.value))
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> write_mes: status = {}({})".format(status, self.get_error_string(status)))
        if Written.value != 1:
            raise VSCANException(
                "<Error> write_mes: some thing wrong with trancieve Written.value ({}) != 1 ".format(Written.value)
            )
        
        if flush:
            self.flush()
        return Written.value
    
    def write_mes_emu(self, mes, flush=True, debug=False):
        """
        Функция эмуляции записи для тестирования внешней логики
        :param mes: записываемое сообщение
        :param flush: скинуть сообщения в шину из буфура
        :return: количество записываемых сообщений
        """
        if debug:
            print("write_mes_emu mes = {}".format(mes))
        self.mes_for_write.put(mes)
        if self.mode == VSCAN_MODE_SELF_RECEPTION:
            self.mes_for_read.put(mes)
        if self.emulation_write_machine:  # Вызывать функцию - реализующие сложные события по записи
            self.emulation_write_machine(self, mes)
        return 1
    
    @staticmethod
    def form_message(frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0):
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
        return mes
    
    # Write proxy. Can message forms inside function
    def write(self, frame_id, data, data_size=None, flags=VSCAN_FLAGS_EXTENDED, timestamp=0, flush=True, debug=False):
        mes = VSCAN_MSG()
        mes = self.form_message(frame_id, data, data_size, flags, timestamp)
        if debug:
            print("CAN write MES: {}".format(mes))
        return self.write_mes(mes, flush)
    
    def write_s(self, message_list, flush=True):
        """
        Отправить список сообщений
        :param message_list: список с сформированными сообщениями типа VSCAN_MES
        :param flush: очищать буфер
        :return:
        """
        
        # _fields_ = [("Id", ctypes.c_uint32), ("Size", ctypes.c_uint8), ("Data", ctypes.c_uint8 * 8),
        #            ("Flags", ctypes.c_uint8), ("Timestamp", ctypes.c_uint16)]
        Written = DWORD(0)
        message_num = len(message_list)
        messages = (VSCAN_MSG * message_num)()
        print("write_s: message_list = {}".format(message_list))
        i = 0
        for m in message_list:
            messages[i].Id = m.Id
            messages[i].Size = m.Size
            messages[i].Data = m.Data
            messages[i].Flags = m.Flags
            messages[i].Timestamp = m.Timestamp
            i += 1
        status = VSCAN_Write(self.can_descr, ctypes.pointer(messages[0]), message_num, ctypes.pointer(Written))
        # print("write_s status = {}, Written = {}".format(status, Written.value))
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> write_s: status = {}({})".format(status, self.get_error_string(status)))
        if Written.value != message_num:
            raise VSCANException(
                "<Error> write_s: some thing wrong with trancieve Written.value ({}) != 1 ".format(Written.value)
            )
        
        if flush:
            self.flush()
        return Written.value
    
    def write_s_emu(self, message_list, flush=True, debug=False):
        """
        Функция эмуляция записи многих сообщений
        :param message_list: список с сообщениями типа VSCAN_MES
        :param flush:
        :return:
        """
        if debug:
            print("write_mes_emu mes = {}".format(message_list))
        for mes in message_list:
            self.mes_for_write.put(mes)
            if self.mode == VSCAN_MODE_SELF_RECEPTION:
                self.mes_for_read.put(mes)
            if self.emulation_write_machine:  # Вызывать функцию - реализующие сложные события по записи
                self.emulation_write_machine(self, mes)
        
        return len(message_list)
    
    # Read proxy, message in dict
    def read(self):
        mes = self.read_mes()
        if mes != None:
            return {"": mes.Id, "Data": list(mes.Data)[:mes.Size]}
        return mes
    
    # Read message
    def read_mes(self, client_fid: int = None):
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
        
        if client_fid is None:
            return mes
        else:
            if mes.Id & (client_fid << 18) == client_fid << 18: # если сообщение с нашим client fid,
                return mes # возвращаем наше сообщение
            else:
                mes = None # сообщение не наше, и работать с ним не нужно
                return mes
    
    def read_mes_emu(self, debug=False):
        """
        Функция виртуального чтения из CAN шины. Возвращает сообщение из очереди
        :return:
        """
        try:
            mes = self.mes_for_read.get(block=False)
        except queue.Empty:
            mes = None
        if debug:
            print("read_mes_emu mes = {}".format(mes))
        return mes
    
    def read_mes_s(self, mes_num, debug=False):
        """
        Функция единовременного получения списка из сообщений
        :param mes_num: Количество ожидаемых сообщений
        :return: список полученных сообщений
        """
        messages = (VSCAN_MSG * mes_num)()
        Readed = DWORD(0)
        status = VSCAN_Read(self.can_descr, ctypes.pointer(messages[0]), mes_num, ctypes.pointer(Readed))
        if status is None:  # Todo WTF? It return None in success
            status = 0
        
        if debug:
            print("read_mes_s: status = {}, Readed = {}".format(status, Readed.value, messages))
        
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> read_mes_s: status = {}({})".format(status, self.get_error_string(status)))
        
        if Readed.value == 0:
            messages_list = None
        else:
            messages_list = list(messages[:Readed.value])
        
        return messages_list
    
    def read_mes_s_emu(self, mes_num, debug=False):
        """
        Функция-эмулятор единовременного получения списка из сообщений
        :param mes_num: Количество ожидаемых сообщений
        :return: список полученных сообщений
        """
        messages_list = []
        for i in range(mes_num):
            try:
                mes = self.mes_for_read.get(block=False)
                messages_list.append(mes)
            except queue.Empty:
                break
            
            if debug:
                print("read_mes_s_emu mes = {}".format(mes))
        
        if len(messages_list) == 0:
            return None
        
        return messages_list
    
    def flush(self):
        status = VSCAN_Flush(self.can_descr)
        if status != VSCAN_ERR_OK:
            raise VSCANException("<Error> read_mes: status = {}({})".format(status, self.get_error_string(status)))
        return status
    
    def flush_emu(self):
        print("flush_emu")
        return VSCAN_ERR_OK
    
    @staticmethod
    def get_error_string(status):
        # Form error string by status code
        string_buf = (ctypes.c_char * VSCAN_GET_ERROR_MAX_STRINGSIZE)()
        p_string_buf = ctypes.pointer(string_buf)
        VSCAN_GetErrorString(status, p_string_buf, VSCAN_GET_ERROR_MAX_STRINGSIZE)
        return string_buf.value


# test for VSCAN.get_error_string
def test_get_error_string():
    for i in range(-20, 10):  # noqa: WPS432
        print("error_code = {}. Error string = {}".format(i, VSCAN.get_error_string(i)))


def can_self_test():
    test_get_error_string()
    
    version = VSCAN.get_api_version()
    print("VSCAN-API Version {}.{}.{}".format(version.Major, version.Minor, version.SubMinor))
    
    port = port_ip
    can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)
    
    # Write some messages
    #can_bus.write(frame_id=0xFF, data=[1, 2, 3, 4, 5, 8])  # noqa: WPS432
    
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


def self_test():
    version = VSCAN.get_api_version()
    print("VSCAN-API Version {}.{}.{}".format(version.Major, version.Minor, version.SubMinor))
    
    port = port_ip
    can_bus = VSCAN(port, VSCAN_MODE_SELF_RECEPTION, VSCAN_SPEED_1M)
    can_bus.write(
        [b'\x01\x00', b'\x01\x00\x00\x00\x00\x00\x00', b'y\x00\x00\x00\x00\x00\x00', b'\x01', b'\x01', b'\x01',
         b'y\x00\x00\x00\x00\x00\x00', b'\x06\x00\x00', b'\x00\x00'],
        data=['00 0a 00 00 00'.split(' ')],
        data_size=len(['00 0a 00 00 00'.split(' ')])
    )
    time.sleep(0.2)
    mes = can_bus.read()
    print(mes)
    status = can_bus.close()
    if status < 0:
        print("<Error> Close: status = {}".format(status))
    else:
        print("<Success> Close: status = {}".format(status))


if __name__ == "__main__":
    self_test()
