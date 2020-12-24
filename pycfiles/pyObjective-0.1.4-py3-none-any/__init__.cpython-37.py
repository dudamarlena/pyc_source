# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\IT\python\dist\pyobject-1.0\pyobject\__init__.py
# Compiled at: 2020-05-10 07:18:39
# Size of source mod 2**32: 3392 bytes
__doc__ = '一个Python对象浏览器模块。\nA python object browser with tkinter and command-lines.\n\n'
import sys
from pprint import pprint
__email__ = '3416445406@qq.com'
__author__ = '七分诚意 qq:3076711200 邮箱:%s' % __email__
__version__ = '1.0'
_ignore_names = [
 '__builtins__', '__doc__']

def objectname(obj):
    """objectname(obj) - 返回一个对象的名称,形如xxmodule.xxclass。
如:objectname(int) -> 'builtins.int'"""
    if not obj.__class__ == type:
        obj = obj.__class__
    if obj.__module__ == '__main__':
        return obj.__name__
    return '{}.{}'.format(obj.__module__, obj.__name__)


def bases(obj, level=0, tab=4):
    """bases(obj) - 打印出该对象的基类
tab:缩进的空格数,默认为4。"""
    if not obj.__class__ == type:
        obj = obj.__class__
    if obj.__bases__:
        if level:
            print((' ' * (level * tab)), end='')
        print(*obj.__bases__, **{'sep': ','})
        for cls in obj.__bases__:
            bases(cls, level, tab)


def shortrepr(obj, maxlength=150):
    result = repr(obj)
    if len(result) > maxlength:
        return result[:maxlength] + '...'
    return result


def describe(obj, level=0, maxlevel=1, tab=4, verbose=False):
    """"描述"一个对象,即打印出对象的各个属性。
参数说明:
maxlevel:打印对象属性的层数。
tab:缩进的空格数,默认为4。
verbose:一个布尔值,是否打印出对象的特殊方法(如__init__)。
"""
    if level == maxlevel:
        result = repr(obj)
        if result.startswith('[') or result.startswith('{'):
            pprint(result)
        else:
            print(result)
    elif level > maxlevel:
        raise ValueError('Argument level is larger than maxlevel')
    else:
        print(shortrepr(obj) + ': ')
        if type(obj) is type:
            print('Base classes of the object:')
            bases(obj, level + 1, tab)
            print()
        for attr in dir(obj):
            if not verbose:
                attr.startswith('_') or 
                try:
                    if attr not in _ignore_names:
                        describe(getattr(obj, attr), level + 1, maxlevel, tab, verbose)
                    else:
                        print(shortrepr(getattr(obj, attr)))
                except AttributeError:
                    print('<AttributeError!>', end='')


desc = describe
try:
    from .browser import *
except ImportError:
    pass

def test():
    try:
        describe(type, verbose=True)
    except BaseException as err:
        try:
            print('STOPPED!', file=(sys.stderr))
            if type(err) is not KeyboardInterrupt:
                raise
            return 1
        finally:
            err = None
            del err

    else:
        return 0


if __name__ == '__main__':
    sys.exit(test())