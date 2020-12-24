# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\branch.py
# Compiled at: 2014-12-11 18:17:41
# Size of source mod 2**32: 3204 bytes
import gettext, locale
from maverig.data import dataHandler
from maverig.data.components.abstractComponent import Attribute, Parameter
from maverig.data.components.utils.dataObject import ObjectDict
from maverig.data.components.abstract import abstractLine
from maverig.data.components.simulators import pyPowerSimulator
current_language, encoding = locale.getdefaultlocale()
locale_path = dataHandler.get_lang_path()
language = gettext.translation(current_language, locale_path, [current_language])
language.install()

class IReal(Attribute):
    name = 'I_real'
    description = 'Branch current (real part)'
    unit = 'A'
    unit_description = 'Ampere'
    static = False


class IImag(Attribute):
    name = 'I_imag'
    description = 'Branch current (imaginary part)'
    unit = 'A'
    unit_description = 'Ampere'
    static = False


class SMax(Attribute):
    name = 'S_max'
    description = 'Maximum apparent power'
    unit = 'VA'
    unit_description = 'Volt Ampere'
    static = True


class IMax(Attribute):
    name = 'I_max'
    description = 'Maximum current'
    unit = 'A'
    unit_description = 'Ampere'
    static = True


class LengthAttr(Attribute):
    name = 'length'
    description = 'Line length'
    unit = 'km'
    unit_description = 'Kilometer'
    static = True


class RPerKm(Attribute):
    name = 'R_per_km'
    description = 'Resistance per unit length'
    unit = 'Ω/km'
    unit_description = 'Ohm per Kilometer'
    static = True


class XPerKm(Attribute):
    name = 'X_per_km'
    description = 'Reactance per unit length'
    unit = 'Ω/km'
    unit_description = 'Ohm per Kilometer'
    static = True


class CPerKm(Attribute):
    name = 'C_per_km'
    description = 'Capacity per unit length'
    unit = 'F/km'
    unit_description = 'Farad per Kilometer'
    static = True


class Online(Attribute):
    name = 'online'
    description = 'online mode'
    unit = ''
    unit_description = 'Boolean flag (True|False)'
    data_type = 'bool'
    static = True


class BranchType(Parameter):
    name = 'btype'
    description = 'branch type'
    data_type = 'string'
    lv_values = [
     'NA2XS2Y_120', 'NA2XS2Y_185', 'AL/ST_70/12/20']
    mv_values = ['NAYY_35', 'NAYY_50', 'NAYY_70', 'NAYY_95', 'NAYY_120', 'NAYY_150', 'NAYY_185', 'NAYY_240']
    accepted_values = lv_values + mv_values
    value = accepted_values[0]


class Length(Parameter):
    name = 'l'
    description = 'length in km'
    data_type = 'float'
    value = 0.1


class Branch(abstractLine.AbstractLine):
    name = 'Branch'
    description = 'Branch'
    simulator = pyPowerSimulator.PyPower()
    drawing_mode = 'line'
    icon = 'branch.svg'
    category = property(lambda self: _('Grid'))
    params = ObjectDict([abstractLine.FromBus, abstractLine.ToBus, BranchType, Length, abstractLine.Online])
    attrs = ObjectDict([abstractLine.PFrom, abstractLine.QFrom, abstractLine.PTo, abstractLine.QTo,
     IReal, IImag, SMax, IMax, LengthAttr, RPerKm, XPerKm, CPerKm, Online])
    docking_ports = [abstractLine.AbstractBusDockingPort(), abstractLine.AbstractBusDockingPort()]