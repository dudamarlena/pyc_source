# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/runtime/runtime.py
# Compiled at: 2020-02-01 17:17:31
# Size of source mod 2**32: 826 bytes
from operator import itemgetter
from typing import List, Mapping
from models.models import Process
from utils.colours import green, blue
from utils.emojis import ZAP, MUSHROOM, TOPHAT

def run(processes: List[Process], options: Mapping[(str, bool)]) -> None:
    quiet, silent, check, verbose = itemgetter('quiet', 'silent', 'check', 'verbose')(options)
    quiet or silent or print(ZAP + blue(' Multi Job ') + ZAP + '\nPlan:')
    for process in processes:
        print(green(process.call if verbose else process.alias))
    else:
        if check:
            return
        for process in processes:
            if not quiet:
                if not silent:
                    print(blue('Running: ') + (process.call if verbose else process.alias))
            output = process.trigger()
            if not silent:
                print(output)