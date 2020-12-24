# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/administration/gui.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 2, 2012\n\n@package ally core request\n@copyright 2011 Sourcefabric o.p.s.\n@license http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the GUI configuration setup for the node presenter plugin.\n'
from ..gui_core.gui_core import publishGui
from ally.container import app

@app.populate(app.DEVEL)
def publishJS():
    publishGui('superdesk/request')