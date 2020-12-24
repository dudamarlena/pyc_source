# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/jpylyzer/jpylyzer/etpatch.py
# Compiled at: 2019-11-05 12:10:53
"""Patch for 'findtext' bug in ElementTree.

TODO:
1) Find out whether these patches are necessary
2) learn how to write and test patches properly
"""
import xml.etree.ElementTree as ET
from . import byteconv as bc
from . import config

def tostring(elem, enc, meth):
    """Return string representation of Element object with user-defined encoding and method."""
    return ET.tostring(elem, enc, meth)


def fromstring(text):
    """Convert string to Element object."""
    return ET.fromstring(text)


def SubElement(parent, tag):
    """Return sub-element from parent element."""
    return ET.SubElement(parent, tag)


class Element(ET.Element):
    """Element class."""

    def findElementText(self, match):
        """Replacement for ET's 'findtext' function.

        This has a bug that will return empty string if text field contains
        integer with value of zero (0); If there is no match, return None
        """
        elt = self.find(match)
        if elt is not None:
            return elt.text
        else:
            return

    def findAllText(self, match):
        """Search element and return list.

        Returned list contains 'Text' attribute of all matching sub-elements.
        Return empty list if element does not exist
        """
        try:
            return [ result.text for result in self.findall(match) ]
        except:
            return []

    def appendChildTagWithText(self, tag, text):
        """Append childnode with text."""
        el = ET.SubElement(self, tag)
        el.text = text

    def appendIfNotEmpty(self, subelement):
        """Append sub-element, but only if subelement is not empty."""
        if subelement:
            self.append(subelement)

    def makeHumanReadable(self, remapTable=None):
        """Take element object, and return a modified version.

        All non-printable 'text' fields (which may contain numeric data or binary
        strings) are replaced by printable strings.

        Property values in original tree may be mapped to alternative (more user-friendly)
        reportable values using a remapTable, which is a nested dictionary.
        """
        remapTable = remapTable or {}
        for elt in self.iter():
            textIn = elt.text
            tag = elt.tag
            try:
                parameterMap = remapTable[tag]
                try:
                    remappedValue = parameterMap[textIn]
                except KeyError:
                    remappedValue = textIn

            except KeyError:
                remappedValue = textIn

            if config.PYTHON_VERSION.startswith(config.PYTHON_2):
                numericTypes = [
                 int, long, float, bool]
            else:
                numericTypes = [
                 int, float, bool]
            if remappedValue is not None:
                textType = type(remappedValue)
                if textType == bytes:
                    textOut = bc.bytesToText(remappedValue)
                elif textType in numericTypes:
                    textOut = str(remappedValue)
                else:
                    textOut = bc.removeControlCharacters(remappedValue)
                elt.text = textOut

        return

    def toxml(self):
        """Convert Element object to XML."""
        return ET.tostring(self, 'UTF-8', 'xml')