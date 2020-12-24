# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/callable_pip/__init__.py
# Compiled at: 2018-04-04 10:28:57
__doc__ = '\nDrop-in replacement for ``pip.main`` + a known-dangerous patch (which is\nappropriately named) which will *try* to patch ``pip.main`` to make it work on\nall versions of ``pip``\n'
import subprocess, sys

def main(*args):
    """
    Invoke pip in a subprocess, with semantics very similar to `pip.main()`

    Why use check_call instead of check_output?
    It's behavior is slightly closer to the older `pip.main()` behavior,
    printing output information directly to stdout.

    check_call was added in py2.5 and is supported through py3.x , so it's more
    compatible than some alternatives like subprocess.run (added in py3.5)
    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip'] + list(args))
        return 0
    except subprocess.CalledProcessError as err:
        return err.returncode


def dangerous_patch():
    """
    Import ``pip`` and patch ``callable_pip.main`` into it as ``pip.main``
    """
    import pip
    pip.main = main


__all__ = ('dangerous_patch', 'main')