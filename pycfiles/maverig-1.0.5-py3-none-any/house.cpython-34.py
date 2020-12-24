# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\house.py
# Compiled at: 2014-12-11 18:17:41
# Size of source mod 2**32: 2827 bytes
import gettext, locale, os, csv
from maverig.data import dataHandler
from maverig.data.components.abstractComponent import DockingPort, Attribute, Parameter
from maverig.data.components.utils.dataObject import ObjectDict
from maverig.data.components.abstract import abstractCSV
from maverig.data.components.simulators import csvSimulator
current_language, encoding = locale.getdefaultlocale()
locale_path = dataHandler.get_lang_path()
language = gettext.translation(current_language, locale_path, [current_language])
language.install()

class PMaxAttr(Attribute):
    name = 'p_max'
    description = 'Maximum Power'
    data_type = 'float'
    unit = 'W'
    unit_description = 'Watt'
    static = True


class NumHouseholdsAttr(Attribute):
    name = 'num_hh'
    description = 'number of households'
    data_type = 'int'
    unit = ''
    unit_description = ''
    static = True


class NumResidents(Attribute):
    name = 'num_res'
    description = 'number of residents'
    data_type = 'int'
    unit = ''
    unit_description = ''
    static = True


class PMaxParam(Parameter):
    public = False
    name = 'p_max'
    description = 'Maximum Power in W'
    data_type = 'float'
    value = 1118


class House(abstractCSV.AbstractCSV):
    name = 'House'
    description = 'House'
    simulator = csvSimulator.CSVSimulator()
    drawing_mode = 'icon'
    icon = 'house.svg'
    category = property(lambda self: _('Consumers'))
    params = ObjectDict([abstractCSV.SimStart, abstractCSV.DataFile, PMaxParam])
    attrs = ObjectDict([abstractCSV.P, PMaxAttr, NumHouseholdsAttr, NumResidents])
    docking_ports = [
     DockingPort(), abstractCSV.BusDockingPort()]

    def prepare_params(self, **global_params):
        """ get complete file names """
        self.params['p_max'].value = self.get_num_hh() * 1118
        super().prepare_params(**global_params)

    def get_num_hh(self):
        """ returns number of households from csv """
        filename = dataHandler.get_normpath(self.params['datafile'].value)
        num_hh = 1
        if os.path.isfile(filename):
            file_ = open(filename, 'rU')
            data = csv.reader(file_, delimiter=',')
            for row in data:
                if 'num_hh' in row:
                    i = row.index('num_hh')
                    row = next(data)
                    num_hh = int(row[i])
                    break

            file_.close()
        return num_hh

    def update_icon(self):
        """ returns number of households from csv and change the household icon"""
        num_hh = self.get_num_hh()
        self.icon = 'house.svg'
        if num_hh > 2:
            self.icon = 'house2-4.svg'
        if num_hh > 4:
            self.icon = 'house4+.svg'