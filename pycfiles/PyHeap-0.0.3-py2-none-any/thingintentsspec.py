# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/thingintentsspec.py
# Compiled at: 2016-01-05 13:27:56
from lxml import etree
from healthvaultlib.exceptions.healthserviceexception import HealthServiceException

class ThingIntentsSpec:
    """
        Specifies the usage intentions for items retrieved in the group.

        Attributes:
            intents     The value may be one of "view", "download",
                        or "transmit".
    """
    allowed_intents = [
     'view', 'download', 'transmit']

    def __init__(self, intents):
        self.intents = intents

    def write_xml(self):
        intents = etree.Element('intents')
        for i in self.intents:
            if i not in self.allowed_intents:
                raise HealthServiceException('Invalid intent')
            intent = etree.Element('intent')
            intent.text = i
            intents.append(intent)

        return intents