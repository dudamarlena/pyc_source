# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/file_model.py
# Compiled at: 2006-03-14 05:23:38
from lxml import etree
from lxml.etree import Element, parse
from xpathmodel import XPathModel, autoconstruct, get_first
from model import NamedObject
SLOW_FILE_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/slow'
from message_hierarchy_model import MSG_NAMESPACE_URI
from attribute_model import DB_NAMESPACE_URI
from slosl_model import SLOSL_NAMESPACE_URI
from edsm_model import EDSM_NAMESPACE_URI
from gui_model import GUI_NAMESPACE_URI

def buildFile():
    return Element('{%s}file' % SLOW_FILE_NAMESPACE_URI)


class FileModel(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = SLOW_FILE_NAMESPACE_URI
    SLOSL_NAMESPACE = SLOSL_NAMESPACE_URI
    EDSM_NAMESPACE = EDSM_NAMESPACE_URI
    GUI_NAMESPACE = GUI_NAMESPACE_URI
    MSG_NAMESPACE = MSG_NAMESPACE_URI
    DB_NAMESPACE = DB_NAMESPACE_URI

    @get_first
    @autoconstruct
    def _get_types(self):
        """./{%(DB_NAMESPACE)s}types"""
        pass

    @get_first
    @autoconstruct
    def _get_attributes(self):
        """./{%(DB_NAMESPACE)s}attributes"""
        pass

    @get_first
    @autoconstruct
    def _get_edsm(self):
        """./{%(EDSM_NAMESPACE)s}edsm"""
        pass

    @get_first
    @autoconstruct
    def _get_message_hierarchy(self):
        """./{%(MSG_NAMESPACE)s}message_hierarchy"""
        pass

    @get_first
    @autoconstruct
    def _get_statements(self):
        """./{%(SLOSL_NAMESPACE)s}statements"""
        pass

    @get_first
    @autoconstruct
    def _get_guidata(self):
        """./{%(GUI_NAMESPACE)s}gui"""
        pass


ns = etree.Namespace(SLOW_FILE_NAMESPACE_URI)
ns['file'] = FileModel