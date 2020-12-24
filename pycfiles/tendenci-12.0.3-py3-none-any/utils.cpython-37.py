# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/utils.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 1995 bytes
import sys, os.path

def python_executable():
    """
    Get the path of the python interpreter that is running the current process,
    for use when spawning a new python process.

    If a virtualenv is used and this interpreter was started without first
    calling `source /path/to/venv/bin/activate` then
    subprocess.Popen('python', ...) and other similar calls will run the default
    system Python instead of the appropriate virtualenv Python.  To ensure that
    the appropriate virtualenv Python is enabled, use this function's return
    value instead of 'python' in such calls.
    """
    path = sys.executable
    if os.path.basename(path).startswith('python'):
        return path
    if os.path.basename(path) == 'uwsgi':
        import uwsgi
        path = uwsgi.opt.get('home')
        if path is not None:
            path += '/bin/python'
            if os.path.isfile(path):
                return path
    path = sys.prefix + '/bin/python'
    if os.path.isfile(path):
        return path
    return 'python'