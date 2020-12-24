# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/metaclasses.py
# Compiled at: 2013-11-30 16:54:41


def _generatemetaclass(bases, metas):
    """Internal function called by child"""
    if metas == (type,):
        metabases = ()
        metaname = '_'
    else:
        metabases = metas
        metaname = '_' + ('').join([ m.__name__ for m in metas ])
    trivial = lambda m: m in metabases or m is type
    for b in bases:
        meta_b = type(b)
        if not trivial(meta_b):
            metabases += (meta_b,)
            metaname += meta_b.__name__

    if not metabases:
        return type
    else:
        if len(metabases) == 1:
            return metabases[0]
        return type(metaname, metabases, {})


def child(*bases, **options):
    """Class factory avoiding metatype conflicts: if the base classes have
   metaclasses conflicting within themselves or with the given metaclass,
   it automatically generates a compatible metaclass and instantiate the
   child class from it. The recognized keywords in the option dictionary
   are name, dic and meta."""
    name = options.get('name', ('').join([ b.__name__ for b in bases ]) + '_')
    dic = options.get('dic', {})
    metas = options.get('metas', (type,))
    return _generatemetaclass(bases, metas)(name, bases, dic)


def test():

    class M_A(type):
        pass

    class M_B(type):
        pass

    A = M_A('A', (), {})
    B = M_B('B', (), {})
    try:

        class C(A, B):
            pass

    except TypeError:
        pass
    else:
        raise RuntimeError

    C = child(A, B, name='C')


if __name__ == '__main__':
    test()