# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/Deco.py
# Compiled at: 2008-03-17 12:58:02
__rev_id__ = '$Id: Deco.py,v 1.4 2005/07/20 07:24:11 rvk Exp $'

def accepts(*types):

    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount

        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), 'arg %r does not match %s' % (a, t)

            return f(*args, **kwds)

        new_f.func_name = f.func_name
        return new_f

    return check_accepts


def returns(rtype):

    def check_returns(f):

        def new_f(*args, **kwds):
            result = f(*args, **kwds)
            assert isinstance(result, rtype), 'return value %r does not match %s' % (result, rtype)
            return result

        new_f.func_name = f.func_name
        return new_f

    return check_returns


if __name__ == '__main__':
    import types

    @returns(types.NoneType)
    @accepts(int, (int, float))
    def func(arg1, arg2):
        pass


    func(1, 2)