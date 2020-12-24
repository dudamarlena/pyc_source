# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyenergy/upgrade.py
# Compiled at: 2014-03-19 12:23:45
"""Energy measurement upgrade tool.

This tools loads pickled objects, upgrades any Measurement types it finds
and then writes the objects back to the file. This is mostly useful for
data saved in the old namedtuple Measurement format, as other measurement
will get upgraded on load anyway.

Usage:
    measurement-upgrade [-v | -vv] FILENAME

Options
    --verbose -v        Be verbose
"""
import pyenergy, logging
from docopt import docopt
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
warning = logger.warning
error = logger.error
info = logger.info
import pickle, sys

def _reconstructor_hack(cls, base, state):
    if base is object:
        obj = object.__new__(cls)
    elif cls == pyenergy.Measurement and base is tuple:
        if not hasattr(_reconstructor_hack, 'warned'):
            warning('Loading from unversioned pickled file.')
            _reconstructor_hack.warned = True
        return pyenergy.Measurement(*state)
    obj = base.__new__(cls, state)
    if base.__init__ != object.__init__:
        base.__init__(obj, state)
    return obj


def find_class_hack(self, module, name):
    if name == '_reconstructor':
        return _reconstructor_hack
    __import__(module)
    mod = sys.modules[module]
    klass = getattr(mod, name)
    return klass


def updateOldPickle(fname):
    oldfind = pickle.Unpickler.find_class
    pickle.Unpickler.find_class = find_class_hack
    objs = []
    f = open(fname, 'r')
    while True:
        try:
            o = pickle.load(f)
            objs.append(o)
        except EOFError:
            break

    f.close()
    print o[0][0]
    f = open(fname, 'w')
    for o in objs:
        pickle.dump(o, f)

    f.close()
    pickle.Unpickler.oldfind = find_class_hack


def main():
    arguments = docopt(__doc__)
    logging.basicConfig()
    if arguments['--verbose'] == 1:
        logging.getLogger('').setLevel(logging.INFO)
    elif arguments['--verbose'] == 2:
        logging.getLogger('').setLevel(logging.DEBUG)
    updateOldPickle(arguments['FILENAME'])


if __name__ == '__main__':
    main()