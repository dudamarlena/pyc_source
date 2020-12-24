# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cb/Projekter/stonebear/stonebear/clean.py
# Compiled at: 2011-09-06 17:55:59
import os, shutil, subprocess

def clean(args, config):
    """
    clean [output_dir]
    """
    subprocess.call(config['preclean'], shell=True)
    cwd = os.getcwd() + '/'
    for o in config['output']:
        co = cwd + o
        if os.path.exists(co):
            if os.path.isdir(co):
                try:
                    shutil.rmtree(co)
                except OSError:
                    raise
                    sys.exit(1)

            else:
                try:
                    os.remove(co)
                except OSError:
                    raise
                    sys.exit(1)

    subprocess.call(config['postclean'], shell=True)