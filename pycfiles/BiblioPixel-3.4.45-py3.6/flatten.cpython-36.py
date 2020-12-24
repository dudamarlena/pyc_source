# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/flatten.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2183 bytes


def flatten(master):
    """
    :param dict master: a multilevel dictionary
    :return: a flattened dictionary
    :rtype: dict

    Flattens a multilevel dictionary into a single-level one so that::

        {'foo':
            {'bar':
               {
                   'a': 1,
                   'b': True,
                   'c': 'hello',
                },
            },
        }

    would become::

        {'foo.bar.a': 1,
         'foo.bar.b': True,
         'foo.bar.a': 1,
         }

    You can mix and match both input (hierarchical) and output (dotted) formats
    in the input without problems - and if you call flatten more than once, it
    has no effect.
    """
    result = {}

    def add(value, *keys):
        if keys in result:
            raise ValueError('Duplicate key %s' % keys)
        result[keys] = value

    def recurse(value, *keys):
        if isinstance(value, dict):
            for k, v in value.items():
                recurse(v, k, *keys)

        else:
            key = '.'.join(reversed(keys))
            if key in result:
                raise ValueError('Duplicate key %s' % str(keys))
            result[key] = value

    recurse(master)
    return result


def unflatten(master):
    """
    :param dict master: a multilevel dictionary
    :return: a unflattened dictionary
    :rtype: dict

    Unflattens a single-level dictionary a multilevel into one so that::

        {'foo.bar.a': 1,
         'foo.bar.b': True,
         'foo.bar.a': 1,
         }

    would become::

        {'foo':
            {'bar':
               {
                   'a': 1,
                   'b': True,
                   'c': 'hello',
                },
            },
        }
    """
    result = {}
    for k, v in master.items():
        *first, last = k.split('.')
        r = result
        for i in first:
            r = r.setdefault(i, {})

        r[last] = v

    return result


def canonical(master):
    """
    :param dict master: a multilevel dictionary
    :return: a canonicalized dictionary that has been completely flattened
             and then unflattened
    :rtype: dict
    """
    return unflatten(flatten(master))