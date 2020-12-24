# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\bus.py
# Compiled at: 2014-12-11 18:17:41
# Size of source mod 2**32: 1052 bytes
import gettext, locale
from maverig.data import dataHandler
from maverig.data.components.abstractComponent import DockingPort
from maverig.data.components.utils.dataObject import ObjectDict
from maverig.data.components.abstract import abstractBus
from maverig.data.components.simulators import pyPowerSimulator
current_language, encoding = locale.getdefaultlocale()
locale_path = dataHandler.get_lang_path()
language = gettext.translation(current_language, locale_path, [current_language])
language.install()

class BusType(abstractBus.BusType):
    value = 'PQ'


class BaseKV(abstractBus.BaseKV):
    value = 0.23


class Bus(abstractBus.AbstractBus):
    name = 'PQBus'
    description = 'PQBus Node'
    simulator = pyPowerSimulator.PyPower()
    drawing_mode = 'node'
    icon = 'bus.svg'
    category = property(lambda self: _('Grid'))
    params = ObjectDict([BusType, BaseKV])
    attrs = ObjectDict([abstractBus.P, abstractBus.Q, abstractBus.Vl, abstractBus.Vm, abstractBus.Va])
    docking_ports = [
     DockingPort()]