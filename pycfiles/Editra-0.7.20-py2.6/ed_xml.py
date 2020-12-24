# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_xml.py
# Compiled at: 2012-12-22 13:45:17
"""
XML base class

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_xml.py 72624 2012-10-06 19:38:14Z CJP $'
__revision__ = '$Revision: 72624 $'
import types
from xml.dom import minidom
import extern.dexml as dexml
from extern.dexml.fields import *
import util

class EdXml(dexml.Model):
    """XML base class"""

    def __init__(self, **kwds):
        super(EdXml, self).__init__(**kwds)

    Xml = property(lambda self: self.GetXml(), lambda self, xstr: self.parse(xstr))
    PrettyXml = property(lambda self: self.GetPrettyXml(), lambda self, xstr: self.parse(xstr))

    def GetPrettyXml(self):
        """Get a nicely formatted version of the rendered xml string
        @return: string

        """
        txt = ''
        try:
            txt = self.render()
            txt = minidom.parseString(txt).toprettyxml()
            txt = txt.replace('\t', '   ')
        except UnicodeEncodeError, err:
            util.Log('[EdXml][err] GetPrettyXml %s' % err)

        return txt

    def GetXml(self):
        """Get the XML string for this object
        @return: string

        """
        xstr = ''
        try:
            xstr = self.render()
        except UnicodeEncodeError, err:
            util.Log('[EdXml][err] GetXml %s' % err)

        return xstr

    def Write(self, path):
        """Write the xml to a file
        @param path: string
        @return: success (bool)

        """
        suceeded = True
        try:
            xmlstr = self.PrettyXml
            if isinstance(xmlstr, types.UnicodeType):
                xmlstr = xmlstr.encode('utf-8')
            handle = open(path, 'wb')
            handle.write(xmlstr)
            handle.close()
        except (IOError, OSError, UnicodeEncodeError):
            suceeded = False

        return suceeded

    @classmethod
    def Load(cls, path):
        """Load this object from a file
        @param path: path to xml file
        @return: instance

        """
        instance = None
        try:
            handle = open(path, 'rb')
            xmlstr = handle.read()
            handle.close()
            instance = cls.parse(xmlstr)
        except (IOError, OSError):
            instance = None

        return instance

    @classmethod
    def LoadString(cls, xmlstr):
        """Load an object from an XML string
        @param cls: Class object
        @param xmlstr: string

        """
        instance = cls.parse(xmlstr)
        return instance