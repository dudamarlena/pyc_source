# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqode/designer.py
# Compiled at: 2014-05-20 12:43:10
__doc__ = '\nRun this script to run qt designer with the pyqode plugins.\n\nRequires\n---------\n\nOn linux you need to install python-qt and python-qt-dev.\n\nOn windows you just have to install PyQt with its designer.\n\nUsage\n-----\n\nYou can try the pyqode qt designer plugin without installing pyqode, just run\ndesigner.pyw from the source package.\n\nIf pyqode is installed, this script is installed into the Scripts folder on\nwindows or in a standard bin folder on linux. Open a terminal and run\n**pyqode_designer**.\n'
import multiprocessing, os
os.environ.setdefault('QT_API', 'PyQt')
import pkg_resources, subprocess, sys

def get_pth_sep():
    """
    Gets platform dependand path separator
    """
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    return sep


def set_plugins_path(env, sep):
    """
    Sets PYQTDESIGNERPATH
    """
    paths = ''
    dict = {}
    if sys.platform != 'win32':
        import pyqode
        root = os.path.dirname(pyqode.__file__)
        for dir_name in os.listdir(root):
            dir_name = os.path.join(root, dir_name)
            if os.path.isdir(dir_name) and '_' not in dir_name:
                for sub_dir in os.listdir(dir_name):
                    if sub_dir == 'plugins':
                        pth = os.path.join(dir_name, sub_dir)
                        paths += pth + sep

    for entrypoint in pkg_resources.iter_entry_points('pyqode_plugins'):
        try:
            plugin = entrypoint.load()
        except pkg_resources.DistributionNotFound:
            pass
        except ImportError:
            print 'failed to import plugin: %r' % entrypoint
        else:
            pth = os.path.dirname(plugin.__file__)
            print 'plugin loaded: %s' % pth
            if pth not in dict:
                paths += pth + sep
                dict[pth] = None

    if 'PYQTDESIGNERPATH' in env:
        pyqt_designer_path = env['PYQTDESIGNERPATH']
        env['PYQTDESIGNERPATH'] = pyqt_designer_path + sep + paths
    else:
        env['PYQTDESIGNERPATH'] = paths
    print 'pyQode plugins paths: %s' % env['PYQTDESIGNERPATH']
    return


def run(env):
    """
    Runs qt designer with our customised environment.
    """
    p = None
    env['PYQODE_NO_COMPLETION_SERVER'] = '1'
    try:
        p = subprocess.Popen(['designer-qt4'], env=env)
        if p.wait():
            raise OSError()
    except OSError:
        try:
            p = subprocess.Popen(['designer'], env=env)
            if p.wait():
                raise OSError()
        except OSError:
            print 'Failed to start Qt Designer'

    if p:
        return p.wait()
    else:
        return -1


def check_env(env):
    """
    Ensures all key and values are strings on windows.
    """
    if sys.platform == 'win32':
        win_env = {}
        for key, value in env.items():
            win_env[str(key)] = str(value)

        env = win_env
    return env


def main():
    """
    Runs the Qt Designer with an adapted plugin path.
    """
    sep = get_pth_sep()
    env = os.environ.copy()
    set_plugins_path(env, sep)
    env = check_env(env)
    return run(env)


if __name__ == '__main__':
    sys.exit(main())