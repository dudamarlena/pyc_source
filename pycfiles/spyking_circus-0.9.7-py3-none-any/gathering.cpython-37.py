# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/gathering.py
# Compiled at: 2020-03-11 05:17:13
# Size of source mod 2**32: 298 bytes
from circus.shared.utils import *
import circus.shared.files as io
from circus.shared.messages import init_logging

def main(params, nb_cpu, nb_gpu, use_gpu):
    _ = init_logging(params.logfile)
    logger = logging.getLogger('circus.gathering')
    io.collect_data(nb_cpu, params, erase=False)