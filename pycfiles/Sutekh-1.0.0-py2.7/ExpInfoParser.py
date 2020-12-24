# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/ExpInfoParser.py
# Compiled at: 2019-12-11 16:37:58
"""Parse expansion and printing info from a json file."""
import json
from logging import Logger
from sutekh.base.core.BaseAdapters import IExpansion, IPrinting, IAbstractCard
from sutekh.core.SutekhObjectMaker import SutekhObjectMaker

class ExpInfoParser(object):
    """Parse expansion and printing info from a JSON file and update the
       database with the correct information."""

    def __init__(self, oLogHandler):
        self.oLogger = Logger('exp info parser')
        if oLogHandler is not None:
            self.oLogger.addHandler(oLogHandler)
        self.oLogHandler = oLogHandler
        self._oMaker = SutekhObjectMaker()
        return

    def _update_printing(self, oPrinting, dPrintInfo):
        """Update the specific printing with the required info"""
        for oProp in oPrinting.properties:
            oPrinting.removePrintingProperty(oProp)

        sDate = dPrintInfo.pop('date')
        sBack = dPrintInfo.pop('back')
        oDateProp = self._oMaker.make_printing_property('Release Date: %s' % sDate)
        oBackProp = self._oMaker.make_printing_property('Back Type: %s' % sBack)
        oPrinting.addPrintingProperty(oDateProp)
        oPrinting.addPrintingProperty(oBackProp)
        aCards = dPrintInfo.pop('cards', [])
        for sCardName in aCards:
            oAbsCard = IAbstractCard(sCardName)
            _oCard = self._oMaker.make_physical_card(oAbsCard, oPrinting)

        for sKey, sValue in dPrintInfo.items():
            oProp = self._oMaker.make_printing_property('%s: %s' % (sKey, sValue))
            oPrinting.addProperty(oProp)

    def _handle_expansion(self, sExp, dExpInfo):
        """Handle updating the specific expansion."""
        oExp = IExpansion(sExp)
        for sVariant in dExpInfo:
            if sVariant == 'None':
                oPrinting = IPrinting((oExp, None))
            else:
                oPrinting = self._oMaker.make_printing(oExp, sVariant)
            self._update_printing(oPrinting, dExpInfo[sVariant])
            oPrinting.syncUpdate()

        return

    def parse(self, fIn):
        """Process the JSON file line into the database"""
        dExpInfo = json.load(fIn)
        if hasattr(self.oLogHandler, 'set_total'):
            self.oLogHandler.set_total(len(dExpInfo))
        for sExp in dExpInfo:
            self._handle_expansion(sExp, dExpInfo[sExp])
            self.oLogger.info('Added Expansion info: %s', sExp)