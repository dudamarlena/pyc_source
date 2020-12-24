# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/endpoint.py
# Compiled at: 2019-09-06 04:57:09
# Size of source mod 2**32: 1089 bytes
__all__ = [
 'endpoint']
import os, sys

def create(myvdfile, myvdefile, myvdsfile):
    os.system('python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/entete.py VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json ' + myvdfile)
    os.system('python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/sets.py VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json ' + myvdefile)
    os.system('python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/dimensionContent.py VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json ' + myvdefile + ' ' + myvdsfile)
    os.system('python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/resultat.py VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json ' + myvdfile)