# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../multi_job/runtime/runtime.py
# Compiled at: 2020-02-14 16:10:30
# Size of source mod 2**32: 815 bytes
from operator import itemgetter
from typing import List, Mapping
from multi_job.models.processes import Process
from multi_job.utils.colours import blue, green
from multi_job.utils.emojis import MUSHROOM, TOPHAT, ZAP

def run(processes: List[Process], options: Mapping[(str, bool)]) -> None:
    quiet, silent, check, verbose = itemgetter('quiet', 'silent', 'check', 'verbose')(options)
    if not (quiet or silent):
        print(ZAP + blue(' Multi Job ') + ZAP + '\nPlan:')
        for process in processes:
            print(green(process.show(verbose)))

    if check:
        return
    for process in processes:
        if not (quiet or silent):
            print(blue('Running: ') + process.show(verbose))
        output = process.trigger()
        if not silent:
            print(output)