#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some tests for pyindex (currently just very basic tests for interleave.py)"""

import unittest
import interleave

class TestInterleave(unittest.TestCase):

    def test_interleave2(self):
        self.assertEqual(hex(interleave.interleave2(0x00, 0xFF)), '0xaaaa')
        self.assertEqual(hex(interleave.interleave2(0x0000, 0xFFFF)), '0xaaaaaaaa')

    def test_interleave3(self):
        self.assertEqual(hex(interleave.interleave3(0x00, 0xFF, 0x00)), '0x492492')
        self.assertEqual(hex(interleave.interleave3(0x0000, 0xFFFF, 0x0000)), '0x12492492')

    def test_idempotency(self):
        integers = (4, 42)
        interleaved = interleave.interleave2(*integers)
        self.assertEqual(integers, interleave.deinterleave2(interleaved))

    def test_interleave4(self):
        self.assertEqual(
            hex(interleave.interleave4(0x00, 0xFF, 0x00, 0x00)),
            '0x22222222'
            )
        self.assertEqual(
            hex(interleave.interleave4(0x0000, 0xFFFF, 0x0000, 0x0000)),
            '0x2222222222222222'
            )

    def test_part1by3(self):
        self.assertEqual(
            hex(interleave.part1by3(0xFFFF)),
            '0x1111111111111111'
            )

    def test_unpart1by3(self):
        self.assertEqual(
            hex(interleave.unpart1by3(0x1111111111111111)),
            '0xffff'
            )

if __name__ == '__main__':
    unittest.main()
