# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shawn/Desktop/projects/cadnano2.5/cadnano/tests/functionaltest_gui.py
# Compiled at: 2018-01-21 22:08:05
# Size of source mod 2**32: 1986 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtTest import QTest
from cadnano.fileio.lattice import HoneycombDnaPart
from cadnano.views.sliceview import slicestyles
from cnguitestcase import GUITestApp

@pytest.fixture()
def cnapp():
    app = GUITestApp()
    yield app
    app.tearDown()


DELAY = 5
RADIUS = slicestyles.SLICE_HELIX_RADIUS

def testCreateVirtualHelixGui(cnapp):
    """Create some VHs"""
    toolbar = cnapp.window.main_toolbar
    action_new_honeycomb = toolbar.widgetForAction(cnapp.window.action_new_dnapart_honeycomb)
    QTest.mouseClick(action_new_honeycomb, (Qt.LeftButton), delay=DELAY)
    slicerootitem = cnapp.window.slice_root
    @py_assert2 = slicerootitem.instance_items
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 1
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.instance_items\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(slicerootitem) if 'slicerootitem' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(slicerootitem) else 'slicerootitem',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    slice_part_item = list(slicerootitem.instance_items.values())[0]
    QTest.keyClick((cnapp.window), (Qt.Key_H), delay=DELAY)
    QTest.keyClick((cnapp.window), (Qt.Key_C), delay=DELAY)
    cnapp.processEvents()
    cmd_count = 1
    for row in range(-2, 2):
        for col in range(-2, 2):
            x, y = HoneycombDnaPart.latticeCoordToPositionXY(RADIUS, row, col)
            pt = QPointF(x, y)
            cnapp.graphicsItemClick(slice_part_item, (Qt.LeftButton), pos=pt, delay=DELAY)
            cmd_count += 1

    cnapp.processEvents()
    vh_count = len(cnapp.document.activePart().getidNums())
    for i in range(cmd_count):
        cnapp.document.undoStack().undo()

    cnapp.processEvents()
    for i in range(cmd_count):
        cnapp.document.undoStack().redo()

    cnapp.processEvents()
    part = list(cnapp.document.children())[0]
    vh_count_after_redo = len(part.getidNums())
    @py_assert1 = vh_count == vh_count_after_redo
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (vh_count, vh_count_after_redo)) % {'py0':@pytest_ar._saferepr(vh_count) if 'vh_count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vh_count) else 'vh_count',  'py2':@pytest_ar._saferepr(vh_count_after_redo) if 'vh_count_after_redo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vh_count_after_redo) else 'vh_count_after_redo'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None