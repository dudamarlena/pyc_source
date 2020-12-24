# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/loader.py
# Compiled at: 2018-09-04 03:34:18
# Size of source mod 2**32: 4530 bytes
"""
This piece of code searches for python code on specific path and
loads AbstractCheck classes from it.
"""
import inspect, logging, os, warnings, six
from ..core.checks.fmf_check import receive_fmf_metadata, FMFAbstractCheck
logger = logging.getLogger(__name__)

def path_to_module(path):
    if path.endswith('.py'):
        path = path[:-3]
    cleaned_path = path.replace('.', '').replace('-', '_')
    path_comps = cleaned_path.split(os.sep)[-2:]
    import_name = '.'.join(path_comps)
    if import_name[0] == '.':
        import_name = import_name[1:]
    return import_name


def _load_module(path):
    module_name = path_to_module(path)
    logger.debug("Will try to load selected file as module '%s'.", module_name)
    if six.PY3:
        from importlib.util import module_from_spec
        from importlib.util import spec_from_file_location
        s = spec_from_file_location(module_name, path)
        m = module_from_spec(s)
        s.loader.exec_module(m)
        return m
    if six.PY2:
        import imp
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            m = imp.load_source(module_name, path)
        return m


def should_we_load(kls):
    """ should we load this class as a check? """
    if kls.__name__.endswith('AbstractCheck'):
        return False
    else:
        if not kls.__name__.endswith('Check'):
            return False
        mro = kls.__mro__
        for m in mro:
            if m.__name__ == 'AbstractCheck':
                return True

        return False


def load_check_classes_from_file(path):
    logger.debug("Getting check(s) from the file '{}'.".format(path))
    m = _load_module(path)
    check_classes = []
    for _, obj in inspect.getmembers(m, inspect.isclass):
        if should_we_load(obj):
            if issubclass(obj, FMFAbstractCheck):
                node_metadata = receive_fmf_metadata(name=(obj.name), path=(os.path.dirname(path)))
                obj.metadata = node_metadata
            check_classes.append(obj)
            logger.debug("Check class '%s' loaded, module: '%s'", obj.__name__, obj.__module__)

    return check_classes


class CheckLoader(object):
    __doc__ = '\n    find recursively all checks on a given path\n    '

    def __init__(self, checks_paths):
        """
        :param checks_paths: list of str, directories where the checks are present
        """
        logger.debug("Will load checks from paths '%s'.", checks_paths)
        for p in checks_paths:
            if os.path.isfile(p):
                raise RuntimeError('Provided path %s is not a directory.' % p)

        self._check_classes = None
        self._mapping = None
        self.paths = checks_paths

    def obtain_check_classes(self):
        """ find children of AbstractCheck class and return them as a list """
        check_classes = set()
        for path in self.paths:
            for root, _, files in os.walk(path):
                for fi in files:
                    if not fi.endswith('.py'):
                        pass
                    else:
                        path = os.path.join(root, fi)
                        check_classes = check_classes.union(set(load_check_classes_from_file(path)))

        return list(check_classes)

    @property
    def check_classes(self):
        if self._check_classes is None:
            self._check_classes = self.obtain_check_classes()
        return self._check_classes

    @property
    def mapping(self):
        if self._mapping is None:
            self._mapping = {}
            for c in self.check_classes:
                self._mapping[c.name] = c

        return self._mapping