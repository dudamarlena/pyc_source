# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/nirspec_monitors/data_trending/utils/process_data.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 11317 bytes
"""This module holds functions for miri data trending

All functions in this module are tailored for the miri datatrending application.
Detailed descriptions are given for every function individually.

-------
    - Daniel Kühbacher

Use
---

Dependencies
------------
MIRI_trend_requestsDRAFT1900201.docx

References
----------

Notes
-----

"""
import jwql.instrument_monitors.nirspec_monitors.data_trending.utils.mnemonics as mn, jwql.instrument_monitors.nirspec_monitors.data_trending.utils.condition as cond, statistics, sqlite3, warnings, numpy as np
from collections import defaultdict

def extract_data(condition, mnemonic):
    """Function extracts data from given mnemmonic at a given condition
    Parameters
    ----------
    condition : object
        conditon object that holds one or more subconditions
    mnemonic : AstropyTable
        holds single table with mnemonic data
    Return
    ------
    temp : list  or None
        holds data that applies to given condition
    """
    temp = []
    for element in mnemonic:
        if condition.state(float(element['time'])):
            temp.append(float(element['value']))

    if len(temp) > 0:
        return temp
    else:
        return


def lamp_distinction(caa_flag, lamp_sel, lamp_curr, lamp_volt):
    """Distincts over all calibration lamps and returns representative current means
        each
    Parameters
    ----------
    """
    lamp_values = defaultdict(list)
    for index, flag in enumerate(caa_flag):
        if flag['value'] == 'ON':
            current_lamp = 'default'
            for lamp in lamp_sel:
                if lamp['time'] <= flag['time']:
                    current_lamp = lamp['value']

            if not current_lamp == 'NO_LAMP':
                if current_lamp == 'DUMMY':
                    pass
                else:
                    try:
                        start_time = flag['time']
                        i = 1
                        if caa_flag[(index + i)]['value'] == 'OFF':
                            end_time = caa_flag[(index + 1)]['time']
                        else:
                            i += 1
                    except IndexError:
                        break

                    temp_curr = []
                    temp_volt = []
                    for curr in lamp_curr:
                        if curr['time'] >= start_time:
                            if curr['time'] < end_time:
                                temp_curr.append(float(curr['value']))
                            else:
                                break

                    for volt in lamp_volt:
                        if volt['time'] >= start_time:
                            if volt['time'] < end_time:
                                temp_volt.append(float(volt['value']))
                            else:
                                break

                    lamp_data = []
                    lamp_data.append(start_time)
                    lamp_data.append(end_time)
                    lamp_data.append(len(temp_curr))
                    lamp_data.append(statistics.mean(temp_curr))
                    lamp_data.append(statistics.stdev(temp_curr))
                    lamp_data.append(len(temp_volt))
                    lamp_data.append(statistics.mean(temp_volt))
                    lamp_data.append(statistics.stdev(temp_volt))
                    lamp_values[current_lamp].append(lamp_data)

    return lamp_values


def extract_filterpos(move_stat, wheel_pos, wheel_val):
    """Extracts ratio values which correspond to given position values and their
       proposed nominals
    Parameters
    ----------
    condition : object
        conditon object that holds one or more subconditions
    nominals : dict
        holds nominal values for all wheel positions
    ratio_mem : AstropyTable
        holds ratio values of one specific mnemonic
    pos_mem : AstropyTable
        holds pos values of one specific mnemonic
    Return
    ------
    pos_values : dict
        holds ratio values and times with corresponding positionlabel as key
    """
    pos_values = defaultdict(list)
    for index, stat in enumerate(move_stat):
        if stat['value'] == 'SUCCESS':
            current_pos = 'default'
            pos_val = 0
            pos_time = 0
            for pos in wheel_pos:
                if pos['time'] <= stat['time']:
                    current_pos = pos['value']
                elif pos['time'] > stat['time']:
                    break

            for val in wheel_val:
                if val['time'] <= stat['time']:
                    pos_val = val['value']
                    pos_time = val['time']
                elif val['time'] > stat['time']:
                    break

            print(current_pos, pos_val, pos_time)
            if current_pos != 'default':
                pos_values[current_pos].append((pos_time, pos_val))
        else:
            continue

    return pos_values


def once_a_day_routine(mnemonic_data):
    """Routine for processing a 15min data file once a day
    Parameters
    ----------
    mnemonic_data : dict
        dict holds time and value in a astropy table with correspining identifier as key
    Return
    ------
    return_data : dict
        Holds extracted data with applied conditions
    """
    m = mnemonic_data
    return_data = dict()
    con_set_1 = [
     cond.unequal(m.mnemonic('INRSD_EXP_STAT'), 'STARTED')]
    condition_1 = cond.condition(con_set_1)
    for identifier in mn.mnemonic_cond_1:
        data = extract_data(condition_1, m.mnemonic(identifier))
        if data != None:
            return_data.update({identifier: data})
        else:
            print('no data for {}'.format(identifier))

    del condition_1
    con_set_2 = [
     cond.equal(m.mnemonic('INRSH_LAMP_SEL'), 'NO_LAMP')]
    condition_2 = cond.condition(con_set_2)
    for identifier in mn.mnemonic_cond_2:
        data = extract_data(condition_2, m.mnemonic(identifier))
        if data != None:
            return_data.update({identifier: data})
        else:
            print('no data for {}'.format(identifier))

    del condition_2
    con_set_3 = [
     cond.unequal(m.mnemonic('INRSM_MOVE_STAT'), 'STARTED')]
    condition_3 = cond.condition(con_set_3)
    for identifier in mn.mnemonic_cond_3:
        data = extract_data(condition_3, m.mnemonic(identifier))
        if data != None:
            return_data.update({identifier: data})
        else:
            print('no data for {}'.format(identifier))

    del condition_3
    return return_data


def whole_day_routine(mnemonic_data):
    """Proposed routine for processing a 15min data file once a day

    Parameters
    ----------
    mnemonic_data : dict
        dict holds time and value in a astropy table with correspining identifier as key

    Return
    ------
    data_cond_1 : dict
        holds extracted data with condition 1 applied
    data_cond_1 : dict
        holds extracted data with condition 2 applied
    """
    m = mnemonic_data
    return_data = dict()
    con_set_ft_10 = [
     cond.equal((m.mnemonic('ICTM_RT_FILTER')), 10, stringval=False)]
    condition_ft_10 = cond.condition(con_set_ft_10)
    for identifier in mn.mnemonic_ft10:
        data = extract_data(condition_ft_10, m.mnemonic(identifier))
        if data != None:
            return_data.update({identifier: data})
        else:
            print('no data for {}'.format(identifier))

    del condition_ft_10
    con_set_caa = [
     cond.equal(m.mnemonic('INRSH_CAA_PWRF_ST'), 'ON')]
    condition_caa = cond.condition(con_set_caa)
    for identifier in mn.mnemonic_caa:
        data = extract_data(condition_caa, m.mnemonic(identifier))
        if data != None:
            return_data.update({identifier: data})
        else:
            print('no data for {}'.format(identifier))

    del condition_caa
    data_lamps = lamp_distinction(m.mnemonic('INRSI_CAA_ON_FLAG'), m.mnemonic('INRSH_LAMP_SEL'), m.mnemonic('INRSI_C_CAA_CURRENT'), m.mnemonic('INRSI_C_CAA_VOLTAGE'))
    return (
     return_data, data_lamps)


def wheelpos_routine(mnemonic_data):
    """Proposed routine for positionsensors each day
    Parameters
    ----------
    mnemonic_data : dict
        dict holds time and value in a astropy table with correspining identifier as key
    Return
    ------
    FW : dict
        holds FW ratio values and times with corresponding positionlabel as key
    GW14 : dict
        holds GW14 ratio values and times with corresponding positionlabel as key
    GW23 : dict
        holds GW23 ratio values and times with corresponding positionlabel as key
    CCC : dict
        holds CCC ratio values and times with corresponding positionlabel as key
    """
    m = mnemonic_data
    FW = extract_filterpos(m.mnemonic('INRSI_FWA_MOVE_ST'), m.mnemonic('INRSI_FWA_MECH_POS'), m.mnemonic('INRSI_C_FWA_POSITION'))
    GWX = extract_filterpos(m.mnemonic('INRSI_GWA_MOVE_ST'), m.mnemonic('INRSI_GWA_MECH_POS'), m.mnemonic('INRSI_C_GWA_X_POSITION'))
    GWY = extract_filterpos(m.mnemonic('INRSI_GWA_MOVE_ST'), m.mnemonic('INRSI_GWA_MECH_POS'), m.mnemonic('INRSI_C_GWA_Y_POSITION'))
    return (
     FW, GWX, GWY)


if __name__ == '__main__':
    pass