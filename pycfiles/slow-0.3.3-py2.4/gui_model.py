# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/gui_model.py
# Compiled at: 2006-03-14 03:40:39
GUI_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/slow-gui'
from lxml import etree
from xpathmodel import XPathModel, autoconstruct, get_first
from edsm_model import EDSM_NAMESPACE_URI
from code_model import CodeContainer

class GuiDataModel(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = GUI_NAMESPACE_URI

    def _get_pos_dict(self, _xpath_result):
        """./{%(DEFAULT_NAMESPACE)s}pos"""
        return dict(((el.ref, el.pos) for el in _xpath_result))

    def _get_testcode_dict(self, _xpath_result):
        """./{%(DEFAULT_NAMESPACE)s}testcode"""
        return dict(((el.view_name, el.code) for el in _xpath_result))

    def _get_pos(self, ref):
        """./{%(DEFAULT_NAMESPACE)s}pos[ @ref = $ref ]"""
        pass

    def _set_pos(self, _xpath_result, ref, x, y):
        """./{%(DEFAULT_NAMESPACE)s}pos[ @ref = $ref ]"""
        if _xpath_result:
            _xpath_result[0].pos = (
             x, y)
        else:
            tag = '{%s}pos' % GUI_NAMESPACE_URI
            etree.SubElement(self, tag, ref=ref, x=str(x), y=str(y))

    @get_first
    def _get_testCode(self, view_name):
        """./{%(DEFAULT_NAMESPACE)s}testcode[ @view_name = $view_name]"""
        pass

    def _set_testCode(self, _xpath_result, view_name, code):
        """./{%(DEFAULT_NAMESPACE)s}testcode[ @view_name = $view_name]"""
        if _xpath_result:
            code_tag = _xpath_result[0]
        else:
            tag = '{%s}testcode' % GUI_NAMESPACE_URI
            code_tag = etree.SubElement(self, tag, view_name=view_name)
        code_tag.language = 'python'
        code_tag.code = code


class IconPositionModel(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = GUI_NAMESPACE_URI
    _attr_ref = './@ref'

    def _get_pos(self):
        return (
         int(self.get('x')), int(self.get('y')))

    def _set_pos(self, pos_tuple):
        self.set('x', str(pos_tuple[0]))
        self.set('y', str(pos_tuple[1]))


class TestCodeContainer(CodeContainer):
    __module__ = __name__
    DEFAULT_NAMESPACE = GUI_NAMESPACE_URI
    _attr_view_name = './@view_name'


ns = etree.Namespace(GUI_NAMESPACE_URI)
ns['gui'] = GuiDataModel
ns['pos'] = IconPositionModel
ns['testcode'] = TestCodeContainer