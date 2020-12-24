# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\ev.py
# Compiled at: 2014-12-11 18:17:42
# Size of source mod 2**32: 983 bytes
import gettext, locale
from maverig.data import dataHandler
from maverig.data.components.abstractComponent import DockingPort
from maverig.data.components.utils.dataObject import ObjectDict
from maverig.data.components.abstract import abstractCSV
from maverig.data.components.simulators import csvSimulator
current_language, encoding = locale.getdefaultlocale()
locale_path = dataHandler.get_lang_path()
language = gettext.translation(current_language, locale_path, [current_language])
language.install()

class EV(abstractCSV.AbstractCSV):
    name = 'EV'
    description = 'electric vehicle'
    simulator = csvSimulator.CSVSimulator()
    drawing_mode = 'icon'
    icon = 'ev.svg'
    category = property(lambda self: _('Storage'))
    params = ObjectDict([abstractCSV.SimStart, abstractCSV.DataFile])
    attrs = ObjectDict([abstractCSV.P])
    docking_ports = [
     DockingPort(), abstractCSV.BusDockingPort()]