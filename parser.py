"""
Таблица статусов ПМУ.

Схема работы - таблица["элемент"] -> идём вниз до поля "VALUE".

Длина "VALUE" == 3 - value = [смещение, размер, номер бита].
Длина "VALUE" == 2 - value = [смещение, размер]
"""

pmu_status_table = {
    "VERSION": {
        "VALUE": [0, 4],
    },# Текущая загруженная версия ПО ПМУ. Десятичное число вида: ГГГГММДД.
    "POWER_STATUSES": {
        "PG_VCC_3V3": { "VALUE": [1, 4, 0], },  # Статус корректного питания
        "PG_VCC_GTX_1V8": {
            "VALUE": [1, 4, 1],
        },
        "PG_VCC_1V8": {
            "VALUE": [1, 4, 2],
        },
        "PG_VCC_1V2": {
            "VALUE": [1, 4, 3],
        },
        "CORE_START": {
            "VALUE": [1, 4, 4],
        },
        "PG_VTT_DDR": {
            "VALUE": [1, 4, 5],
        },
        "PG_VDD_DDR_1V2": {
            "VALUE": [1, 4, 6],
        },
        "PG_VCCPS_PLL": {
            "VALUE": [1, 4, 7],
        },
        "PG_VMGTAVTT": {
            "VALUE": [1, 4, 8],
        },
        "PG_VMGTAVCC": {
            "VALUE": [1, 4, 9],
        },
        "PG_MGTRAVCC": {
            "VALUE": [1, 4, 10],
        },
        "PG_VPP": {
            "VALUE": [1, 4, 11],
        },
        "PG_VCCPSDDR_PLL": {
            "VALUE": [1, 4, 12],
        },
        "PG_VCCIO_1V8": {
            "VALUE": [1, 4, 13],
        },
        "PS_DONE": {
            "VALUE": [1, 4, 14],
        },
        "PS_ERR_OUT": {
            "VALUE": [1, 4, 15],
        },
        "BAT_INACTIVE": {
            "VALUE": [1, 4, 16],
        },
        "VIP_FAIL": {
            "VALUE": [1, 4, 17],
        },
        "RESERVED": {
            "VALUE": [1, 4, tuple(range(19, 31))],
        }
    },
    "TELEMETRY_DATA": {
        "E_ADC_27V_VOLT": { "VALUE": [2, 2]},
        "E_ADC_27V_CUR": { "VALUE": [2, 2]},
        "E_ADC_CAP_VOLT": { "VALUE": [3, 2]},
        "TOTAL_POWER": { "VALUE": [3, 2]},
        "ADC_5V_VOLT": { "VALUE": [4, 2]},
        "ADC_5V_CUR": { "VALUE": [4, 2]},
        "ADC_9V_VOLT": { "VALUE": [5, 2]},
        "ADC_9V_CUR": { "VALUE": [5, 2]},
        "MEAS_CORE_VOLT": { "VALUE": [6, 2]},
        "MEAS_CORE_CUR": { "VALUE": [6, 2]},
        "MEAS_3V3_VOLT": { "VALUE": [7, 2]},
        "MEAS_3V3_CUR": { "VALUE": [7, 2]},
        "MEAS_GTX_VOLT": { "VALUE": [8, 2]},
        "MEAS_GTX_CUR": { "VALUE": [8, 2]},
        "MEAS_DDR4_VOLT": { "VALUE": [9, 2]},
        "MEAS_DDR4_CUR": { "VALUE": [9, 2]},
        "TOTAL_MUEP_POWER": { "VALUE": [10, 2]},
        "RESERVED": { "VALUE": [10, 2] }
    },
    "TEMPERATURE": {
        "MEAS_VIP_TEMP": { "VALUE": [11, 1]},
        "E_ADC_VIP_TEMP": { "VALUE": [11, 1]},
        "E_ADC_LT8210_TEMP":{ "VALUE":  [11, 1]},
        "E_ADC_LT8705_TEMP": { "VALUE": [11, 1]},
        "MEAS_PMU_TEMP": { "VALUE": [12, 1]},
        "MEAS_MUEP_TEMP": { "VALUE": [12, 1]},
        "MEAS_MHPO_TEMP": { "VALUE": [12, 1]},
        "TERMO_PMU_AVBL": { "VALUE": [12, 1]},
        "MEAS_FPGA_TEMP": { "VALUE": [13, 1]},
        "MEAS_LTM_1_TEMP": { "VALUE": [13, 1]},
        "MEAS_LTM_2_TEMP": { "VALUE": [13, 1]},
        "TERMO_MUEP_AVBL": { "VALUE": [13, 1]},
    },
    "CALIBRATION_VALUES": {
        "ADC_CALIBR": { "VALUE": [14, 2]},
        "E_ADC_CALIBR_1": { "VALUE": [14, 2]},
        "E_ADC_CALIBR_0": { "VALUE": [15, 2]},
        "RESERVED": { "VALUE": [15, 2]},
    }
}

def parse_by_name(field, subfield = ""):
    working = None
    for a, b in pmu_status_table.items():
        if a == field:
            if len(b) == 1:
                working = b["VALUE"]
            else:
                for key, item in b.items():
                    if key == subfield:
                        working = item["VALUE"]
    offset, size = working
    return offset, size
    
def parse_by_index(offset, size, bit=None):
    working = None
    for a, b in pmu_status_table.items():
        if len(b) == 1:
            working = b["VALUE"]
            w_offset, w_size = working
            if w_offset == offset and w_size == size:
                return a, working
        else:
            for key, item in b.items():
                working = item["VALUE"]
                if len(working) == 2:
                    w_offset, w_size = working
                    if w_offset == offset and w_size == size:
                        return key, working
                elif len(working) == 3:
                    w_offset, w_size, w_bit = working
                    if w_offset == offset and w_size == size and (bit in w_bit if isinstance(w_bit, tuple) else bit == w_bit):
                        return key, working
                
                
print(parse_by_index(1,4,1))
