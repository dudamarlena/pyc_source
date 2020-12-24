# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev\pylib\visvis\utils\ssdf\tests\test_random.py
# Compiled at: 2017-05-31 18:20:46
# Size of source mod 2**32: 10934 bytes
""" Script test_random

Create random ssdf structs, serialize these, read back, and test if
they represent the same data.

"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, time, sys, random, string, numpy as np, ssdf
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    text_type = str
    binary_type = bytes
    ascii_type = str
    unichr = chr
    xrange = range
else:
    string_types = (
     basestring,)
    text_type = unicode
    binary_type = str
    ascii_type = str
homedir = '/home/almar/'
if not os.path.isdir(homedir):
    homedir = 'c:/almar/'
CHARS = string.printable + (unichr(169) + unichr(181) + unichr(202) + unichr(1220) + unichr(1138) + unichr(1297))
NAMECHARS = str('abcdefghijklmnopqrstuvwxyz_0123456789')

class Generator:

    def random_object(self, level):
        if level > 0:
            id = random.randrange(7) + 1
        else:
            id = random.randrange(5) + 1
        if id == 1:
            return
        if id == 2:
            return self.random_int()
        if id == 3:
            return self.random_float()
        if id == 4:
            return self.random_string()
        if id == 5:
            return self.random_array()
        if level > 0:
            if id == 6:
                return self.random_list(level)
        if level > 0:
            if id == 7:
                return self.random_struct(level)

    def random_int(self):
        return random.randint(-4611686018427387904, 4611686018427387904)

    def random_float(self):
        return (random.random() - 0.5) * 10000

    def random_string(self, maxn=16):
        n = random.randrange(0, maxn)
        return ''.join(random.sample(CHARS, n))

    def random_array(self, maxn=16):
        ndim = random.randrange(0, 4)
        shape = random.sample(xrange(maxn), ndim)
        dtype = random.choice([key for key in ssdf.ssdf_text._DTYPES.keys()])
        if 'int' in dtype:
            return np.random.random_integers(0, 100, shape).astype(dtype)
        else:
            return np.random.random_sample(shape).astype(dtype)

    def random_struct(self, level, maxn=16):
        level -= 1
        s = ssdf.new()
        n = random.randrange(0, maxn)
        for i in range(n):
            n = random.randrange(0, maxn)
            name = random.choice(NAMECHARS[:-10])
            name += ''.join(random.sample(NAMECHARS, n))
            if name.startswith('__'):
                name = 'x' + name
            s[name] = self.random_object(level)

        if random.random() > 0.5:
            return s
        else:
            return s.__dict__

    def random_list(self, level, maxn=16):
        level -= 1
        items = []
        n = random.randrange(0, maxn)
        for i in range(n):
            items.append(self.random_object(level))

        if random.random() > 0.5:
            return items
        else:
            return tuple(items)

    @classmethod
    def create_struct(cls, level=8):
        gen = cls()
        return gen.random_struct(level)


def compare(ob1, ob2, verbose=True):
    """ compare(ob1, ob2, verbose=True)
    
    Compare two (ssdf-compatible) objects. If verbose is True (the default)
    and the objects are not equal, a message is printed indicating the
    first found inequality.
    
    """
    not_equal = ssdf.ssdf_base._not_equal(ob1, ob2)
    if verbose:
        if not_equal:
            print(not_equal)
    return not not_equal


class Tester:

    def __init__(self):
        self._tests = []
        self._stop = False
        self._s = None

    def enable_np(self):
        ssdf.np = np

    def disable_np(self):
        ssdf.np = None

    def run(self, amount=100000):
        self._stop = False
        t0 = time.time()
        maxtests = amount
        while len(self._tests) < maxtests and not self._stop:
            s = Generator.create_struct()
            n = ssdf.count(s)
            self._s = s
            times = []
            sizes = []
            t1 = time.time()
            text = ssdf.saves(s)
            times.append(time.time() - t1)
            t1 = time.time()
            s2 = ssdf.loads(text)
            times.append(time.time() - t1)
            if not compare(s, s2):
                print('Test text failed after %i iterations.' % len(self._tests))
                break
            t1 = time.time()
            bb = ssdf.saveb(s)
            times.append(time.time() - t1)
            t1 = time.time()
            s2 = ssdf.loadb(bb)
            times.append(time.time() - t1)
            if not compare(s, s2):
                print('Test bin failed after %i iterations.' % len(self._tests))
                break
            fname = homedir + 'projects/ssdftest.ssdf'
            t1 = time.time()
            ssdf.save(fname, s)
            times.append(time.time() - t1)
            t1 = time.time()
            s2 = ssdf.load(fname)
            times.append(time.time() - t1)
            sizes.append(os.stat(fname).st_size)
            if not compare(s, s2):
                print('Test text-file failed after %i iterations.' % len(self._tests))
                break
            fname = homedir + 'projects/ssdftest.bsdf'
            t1 = time.time()
            ssdf.save(fname, s)
            times.append(time.time() - t1)
            t1 = time.time()
            s2 = ssdf.load(fname)
            times.append(time.time() - t1)
            sizes.append(os.stat(fname).st_size)
            if not compare(s, s2):
                print('Test bin-file failed after %i iterations.' % len(self._tests))
                break
            self._tests.append((n, times, sizes))
            print('%i tests successfull' % len(self._tests))
            time.sleep(0.001)

    def test_numpy(self, amount=10):
        for iter in range(amount):
            s = Generator.create_struct()
            self._s = s
            self.enable_np()
            text = ssdf.saves(s)
            self.disable_np()
            s2 = ssdf.loads(text)
            text = ssdf.saves(s2)
            self.enable_np()
            s3 = ssdf.loads(text)
            if not compare(s, s3):
                print('Test text failed after %i iterations.' % iter)
                break
            self.enable_np()
            bb = ssdf.saveb(s)
            self.disable_np()
            s2 = ssdf.loadb(bb)
            bb = ssdf.saveb(s2)
            self.enable_np()
            s3 = ssdf.loadb(bb)
            if not compare(s, s3):
                print('Test bin failed after %i iterations.' % iter)
                break
            print('%i tests successfull' % iter)
            time.sleep(0.001)

        self.enable_np()


def find(s, name):
    """ To find an object with a certain name.
    """
    for n in s:
        if ssdf.isstruct(s):
            v = s[n]
        else:
            v = n
            n = None
        res = None
        if n == name:
            return v
        if ssdf.isstruct(v) or isinstance(v, dict):
            res = find(v, name)
        else:
            if isinstance(v, (list, tuple)):
                res = find(v, name)
            else:
                if n:
                    print(n)
        if res:
            return res


def show(self):
    import visvis as vv
    if len(self._tests) > 1000:
        tests = random.sample(self._tests, 1000)
    else:
        tests = self._tests
    nn = [test[0] for test in tests]
    vv.figure(1)
    vv.clf()
    plotKwargsText = {'ms':'.', 
     'mc':'b',  'mw':5,  'ls':''}
    plotKwargsBin = {'ms':'.',  'mc':'r',  'mw':5,  'ls':''}
    vv.subplot(221)
    (vv.plot)(nn, [test[2][0] for test in tests], **plotKwargsText)
    (vv.plot)(nn, [test[2][1] for test in tests], **plotKwargsBin)
    vv.legend('text', 'binary')
    vv.title('File size')
    vv.subplot(223)
    (vv.plot)(nn, [test[1][4] for test in tests], **plotKwargsText)
    (vv.plot)(nn, [test[1][6] for test in tests], **plotKwargsBin)
    vv.legend('text', 'binary')
    vv.title('Save time')
    vv.subplot(224)
    (vv.plot)(nn, [test[1][5] for test in tests], **plotKwargsText)
    (vv.plot)(nn, [test[1][7] for test in tests], **plotKwargsBin)
    vv.legend('text', 'binary')
    vv.title('Load time')


if __name__ == '__main__':
    tester = Tester()
    tester.run()