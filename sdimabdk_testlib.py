""" used: string.hexdigits """
import string
from enum import Enum
import pprint
import ctypes

from vs_can_lib import VSCANException


class VSCANMessage:
    class Parameters(Enum):
        MEM = 0
        SPI = 1
        I2C = 2
        ADC = 3
        SYS = 4
        PIN = 5
        WORD = 6

    class Functions(Enum):
        READ = 0
        WRITE = 1
        SET = 2
        RESET = 3

    # возможные сочетания функций и параметров.
    ftp_dict: dict[Functions, list[Parameters]] = {Functions.READ: list(Parameters),
                                                   Functions.WRITE: [Parameters.MEM, Parameters.I2C, Parameters.SPI],
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
        return (self.expected_response_length[self.function])[self.parameter]

    @property
    def verify_message(self) -> bool:
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

            return str(f'{form_instruction_byte(self.function, self.parameter).zfill(2)} {self.request}')  # переделать.

        # - Бэрримор, что у меня хлюпает в реквесте?
        # - [None, ''], сэр!
        # - [None, '']?! Что они там делают?!
        # - Хлюпают, сэр...
        raise VSCANException('<Error> form_data: invalid request!')

    def __init__(self, function: Functions, parameter: Parameters, request: str):
        self.function = function
        self.parameter = parameter
        self.request = request
        self.message = self.form_message()
        self.is_valid_message = self.verify_message

    def __str__(self):
        return f"{'-' * 10}\n" \
               f'function: {self.function}\n' \
               f'parameter: {self.parameter}\n' \
               f'request: {self.request}\n' \
               f'message: {self.message}\n' \
               f'is_valid_message: {self.is_valid_message}\n' \
            # f'expected_response_length: {self.expected_response_length}' \

    def __repr__(self):
        return self.message


class CAN:
    class RCI(Enum):
        RCI_1 = 1
        RCI_2 = 2

    class Status(Enum):
        LCC = 2  # #define STATUS_LCC    	  NOC_LCC
        STATUS_FID = 120  # функция ПМУ

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

# LCC_MASK = (7 << CAN.ID_POS.LCC.value)
# FID_MASK = 0x7F
# RLP_MASK = (7 << CAN.ID_POS.P.value)
# SLP_MASK = (3 << CAN.ID_POS.P.value)


class VSCANId:
    def __init__(self):
        self.message_id = [''] * 9  # list of the message id
        self.rci = self.message_id[0] = CAN.RCI.RCI_1.value  # rci. @doc: RCI_1 - 1, RCI_2 - 2
        self.sid = self.message_id[1] = 1  # sid. @doc:
        self.server_fid = self.message_id[2] = 121  # server_fid /
        self.privacy = self.message_id[3] = 1  # privacy
        self.local_bus = self.message_id[4] = 1  # local_bus
        self.msg_type = self.message_id[5] = 1  # msg_type
        self.client_fid = self.message_id[6] = 121  # client_fid
        self.lcc = self.message_id[7] = CAN.LCC.TMC.value  # lcc
        self.empty = self.message_id[8] = ''  # ?

    def __str__(self):
        return f"{'-' * 10}\n" \
               f'ID: {self.message_id}\n' \
               f'RCI [0-1]: {self.rci}\n' \
               f'SID [2-8]: {self.sid}\n' \
               f'Server FID: {self.server_fid}\n' \
               f'Privacy: {self.privacy}\n' \
               f'Local bus: {self.local_bus}\n' \
               f'Message type: {self.msg_type}\n' \
               f'Client FID: {self.client_fid}\n' \
               f'LCC: {self.lcc}\n' \
               f'empty: {self.empty}\n'

def check_vscan_msg():
    test_msg = VSCANMessage(VSCANMessage.Functions.WRITE, VSCANMessage.Parameters.MEM, 'DE AD BE EF')
    print(test_msg)

    invalid_msg = VSCANMessage(VSCANMessage.Functions.SET, VSCANMessage.Parameters.PIN, '01 02 03')
    print(invalid_msg)


def check_vscan_id():
    test_id = VSCANId()
    print(test_id)


if __name__ == '__main__':
    check_vscan_id()
