# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/tests/test_geos.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import ctypes, json, random
from binascii import a2b_hex, b2a_hex
from io import BytesIO
from django.contrib.gis import memoryview
from django.contrib.gis.geos import GEOSException, GEOSIndexError, GEOSGeometry, GeometryCollection, Point, MultiPoint, Polygon, MultiPolygon, LinearRing, LineString, MultiLineString, fromfile, fromstr, geos_version_info
from django.contrib.gis.geos.base import gdal, numpy, GEOSBase
from django.contrib.gis.geos.libgeos import GEOS_PREPARE
from django.contrib.gis.geometry.test_data import TestDataMixin
from django.utils.encoding import force_bytes
from django.utils import six
from django.utils.six.moves import xrange
from django.utils import unittest

class GEOSTest(unittest.TestCase, TestDataMixin):

    @property
    def null_srid(self):
        """
        Returns the proper null SRID depending on the GEOS version.
        See the comments in `test_srid` for more details.
        """
        info = geos_version_info()
        if info[b'version'] == b'3.0.0' and info[b'release_candidate']:
            return -1
        else:
            return
            return

    def test_base(self):
        """Tests out the GEOSBase class."""

        class FakeGeom1(GEOSBase):
            pass

        c_float_p = ctypes.POINTER(ctypes.c_float)

        class FakeGeom2(GEOSBase):
            ptr_type = c_float_p

        fg1 = FakeGeom1()
        fg2 = FakeGeom2()
        fg1.ptr = ctypes.c_void_p()
        fg1.ptr = None
        fg2.ptr = c_float_p(ctypes.c_float(5.23))
        fg2.ptr = None
        for fg in (fg1, fg2):
            self.assertRaises(GEOSException, fg._get_ptr)

        bad_ptrs = (
         5, ctypes.c_char_p(b'foobar'))
        for bad_ptr in bad_ptrs:
            self.assertRaises(TypeError, fg1._set_ptr, bad_ptr)
            self.assertRaises(TypeError, fg2._set_ptr, bad_ptr)

        return

    def test_wkt(self):
        """Testing WKT output."""
        for g in self.geometries.wkt_out:
            geom = fromstr(g.wkt)
            self.assertEqual(g.ewkt, geom.wkt)

    def test_hex(self):
        """Testing HEX output."""
        for g in self.geometries.hex_wkt:
            geom = fromstr(g.wkt)
            self.assertEqual(g.hex, geom.hex.decode())

    def test_hexewkb(self):
        """Testing (HEX)EWKB output."""
        ogc_hex = b'01010000000000000000000000000000000000F03F'
        ogc_hex_3d = b'01010000800000000000000000000000000000F03F0000000000000040'
        hexewkb_2d = b'0101000020E61000000000000000000000000000000000F03F'
        hexewkb_3d = b'01010000A0E61000000000000000000000000000000000F03F0000000000000040'
        pnt_2d = Point(0, 1, srid=4326)
        pnt_3d = Point(0, 1, 2, srid=4326)
        self.assertEqual(ogc_hex, pnt_2d.hex)
        self.assertEqual(ogc_hex_3d, pnt_3d.hex)
        self.assertEqual(hexewkb_2d, pnt_2d.hexewkb)
        if GEOS_PREPARE:
            self.assertEqual(hexewkb_3d, pnt_3d.hexewkb)
            self.assertEqual(True, GEOSGeometry(hexewkb_3d).hasz)
        else:
            try:
                hexewkb = pnt_3d.hexewkb
            except GEOSException:
                pass
            else:
                self.fail(b'Should have raised GEOSException.')

        self.assertEqual(memoryview(a2b_hex(hexewkb_2d)), pnt_2d.ewkb)
        if GEOS_PREPARE:
            self.assertEqual(memoryview(a2b_hex(hexewkb_3d)), pnt_3d.ewkb)
        else:
            try:
                ewkb = pnt_3d.ewkb
            except GEOSException:
                pass
            else:
                self.fail(b'Should have raised GEOSException')

        self.assertEqual(4326, GEOSGeometry(hexewkb_2d).srid)

    def test_kml(self):
        """Testing KML output."""
        for tg in self.geometries.wkt_out:
            geom = fromstr(tg.wkt)
            kml = getattr(tg, b'kml', False)
            if kml:
                self.assertEqual(kml, geom.kml)

    def test_errors(self):
        """Testing the Error handlers."""
        for err in self.geometries.errors:
            with self.assertRaises((GEOSException, ValueError)):
                _ = fromstr(err.wkt)

        self.assertRaises(GEOSException, GEOSGeometry, memoryview(b'0'))

        class NotAGeometry(object):
            pass

        self.assertRaises(TypeError, GEOSGeometry, NotAGeometry())
        self.assertRaises(TypeError, GEOSGeometry, None)
        return

    def test_wkb(self):
        """Testing WKB output."""
        for g in self.geometries.hex_wkt:
            geom = fromstr(g.wkt)
            wkb = geom.wkb
            self.assertEqual(b2a_hex(wkb).decode().upper(), g.hex)

    def test_create_hex(self):
        """Testing creation from HEX."""
        for g in self.geometries.hex_wkt:
            geom_h = GEOSGeometry(g.hex)
            geom_t = fromstr(g.wkt)
            self.assertEqual(geom_t.wkt, geom_h.wkt)

    def test_create_wkb(self):
        """Testing creation from WKB."""
        for g in self.geometries.hex_wkt:
            wkb = memoryview(a2b_hex(g.hex.encode()))
            geom_h = GEOSGeometry(wkb)
            geom_t = fromstr(g.wkt)
            self.assertEqual(geom_t.wkt, geom_h.wkt)

    def test_ewkt(self):
        """Testing EWKT."""
        srids = (-1, 32140)
        for srid in srids:
            for p in self.geometries.polygons:
                ewkt = b'SRID=%d;%s' % (srid, p.wkt)
                poly = fromstr(ewkt)
                self.assertEqual(srid, poly.srid)
                self.assertEqual(srid, poly.shell.srid)
                self.assertEqual(srid, fromstr(poly.ewkt).srid)

    @unittest.skipUnless(gdal.HAS_GDAL, b'gdal is required')
    def test_json(self):
        """Testing GeoJSON input/output (via GDAL)."""
        for g in self.geometries.json_geoms:
            geom = GEOSGeometry(g.wkt)
            if not hasattr(g, b'not_equal'):
                self.assertEqual(json.loads(g.json), json.loads(geom.json))
                self.assertEqual(json.loads(g.json), json.loads(geom.geojson))
            self.assertEqual(GEOSGeometry(g.wkt), GEOSGeometry(geom.json))

    def test_fromfile(self):
        """Testing the fromfile() factory."""
        ref_pnt = GEOSGeometry(b'POINT(5 23)')
        wkt_f = BytesIO()
        wkt_f.write(force_bytes(ref_pnt.wkt))
        wkb_f = BytesIO()
        wkb_f.write(bytes(ref_pnt.wkb))
        for fh in (wkt_f, wkb_f):
            fh.seek(0)
            pnt = fromfile(fh)
            self.assertEqual(ref_pnt, pnt)

    def test_eq(self):
        """Testing equivalence."""
        p = fromstr(b'POINT(5 23)')
        self.assertEqual(p, p.wkt)
        self.assertNotEqual(p, b'foo')
        ls = fromstr(b'LINESTRING(0 0, 1 1, 5 5)')
        self.assertEqual(ls, ls.wkt)
        self.assertNotEqual(p, b'bar')
        for g in (p, ls):
            self.assertNotEqual(g, None)
            self.assertNotEqual(g, {b'foo': b'bar'})
            self.assertNotEqual(g, False)

        return

    def test_points(self):
        """Testing Point objects."""
        prev = fromstr(b'POINT(0 0)')
        for p in self.geometries.points:
            pnt = fromstr(p.wkt)
            self.assertEqual(pnt.geom_type, b'Point')
            self.assertEqual(pnt.geom_typeid, 0)
            self.assertEqual(p.x, pnt.x)
            self.assertEqual(p.y, pnt.y)
            self.assertEqual(True, pnt == fromstr(p.wkt))
            self.assertEqual(False, pnt == prev)
            self.assertAlmostEqual(p.x, pnt.tuple[0], 9)
            self.assertAlmostEqual(p.y, pnt.tuple[1], 9)
            if hasattr(p, b'z'):
                self.assertEqual(True, pnt.hasz)
                self.assertEqual(p.z, pnt.z)
                self.assertEqual(p.z, pnt.tuple[2], 9)
                tup_args = (p.x, p.y, p.z)
                set_tup1 = (2.71, 3.14, 5.23)
                set_tup2 = (5.23, 2.71, 3.14)
            else:
                self.assertEqual(False, pnt.hasz)
                self.assertEqual(None, pnt.z)
                tup_args = (p.x, p.y)
                set_tup1 = (2.71, 3.14)
                set_tup2 = (3.14, 2.71)
            self.assertEqual(p.centroid, pnt.centroid.tuple)
            pnt2 = Point(tup_args)
            pnt3 = Point(*tup_args)
            self.assertEqual(True, pnt == pnt2)
            self.assertEqual(True, pnt == pnt3)
            pnt.y = 3.14
            pnt.x = 2.71
            self.assertEqual(3.14, pnt.y)
            self.assertEqual(2.71, pnt.x)
            pnt.tuple = set_tup1
            self.assertEqual(set_tup1, pnt.tuple)
            pnt.coords = set_tup2
            self.assertEqual(set_tup2, pnt.coords)
            prev = pnt

        return

    def test_multipoints(self):
        """Testing MultiPoint objects."""
        for mp in self.geometries.multipoints:
            mpnt = fromstr(mp.wkt)
            self.assertEqual(mpnt.geom_type, b'MultiPoint')
            self.assertEqual(mpnt.geom_typeid, 4)
            self.assertAlmostEqual(mp.centroid[0], mpnt.centroid.tuple[0], 9)
            self.assertAlmostEqual(mp.centroid[1], mpnt.centroid.tuple[1], 9)
            self.assertRaises(GEOSIndexError, mpnt.__getitem__, len(mpnt))
            self.assertEqual(mp.centroid, mpnt.centroid.tuple)
            self.assertEqual(mp.coords, tuple(m.tuple for m in mpnt))
            for p in mpnt:
                self.assertEqual(p.geom_type, b'Point')
                self.assertEqual(p.geom_typeid, 0)
                self.assertEqual(p.empty, False)
                self.assertEqual(p.valid, True)

    def test_linestring(self):
        """Testing LineString objects."""
        prev = fromstr(b'POINT(0 0)')
        for l in self.geometries.linestrings:
            ls = fromstr(l.wkt)
            self.assertEqual(ls.geom_type, b'LineString')
            self.assertEqual(ls.geom_typeid, 1)
            self.assertEqual(ls.empty, False)
            self.assertEqual(ls.ring, False)
            if hasattr(l, b'centroid'):
                self.assertEqual(l.centroid, ls.centroid.tuple)
            if hasattr(l, b'tup'):
                self.assertEqual(l.tup, ls.tuple)
            self.assertEqual(True, ls == fromstr(l.wkt))
            self.assertEqual(False, ls == prev)
            self.assertRaises(GEOSIndexError, ls.__getitem__, len(ls))
            prev = ls
            self.assertEqual(ls, LineString(ls.tuple))
            self.assertEqual(ls, LineString(*ls.tuple))
            self.assertEqual(ls, LineString([ list(tup) for tup in ls.tuple ]))
            self.assertEqual(ls.wkt, LineString(*tuple(Point(tup) for tup in ls.tuple)).wkt)
            if numpy:
                self.assertEqual(ls, LineString(numpy.array(ls.tuple)))

    def test_multilinestring(self):
        """Testing MultiLineString objects."""
        prev = fromstr(b'POINT(0 0)')
        for l in self.geometries.multilinestrings:
            ml = fromstr(l.wkt)
            self.assertEqual(ml.geom_type, b'MultiLineString')
            self.assertEqual(ml.geom_typeid, 5)
            self.assertAlmostEqual(l.centroid[0], ml.centroid.x, 9)
            self.assertAlmostEqual(l.centroid[1], ml.centroid.y, 9)
            self.assertEqual(True, ml == fromstr(l.wkt))
            self.assertEqual(False, ml == prev)
            prev = ml
            for ls in ml:
                self.assertEqual(ls.geom_type, b'LineString')
                self.assertEqual(ls.geom_typeid, 1)
                self.assertEqual(ls.empty, False)

            self.assertRaises(GEOSIndexError, ml.__getitem__, len(ml))
            self.assertEqual(ml.wkt, MultiLineString(*tuple(s.clone() for s in ml)).wkt)
            self.assertEqual(ml, MultiLineString(*tuple(LineString(s.tuple) for s in ml)))

    def test_linearring(self):
        """Testing LinearRing objects."""
        for rr in self.geometries.linearrings:
            lr = fromstr(rr.wkt)
            self.assertEqual(lr.geom_type, b'LinearRing')
            self.assertEqual(lr.geom_typeid, 2)
            self.assertEqual(rr.n_p, len(lr))
            self.assertEqual(True, lr.valid)
            self.assertEqual(False, lr.empty)
            self.assertEqual(lr, LinearRing(lr.tuple))
            self.assertEqual(lr, LinearRing(*lr.tuple))
            self.assertEqual(lr, LinearRing([ list(tup) for tup in lr.tuple ]))
            if numpy:
                self.assertEqual(lr, LinearRing(numpy.array(lr.tuple)))

    def test_polygons_from_bbox(self):
        """Testing `from_bbox` class method."""
        bbox = (-180, -90, 180, 90)
        p = Polygon.from_bbox(bbox)
        self.assertEqual(bbox, p.extent)
        x = 3.141592653589793
        bbox = (0, 0, 1, x)
        p = Polygon.from_bbox(bbox)
        y = p.extent[(-1)]
        self.assertEqual(format(x, b'.13f'), format(y, b'.13f'))

    def test_polygons(self):
        """Testing Polygon objects."""
        prev = fromstr(b'POINT(0 0)')
        for p in self.geometries.polygons:
            poly = fromstr(p.wkt)
            self.assertEqual(poly.geom_type, b'Polygon')
            self.assertEqual(poly.geom_typeid, 3)
            self.assertEqual(poly.empty, False)
            self.assertEqual(poly.ring, False)
            self.assertEqual(p.n_i, poly.num_interior_rings)
            self.assertEqual(p.n_i + 1, len(poly))
            self.assertEqual(p.n_p, poly.num_points)
            self.assertAlmostEqual(p.area, poly.area, 9)
            self.assertAlmostEqual(p.centroid[0], poly.centroid.tuple[0], 9)
            self.assertAlmostEqual(p.centroid[1], poly.centroid.tuple[1], 9)
            self.assertEqual(True, poly == fromstr(p.wkt))
            self.assertEqual(False, poly == prev)
            self.assertEqual(True, poly != prev)
            ring = poly.exterior_ring
            self.assertEqual(ring.geom_type, b'LinearRing')
            self.assertEqual(ring.geom_typeid, 2)
            if p.ext_ring_cs:
                self.assertEqual(p.ext_ring_cs, ring.tuple)
                self.assertEqual(p.ext_ring_cs, poly[0].tuple)
            self.assertRaises(GEOSIndexError, poly.__getitem__, len(poly))
            self.assertRaises(GEOSIndexError, poly.__setitem__, len(poly), False)
            self.assertRaises(GEOSIndexError, poly.__getitem__, -1 * len(poly) - 1)
            for r in poly:
                self.assertEqual(r.geom_type, b'LinearRing')
                self.assertEqual(r.geom_typeid, 2)

            self.assertRaises(TypeError, Polygon, 0, [1, 2, 3])
            self.assertRaises(TypeError, Polygon, b'foo')
            rings = tuple(r for r in poly)
            self.assertEqual(poly, Polygon(rings[0], rings[1:]))
            ring_tuples = tuple(r.tuple for r in poly)
            self.assertEqual(poly, Polygon(*ring_tuples))
            self.assertEqual(poly.wkt, Polygon(*tuple(r for r in poly)).wkt)
            self.assertEqual(poly.wkt, Polygon(*tuple(LinearRing(r.tuple) for r in poly)).wkt)

    def test_polygon_comparison(self):
        p1 = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
        p2 = Polygon(((0, 0), (0, 1), (1, 0), (0, 0)))
        self.assertTrue(p1 > p2)
        self.assertFalse(p1 < p2)
        self.assertFalse(p2 > p1)
        self.assertTrue(p2 < p1)
        p3 = Polygon(((0, 0), (0, 1), (1, 1), (2, 0), (0, 0)))
        p4 = Polygon(((0, 0), (0, 1), (2, 2), (1, 0), (0, 0)))
        self.assertFalse(p4 < p3)
        self.assertTrue(p3 < p4)
        self.assertTrue(p4 > p3)
        self.assertFalse(p3 > p4)

    def test_multipolygons(self):
        """Testing MultiPolygon objects."""
        prev = fromstr(b'POINT (0 0)')
        for mp in self.geometries.multipolygons:
            mpoly = fromstr(mp.wkt)
            self.assertEqual(mpoly.geom_type, b'MultiPolygon')
            self.assertEqual(mpoly.geom_typeid, 6)
            self.assertEqual(mp.valid, mpoly.valid)
            if mp.valid:
                self.assertEqual(mp.num_geom, mpoly.num_geom)
                self.assertEqual(mp.n_p, mpoly.num_coords)
                self.assertEqual(mp.num_geom, len(mpoly))
                self.assertRaises(GEOSIndexError, mpoly.__getitem__, len(mpoly))
                for p in mpoly:
                    self.assertEqual(p.geom_type, b'Polygon')
                    self.assertEqual(p.geom_typeid, 3)
                    self.assertEqual(p.valid, True)

                self.assertEqual(mpoly.wkt, MultiPolygon(*tuple(poly.clone() for poly in mpoly)).wkt)

    def test_memory_hijinks(self):
        """Testing Geometry __del__() on rings and polygons."""
        poly = fromstr(self.geometries.polygons[1].wkt)
        ring1 = poly[0]
        ring2 = poly[1]
        del ring1
        del ring2
        ring1 = poly[0]
        ring2 = poly[1]
        del poly
        s1, s2 = str(ring1), str(ring2)

    def test_coord_seq(self):
        """Testing Coordinate Sequence objects."""
        for p in self.geometries.polygons:
            if p.ext_ring_cs:
                poly = fromstr(p.wkt)
                cs = poly.exterior_ring.coord_seq
                self.assertEqual(p.ext_ring_cs, cs.tuple)
                self.assertEqual(len(p.ext_ring_cs), len(cs))
                for i in xrange(len(p.ext_ring_cs)):
                    c1 = p.ext_ring_cs[i]
                    c2 = cs[i]
                    self.assertEqual(c1, c2)
                    if len(c1) == 2:
                        tset = (5, 23)
                    else:
                        tset = (5, 23, 8)
                    cs[i] = tset
                    for j in range(len(tset)):
                        cs[i] = tset
                        self.assertEqual(tset[j], cs[i][j])

    def test_relate_pattern(self):
        """Testing relate() and relate_pattern()."""
        g = fromstr(b'POINT (0 0)')
        self.assertRaises(GEOSException, g.relate_pattern, 0, b'invalid pattern, yo')
        for rg in self.geometries.relate_geoms:
            a = fromstr(rg.wkt_a)
            b = fromstr(rg.wkt_b)
            self.assertEqual(rg.result, a.relate_pattern(b, rg.pattern))
            self.assertEqual(rg.pattern, a.relate(b))

    def test_intersection(self):
        """Testing intersects() and intersection()."""
        for i in xrange(len(self.geometries.topology_geoms)):
            a = fromstr(self.geometries.topology_geoms[i].wkt_a)
            b = fromstr(self.geometries.topology_geoms[i].wkt_b)
            i1 = fromstr(self.geometries.intersect_geoms[i].wkt)
            self.assertEqual(True, a.intersects(b))
            i2 = a.intersection(b)
            self.assertEqual(i1, i2)
            self.assertEqual(i1, a & b)
            a &= b
            self.assertEqual(i1, a)

    def test_union(self):
        """Testing union()."""
        for i in xrange(len(self.geometries.topology_geoms)):
            a = fromstr(self.geometries.topology_geoms[i].wkt_a)
            b = fromstr(self.geometries.topology_geoms[i].wkt_b)
            u1 = fromstr(self.geometries.union_geoms[i].wkt)
            u2 = a.union(b)
            self.assertEqual(u1, u2)
            self.assertEqual(u1, a | b)
            a |= b
            self.assertEqual(u1, a)

    def test_difference(self):
        """Testing difference()."""
        for i in xrange(len(self.geometries.topology_geoms)):
            a = fromstr(self.geometries.topology_geoms[i].wkt_a)
            b = fromstr(self.geometries.topology_geoms[i].wkt_b)
            d1 = fromstr(self.geometries.diff_geoms[i].wkt)
            d2 = a.difference(b)
            self.assertEqual(d1, d2)
            self.assertEqual(d1, a - b)
            a -= b
            self.assertEqual(d1, a)

    def test_symdifference(self):
        """Testing sym_difference()."""
        for i in xrange(len(self.geometries.topology_geoms)):
            a = fromstr(self.geometries.topology_geoms[i].wkt_a)
            b = fromstr(self.geometries.topology_geoms[i].wkt_b)
            d1 = fromstr(self.geometries.sdiff_geoms[i].wkt)
            d2 = a.sym_difference(b)
            self.assertEqual(d1, d2)
            self.assertEqual(d1, a ^ b)
            a ^= b
            self.assertEqual(d1, a)

    def test_buffer(self):
        """Testing buffer()."""
        for bg in self.geometries.buffer_geoms:
            g = fromstr(bg.wkt)
            exp_buf = fromstr(bg.buffer_wkt)
            quadsegs = bg.quadsegs
            width = bg.width
            self.assertRaises(ctypes.ArgumentError, g.buffer, width, float(quadsegs))
            buf = g.buffer(width, quadsegs)
            self.assertEqual(exp_buf.num_coords, buf.num_coords)
            self.assertEqual(len(exp_buf), len(buf))
            for j in xrange(len(exp_buf)):
                exp_ring = exp_buf[j]
                buf_ring = buf[j]
                self.assertEqual(len(exp_ring), len(buf_ring))
                for k in xrange(len(exp_ring)):
                    self.assertAlmostEqual(exp_ring[k][0], buf_ring[k][0], 9)
                    self.assertAlmostEqual(exp_ring[k][1], buf_ring[k][1], 9)

    def test_srid(self):
        """Testing the SRID property and keyword."""
        pnt = Point(5, 23, srid=4326)
        self.assertEqual(4326, pnt.srid)
        pnt.srid = 3084
        self.assertEqual(3084, pnt.srid)
        self.assertRaises(ctypes.ArgumentError, pnt.set_srid, b'4326')
        poly = fromstr(self.geometries.polygons[1].wkt, srid=4269)
        self.assertEqual(4269, poly.srid)
        for ring in poly:
            self.assertEqual(4269, ring.srid)

        poly.srid = 4326
        self.assertEqual(4326, poly.shell.srid)
        gc = GeometryCollection(Point(5, 23), LineString((0, 0), (1.5, 1.5), (3, 3)), srid=32021)
        self.assertEqual(32021, gc.srid)
        for i in range(len(gc)):
            self.assertEqual(32021, gc[i].srid)

        hex = b'0101000020E610000000000000000014400000000000003740'
        p1 = fromstr(hex)
        self.assertEqual(4326, p1.srid)
        exp_srid = self.null_srid
        p2 = fromstr(p1.hex)
        self.assertEqual(exp_srid, p2.srid)
        p3 = fromstr(p1.hex, srid=-1)
        self.assertEqual(-1, p3.srid)

    def test_mutable_geometries(self):
        """Testing the mutability of Polygons and Geometry Collections."""
        for p in self.geometries.polygons:
            poly = fromstr(p.wkt)
            self.assertRaises(TypeError, poly.__setitem__, 0, LineString((1, 1), (2,
                                                                                  2)))
            shell_tup = poly.shell.tuple
            new_coords = []
            for point in shell_tup:
                new_coords.append((point[0] + 500.0, point[1] + 500.0))

            new_shell = LinearRing(*tuple(new_coords))
            poly.exterior_ring = new_shell
            s = str(new_shell)
            self.assertEqual(poly.exterior_ring, new_shell)
            self.assertEqual(poly[0], new_shell)

        for tg in self.geometries.multipoints:
            mp = fromstr(tg.wkt)
            for i in range(len(mp)):
                pnt = mp[i]
                new = Point(random.randint(21, 100), random.randint(21, 100))
                mp[i] = new
                s = str(new)
                self.assertEqual(mp[i], new)
                self.assertEqual(mp[i].wkt, new.wkt)
                self.assertNotEqual(pnt, mp[i])

        for tg in self.geometries.multipolygons:
            mpoly = fromstr(tg.wkt)
            for i in xrange(len(mpoly)):
                poly = mpoly[i]
                old_poly = mpoly[i]
                for j in xrange(len(poly)):
                    r = poly[j]
                    for k in xrange(len(r)):
                        r[k] = (r[k][0] + 500.0, r[k][1] + 500.0)

                    poly[j] = r

                self.assertNotEqual(mpoly[i], poly)
                mpoly[i] = poly
                s = str(poly)
                self.assertEqual(mpoly[i], poly)
                self.assertNotEqual(mpoly[i], old_poly)

    def test_threed(self):
        """Testing three-dimensional geometries."""
        pnt = Point(2, 3, 8)
        self.assertEqual((2.0, 3.0, 8.0), pnt.coords)
        self.assertRaises(TypeError, pnt.set_coords, (1.0, 2.0))
        pnt.coords = (1.0, 2.0, 3.0)
        self.assertEqual((1.0, 2.0, 3.0), pnt.coords)
        ls = LineString((2.0, 3.0, 8.0), (50.0, 250.0, -117.0))
        self.assertEqual(((2.0, 3.0, 8.0), (50.0, 250.0, -117.0)), ls.tuple)
        self.assertRaises(TypeError, ls.__setitem__, 0, (1.0, 2.0))
        ls[0] = (1.0, 2.0, 3.0)
        self.assertEqual((1.0, 2.0, 3.0), ls[0])

    def test_distance(self):
        """Testing the distance() function."""
        pnt = Point(0, 0)
        self.assertEqual(0.0, pnt.distance(Point(0, 0)))
        self.assertEqual(1.0, pnt.distance(Point(0, 1)))
        self.assertAlmostEqual(1.41421356237, pnt.distance(Point(1, 1)), 11)
        ls1 = LineString((0, 0), (1, 1), (2, 2))
        ls2 = LineString((5, 2), (6, 1), (7, 0))
        self.assertEqual(3, ls1.distance(ls2))

    def test_length(self):
        """Testing the length property."""
        pnt = Point(0, 0)
        self.assertEqual(0.0, pnt.length)
        ls = LineString((0, 0), (1, 1))
        self.assertAlmostEqual(1.41421356237, ls.length, 11)
        poly = Polygon(LinearRing((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
        self.assertEqual(4.0, poly.length)
        mpoly = MultiPolygon(poly.clone(), poly)
        self.assertEqual(8.0, mpoly.length)

    def test_emptyCollections(self):
        """Testing empty geometries and collections."""
        gc1 = GeometryCollection([])
        gc2 = fromstr(b'GEOMETRYCOLLECTION EMPTY')
        pnt = fromstr(b'POINT EMPTY')
        ls = fromstr(b'LINESTRING EMPTY')
        poly = fromstr(b'POLYGON EMPTY')
        mls = fromstr(b'MULTILINESTRING EMPTY')
        mpoly1 = fromstr(b'MULTIPOLYGON EMPTY')
        mpoly2 = MultiPolygon(())
        for g in [gc1, gc2, pnt, ls, poly, mls, mpoly1, mpoly2]:
            self.assertEqual(True, g.empty)
            if isinstance(g, Polygon):
                self.assertEqual(1, len(g))
                self.assertEqual(1, g.num_geom)
                self.assertEqual(0, len(g[0]))
            elif isinstance(g, (Point, LineString)):
                self.assertEqual(1, g.num_geom)
                self.assertEqual(0, len(g))
            else:
                self.assertEqual(0, g.num_geom)
                self.assertEqual(0, len(g))
            if isinstance(g, Point):
                self.assertRaises(GEOSIndexError, g.get_x)
            elif isinstance(g, Polygon):
                lr = g.shell
                self.assertEqual(b'LINEARRING EMPTY', lr.wkt)
                self.assertEqual(0, len(lr))
                self.assertEqual(True, lr.empty)
                self.assertRaises(GEOSIndexError, lr.__getitem__, 0)
            else:
                self.assertRaises(GEOSIndexError, g.__getitem__, 0)

    def test_collections_of_collections(self):
        """Testing GeometryCollection handling of other collections."""
        coll = [ mp.wkt for mp in self.geometries.multipolygons if mp.valid ]
        coll.extend([ mls.wkt for mls in self.geometries.multilinestrings ])
        coll.extend([ p.wkt for p in self.geometries.polygons ])
        coll.extend([ mp.wkt for mp in self.geometries.multipoints ])
        gc_wkt = b'GEOMETRYCOLLECTION(%s)' % (b',').join(coll)
        gc1 = GEOSGeometry(gc_wkt)
        gc2 = GeometryCollection(*tuple(g for g in gc1))
        self.assertEqual(gc1, gc2)

    @unittest.skipUnless(gdal.HAS_GDAL, b'gdal is required')
    def test_gdal(self):
        """Testing `ogr` and `srs` properties."""
        g1 = fromstr(b'POINT(5 23)')
        self.assertIsInstance(g1.ogr, gdal.OGRGeometry)
        self.assertIsNone(g1.srs)
        if GEOS_PREPARE:
            g1_3d = fromstr(b'POINT(5 23 8)')
            self.assertIsInstance(g1_3d.ogr, gdal.OGRGeometry)
            self.assertEqual(g1_3d.ogr.z, 8)
        g2 = fromstr(b'LINESTRING(0 0, 5 5, 23 23)', srid=4326)
        self.assertIsInstance(g2.ogr, gdal.OGRGeometry)
        self.assertIsInstance(g2.srs, gdal.SpatialReference)
        self.assertEqual(g2.hex, g2.ogr.hex)
        self.assertEqual(b'WGS 84', g2.srs.name)

    def test_copy(self):
        """Testing use with the Python `copy` module."""
        import copy
        poly = GEOSGeometry(b'POLYGON((0 0, 0 23, 23 23, 23 0, 0 0), (5 5, 5 10, 10 10, 10 5, 5 5))')
        cpy1 = copy.copy(poly)
        cpy2 = copy.deepcopy(poly)
        self.assertNotEqual(poly._ptr, cpy1._ptr)
        self.assertNotEqual(poly._ptr, cpy2._ptr)

    @unittest.skipUnless(gdal.HAS_GDAL, b'gdal is required to transform geometries')
    def test_transform(self):
        """Testing `transform` method."""
        orig = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
        trans = GEOSGeometry(b'POINT (992385.4472045 481455.4944650)', 2774)
        t1, t2, t3 = orig.clone(), orig.clone(), orig.clone()
        t1.transform(trans.srid)
        t2.transform(gdal.SpatialReference(b'EPSG:2774'))
        ct = gdal.CoordTransform(gdal.SpatialReference(b'WGS84'), gdal.SpatialReference(2774))
        t3.transform(ct)
        k1 = orig.clone()
        k2 = k1.transform(trans.srid, clone=True)
        self.assertEqual(k1, orig)
        self.assertNotEqual(k1, k2)
        prec = 3
        for p in (t1, t2, t3, k2):
            self.assertAlmostEqual(trans.x, p.x, prec)
            self.assertAlmostEqual(trans.y, p.y, prec)

    @unittest.skipUnless(gdal.HAS_GDAL, b'gdal is required to transform geometries')
    def test_transform_3d(self):
        p3d = GEOSGeometry(b'POINT (5 23 100)', 4326)
        p3d.transform(2774)
        if GEOS_PREPARE:
            self.assertEqual(p3d.z, 100)
        else:
            self.assertIsNone(p3d.z)

    def test_transform_noop(self):
        """ Testing `transform` method (SRID match) """
        if gdal.HAS_GDAL:
            g = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
            gt = g.tuple
            g.transform(4326)
            self.assertEqual(g.tuple, gt)
            self.assertEqual(g.srid, 4326)
            g = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
            g1 = g.transform(4326, clone=True)
            self.assertEqual(g1.tuple, g.tuple)
            self.assertEqual(g1.srid, 4326)
            self.assertTrue(g1 is not g, b"Clone didn't happen")
        old_has_gdal = gdal.HAS_GDAL
        try:
            gdal.HAS_GDAL = False
            g = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
            gt = g.tuple
            g.transform(4326)
            self.assertEqual(g.tuple, gt)
            self.assertEqual(g.srid, 4326)
            g = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
            g1 = g.transform(4326, clone=True)
            self.assertEqual(g1.tuple, g.tuple)
            self.assertEqual(g1.srid, 4326)
            self.assertTrue(g1 is not g, b"Clone didn't happen")
        finally:
            gdal.HAS_GDAL = old_has_gdal

    def test_transform_nosrid(self):
        """ Testing `transform` method (no SRID or negative SRID) """
        g = GEOSGeometry(b'POINT (-104.609 38.255)', srid=None)
        self.assertRaises(GEOSException, g.transform, 2774)
        g = GEOSGeometry(b'POINT (-104.609 38.255)', srid=None)
        self.assertRaises(GEOSException, g.transform, 2774, clone=True)
        g = GEOSGeometry(b'POINT (-104.609 38.255)', srid=-1)
        self.assertRaises(GEOSException, g.transform, 2774)
        g = GEOSGeometry(b'POINT (-104.609 38.255)', srid=-1)
        self.assertRaises(GEOSException, g.transform, 2774, clone=True)
        return

    def test_transform_nogdal(self):
        """ Testing `transform` method (GDAL not available) """
        old_has_gdal = gdal.HAS_GDAL
        try:
            gdal.HAS_GDAL = False
            g = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
            self.assertRaises(GEOSException, g.transform, 2774)
            g = GEOSGeometry(b'POINT (-104.609 38.255)', 4326)
            self.assertRaises(GEOSException, g.transform, 2774, clone=True)
        finally:
            gdal.HAS_GDAL = old_has_gdal

    def test_extent(self):
        """Testing `extent` method."""
        mp = MultiPoint(Point(5, 23), Point(0, 0), Point(10, 50))
        self.assertEqual((0.0, 0.0, 10.0, 50.0), mp.extent)
        pnt = Point(5.23, 17.8)
        self.assertEqual((5.23, 17.8, 5.23, 17.8), pnt.extent)
        poly = fromstr(self.geometries.polygons[3].wkt)
        ring = poly.shell
        x, y = ring.x, ring.y
        xmin, ymin = min(x), min(y)
        xmax, ymax = max(x), max(y)
        self.assertEqual((xmin, ymin, xmax, ymax), poly.extent)

    def test_pickle(self):
        """Testing pickling and unpickling support."""
        from django.utils.six.moves import cPickle
        import pickle

        def get_geoms(lst, srid=None):
            return [ GEOSGeometry(tg.wkt, srid) for tg in lst ]

        tgeoms = get_geoms(self.geometries.points)
        tgeoms.extend(get_geoms(self.geometries.multilinestrings, 4326))
        tgeoms.extend(get_geoms(self.geometries.polygons, 3084))
        tgeoms.extend(get_geoms(self.geometries.multipolygons, 900913))
        no_srid = self.null_srid == -1
        for geom in tgeoms:
            s1, s2 = cPickle.dumps(geom), pickle.dumps(geom)
            g1, g2 = cPickle.loads(s1), pickle.loads(s2)
            for tmpg in (g1, g2):
                self.assertEqual(geom, tmpg)
                if not no_srid:
                    self.assertEqual(geom.srid, tmpg.srid)

        return

    @unittest.skipUnless(GEOS_PREPARE, b'geos >= 3.1.0 is required')
    def test_prepared(self):
        """Testing PreparedGeometry support."""
        mpoly = GEOSGeometry(b'MULTIPOLYGON(((0 0,0 5,5 5,5 0,0 0)),((5 5,5 10,10 10,10 5,5 5)))')
        prep = mpoly.prepared
        pnts = [
         Point(5, 5), Point(7.5, 7.5), Point(2.5, 7.5)]
        covers = [True, True, False]
        for pnt, c in zip(pnts, covers):
            self.assertEqual(mpoly.contains(pnt), prep.contains(pnt))
            self.assertEqual(mpoly.intersects(pnt), prep.intersects(pnt))
            self.assertEqual(c, prep.covers(pnt))

    def test_line_merge(self):
        """Testing line merge support"""
        ref_geoms = (
         fromstr(b'LINESTRING(1 1, 1 1, 3 3)'),
         fromstr(b'MULTILINESTRING((1 1, 3 3), (3 3, 4 2))'))
        ref_merged = (
         fromstr(b'LINESTRING(1 1, 3 3)'),
         fromstr(b'LINESTRING (1 1, 3 3, 4 2)'))
        for geom, merged in zip(ref_geoms, ref_merged):
            self.assertEqual(merged, geom.merged)

    @unittest.skipUnless(GEOS_PREPARE, b'geos >= 3.1.0 is required')
    def test_valid_reason(self):
        """Testing IsValidReason support"""
        g = GEOSGeometry(b'POINT(0 0)')
        self.assertTrue(g.valid)
        self.assertIsInstance(g.valid_reason, six.string_types)
        self.assertEqual(g.valid_reason, b'Valid Geometry')
        g = GEOSGeometry(b'LINESTRING(0 0, 0 0)')
        self.assertFalse(g.valid)
        self.assertIsInstance(g.valid_reason, six.string_types)
        self.assertTrue(g.valid_reason.startswith(b'Too few points in geometry component'))

    @unittest.skipUnless(geos_version_info()[b'version'] >= b'3.2.0', b'geos >= 3.2.0 is required')
    def test_linearref(self):
        """Testing linear referencing"""
        ls = fromstr(b'LINESTRING(0 0, 0 10, 10 10, 10 0)')
        mls = fromstr(b'MULTILINESTRING((0 0, 0 10), (10 0, 10 10))')
        self.assertEqual(ls.project(Point(0, 20)), 10.0)
        self.assertEqual(ls.project(Point(7, 6)), 24)
        self.assertEqual(ls.project_normalized(Point(0, 20)), 1.0 / 3)
        self.assertEqual(ls.interpolate(10), Point(0, 10))
        self.assertEqual(ls.interpolate(24), Point(10, 6))
        self.assertEqual(ls.interpolate_normalized(1.0 / 3), Point(0, 10))
        self.assertEqual(mls.project(Point(0, 20)), 10)
        self.assertEqual(mls.project(Point(7, 6)), 16)
        self.assertEqual(mls.interpolate(9), Point(0, 9))
        self.assertEqual(mls.interpolate(17), Point(10, 7))

    def test_geos_version(self):
        """Testing the GEOS version regular expression."""
        from django.contrib.gis.geos.libgeos import version_regex
        versions = [
         ('3.0.0rc4-CAPI-1.3.3', '3.0.0', '1.3.3'),
         ('3.0.0-CAPI-1.4.1', '3.0.0', '1.4.1'),
         ('3.4.0dev-CAPI-1.8.0', '3.4.0', '1.8.0'),
         ('3.4.0dev-CAPI-1.8.0 r0', '3.4.0', '1.8.0')]
        for v_init, v_geos, v_capi in versions:
            m = version_regex.match(v_init)
            self.assertTrue(m, msg=b"Unable to parse the version string '%s'" % v_init)
            self.assertEqual(m.group(b'version'), v_geos)
            self.assertEqual(m.group(b'capi_version'), v_capi)


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(GEOSTest))
    return s


def run(verbosity=2):
    unittest.TextTestRunner(verbosity=verbosity).run(suite())