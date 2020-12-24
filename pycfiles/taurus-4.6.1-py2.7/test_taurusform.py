# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/panel/test/test_taurusform.py
# Compiled at: 2019-08-19 15:09:30
"""Unit tests for Taurus Forms"""
import unittest
from taurus.qt.qtgui.test import GenericWidgetTestCase
from taurus.qt.qtgui.panel import TaurusForm, TaurusAttrForm

class TaurusFormTest(GenericWidgetTestCase, unittest.TestCase):
    """
    Generic tests for TaurusForm widget.

    .. seealso: :class:`taurus.qt.qtgui.test.base.GenericWidgetTestCase`
    """
    _klass = TaurusForm
    modelnames = [['sys/tg_test/1'],
     [
      'sys/tg_test/1/wave'], [],
     '',
     [
      'eval:1'],
     None,
     [ 'sys/tg_test/1/%s' % a for a in ('short_scalar', 'double_array', 'uchar_image_ro',
                                   'string_spectrum', 'no_value', 'throw_exception')
     ],
     [
      ''],
     'sys/tg_test/1,eval:1',
     'sys/tg_test/1/short_image eval:rand(16)',
     [
      None]]


class TaurusAttrFormTest(GenericWidgetTestCase, unittest.TestCase):
    """
    Generic tests for TaurusAttrForm widget.

    .. seealso: :class:`taurus.qt.qtgui.test.base.GenericWidgetTestCase`
    """
    _klass = TaurusAttrForm
    modelnames = ['sys/tg_test/1', None]