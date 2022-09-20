"""
VSCAN Interface for SD IMA BK.
"""
import inspect
import logging
from enum import Enum
from typing import Any, Optional

logger = logging.getLogger(__name__)


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
            message if error_code is None else f"{message} [code: {error_code}]"
        )


class SDIMABDKOperationError(SDIMABDKError):
    """
    This class is used to raise an error when an operation is not supported by the SDIMABDK Library.
    """
    pass


class VSCANId:
    """
    SD IMA BK bus.
    """

    # the message structure.
    # element = (pos, bit count, test value)
    class MessageStructure(Enum):
        RCI = (0, 2, 1)
        SID = (1, 7, 1)
        S_FID = (2, 7, 121)
        P = (3, 1, 1)
        L = (4, 1, 1)
        S = (5, 1, 1)
        FID = (6, 7, 121)
        LCC = (7, 3, 6)
        UNK = (8, 3, 0)

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

    @staticmethod
    def make_bits(
            count: Optional[int] = 1,
            value: Optional[Any] = None
    ) -> bytes:
        """
        `make_bits` takes an integer `count` and a value and returns a list of bits
        :param count: The number of bits to make
        :type count: Optional[int]
        :param value: The value to be repeated
        :type value: Optional[Any]
        """
        return bytes(value.to_bytes(count, byteorder='little'), )

    def __init__(
            self,
            rci: Optional[int] = None,
            sid: Optional[int] = None,
            s_fid: Optional[int] = None,
            p: Optional[int] = None,
            l: Optional[int] = None,
            s: Optional[int] = None,
            c_fid: Optional[int] = None,
            lcc: Optional[int] = None,
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

        # magic internal python stuff.
        sig, init_locals = inspect.signature(self.__init__), locals()
        params = [init_locals[param.name] for param in sig.parameters.values()]
        # если в инит засунули 8 null'ов - значит мы хотим сделать тест.
        test_mode = params.count(None) == 8
        if not test_mode and None in params:
            raise SDIMABDKOperationError('Invalid parameters!')

        self.message_id = []

        # read information about the msgid from __MESSAGE_STRUCTURE class.
        for bit in self.MessageStructure:
            id = self.message_id
            at, bit_count, test_val = bit.value
            id.insert(at,
                self.make_bits(bit_count, test_val if test_mode else params[at - 1])
            )

        self.message_id[8] = None

    def __repr__(self):
        return ''.join([f'{str(f"{bit.name} [{bit.value[0]}]").ljust(10, " ")}: '
                        f'{self.message_id[bit.value[0]]}\n'
                        for bit in self.MessageStructure])


#print(VSCANId())


class PSDone(Enum):
    PS_LOADED: 1
    PS_NOT_LOADED: 0


class PSError(Enum):
    PS_NO_ERROR: 0
    PS_ERROR: 1

class VIPStatus(Enum):
    VIP_VALID: 0
    VIP_FAILED: 1

class PowerStatuses(Enum):
    PG_VCC_3V3: 0
    PG_VCC_GTX_1V8: 1
    PG_VCC_1V8: 2
    PG_VCC_1V2: 3
    CORE_START: 4
    PG_VTT_DDR: 5
    PG_VDD_DDR_1V2: 6
    PG_VCCPS_PLL: 7
    PG_VMGTAVTT: 8
    PG_VMGTAVCC: 9
    PG_MGTRAVCC: 10
    PG_VPP: 11
    PG_VCCPSDDR_PLL: 12
    PG_VCCIO_1V8: 13
    PS_DONE: (14, PSDone)
    PS_ERR_OUT: (15, PSError)
    BAT_INACTIVE: 16
    VIP_FAIL: (17, VIPStatus)

# class PMUStatus(Enum):
#     #   ИМЯ    РАЗМЕР, СМЕЩЕНИЕ
#     PMU_VERSION: (0, 4)
#     POWER_STATUS: (1, 4, PowerStatuses)

from dataclasses import dataclass

class StatusElement:
    def __init__(self, offset, size):
        self._offset = offset
        self._size = size

    def set(self, elements: Optional[Any]):
        self._elements = elements

@dataclass
class PMUStatus(object):
    Version: StatusElement(0, 4)
    PowerStatus: StatusElement(1, 4).set(PowerStatuses)

    def __post_init__(self):
        try:
            self.Version = int(self.Version)
        except (ValueError, TypeError):
            # could not convert age to an integer
            self.Version = None

status = PMUStatus()
print(status.Version)