# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/matchengine/settings.py
# Compiled at: 2017-02-10 11:07:01
"""Copyright 2016 Dana-Farber Cancer Institute"""
import os, sys, json, logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
TUMOR_TREE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/tumor_tree.txt'))
months = [
 'January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
MONGO_URI = 'mongodb://localhost:27017/matchminer?replicaSet=rs0'
uri_check = os.getenv('MONGO_URI', None)
if uri_check:
    MONGO_URI = uri_check