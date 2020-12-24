# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/tests/test_io.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import binascii, unittest
from django.contrib.gis import memoryview
from django.contrib.gis.geos import GEOSGeometry, WKTReader, WKTWriter, WKBReader, WKBWriter, geos_version_info
from django.utils import six

class GEOSIOTest(unittest.TestCase):

    def test01_wktreader(self):
        wkt_r = WKTReader()
        wkt = b'POINT (5 23)'
        ref = GEOSGeometry(wkt)
        g1 = wkt_r.read(wkt.encode())
        g2 = wkt_r.read(wkt)
        for geom in (g1, g2):
            self.assertEqual(ref, geom)

        self.assertRaises(TypeError, wkt_r.read, 1)
        self.assertRaises(TypeError, wkt_r.read, memoryview(b'foo'))

    def test02_wktwriter(self):
        wkt_w = WKTWriter()
        self.assertRaises(TypeError, wkt_w._set_ptr, WKTReader.ptr_type())
        ref = GEOSGeometry(b'POINT (5 23)')
        ref_wkt = b'POINT (5.0000000000000000 23.0000000000000000)'
        self.assertEqual(ref_wkt, wkt_w.write(ref).decode())

    def test03_wkbreader(self):
        wkb_r = WKBReader()
        hex = b'000000000140140000000000004037000000000000'
        wkb = memoryview(binascii.a2b_hex(hex))
        ref = GEOSGeometry(hex)
        g1 = wkb_r.read(wkb)
        g2 = wkb_r.read(hex)
        for geom in (g1, g2):
            self.assertEqual(ref, geom)

        bad_input = (1, 5.23, None, False)
        for bad_wkb in bad_input:
            self.assertRaises(TypeError, wkb_r.read, bad_wkb)

        return

    def test04_wkbwriter(self):
        wkb_w = WKBWriter()
        g = GEOSGeometry(b'POINT (5 23)')
        hex1 = b'010100000000000000000014400000000000003740'
        wkb1 = memoryview(binascii.a2b_hex(hex1))
        hex2 = b'000000000140140000000000004037000000000000'
        wkb2 = memoryview(binascii.a2b_hex(hex2))
        self.assertEqual(hex1, wkb_w.write_hex(g))
        self.assertEqual(wkb1, wkb_w.write(g))
        for bad_byteorder in (-1, 2, 523, 'foo', None):
            self.assertRaises(ValueError, wkb_w._set_byteorder, bad_byteorder)

        wkb_w.byteorder = 0
        self.assertEqual(hex2, wkb_w.write_hex(g))
        self.assertEqual(wkb2, wkb_w.write(g))
        wkb_w.byteorder = 1
        g = GEOSGeometry(b'POINT (5 23 17)')
        g.srid = 4326
        hex3d = b'0101000080000000000000144000000000000037400000000000003140'
        wkb3d = memoryview(binascii.a2b_hex(hex3d))
        hex3d_srid = b'01010000A0E6100000000000000000144000000000000037400000000000003140'
        wkb3d_srid = memoryview(binascii.a2b_hex(hex3d_srid))
        for bad_outdim in (-1, 0, 1, 4, 423, 'foo', None):
            self.assertRaises(ValueError, wkb_w._set_outdim, bad_outdim)

        if not geos_version_info()[b'version'].startswith(b'3.0.'):
            wkb_w.outdim = 3
            self.assertEqual(hex3d, wkb_w.write_hex(g))
            self.assertEqual(wkb3d, wkb_w.write(g))
            wkb_w.srid = True
            self.assertEqual(hex3d_srid, wkb_w.write_hex(g))
            self.assertEqual(wkb3d_srid, wkb_w.write(g))
        return


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(GEOSIOTest))
    return s


def run(verbosity=2):
    unittest.TextTestRunner(verbosity=verbosity).run(suite())