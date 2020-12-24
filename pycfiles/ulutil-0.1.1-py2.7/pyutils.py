# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/pyutils.py
# Compiled at: 2014-12-19 21:47:08
import copy, string, collections, contextlib

@contextlib.contextmanager
def as_handle(handleish, mode='r', **kwargs):
    """Open handleish as file.
    
    Stolen from Biopython
    """
    if isinstance(handleish, basestring):
        with open(handleish, mode, **kwargs) as (fp):
            yield fp
    else:
        yield handleish


cleanup_table = string.maketrans('/*|><+ ', '_____p_')

def cleanup_id(identifier):
    return identifier.translate(cleanup_table)


class nesteddict(collections.defaultdict):
    """Nested dictionary structure.
    
    Based on Stack Overflow question 635483
    """

    def __init__(self, default=None):
        if default == None:
            collections.defaultdict.__init__(self, nesteddict)
        else:
            collections.defaultdict.__init__(self, default)
        self.locked = False
        return

    def lock(self):
        self.default_factory = None
        self.locked = True
        for value in self.itervalues():
            if isinstance(value, nesteddict):
                value.lock()

        return

    def unlock(self):
        self.default_factory = nesteddict
        self.locked = False
        for value in self.itervalues():
            if isinstance(value, nesteddict):
                value.unlock()

    def islocked(self):
        return self.locked

    def todict(self):
        raise NotImplementedError
        for key, val in self.iteritems():
            if isinstance(val, nesteddict):
                val.todict()
                self[key] = dict(val)

        self = dict(self)

    @staticmethod
    def asdict(d):
        d = copy.deepcopy(d)
        for key, val in d.iteritems():
            if isinstance(val, nesteddict):
                d[key] = nesteddict.asdict(val)

        return dict(d)

    def nested_setdefault(self, keylist, default):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]

        key = keylist[(-1)]
        return curr_dict.setdefault(key, default)

    def nested_get(self, keylist, default):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]

        key = keylist[(-1)]
        return curr_dict.get(key, default)

    def nested_assign(self, keylist, val):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]

        key = keylist[(-1)]
        curr_dict[key] = val
        return self

    def walk(self):
        for key, value in self.iteritems():
            if isinstance(value, nesteddict):
                for tup in value.walk():
                    yield (
                     key,) + tup

            else:
                yield (
                 key, value)

    def nested_increment(self, keylist, increment=1):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]

        key = keylist[(-1)]
        curr_dict[key] = curr_dict.get(key, 0) + increment

    def nested_add(self, keylist, obj):
        curr_dict = self
        for key in keylist[:-1]:
            curr_dict = curr_dict[key]

        key = keylist[(-1)]
        curr_dict.setdefault(key, set()).add(obj)