# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/src_import/ryo-iso/ryo_iso/cli.py
# Compiled at: 2019-11-12 05:13:56
# Size of source mod 2**32: 677 bytes
import sys, ryo_iso
from doit.doit_cmd import DoitMain
from doit.cmd_base import ModuleTaskLoader
cfgs = ryo_iso.Config.data.values()
if not all(map(lambda x: x.exists(), cfgs)):
    import ryo_iso.tasks.init
    module = ryo_iso.tasks.init
else:
    ryo_iso.config._ctx = {}
    ryo_iso.config._ctx['config'] = ryo_iso.config.Config()
    import ryo_iso.tasks.main
    module = ryo_iso.tasks.main

def cli(argv=None):
    if argv is not None:
        DoitMain(ModuleTaskLoader(module)).run(argv)
    else:
        sys.exit(DoitMain(ModuleTaskLoader(module)).run(sys.argv[1:]))