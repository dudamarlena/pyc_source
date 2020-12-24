# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/unit/utils/test_dart_loader.py
# Compiled at: 2019-01-12 17:06:36
# Size of source mod 2**32: 2192 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, platform, pytest, dartpy
from dartpy.utils import DartLoader
import os
from tests.util import get_asset_path

def test_parse_skeleton_non_existing_path_returns_null():
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isfile
    @py_assert6 = 'skel/cubes.skel'
    @py_assert8 = get_asset_path(@py_assert6)
    @py_assert10 = @py_assert3(@py_assert8)
    @py_assert13 = True
    @py_assert12 = @py_assert10 is @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('is', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n})\n} is %(py14)s', ), (@py_assert10, @py_assert13)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py14':@pytest_ar._saferepr(@py_assert13)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None
    loader = DartLoader()
    @py_assert1 = loader.parseSkeleton
    @py_assert4 = 'skel/test/does_not_exist.urdf'
    @py_assert6 = get_asset_path(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.parseSkeleton\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} is %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(loader) if 'loader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loader) else 'loader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_parse_skeleton_invalid_urdf_returns_null():
    loader = DartLoader()
    @py_assert1 = loader.parseSkeleton
    @py_assert4 = 'urdf/invalid.urdf'
    @py_assert6 = get_asset_path(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.parseSkeleton\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} is %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(loader) if 'loader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loader) else 'loader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_parse_skeleton_missing_mesh_returns_null():
    loader = DartLoader()
    @py_assert1 = loader.parseSkeleton
    @py_assert4 = 'urdf/missing_mesh.urdf'
    @py_assert6 = get_asset_path(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.parseSkeleton\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} is %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(loader) if 'loader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loader) else 'loader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_parse_skeleton_invalid_mesh_returns_null():
    loader = DartLoader()
    @py_assert1 = loader.parseSkeleton
    @py_assert4 = 'urdf/invalid_mesh.urdf'
    @py_assert6 = get_asset_path(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.parseSkeleton\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} is %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(loader) if 'loader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loader) else 'loader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_parse_skeleton_missing_package_returns_null():
    loader = DartLoader()
    @py_assert1 = loader.parseSkeleton
    @py_assert4 = 'urdf/missing_package.urdf'
    @py_assert6 = get_asset_path(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.parseSkeleton\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} is %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(loader) if 'loader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loader) else 'loader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_parse_skeleton_loads_primitive_geometry():
    loader = DartLoader()
    @py_assert1 = loader.parseSkeleton
    @py_assert4 = 'urdf/test/primitive_geometry.urdf'
    @py_assert6 = get_asset_path(@py_assert4)
    @py_assert8 = @py_assert1(@py_assert6)
    @py_assert11 = None
    @py_assert10 = @py_assert8 is not @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.parseSkeleton\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n} is not %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(loader) if 'loader' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loader) else 'loader',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(get_asset_path) if 'get_asset_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_asset_path) else 'get_asset_path',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None


def test_parse_joint_properties():
    loader = DartLoader()
    robot = loader.parseSkeleton(get_asset_path('urdf/test/joint_properties.urdf'))
    @py_assert2 = None
    @py_assert1 = robot is not @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert1,), ('%(py0)s is not %(py3)s', ), (robot, @py_assert2)) % {'py0':@pytest_ar._saferepr(robot) if 'robot' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(robot) else 'robot',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


if __name__ == '__main__':
    pytest.main()