"""
VSCAN Interface for SD IMA BK.
"""
import inspect
import logging
from pprint import pprint
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
    [ word offset | internal offset | group name | bit offset* | field name* | element type ].
    """
    value = None
    element_type = None
    elements = []

    def __init__(self,
                 offset: Optional[int] = None,
                 size_or_list: Optional = None,
                 name: Optional[str] = '',
                 fields=None
                 ):
        Element.element_type = None
        if fields is None:
            fields = []
        self.word_offset = offset
        Element.value = None
        self.size_or_list = size_or_list
        self.name = name
        self.fields = fields
        self.parse_addition()

    def get_type(self):
        if not self.fields and not isinstance(self.size_or_list, list):
            self.element_type = 1
        if self.fields:
            self.element_type = 2
        elif isinstance(self.size_or_list, list):
            self.element_type = 3

    def parse_addition(self):
        self.get_type()
        if self.element_type == 1:
            Element.elements.append((self.word_offset, self.size_or_list, self.name, Element.value, self.element_type))
        elif self.element_type == 2:
            for field in self.fields:
                offset, name = field
                Element.elements.append(
                    (self.word_offset, self.size_or_list, self.name,
                     list(offset) if isinstance(offset, range) else offset, name, Element.value,
                     self.element_type)
                )
        elif self.element_type == 3:
            for field in self.size_or_list:
                Element.elements.append((self.word_offset, field[0], field[1], Element.value, self.element_type))
        return Element.elements


class TableHelper(Element):
    def __init__(self):
        self.size = None
        self.bit_name = None
        self.bit_offset = None
        self.elements = None
        self.word_offset = None

    def parse_element(self, element):
        self.word_offset, self.size, self.name, *other = element
        self.element_type = ''.join(map(str, other)) if len(other) == 1 else other[-1]
        other.pop()
        self.bit_offset, self.bit_name, self.value = '', '', None
        if len(other) == 2:
            self.bit_offset, self.bit_name = other

    def get(self, offset: Optional[int] = None, bit: Optional[int] = None, name: Optional[str] = ''):
        self.elements = Element.elements
        to_ret = []
        for element in self.elements:
            self.parse_element(element)
            if self.word_offset == offset:
                to_ret.append(element)
            if self.element_type == 2 and self.bit_offset == bit and self.word_offset is not None:
                to_ret.append(element)
            if self.name == name:
                to_ret.append(element)
        return to_ret if to_ret is not None else None

    def __setattr__(self, key, value):
        key.value = value


class PMUStatuses(TableHelper):
    Table = [
        Element(0, 4, 'Version'),
        Element(1, 4, 'Power', [
            (0, 'PG_VCC_3V3'),
            (1, 'PG_VCC_GTX_1V8'),
            (2, 'PG_VCC_1V8'),
            (3, 'PG_VCC_1V2'),
            (4, 'CORE_START'),
            (5, 'PG_VTT_DDR'),
            (6, 'PG_VDD_DDR_1V2'),
            (7, 'PG_VCCPS_PLL'),
            (8, 'PG_VMGTAVTT'),
            (9, 'PG_VMGTAVCC'),
            (10, 'PG_MGTRAVCC'),
            (11, 'PG_VPP'),
            (12, 'PG_VCCPSDDR_PLL'),
            (13, 'PG_VCCIO_1V8'),
            (14, 'PS_DONE'),
            (15, 'PS_ERR_OUT'),
            (16, 'BAT_INACTIVE'),
            (17, 'VIP_FAIL'),
            (list(range(19, 32)), 'RESERVED')]),
        Element(2, [(2, 'E_ADC_27V_VOLT'), (2, 'E_ADC_27V_CUR')]),
        Element(3, [(2, 'E_ADC_CAP_VOLT'), (2, 'TOTAL_POWER')]),
        Element(4, [(2, 'ADC_5V_VOLT'), (2, 'ADC_5V_CUR')]),
        Element(8, [(2, 'MEAS_GTX_VOLT'), (2, 'MEAS_GTX_CUR')]),
        Element(9, [(2, 'MEAS_DDR4_VOLT'), (2, 'MEAS_DDR4_CUR')]),
        Element(10, [(2, 'TOTAL_MUEP_POWER'), (2, 'RESERVED')]),
        Element(11, [(1, 'MEAS_VIP_TEMP'), (1, 'E_ADC_VIP_TEMP'), (1, 'E_ADC_LT8210_TEMP'), (1, 'E_ADC_LT8705_TEMP')]),
        Element(12, [(1, 'MEAS_PMU_TEMP'), (1, 'MEAS_MUEP_TEMP'), (1, 'MEAS_MHPO_TEMP'), (1, 'TERMO_PMU_AVBL')]),
        Element(13, [(1, 'MEAS_FPGA_TEMP'), (1, 'MEAS_LTM_1_TEMP'), (1, 'MEAS_LTM_2_TEMP'), (1, 'TERMO_MUEP_AVBL')]),
        Element(14, [(2, 'ADC_CALIBR'), (2, 'E_ADC_CALIBR_1')]),
        Element(15, [(2, 'E_ADC_CALIBR_0'), (2, 'RESERVED'), (4, 'BATTERY_POWER_STATUS')]),
    ]


class MUEPStatuses(TableHelper):
    Table = [
        Element(0, 2, 'StateFlags', [
            (0, 'M_READY'),
            (1, 'M_MUEP_FAULT'),
            (2, 'M_GLOBAL_SMPE_FAULT'),
            (3, 'M_GLOBAL_MHPO_FAULT'),
            (4, 'M_GLOBAL_SSD0_FAULT'),
            (5, 'M_GLOBAL_SSD1_FAULT'),
            (6, 'M_GLOBAL_SATA_FAULT'),
            (7, 'M_GLOBAL_FCRT_FAULT'),

            (8, 'M_PELTIE_ON'),
            (range(9 - 10), 'M_SMPE_INACTIVE'),
            (range(11 - 12), 'M_MHPO_INACTIVE'),
            (13, 'M_TECH_UART_ON'),
            (14, 'M_TECH_ETHERNET_ON'),
            (15, 'RESERVED'),
        ]),
        Element(2, 2, 'WorkStatus', [
            (range(0 - 2), 'M_MODE'),
            (3, 'M_WDT_ON'),
            (4, 'M_MHPO_AVBL'),
            (5, 'M_SMPE_AVBL'),
            (6, 'M_SOFT_CRC_MUEP_ERR'),
            (7, 'M_SOFT_CRC_PMU_ERR'),
            (range(8 - 15), 'M_START_CAUSE'),
        ]),
        Element(4, 4, 'CycleCounter', [(range(0 - 31), 'M_COUNTER_SOFT')]),
        Element(8, 4, 'CycleCounter1', [(range(0 - 31), 'M_COUNTER_STATE')]),
        Element(12, 4, 'ServerTime', [(range(0 - 31), 'TIME')]),
        Element(16, 4, 'MUEPSoftVersion', [(range(0 - 31), 'M_MUEP_SOFT_VER')]),
        Element(20, 4, 'MUEPHwVersion', [(range(0 - 31), 'M_MUEP_HW_VER')]),
        Element(24, 4, 'PMUSoftVersion', [(range(0 - 31), 'M_PMU_SOFT_VER')]),
        Element(28, 4, 'MUEPSoftCRC', [(range(0 - 31), 'M_MUEP_SOFT_CRC')]),
        Element(32, 4, 'MUEPHwCRC', [(range(0 - 31), 'M_MUEP_HW_CRC')]),
        Element(36, 4, 'PMUSoftCRC', [(range(0 - 31), 'M_PMU_SOFT_CRC')]),
        Element(40, 2, 'M_NUM_FC_RT_CONFIG', [(range(0 - 15), 'M_NUM_FC_RT_CONFIG')]),
        Element(42, 2, 'M_VER_FC_RT_CONFIG', [(range(0 - 15), 'M_VER_FC_RT_CONFIG')]),
    ]


val = [[int(value)] for value in range(1, 512)]

pmu = PMUStatuses()

pmu.Table[1] = val[1]
print(pmu.Table[1])
