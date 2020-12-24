# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/unit/utils/test_dart_loader.py
# Compiled at: 2018-10-11 04:24:45
# Size of source mod 2**32: 2079 bytes
import platform, pytest
from dartpy.utils import DartLoader
from tests.util import get_asset_path

def test_parse_skeleton_non_existing_path_returns_null():
    loader = DartLoader()
    assert loader.parseSkeleton(get_asset_path('skel/test/does_not_exist.urdf')) is None


def test_parse_skeleton_invalid_urdf_returns_null():
    loader = DartLoader()
    assert loader.parseSkeleton(get_asset_path('urdf/invalid.urdf')) is None


def test_parse_skeleton_missing_mesh_returns_null():
    loader = DartLoader()
    assert loader.parseSkeleton(get_asset_path('urdf/missing_mesh.urdf')) is None


def test_parse_skeleton_invalid_mesh_returns_null():
    loader = DartLoader()
    assert loader.parseSkeleton(get_asset_path('urdf/invalid_mesh.urdf')) is None


def test_parse_skeleton_missing_package_returns_null():
    loader = DartLoader()
    assert loader.parseSkeleton(get_asset_path('urdf/missing_package.urdf')) is None


def test_parse_skeleton_loads_primitive_geometry():
    loader = DartLoader()
    assert loader.parseSkeleton(get_asset_path('urdf/primitive_geometry.urdf')) is not None


def test_parse_joint_properties():
    loader = DartLoader()
    robot = loader.parseSkeleton(get_asset_path('urdf/joint_properties.urdf'))
    if not robot is not None:
        raise AssertionError
    else:
        joint1 = robot.getJoint(1)
        assert joint1 is not None
        assert joint1.getDampingCoefficient(0) == pytest.approx(1.2, 1e-12)
        assert joint1.getCoulombFriction(0) == pytest.approx(2.3, 1e-12)
        joint2 = robot.getJoint(2)
        assert joint2 is not None
        assert joint2.getPositionLowerLimit(0) == -float('inf')
        assert joint2.getPositionUpperLimit(0) == float('inf')
    if not platform.linux_distribution()[1] == '14.04':
        if not joint2.isCyclic(0):
            raise AssertionError


if __name__ == '__main__':
    pytest.main()