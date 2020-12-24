# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/nasif12/home_if12/wachutka/workspace/wBuild/wbuild/autolink.py
# Compiled at: 2018-05-23 08:03:04
# Size of source mod 2**32: 882 bytes
import os, glob
from yaml import load
from os import link
from pathlib import Path
from wbuild.utils import Config

def autolink(config):
    conf = Config()
    scriptsPath = conf.get('scriptsPath')
    S = Path(scriptsPath)
    tasks = load(open(config))
    for filename in glob.iglob(scriptsPath + '/**/*.ln.R', recursive=True):
        os.remove(filename)

    for task in tasks:
        print(task)
        if task['dst'] is None:
            pass
        else:
            if task['src'] is None:
                pass
            else:
                for dst in task['dst']:
                    if dst is None:
                        pass
                    else:
                        if not os.path.exists(str(S / dst)):
                            os.makedirs(str(S / dst))
                        for src in task['src']:
                            if src is None:
                                pass
                            else:
                                link(str(S / Path(src)), str(S / Path(dst) / Path(src).stem) + '.ln.R')