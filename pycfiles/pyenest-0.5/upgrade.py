# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyenergy/upgrade.py
# Compiled at: 2014-03-19 12:23:45
__doc__ = 'Energy measurement upgrade tool.\n\nThis tools loads pickled objects, upgrades any Measurement types it finds\nand then writes the objects back to the file. This is mostly useful for\ndata saved in the old namedtuple Measurement format, as other measurement\nwill get upgraded on load anyway.\n\nUsage:\n    measurement-upgrade [-v | -vv] FILENAME\n\nOptions\n    --verbose -v        Be verbose\n'
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