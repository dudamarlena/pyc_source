# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/__init__.py
# Compiled at: 2020-03-26 10:16:52
# Size of source mod 2**32: 707 bytes
import importlib
__version__ = '0.9.7'

def launch(task, filename, nb_cpu, nb_gpu, use_gpu, output=None, benchmark=None, extension='', sim_same_elec=None):
    from circus.shared.parser import CircusParser
    params = CircusParser(filename)
    if task not in ('filtering', 'benchmarking'):
        params.get_data_file()
    else:
        module = importlib.import_module('circus.' + task)
        if task == 'benchmarking':
            module.main(params, nb_cpu, nb_gpu, use_gpu, output, benchmark, sim_same_elec)
        else:
            if task in ('converting', 'deconverting', 'merging'):
                module.main(params, nb_cpu, nb_gpu, use_gpu, extension)
            else:
                module.main(params, nb_cpu, nb_gpu, use_gpu)