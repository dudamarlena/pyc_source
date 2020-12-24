# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\venvs.py
# Compiled at: 2018-07-06 18:13:01
# Size of source mod 2**32: 2599 bytes
import pathlib, sys, os, virtualenv
from appdirs import user_config_dir, site_config_dir, user_cache_dir
import subprocess, platform
op_sys = platform.system()
if op_sys == 'Darwin':
    user_venv_dir = os.path.join(user_cache_dir(appname='xicam'), 'venvs')
else:
    user_venv_dir = os.path.join(user_config_dir(appname='xicam'), 'venvs')
site_venv_dir = os.path.join(site_config_dir(appname='xicam'), 'venvs')
venvs = {}
observers = []
execfile = lambda filename, globals=None, locals=None: exec(open(filename).read(), globals, locals)

def create_environment(name: str):
    """
    Create a new virtual environment in the user_venv_dir with name name.

    Parameters
    ----------
    name : str
        Name of virtual envirnoment to create.
    """
    venvpath = str(pathlib.Path(user_venv_dir, name))
    if not os.path.isdir(venvpath):
        env = os.environ.copy()
        if 'python' not in os.path.basename(sys.executable):
            python = os.path.join(os.path.dirname(sys.executable), 'python')
            env['VIRTUALENV_INTERPRETER_RUNNING'] = 'true'
        else:
            python = sys.executable
        p = subprocess.Popen([python, virtualenv.__file__, venvpath], env=env)
        p.wait()


def use_environment(name):
    """
    Activate the virtual environment with name name in user_venv_dir

    Parameters
    ----------
    name : str
        Name of virtual environment to activate
    """
    global current_environment
    activate_script = pathlib.Path(user_venv_dir, name, 'bin', 'activate_this.py')
    print('Using venv in:', activate_script)
    if not activate_script.is_file():
        activate_script = pathlib.Path(user_venv_dir, name, 'Scripts', 'activate_this.py')
    if not activate_script.is_file():
        raise ValueError(f"Virtual environment '{name}' could not be found.")
    activate_script = str(activate_script)
    execfile(activate_script, dict(__file__=activate_script))
    current_environment = str(pathlib.Path(user_venv_dir, name))
    for observer in observers:
        observer.venvChanged()


create_environment('default')
use_environment('default')
current_environment = str(pathlib.Path(user_venv_dir, 'default'))