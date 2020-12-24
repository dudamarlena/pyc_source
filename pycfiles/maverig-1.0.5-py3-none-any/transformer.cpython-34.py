# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\transformer.py
# Compiled at: 2014-12-11 18:17:41
# Size of source mod 2**32: 3058 bytes
import gettext, locale
from maverig.data import dataHandler
from maverig.data.components.abstractComponent import Parameter, Attribute
from maverig.data.components.utils.dataObject import ObjectDict
from maverig.data.components.abstract import abstractLine
from maverig.data.components.simulators import pyPowerSimulator
current_language, encoding = locale.getdefaultlocale()
locale_path = dataHandler.get_lang_path()
language = gettext.translation(current_language, locale_path, [current_language])
language.install()

class SR(Attribute):
    name = 'S_r'
    description = 'Rated apparent power'
    unit = 'VA'
    unit_description = 'Volt Ampere'
    static = True


class IMaxP(Attribute):
    name = 'I_max_p'
    description = 'Maximum current on primary side'
    unit = 'A'
    unit_description = 'Ampere'
    static = True


class IMaxS(Attribute):
    name = 'I_max_s'
    description = 'Maximum current on secondary side'
    unit = 'A'
    unit_description = 'Ampere'
    static = True


class PLoss(Attribute):
    name = 'P_loss'
    description = 'Active power loss'
    unit = 'W'
    unit_description = 'Watt'
    static = True


class UP(Attribute):
    name = 'U_p'
    description = 'Nominal primary voltage'
    unit = 'V'
    unit_description = 'Volt'
    static = True


class US(Attribute):
    name = 'U_s'
    description = 'Nominal secondary voltage'
    unit = 'V'
    unit_description = 'Volt'
    static = True


class Taps(Attribute):
    name = 'taps'
    description = 'Dict. of possible tap turns and their values'
    data_type = 'string'
    static = True


class TapTurn(Attribute):
    name = 'tap_turn'
    description = 'Currently active tap turn'
    unit = ''
    unit_description = 'Tap Turn'
    data_type = 'int'
    static = True


class TransformerType(Parameter):
    name = 'ttype'
    description = 'transformer type'
    data_type = 'string'
    hv2mv_values = ['TRAFO_31', 'TRAFO_40']
    mv2lv_values = ['TRAFO_200', 'TRAFO_250', 'TRAFO_400', 'TRAFO_630']
    accepted_values = hv2mv_values + mv2lv_values
    value = accepted_values[0]


class Tap(Parameter):
    name = 'tap'
    description = 'transformer tap'
    data_type = 'int'
    accepted_values = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    value = 0


class Transformer(abstractLine.AbstractLine):
    name = 'Transformer'
    description = 'Transformer'
    simulator = pyPowerSimulator.PyPower()
    drawing_mode = 'line-icon-line'
    icon = 'transformer.svg'
    category = property(lambda self: _('Grid'))
    params = ObjectDict([abstractLine.FromBus, abstractLine.ToBus, TransformerType, abstractLine.Online, Tap])
    attrs = ObjectDict([abstractLine.PFrom, abstractLine.QFrom, abstractLine.PTo, abstractLine.QTo,
     SR, IMaxP, IMaxS, PLoss, UP, US, Taps, TapTurn])
    docking_ports = [abstractLine.AbstractBusDockingPort(), abstractLine.AbstractBusDockingPort()]