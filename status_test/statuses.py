from ctypes import Structure, c_int


class CustomStructure(Structure):
    def __str__(self):
        new_line = '\n'
        return f'{self.__class__.__name__} statuses:\n' \
               f'{"-" * 10}\n' \
               f'{new_line.join([f"{field[0]}: {str(getattr(self, field[0]))}" for field in self._fields_])}'


class NestedCustomStructure(Structure):
    def __str__(self):
        new_line = '\n     '
        return f'\n     {new_line.join([f"{field[0]}: {getattr(self, field[0])}" for field in self._fields_])}'


class Statuses:
    class PMU(CustomStructure):
        class PowerStatuses(NestedCustomStructure):
            _fields_ = [("PG_VCC_3V3", c_int, 1),
                        ("PG_VCC_GTX_1V8", c_int, 1),
                        ("PG_VCC_1V8", c_int, 1),
                        ("PG_VCC_1V2", c_int, 1),
                        ("CORE_START", c_int, 1),
                        ("PG_VTT_DDR", c_int, 1),
                        ("PG_VDD_DDR_1V2", c_int, 1),
                        ("PG_VCCPS_PLL", c_int, 1),
                        ("PG_VMGTAVTT", c_int, 1),
                        ("PG_VMGTAVCC", c_int, 1),
                        ("PG_MGTRAVCC", c_int, 1),
                        ("PG_VPP", c_int, 1),
                        ("PG_VCCPSDDR_PLL", c_int, 1),
                        ("PG_VCCIO_1V8", c_int, 1),
                        ("PS_DONE", c_int, 1),
                        ("PS_ERR_OUT", c_int, 1),
                        ("BAT_INACTIVE", c_int, 1),
                        ("VIP_FAIL", c_int, 1)]
        
        class TelemetryData(NestedCustomStructure):
            _fields_ = [("E_ADC_27V_VOLT", c_int, 2),
                        ("E_ADC_27V_CUR", c_int, 2),
                        ("E_ADC_CAP_VOLT", c_int, 2),
                        ("TOTAL_POWER", c_int, 2),
                        ("ADC_5V_VOLT", c_int, 2),
                        ("ADC_5V_CUR", c_int, 2),
                        ("ADC_9V_VOLT", c_int, 2),
                        ("ADC_9V_CUR", c_int, 2),
                        ("MEAS_CORE_VOLT", c_int, 2),
                        ("MEAS_CORE_CUR", c_int, 2),
                        ("MEAS_3V3_VOLT", c_int, 2),
                        ("MEAS_3V3_CUR", c_int, 2),
                        ("MEAS_GTX_VOLT", c_int, 2),
                        ("MEAS_GTX_CUR", c_int, 2),
                        ("MEAS_DDR4_VOLT", c_int, 2),
                        ("MEAS_DDR4_CUR", c_int, 2),
                        ("TOTAL_MUEP_POWER", c_int, 2)]
        
        class Temperature(NestedCustomStructure):
            _fields_ = [("MEAS_VIP_TEMP", c_int, 1),
                        ("E_ADC_VIP_TEMP", c_int, 1),
                        ("E_ADC_LT8210_TEMP", c_int, 1),
                        ("E_ADC_LT8705_TEMP", c_int, 1),
                        ("MEAS_PMU_TEMP", c_int, 1),
                        ("MEAS_MUEP_TEMP", c_int, 1),
                        ("MEAS_MHPO_TEMP", c_int, 1),
                        ("TERMO_PMU_AVBL", c_int, 1),
                        ("MEAS_FPGA_TEMP", c_int, 1),
                        ("MEAS_LTM_1_TEMP", c_int, 1),
                        ("MEAS_LTM_2_TEMP", c_int, 1),
                        ("TERMO_MUEP_AVBL", c_int, 1)]
        
        class CalibrationValues(NestedCustomStructure):
            _fields_ = [("ADC_CALIBR", c_int, 2),
                        ("E_ADC_CALIBR_1", c_int, 2),
                        ("E_ADC_CALIBR_0", c_int, 2)]
        
        _pack_ = 1
        _fields_ = [("Version", c_int, 4),
                    ("Power", PowerStatuses),
                    ("Telemetry", TelemetryData),
                    ("Temperature", Temperature),
                    ("Calibration", CalibrationValues)
                    ]
    
    class MUEP(CustomStructure):
        class State(NestedCustomStructure):
            _fields_ = [("M_READY", c_int, 1),
                        ("M_MUEP_FAULT", c_int, 1),
                        ("M_GLOBAL_SMPE_FAULT", c_int, 1),
                        ("M_GLOBAL_MHPO_FAULT", c_int, 1),
                        ("M_GLOBAL_SSD0_FAULT", c_int, 1),
                        ("M_GLOBAL_SSD1_FAULT", c_int, 1),
                        ("M_GLOBAL_SATA_FAULT", c_int, 1),
                        ("M_GLOBAL_FCRT_FAULT", c_int, 1),
                        ("M_PELTIE_ON", c_int, 1),
                        ("M_SMPE_INACTIVE", c_int, 1),
                        ("M_MHPO_INACTIVE", c_int, 1),
                        ("M_TECH_UART_ON", c_int, 1),
                        ("M_TECH_ETHERNET_ON", c_int, 1)]
        
        # @todo: тут нужен юнион.


a = Statuses.PMU()
print(a)
