# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/BaseSutekhXMLParser.py
# Compiled at: 2019-12-11 16:37:57
"""Base class for sutekh specific XML parser
   """
from sutekh.base.io.BaseCardSetIO import BaseCardXMLParser

class BaseSutekhXMLParser(BaseCardXMLParser):
    """Base class for Sutekh XML files.

       Defines typename and version tag as required for the subclasses."""
    sTypeName = 'Sutekh'
    sVersionTag = 'sutekh_xml_version'