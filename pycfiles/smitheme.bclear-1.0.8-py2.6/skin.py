# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aaltepet/silva/dev-silva2.3/src/smitheme.bclear/smitheme/bclear/skin.py
# Compiled at: 2011-11-02 13:01:17
from silva.core.smi.interfaces import ISMILayer
from silva.core.layout.jquery.interfaces import IJQueryResources
from silva.core import conf as silvaconf

class ISMIBClearLayer(ISMILayer):
    pass


class ISMIBClearSkin(ISMIBClearLayer):
    silvaconf.resource('bclear.css')
    silvaconf.resource('jquery.smi.js')