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
            message if error_code is None else f"[code: {error_code}] {message}"
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
            local_bus: Optional[int] = None,
            msg_type: Optional[int] = None,
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
        :param local_bus:
            локальная шина, всегда 1
        :param msg_type:
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
            at, bit_count, test_val = bit.value
            self.message_id.insert(at, self.make_bits(bit_count, test_val if test_mode else params[at - 1]))
        self.message_id[8] = None

    def __repr__(self):
        return ''.join([f'{str(f"{bit.name} [{bit.value[0]}]").ljust(10, " ")}: '
                        f'{self.message_id[bit.value[0]]}\n'
                        for bit in self.MessageStructure])


class Element:
    """
    An element class for PMUStatus table.
    """

    def __init__(
            self,
            offset,
            size,
            fields: Optional[list[str, int]] = None
    ):
        __offsets = []
        self._offset = offset
        if type(size) == list:
            self._elements = []
            for _, val in enumerate(size):
                # _ - индекс, val[1] - поле, val[0] - размер области
                self._elements.insert(_, val[1])
                __offsets.insert(_, val[0])
            self._elements = list(zip(__offsets, self._elements))
        else:
            self._elements = list(zip(range(size), [[None for _ in range(8)] for _ in range(size)]))
        if fields is not None:
            self._elements = [[None for _ in range(8)] for _ in range(size)]
            for idx, el in enumerate(list(fields)):
                # idx - index, el[0] - поле, el[1] - номер бита
                if not type(el[1]) == list:
                    a, b = divmod(int(el[1]), 8)
                    # print(self._elements[a][1])
                    self._elements[a][b] = el[0]
                    __offsets.insert(int(el[1]), el[1])
                else:
                    # el[1] - range.
                    for i in el[1]:
                        a, b = divmod(int(i), 8)
                        self._elements[a][b] = el[0]
                        __offsets.insert(int(i), i)
            self._elements = list(zip(__offsets, self._elements))

    def elements(self):
        return self._elements


class PMUStatuses:
    Version = Element(0, 4)
    Power = Element(1, 4, [
        ('PG_VCC_3V3', 0),
        ('PG_VCC_GTX_1V8', 1),
        ('PG_VCC_1V8', 2),
        ('PG_VCC_1V2', 3),
        ('CORE_START', 4),
        ('PG_VTT_DDR', 5),
        ('PG_VDD_DDR_1V2', 6),
        ('PG_VCCPS_PLL', 7),
        ('PG_VMGTAVTT', 8),
        ('PG_VMGTAVCC', 9),
        ('PG_MGTRAVCC', 10),
        ('PG_VPP', 11),
        ('PG_VCCPSDDR_PLL', 12),
        ('PG_VCCIO_1V8', 13),
        ('PS_DONE', 14),
        ('PS_ERR_OUT', 15),
        ('BAT_INACTIVE', 16),
        ('VIP_FAIL', 17),
        ('RESERVED', list(range(19, 32)))
    ])

    TelemetricData = [
        Element(2, [(2, 'E_ADC_27V_VOLT'), (2, 'E_ADC_27V_CUR')]),
        Element(3, [(2, 'E_ADC_CAP_VOLT'), (2, 'TOTAL_POWER')]),
        Element(4, [(2, 'ADC_5V_VOLT'), (2, 'ADC_5V_CUR')]),
        Element(5, [(2, 'ADC_9V_VOLT'), (2, 'ADC_9V_CUR')]),
        Element(6, [(2, 'MEAS_CORE_VOLT'), (2, 'MEAS_CORE_CUR')]),
        Element(7, [(2, 'MEAS_3V3_VOLT'), (2, 'MEAS_3V3_CUR')]),
        Element(8, [(2, 'MEAS_GTX_VOLT'), (2, 'MEAS_GTX_CUR')]),
        Element(9, [(2, 'MEAS_DDR4_VOLT'), (2, 'MEAS_DDR4_CUR')]),
        Element(10, [(2, 'TOTAL_MUEP_POWER'), (2, 'RESERVED')]),
    ]

    Temperature = [
        Element(11, [(1, 'MEAS_VIP_TEMP'), (1, 'E_ADC_VIP_TEMP'), (1, 'E_ADC_LT8210_TEMP'), (1, 'E_ADC_LT8705_TEMP')]),
        Element(12, [(1, 'MEAS_PMU_TEMP'), (1, 'MEAS_MUEP_TEMP'), (1, 'MEAS_MHPO_TEMP'), (1, 'TERMO_PMU_AVBL')]),
        Element(13, [(1, 'MEAS_FPGA_TEMP'), (1, 'MEAS_LTM_1_TEMP'), (1, 'MEAS_LTM_2_TEMP'), (1, 'TERMO_MUEP_AVBL')]),
    ]

    CalibrationValues = [
        Element(14, [(2, 'ADC_CALIBR'), (2, 'E_ADC_CALIBR_1')]),
        Element(15, [(2, 'E_ADC_CALIBR_0'), (2, 'RESERVED'), (4, 'BATTERY_POWER_STATUS')]),
    ]


s = PMUStatuses

print(s.Temperature[2].elements())
