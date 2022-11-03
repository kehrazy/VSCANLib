"""
VSCAN Interface for SD IMA BK.
"""
import ctypes
import inspect


import logging
import string

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








class VSCANId:
    class MsgUnion(ctypes.Union):
        class Msg(ctypes.Structure):
            _fields_ = [("rci", ctypes.c_int, 2),
                        ("sid", ctypes.c_int, 7),
                        ("sfid", ctypes.c_int, 7),
                        ("p", ctypes.c_int, 1),
                        ("l", ctypes.c_int, 1),
                        ("s", ctypes.c_int, 1),
                        ("client_fid", ctypes.c_int, 7),
                        ("lcc", ctypes.c_int, 3),
                        ]
        
        _fields_ = [
            ('bits', Msg),
            ('id', ctypes.c_int),
        ]

        
    
    def __init__(
            self,
            rci = None,
            sid: Optional[int] = None,
            s_fid: Optional[int] = None,
            p: Optional[int] = None,
            l: Optional[int] = None,
            s: Optional[int] = None,
            c_fid: Optional[int] = None,
            lcc: Optional[int] = None,
    ) -> None:
        sig, init_locals = inspect.signature(self.__init__), locals()
        params = [init_locals[param.name] for param in sig.parameters.values()]
        
        # если в инит засунули 8 null'ов - значит мы хотим сделать тест.
        test_mode = params.count(None) == 8
        if not test_mode and None in params:
            raise SDIMABDKOperationError('Invalid parameters!')
        
        msg = self.MsgUnion()
        msg.bits.rci = rci if not test_mode else 0
        msg.bits.sid = sid if not test_mode else 8
        msg.bits.sfid = s_fid if not test_mode else 120
        msg.bits.p = p if not test_mode else 1
        msg.bits.l = l if not test_mode else 1
        msg.bits.s = s if not test_mode else 1
        msg.bits.client_fid = c_fid if not test_mode else 127
        msg.bits.lcc = lcc if not test_mode else 6

        self.id = msg.id
        self.bits = msg.bits


def test():
    msg = VSCANId(
        rci=0,
        sid=63,
        s_fid=120,
        p=1,
        l=1,
        s=1,
        c_fid=127,
        lcc=6
    )
    print(hex(msg.id))
    print(msg.bits.sid)


test()
