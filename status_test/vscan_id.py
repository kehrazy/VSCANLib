import ctypes
import inspect
from dataclasses import dataclass, fields
from typing import Optional


# @note: @i.fedenko - a better class for handling exceptions?
class VSCANIdError(Exception):
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


class VSCANIdOperationError(VSCANIdError):
    """
    This class is used to raise an error when an operation is not supported by the SDIMABDK Library.
    """


@dataclass
class VSCANIdParams:
    """
    Структура, передающаяся в VSCANId().
    rci: номер шины
    sid: идентификатор сервера
    s_fid: идентификатор функции сервера
    p: приватность (всегда 1)
    l: локальная шина (всегда 1)
    s: тип сообщения
    c_fid: идентификатор функции клиента
    lcc: номер логического коммуникационного канала
    """
    rci: int
    sid: int
    s_fid: int
    p: int
    l: int
    s: int
    c_fid: int
    lcc: int


class VSCANId:
    """This class represents the VSCAN message ID.
    Attributes:
        self.id (int): The number, representing the VSCAN message ID.
        self.msg (Msg): An attribute, holding all the field values of the id attribute above.
    """
    
    class MsgUnion(ctypes.Union):
        """
        Класс MsgUnion используется для создания числа 'id', передающемуся в VSCANLib.
        """
        
        class Msg(ctypes.Structure):
            """
            Этот субкласс держит в себе структуру ID сообщения VSCAN.
            """
            _fields_ = [("rci", ctypes.c_int, 2),
                        ("sid", ctypes.c_int, 7),
                        ("sfid", ctypes.c_int, 7),
                        ("p", ctypes.c_int, 1),
                        ("l", ctypes.c_int, 1),
                        ("s", ctypes.c_int, 1),
                        ("client_fid", ctypes.c_int, 7),
                        ("lcc", ctypes.c_int, 3)]
        
        _fields_ = [
            ('bits', Msg),
            ('id', ctypes.c_int),
        ]
    
    def __init__(
            self,
            id_params: VSCANIdParams = None,
            test_mode: bool = False
    ) -> None:
        # создадим юнион со структурой айдишника,
        union = self.MsgUnion()
        # и забьём в него наши данные.
        union.bits.rci = id_params.rci if not test_mode else 0
        union.bits.sid = id_params.sid if not test_mode else 8
        union.bits.sfid = id_params.s_fid if not test_mode else 120
        union.bits.p = id_params.p if not test_mode else 1
        union.bits.l = id_params.l if not test_mode else 1
        union.bits.s = id_params.s if not test_mode else 1
        union.bits.client_fid = id_params.c_fid if not test_mode else 127
        union.bits.lcc = id_params.lcc if not test_mode else 6
        # вернём аттрибуты id и bits.
        self.id = union.id
        self.bits = union.bits


msg = VSCANId(
    VSCANIdParams(
        rci=0,
        sid=63,
        s_fid=120,
        p=1,
        l=1,
        s=1,
        c_fid=127,
        lcc=6
    )
)

test_msg = VSCANId(test_mode=True)
print(hex(msg.id))
print(msg.bits.sid)
