# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/GuessFileParser.py
# Compiled at: 2019-12-11 16:37:58
"""Attempt to gues the correct format from Sutekh's available parsers."""
from sutekh.base.io.BaseGuessFileParser import BaseGuessFileParser
from sutekh.io.AbstractCardSetParser import AbstractCardSetParser
from sutekh.io.PhysicalCardSetParser import PhysicalCardSetParser
from sutekh.io.PhysicalCardParser import PhysicalCardParser
from sutekh.io.ARDBXMLDeckParser import ARDBXMLDeckParser
from sutekh.io.ARDBXMLInvParser import ARDBXMLInvParser
from sutekh.io.ARDBTextParser import ARDBTextParser
from sutekh.io.JOLDeckParser import JOLDeckParser
from sutekh.io.ELDBInventoryParser import ELDBInventoryParser
from sutekh.io.ELDBDeckFileParser import ELDBDeckFileParser
from sutekh.io.ELDBHTMLParser import ELDBHTMLParser
from sutekh.io.LackeyDeckParser import LackeyDeckParser
from sutekh.io.SLDeckParser import SLDeckParser
from sutekh.io.SLInventoryParser import SLInventoryParser

class GuessFileParser(BaseGuessFileParser):
    """Parser which guesses the file type"""
    PARSERS = [
     PhysicalCardSetParser,
     AbstractCardSetParser,
     PhysicalCardParser,
     ARDBXMLDeckParser,
     ARDBXMLInvParser,
     ARDBTextParser,
     ELDBInventoryParser,
     ELDBDeckFileParser,
     ELDBHTMLParser,
     SLDeckParser,
     SLInventoryParser,
     LackeyDeckParser,
     JOLDeckParser]