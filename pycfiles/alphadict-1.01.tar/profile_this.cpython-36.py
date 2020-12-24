# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/utils/profile_this.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 781 bytes
__doc__ = '\nModule profile_this: decorator that profiles a function\n'
import cProfile

def profile_this(fn):

    def profiled_fn(*args, **kwargs):
        filename = fn.__name__ + '.profile'
        prof = cProfile.Profile()
        ret = (prof.runcall)(fn, *args, **kwargs)
        prof.dump_stats(filename)
        return ret

    return profiled_fn


if __name__ == '__main__':

    def f1():
        a = [x * x for x in range(10000)]
        return a


    def f2():
        a = [x * x for x in range(20000)]
        return a


    def f3():
        a = [x * x for x in range(30000)]
        return a


    @profile_this
    def test():
        f1()
        f2()
        f3()


    test()
    print('Profile is available in test.profile.Use runsnake or snakeviz to view it')