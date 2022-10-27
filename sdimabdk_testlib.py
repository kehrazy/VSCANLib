"""
VSCAN Interface for SD IMA BK.
"""
import ctypes
import inspect
import logging
import string
import struct
from pprint import pprint
from enum import Enum
from typing import Any, Optional

import vs_can_lib
from vs_can_lib import VSCANException

class SDIMABDKError(Exception):
	"""
    A custom exception class.
    """
	
	def __init__(
			self,
			message: str = "",
			error_code: Optional[int] = None,
	) -> None:
		self.error_code = error_code
		super().__init__(
			message if error_code is None else f"[code: {error_code}] {message}"
		)


class SDIMABDKOperationError(SDIMABDKError):
	"""
    This class is used to raise an error when an operation is not supported by the SDIMABDK Library.
    """
	pass


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
												   Functions.WRITE: [Parameters.MEM, Parameters.I2C, Parameters.SPI],
												   Functions.SET: [Parameters.PIN], Functions.RESET: [Parameters.PIN]}
	
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
		#if self.request:
			def form_instruction_byte(func, param, addr):
				# byte =    hex(function)         +              hex(parameter << 4)
				return addr | (func + (param << 4) << addr.bit_length())
			a = []
			print(f'param: {self.parameter.value}')
			print(f'func: {self.function.value}')
			print(f'addr: {hex(self.request)}')
			a.append(self.function.value + (self.parameter.value << 4))
			print(f'instruction byte: {hex(a[0])}')
			for i in list(self.request.to_bytes((self.request.bit_length() + 7) // 8, 'little'))[::-1]:
				a.append(i)
			
			print('full instruction:',' '.join(hex(i) for i in a))
			return a
			# - Бэрримор, что у меня хлюпает в реквесте?
			# - [None, ''], сэр!
			# - [None, '']?! Что они там делают?!
			# - Хлюпают, сэр...
		#raise VSCANException('<Error> form_data: invalid request!')
	
	def __init__(self, function, parameter, request):
		self.function = function
		self.parameter = parameter
		self.request = request
		self.message = self.form_message()
	

class VSCANId:
	class MessageStructure(Enum):
		BUS_NUMBER = (0, 2, 1)
		SERVER_ID = (1, 7, 1)
		SERVER_FUNC_ID = (8, 7, 121)
		PRIVACY = (15, 1, 1)
		LOCAL_BUS = (16, 1, 1)
		MSG_TYPE = (17, 1, 1)
		CLIENT_FUNC_ID = (18, 7, 121)
		LOGICAL_CHANNEL_NUM = (25, 3, 6)
		UNK = (28, 3, 0)
	def __init__(
			self,
			rci: Optional[int] = None,
			sid: Optional[int] = None,
			s_fid: Optional[int] = None,
			p: Optional[int] = None,
			local_bus: Optional[int] = None,
			msg_type: Optional[int] = None,
			c_fid: Optional[int] = None,
			lcc: Optional[int] = None,
	) -> None:

		sig, init_locals = inspect.signature(self.__init__), locals()
		params = [init_locals[param.name] for param in sig.parameters.values()]
		
		# если в инит засунули 8 null'ов - значит мы хотим сделать тест.
		test_mode = params.count(None) == 8
		if not test_mode and None in params:
			raise SDIMABDKOperationError('Invalid parameters!')
		
		self.message_id = 0x0
		
		# read information about the msgid from __MESSAGE_STRUCTURE class.
		for bit in self.MessageStructure:
			bit_pos, _bit_count, test_val = bit.value
			print(f'{bin(test_val)[2:]}({test_val})@{bit_pos}')
			self.message_id = self.message_id | (test_val << bit_pos)
			print(f'{"".join([str(x).ljust(1) for x in bin(self.message_id)[2:].zfill(32)])}')
		
		print(f'python bin: {bin(self.message_id)}')
		self.message_id = ctypes.c_uint32(self.message_id).value
	
	def test_bit(self):
		mask = 1 << 18
		return self.message_id & mask
		
	def __str__(self):
		return str(self.message_id)
def test():
	print(VSCANMessage(VSCANMessage.Functions.READ,VSCANMessage.Parameters.MEM,0xDEADBEEF).message)
	#print(f'uint32_t: {VSCANId()}')
test()
