# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/vdj/params.py
# Compiled at: 2014-12-16 17:37:19
"""params.py

Define directory and file names that must be manually modified
to point to certain resources.
"""
import os, warnings
warnings.simplefilter('always')

def parse_config_file(path=os.path.expanduser('~/.vdjconfig')):
    config_data = {}
    ip = open(path, 'r')
    for line in ip:
        if line.startswith('#') or line.strip() == '':
            continue
        data = map(lambda s: s.strip(), line.split('\t'))
        config_data[data[0]] = data[1]

    ip.close()
    return config_data


config_data = parse_config_file()
try:
    vdj_dir = config_data['vdj_dir']
except KeyError:
    print 'Could not successfully set vdj_dir.  Does ~/.vdjconfig exist?'
    raise

try:
    imgt_dir = config_data['imgt_dir']
except KeyError:
    warning.warn('Could not find imgt_dir in .vdjconfig. May cause problems loading refseq.')

data_dir = 'data'
processed_dir = 'processed'
organism = 'human'