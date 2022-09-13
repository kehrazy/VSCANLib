""" used: string.hexdigits """
import string
from enum import Enum
from typing import Dict

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
                raise VSCANException(f'<Error> Invalid request! {byte} is not a hex byte!')

        return True

    def form_message(self) -> str:
        if self.request:
            def form_instruction_byte(func, param):
                # byte =    hex(function)         +              hex(parameter << 4)
                return str(int(f'{func.value:X}') + int(f'{int(bin(param.value << 4), 2):X}')) # переписать
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
        self.expected_response_length = self.get_response_length()
    def __str__(self):
        return f"{'-'*10}\n" \
               f'function: {self.function}\n' \
               f'parameter: {self.parameter}\n' \
               f'request: {self.request}\n' \
               f'message: {self.message}\n' \
               f'is_valid_message: {self.is_valid_message}\n' \
               f'expected_response_length: {self.expected_response_length}' \

def check_test_state_arinc825():
    test_msg = VSCANMessage(VSCANMessage.Functions.WRITE, VSCANMessage.Parameters.MEM, 'DE AD BE EF')
    print(test_msg)

    invalid_msg = VSCANMessage(VSCANMessage.Functions.SET, VSCANMessage.Parameters.PIN, '01 02 03')
    print(invalid_msg)


if __name__ == '__main__':
    check_test_state_arinc825()
