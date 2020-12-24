# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/schemes.py
# Compiled at: 2017-12-07 11:03:48
# Size of source mod 2**32: 205 bytes
import yaml
schemes = {'base':yaml.load(open('yamls/arkdbschema.yaml')), 
 'ark':yaml.load(open('yamls/arkdbschema.yaml')), 
 'oxycoin':yaml.load(open('yamls/oxycoindbschema.yaml'))}