# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/setuptools/setuptools/launch.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 787 bytes
"""
Launch the Python script on the command line after
setuptools is bootstrapped via import.
"""
import tokenize, sys

def run():
    """
    Run the script in sys.argv[1] as if it had
    been invoked naturally.
    """
    __builtins__
    script_name = sys.argv[1]
    namespace = dict(__file__=script_name,
      __name__='__main__',
      __doc__=None)
    sys.argv[:] = sys.argv[1:]
    open_ = getattr(tokenize, 'open', open)
    script = open_(script_name).read()
    norm_script = script.replace('\\r\\n', '\\n')
    code = compile(norm_script, script_name, 'exec')
    exec(code, namespace)


if __name__ == '__main__':
    run()