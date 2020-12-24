# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/cpu.py
# Compiled at: 2019-02-11 13:08:11
# Size of source mod 2**32: 1676 bytes
from mercury_agent.inspector.inspectors import inspector
from mercury_agent.inspector.hwlib.cpuinfo import CPUInfo

@inspector.expose('cpu')
def cpu_inspector():
    _cpu = []
    cpu_info = CPUInfo()
    processors = cpu_info.physical_index
    for _id in processors:
        processor = processors[_id][0]
        _proc_dict = dict()
        _proc_dict['physical_id'] = _id
        _proc_dict['cores'] = int(processor['cpu_cores'])
        _proc_dict['threads'] = int(processor['siblings'])
        _proc_dict['model_name'] = processor['model_name']
        _proc_dict['cache_size'] = processor['cache_size']
        _proc_dict['cache_alignment'] = int(processor['cache_alignment'])
        _proc_dict['flags'] = processor['flags'].split()
        _proc_dict['frequency'] = CPUInfo.get_speed_info(processor)
        _cpu.append(_proc_dict)
        _cpu.sort(key=(lambda k: k['physical_id']))

    return _cpu


if __name__ == '__main__':
    from pprint import pprint
    pprint(cpu_inspector())