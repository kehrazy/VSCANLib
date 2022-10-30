"""
VSCAN Interface for SD IMA BK.
"""
import ctypes
import inspect
from bifield import Bitfield

import logging
import string

from pprint import pprint
from enum import Enum
from typing import Any, Optional

import vs_can_lib
from bits import Bits
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


class Msg(ctypes.Structure):
    _fields_ = [("rci", ctypes.c_int, 2),
                ("sid", ctypes.c_int, 7),
                ("sfid", ctypes.c_int, 7),
                ("p", ctypes.c_int, 1),
                ("l", ctypes.c_int, 1),
                ("s", ctypes.c_int, 1),
                ("client_fid", ctypes.c_int, 7),
                ("lcc", ctypes.c_int, 3),
                ("pad", ctypes.c_int, 3)]


class MsgUnion(ctypes.Union):
    _fields_ = [
        ('bits', Msg),
        ('id', ctypes.c_int),
    ]


class VSCANId:
    
    # class MessageStructure(Enum):
    #     BUS_NUMBER = (0, 1, 1)
    #     SERVER_ID = (2, 7, 1)
    #     SERVER_FUNC_ID = (15, 1, 121)
    #     PRIVACY = (16, 1, 1)
    #     LOCAL_BUS = (17, 1, 1)
    #     MSG_TYPE = (18, 1, 1)
    #     CLIENT_FUNC_ID = (19, 7, 121)
    #     LOGICAL_CHANNEL_NUM = (26, 2, 6)
    #     UNK = (28, 3, 0)v
    
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
        # test output should be 0x1bfff020 [11011111111111111000000100000]
        # for bit in self.MessageStructure:
        #     pos, count, val = bit.value
        #     self.message_id |= val << pos
        #     print(f'{hex(self.message_id)}: {bin(self.message_id)}')
        # print(f'{bin(0x1BFFF020)[2:]}')
        # self.message_id = (int(bin(self.message_id), 2) | int(bin((test_val << bit_pos)), 2))
        # print(f'{"".join([str(x).ljust(1) for x in bin(self.message_id)[2:]])}')
        # print(' ' * bit_pos + '^')
        # print(' ' * bit_pos + f'{bin(test_val)[2:]}({test_val})@{bit_pos}')
        # Todo: this
        # test = MsgUnion()
        # print(ctypes.sizeof(Msg))
        # test.bits.rci = 5
        # test.bits.sid = 8
        # test.bits.sfid = 120
        # test.bits.p = 1
        # test.bits.l = 1
        # test.bits.s = 1
        # test.bits.cfid = 127
        # test.bits.lcc = 6
        # test.bits.pad = 0
        # print(hex(test.id))
        a = Bits(0xFFFFFFF)
        a[0:1] = 1
        a[1:8] = 8
        a[8:15] = 120
        a[16] = 1
        a[17] = 1
        a[18] = 1
        a[18:25] = 127
        a[25:28] = 6
        print(hex(a))
        # test = MsgUnion()
        # test.bits.rci = 0
        # test.bits.sid = 112
        # test.bits.sfid = 127
        # test.bits.p = 1
        # test.bits.l = 1
        # test.bits.s = 1
        # test.bits.client_fid = 0
        # test.bits.lcc = 0
        # print(hex(test.id))
        
        # test = MsgUnion()
        # test.id = 0x1bfff020
        # print(test.bits.rci)
        # print(test.bits.sid)
        # print(test.bits.sfid)
        # print(test.bits.p)
        # print(test.bits.l)
        # print(test.bits.s)
        # print(test.bits.client_fid)
        # print(test.bits.lcc)
        
        # print('-'*25 + '\n')
        # print(f'{bin(self.message_id)[2:]}')
        # self.message_id = ctypes.c_uint32(self.message_id).value
    
    def test_bit(self):
        mask = 1 << 18
        return self.message_id & mask
    
    def __str__(self):
        return str(self.message_id)


def test():
    # print(VSCANMessage(VSCANMessage.Functions.READ,VSCANMessage.Parameters.WORD,0x000000).message)
    msg = VSCANId().message_id
    # print(f'my: {len(bin(msg)[2:])} {bin(msg)[2:]}')
    # print(f'og: {(len(bin(0x1BFFF020)[2:]))} {bin(0x1BFFF020)[2:]}')


test()
