# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/kohlrabi/lib/python3.5/site-packages/libkohlrabi/server.py
# Compiled at: 2016-04-01 07:48:41
# Size of source mod 2**32: 1278 bytes
"""
Main server class.
"""
import importlib, logging, sys, traceback
from libkohlrabi.kohlrabi import Kohlrabi
logging.basicConfig(filename='/dev/null', level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s -> %(message)s')
root = logging.getLogger()
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root.addHandler(consoleHandler)
logger = logging.getLogger('Kohlrabi')

def run(args):
    logger.info('Starting Kohlrabi server...')
    obj = args.app_object
    mod = obj.split(':')[0]
    try:
        mod_o = importlib.import_module(mod)
    except ImportError:
        logger.error('Could not load module {}'.format(mod))
        traceback.print_exc()
        sys.exit(1)

    vegetable = obj.split(':')[1]
    try:
        veg_obj = getattr(mod_o, vegetable)
        assert isinstance(veg_obj, Kohlrabi)
    except AttributeError:
        logger.error('Could not load object {} from module {}'.format(vegetable, mod))
        sys.exit(1)
    except AssertionError:
        logger.error('Specified object {} was not a Kohlrabi instance.'.format(vegetable))
        logger.error('Instead, it was a {}'.format())
        sys.exit(1)

    veg_obj.begin()