# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\utils\simInit.py
# Compiled at: 2015-02-17 03:50:15
# Size of source mod 2**32: 2337 bytes
import csv, os
from maverig.data import dataHandler
from maverig.data.components.utils.pyPowerSerializer import PyPowerSerializer
from maverig.utils.scenarioErrors import ScenarioConnectionError

def on_sim_init_parents_pypower(model, elem):
    return [
     {'elem_id': 'PyPower.Grid_0', 
      'sim_model': 'PyPower.Grid', 
      'params': {'gridfile': PyPowerSerializer().serialize_to_file(model.elements)}, 
      'attrs': {},  'docking_ports': {}}]


def on_sim_init_powertransmitter(model, elem):
    """ fill docking dependent parameters """
    try:
        elem['params']['fbus'], _ = elem['docking_ports']['0']['out'][0]
        elem['params']['tbus'], _ = elem['docking_ports']['1']['out'][0]
    except:
        raise ScenarioConnectionError(elem['elem_id'])


def on_set_param_house(model, elem, param_name):

    def set_nums():
        """ returns number of households from csv """
        filename = dataHandler.get_normpath(elem['params']['datafile'])
        elem['params']['num_hh'] = 1
        if os.path.isfile(filename):
            file_ = open(filename, 'rU')
            data = csv.reader(file_, delimiter=',')
            for row in data:
                row = [field.strip() for field in row]
                if 'num_hh' in row:
                    num_hh_index = row.index('num_hh')
                    num_res_index = row.index('num_res')
                    row = next(data)
                    elem['params']['num_hh'] = int(row[num_hh_index])
                    elem['params']['num_res'] = int(row[num_res_index])
                    break

            file_.close()

    def set_icon():
        """ returns number of households from csv and change the household icon"""
        elem['icon'] = 'house.svg'
        if elem['params']['num_hh'] > 2:
            elem['icon'] = 'house2-4.svg'
        elif elem['params']['num_hh'] > 4:
            elem['icon'] = 'house4+.svg'

    if param_name == 'datafile':
        set_nums()
        set_icon()
        if elem['params']['P_max'] % 1118 == 0:
            elem['params']['P_max'] = elem['params']['num_hh'] * 1118