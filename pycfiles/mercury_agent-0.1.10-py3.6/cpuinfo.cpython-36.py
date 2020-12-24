# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/cpuinfo.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 4868 bytes
import os

def build_index(l, key):
    our_dict = dict()
    for d in l:
        if key not in d:
            pass
        else:
            idx = d[key]
            if idx in our_dict:
                our_dict[idx].append(d)
            else:
                our_dict[idx] = [
                 d]

    return our_dict


def get_cpufreq_info(cpu):
    sys_cpu_path = '/sys/devices/system/cpu/cpu%s/cpufreq' % str(cpu)
    if not os.path.exists(sys_cpu_path):
        return dict()
    else:

        def read(path):
            with open(path) as (fp):
                return int(fp.read().strip())

        freq = dict()
        freq['min'] = read(os.path.join(sys_cpu_path, 'scaling_min_freq'))
        freq['max'] = read(os.path.join(sys_cpu_path, 'scaling_max_freq'))
        freq['cur'] = read(os.path.join(sys_cpu_path, 'scaling_cur_freq'))
        return freq


class CPUInfo(object):

    def __init__(self):
        if not os.path.exists('/proc/cpuinfo'):
            raise OSError('/proc/cpuinfo is missing. Bro, do you even linux?')
        with open('/proc/cpuinfo') as (fp):
            self.raw_cpuinfo = fp.read()
        cores = self.raw_cpuinfo.split('\n\n')
        self.core_dicts = list()
        for core in cores:
            if not core:
                pass
            else:
                core_dict = dict()
                for attribute in core.splitlines():
                    if not attribute:
                        pass
                    else:
                        k, v = attribute.split(':')
                        fixed_key = k.strip().replace(' ', '_').lower()
                        stripped_value = v.strip()
                        if fixed_key in ('processor', 'physical_id', 'core_id', 'cpu_cores'):
                            stripped_value = int(stripped_value)
                        core_dict[fixed_key] = stripped_value

                self.core_dicts.append(core_dict)

        self.core_dicts.sort(key=(lambda d: d['processor']))

    @property
    def physical_index(self):
        return build_index(self.core_dicts, 'physical_id')

    @property
    def logical_processor_index(self):
        return build_index(self.core_dicts, 'processor')

    @property
    def processor_ids(self):
        return [core_dict['processor'] for core_dict in self.core_dicts]

    @property
    def physical_processor_count(self):
        return len(self.physical_index)

    @property
    def logical_core_count(self):
        return len(self.core_dicts)

    @property
    def total_physical_core_count(self):
        return self.cores_per_processor * self.physical_processor_count

    def get_cores(self, physical_id):
        return self.physical_index.get(physical_id)

    @property
    def cores_per_processor(self):
        return self.one_core.get('cpu_cores')

    @property
    def core_zero_index(self):
        physical_index = self.physical_index
        for physical_id in physical_index:
            physical_index[physical_id] = physical_index[physical_id][0]

        return physical_index

    @staticmethod
    def get_speed_info(core_dict):
        speed_info = dict()
        processor_id = int(core_dict['processor'])
        speed_info['model_name'] = core_dict['model_name']
        cpufreq = get_cpufreq_info(processor_id)
        cpufreq_enabled = bool(cpufreq) or False
        speed_info['bogomips'] = float(core_dict['bogomips'])
        speed_info['cpufreq_enabled'] = cpufreq_enabled
        if cpufreq_enabled:
            speed_info['current'] = float(cpufreq['cur'])
            speed_info['min'] = float(cpufreq['min'])
            speed_info['max'] = float(cpufreq['max'])
        else:
            cpu_speed = core_dict['cpu_mhz']
            speed_info['current'] = float(cpu_speed)
            speed_info['min'] = float(cpu_speed)
            speed_info['max'] = float(cpu_speed)
        return speed_info

    def get_physical_speed_info(self):
        speed_info = list()
        zero_index = self.core_zero_index
        for physical_processor in zero_index:
            core_dict = zero_index[physical_processor]
            speed_info.append(self.get_speed_info(core_dict))

        return speed_info

    @property
    def one_core(self):
        return self.core_dicts and self.core_dicts[0] or dict()