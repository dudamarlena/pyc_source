# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/agacsayisi/tree.py
# Compiled at: 2018-08-01 09:35:08
# Size of source mod 2**32: 2296 bytes


def numberOfTrees(co2_amount):
    tree = co2_amount / 11.7934016
    return tree


def multiplier(energy=23844012, coeff=0.45110999999999996):
    result = coeff * energy
    return result


def coefficient(energy=23844012, nat_gas=28, imp_coal=16, lignite=15, coal=1, wind_power=5, geothermal_energy=3, solar_energy=3):
    ton1 = energy * nat_gas / 100 * 499 / 1000
    ton2 = energy * imp_coal / 100 * 888 / 1000
    ton3 = energy * lignite / 100 * 1054 / 1000
    ton4 = energy * coal / 100 * 888 / 1000
    ton5 = energy * wind_power / 100 * 10 / 1000
    ton6 = energy * geothermal_energy / 100 * 38 / 1000
    ton7 = energy * solar_energy / 100 * 23 / 1000
    summation = ton1 + ton2 + ton3 + ton4 + ton5 + ton6 + ton7
    coeff = summation / energy
    return coeff