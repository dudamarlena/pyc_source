# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/tests/pdb_procbundle.py
# Compiled at: 2018-07-31 09:26:23
# Size of source mod 2**32: 411 bytes
import zaggregator, zaggregator.utils as utils, zaggregator.tests as tests, zaggregator.procbundle as pb
from zaggregator.procbundle import ProcBundle
from zaggregator.proctable import ProcTable
from zaggregator.procmirror import ProcessMirror
from zaggregator.tests import cycle
if __name__ == '__main__':
    pt = ProcTable()
    for p in pt._procs:
        print(p)