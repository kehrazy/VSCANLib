from unittest import TestCase
from status_test.vscan_id import VSCANId, VSCANIdParams


class TestVSCANId(TestCase):
    def test_TestVSCANId(self):
        self.assertEqual(VSCANId(test_mode=True).id, 0x1bfff020)
        self.assertEqual(VSCANId(VSCANIdParams(
            rci=0,
            sid=63,
            s_fid=120,
            p=1,
            l=1,
            s=1,
            c_fid=127,
            lcc=6
        )).id, 0x1bfff0fc)
