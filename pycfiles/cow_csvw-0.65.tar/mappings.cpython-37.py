# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amp/src/COW/src/converter/mappings.py
# Compiled at: 2019-06-11 08:11:14
# Size of source mod 2**32: 1607 bytes
"""DEPRECATED"""
napp = {'mappings':{'AGE': lambda x: x.zfill(3)}, 
 'nocode':[
  'BPLPARSE', 'CFU', 'COUNTYUS',
  'ENUMDIST', 'FAMUNIT', 'HEADLOC', 'HHNBRNO',
  'LINENUM', 'MOMLOC', 'NAMEFRST', 'NAMELAST', 'NHGISJOIN',
  'OCCSTRNG', 'PAGENUM', 'PARISHGB', 'PARSE', 'PERNUM',
  'POPLOC', 'QOCCGB', 'RECTYPE', 'REEL', 'RESLSNO',
  'SDSTCA', 'SEAUS', 'SERVANTS', 'SPLOC'], 
 'integer':[
  'AGE', 'CFUSIZE', 'CITYPOP', 'CNTYAREA', 'ELDCH', 'HHWT',
  'NCOUPLES', 'NFAMS', 'NMOTHERS', 'NUMPERHH', 'OCSCORUS',
  'PERWT', 'REALPROP', 'RELATS', 'SEIUS', 'SERIAL', 'YEAR',
  'YNGCH', 'YRSUSA1']}
canfam = {'mappings':{'relhead2': lambda x: x[0:3]}, 
 'nocode':[
  'occ', 'hhdid', 'indlnm', 'indfnm', 'dwellid', 'chknote',
  'indnote', 'location'], 
 'integer':[
  'ageyr', 'magemo', 'moschool', 'urbpop', 'earnings', 'earnper', 'exearn']}
mosaic = {'nocode':[
  'fname', 'lname', 'occupat'], 
 'integer':[
  'age', 'hhsize', 'year']}