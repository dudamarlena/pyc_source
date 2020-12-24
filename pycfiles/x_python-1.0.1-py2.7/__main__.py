# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/__main__.py
# Compiled at: 2020-05-02 11:58:36
"""A main program for xpython."""
import click, logging, sys
from xpython import execfile
from xpython.version import VERSION
from xdis import PYTHON_VERSION

def version_message():
    mess = 'xpython, version %s running from Python %s' % (
     VERSION, PYTHON_VERSION)
    return mess


@click.command()
@click.version_option(version_message(), '-V', '--version')
@click.option('-m', '--module', default=False, help='PATH is a module name, not a Python main program')
@click.option('-d', '--debug-level', default=0, help='debug output level in running')
@click.argument('path', nargs=1, type=click.Path(readable=True), required=True)
@click.argument('args', nargs=-1)
def main(module, debug_level, path, args):
    """
    Runs Python programs or bytecode using a bytecode interpreter written in Python.
    """
    if module:
        run_fn = execfile.run_python_module
    else:
        run_fn = execfile.run_python_file
    if debug_level > 1:
        level = logging.DEBUG
    else:
        if debug_level == 1:
            level = logging.INFO
        else:
            level = logging.WARNING
        logging.basicConfig(level=level)
        try:
            run_fn(path, args)
        except execfile.CannotCompile as e:
            if debug_level > 1:
                raise
            print e
            sys.exit(1)
        except execfile.NoSource as e:
            if debug_level > 1:
                raise
            print e
            sys.exit(2)
        except execfile.WrongBytecode as e:
            if debug_level > 1:
                raise
            print e
            sys.exit(3)


if __name__ == '__main__':
    main(auto_envvar_prefix='XPYTHON')