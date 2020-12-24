# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/config/resources.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 674 bytes
"""
Created on Feb 1, 2018

@author: stelios
"""
import os
datahost = os.environ.get('datahost', '')
datadata = os.environ.get('datadata', 'ATLASDR1')
datauser = os.environ.get('datauser', '')
datapass = os.environ.get('datapass', '')
adminuser = os.environ.get('adminuser', '')
adminpass = os.environ.get('adminpass', '')
admingroup = os.environ.get('admingroup', '')
datacatalog = os.environ.get('datacatalog', 'ATLASDR1')
datatype = os.environ.get('datatype', 'mssql')
datadriver = 'net.sourceforge.jtds.jdbc.Driver'
dataurl = os.environ.get('dataurl', '')
endpoint = os.environ.get('endpoint', '')
osa_endpoint = os.environ.get('osa_endpoint', '')
maxrows = os.environ.get('maxrows', 1000000)