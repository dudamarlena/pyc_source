# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/amp/src/COW/src/converter/mappings.py
# Compiled at: 2019-06-11 08:11:14
__doc__ = 'DEPRECATED'
napp = {'mappings': {'AGE': lambda x: x.zfill(3)}, 
   'nocode': [
            'BPLPARSE', 'CFU', 'COUNTYUS',
            'ENUMDIST', 'FAMUNIT', 'HEADLOC', 'HHNBRNO',
            'LINENUM', 'MOMLOC', 'NAMEFRST', 'NAMELAST', 'NHGISJOIN',
            'OCCSTRNG', 'PAGENUM', 'PARISHGB', 'PARSE', 'PERNUM',
            'POPLOC', 'QOCCGB', 'RECTYPE', 'REEL', 'RESLSNO',
            'SDSTCA', 'SEAUS', 'SERVANTS', 'SPLOC'], 
   'integer': [
             'AGE', 'CFUSIZE', 'CITYPOP', 'CNTYAREA', 'ELDCH', 'HHWT',
             'NCOUPLES', 'NFAMS', 'NMOTHERS', 'NUMPERHH', 'OCSCORUS',
             'PERWT', 'REALPROP', 'RELATS', 'SEIUS', 'SERIAL', 'YEAR',
             'YNGCH', 'YRSUSA1']}
canfam = {'mappings': {'relhead2': lambda x: x[0:3]}, 
   'nocode': [
            'occ', 'hhdid', 'indlnm', 'indfnm', 'dwellid', 'chknote',
            'indnote', 'location'], 
   'integer': [
             'ageyr', 'magemo', 'moschool', 'urbpop', 'earnings', 'earnper', 'exearn']}
mosaic = {'nocode': [
            'fname', 'lname', 'occupat'], 
   'integer': [
             'age', 'hhsize', 'year']}