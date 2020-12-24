# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/codec_interface/utils.py
# Compiled at: 2014-02-04 19:25:36
# Size of source mod 2**32: 511 bytes
import importlib, glob, os, logging

def load_all_codecs():
    for module in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
        module = os.path.basename(module)
        if not module.startswith('_') and module != 'utils.py' and module != 'base_codec.py':
            logging.info('utils.py(codec_interface): Loading "{}"'.format(module))
            importlib.import_module('.' + module[:-3], 'batman.codec_interface')
            continue