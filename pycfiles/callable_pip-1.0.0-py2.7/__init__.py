# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/callable_pip/__init__.py
# Compiled at: 2018-04-04 10:28:57
"""
Drop-in replacement for ``pip.main`` + a known-dangerous patch (which is
appropriately named) which will *try* to patch ``pip.main`` to make it work on
all versions of ``pip``
"""
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