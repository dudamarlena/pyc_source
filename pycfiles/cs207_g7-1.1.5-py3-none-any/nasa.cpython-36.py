# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/nasa.py
# Compiled at: 2017-11-19 20:34:23
# Size of source mod 2**32: 1072 bytes
import sqlite3, os

def getNASACoeff(species, temperature):
    db = sqlite3.connect(os.path.dirname(__file__) + '/data/NASA.sqlite')
    cursor = db.cursor()
    lowTemp = 'SELECT * FROM LOW WHERE SPECIES_NAME = "{}" \t\tAND TLOW <= {} AND THIGH >= {}'.format(species, temperature, temperature)
    highTemp = 'SELECT * FROM HIGH WHERE SPECIES_NAME = "{}" \t\tAND TLOW <= {} AND THIGH >= {}'.format(species, temperature, temperature)
    output = cursor.execute(lowTemp).fetchall()
    if len(output) == 0:
        output = cursor.execute(highTemp).fetchall()
    if len(output) == 0:
        cursor.close()
        raise Exception('Unable to find valid NASA coefficients for {} at {}'.format(species, temperature))
    cursor.close()
    return list(output[0])[3:]