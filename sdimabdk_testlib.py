"""
VSCAN Interface for SD IMA BK.
"""

from typing import Type, Any, Optional, Tuple
from enum import Enum
import inspect
from contextlib import contextmanager

import copy
import sys
import io
import time
import logging

if sys.version_info >= (3, 9):
    from collections.abc import Generator
else:
    from typing import Generator

logger = logging.getLogger(__name__)

try:
    import vs_can_lib
except ImportError:
    logger.warning(
        "You can't use this back-end without the vs_can_lib module."
    )
    serial = None

class SDIMABDKError(Exception):
    """Base class for all CAN related exceptions.
    If specified, the error code is automatically appended to the message:
    >>> # With an error code (it also works with a specific error):
    >>> error = SDIMABDKError(message="Failed to do the thing", error_code=42)
    >>> str(error)
    'Failed to do the thing [Error Code 42]'
    >>>
    >>> # Missing the error code:
    >>> plain_error = SDIMABDKError(message="Something went wrong ...")
    >>> str(plain_error)
    'Something went wrong ...'
    :param error_code:
        An optional error code to narrow down the cause of the fault
    :arg error_code:
        An optional error code to narrow down the cause of the fault
    """

    def __init__(
        self,
        message: str = "",
        error_code: Optional[int] = None,
    ) -> None:
        self.error_code = error_code
        super().__init__(
            message if error_code is None else f"{message} [code: {error_code}]"
        )

class SDIMABDKOperationError(Exception):
    """
    Indicates that SDIMABDK encountered an error while operating.
    """
    pass

@contextmanager
def error_check(
    error_message: Optional[str] = None,
    exception_type: Type[SDIMABDKError] = SDIMABDKOperationError,
) -> Generator[None, None, None]:
    """Catches any exceptions and turns them into the new type while preserving the stack trace."""
    try:
        yield
    except Exception as error:  # pylint: disable=broad-except
        if error_message is None:
            raise exception_type(str(error)) from error
        else:
            raise exception_type(error_message) from error



class SDIMABDKBus:
    """
    SD IMA BK bus.
    """

    # the message structure with the bit position and the amount of bits.
    class __MESSAGE_STRUCTURE(Enum):
        RCI = (0, 2)
        SID = (1, 7)
        S_FID = (2, 7)
        P = (3, 1)
        L = (4, 1)
        S = (5, 1)
        FID = (6, 7)
        LCC = (7, 3)
        UNK = (8, 3)

    _REPLY = 0
    _REQUEST = 1

    _FID_IDS = {
        'MFC': 0,
        'IMA': 15,
        'TEST': 121,
        'UTDS': 126,
        'TTM': 127
    }

    _RCI_VALUES = {
        'RCI_FIRST': 1,
        'RCI_SECOND': 2,
    }

    _SID_VALUES = {
        'REPLY': 0,
        'REQUEST': 1,
    }


    class Status():
        LCC = 2  # #define STATUS_LCC    	  NOC_LCC
        FID = 120  # функция ПМУ
        TEST = 121

    class LCC():
        EEC = 0  # исключительное событие
        NOC = 2  # нормальная операция
        NSC = 4  # сервис шины
        UDC = 5  # пользовательский канал
        TMC = 6  # тестирование и поддержка
        FMC = 7  # канал миграции

    class FID():
        MFC = 0  # Multicast Function Code ID
        IMA = 15  # Integral Modular Avionics
        TEST = 121
        UTDS = 126  # Upload Target or Download Source
        TTM = 127  # Temporary Test and Maintenance

    class ID_POS():
        RCI = 0
        SID = 2
        S_FID = 9
        P = 16
        L = 17
        S = 18
        R = 18
        C_FID = 19
        LCC = 26

    class MessageType():
        CLIENT = 1
        SERVER = 0

    class Privacy():
        value = 1

    class LocalBus():
        value = 1

    @staticmethod
    def make_bits(
            count: Optional[int] = 1,
            value: Optional[Any] = None
    ) -> bytes:
        """
        `make_bits` takes an integer `count` and a value and returns a list of `count` copies of `value`
        :param count: The number of bits to make
        :type count: Optional[int]
        :param value: The value to be repeated
        :type value: Optional[Any]
        """
        return bytes(value.to_bytes(count, byteorder='little'))


    def __init__(
            self,
            rci: Optional[str] = None,
            sid: Optional[str] = None,
            s_fid: Optional[str] = None,
            p: Optional[str] = None,
            l: Optional[str] = None,
            s: Optional[str] = None,
            c_fid: Optional[str] = None,
            lcc: Optional[str] = None,
            *args: Any,
    ) -> None:
        """
        :param str rci:
             идентификатор резервирования канала
        :param sid:
            идентификатор модуля сервера
        :param s_fid:
            идентификатор функции сервера
        :param p:
            приватность, всегда 1
        :param l:
            локальная шина, всегда 1
        :param s:
            тип сообщения, клиент/запрос - 1, сервер/ответ - 0
        :param c_fid:
            идентификатор функции клиента.
        :param lcc:
            номер логического коммуникационного канала.

        :raise ValueError: if any of the options are invalid
        :raise VSCANError: API Error.

        Leave initializer empty to make a test connection.
        """
        if len([x for x in locals().values()
                if (not callable(x)) and
                (not isinstance(x, SDIMABDKBus)) and
                (x is not None)]) != len(args):

                raise SDIMABDKOperationError('Arguments provided are None or not valid.')

        if vs_can_lib is None:
            raise ImportError('The VSCAN Library is not installed.')











SDIMABDKBus('1','2','3','4')
