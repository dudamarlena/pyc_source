# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_gpu.py
# Compiled at: 2017-02-11 10:25:25
"""GPU plugin (limited to NVIDIA chipsets)"""
from ocglances.logger import logger
from ocglances.plugins.glances_plugin import GlancesPlugin
try:
    import pynvml
except ImportError:
    logger.debug('Could not import pynvml.  NVIDIA stats will not be collected.')
    gpu_nvidia_tag = False
else:
    gpu_nvidia_tag = True

class Plugin(GlancesPlugin):
    """Glances GPU plugin (limited to NVIDIA chipsets).

    stats is a list of dictionaries with one entry per GPU
    """

    def __init__(self, args=None):
        """Init the plugin"""
        super(Plugin, self).__init__(args=args)
        self.init_nvidia()
        self.display_curse = True
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def init_nvidia(self):
        """Init the NVIDIA API"""
        if not gpu_nvidia_tag:
            self.nvml_ready = False
        try:
            pynvml.nvmlInit()
            self.device_handles = self.get_device_handles()
            self.nvml_ready = True
        except Exception:
            logger.debug('pynvml could not be initialized.')
            self.nvml_ready = False

        return self.nvml_ready

    def get_key(self):
        """Return the key of the list."""
        return 'gpu_id'

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update the GPU stats"""
        self.reset()
        if not self.nvml_ready:
            return self.stats
        if self.input_method == 'local':
            self.stats = self.get_device_stats()
        elif self.input_method == 'snmp':
            pass
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for i in self.stats:
            self.views[i[self.get_key()]] = {'proc': {}, 'mem': {}}
            if 'proc' in i:
                alert = self.get_alert(i['proc'], header='proc')
                self.views[i[self.get_key()]]['proc']['decoration'] = alert
            if 'mem' in i:
                alert = self.get_alert(i['mem'], header='mem')
                self.views[i[self.get_key()]]['mem']['decoration'] = alert

        return True

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.stats == [] or self.is_disable():
            return ret
        same_name = all(s['name'] == self.stats[0]['name'] for s in self.stats)
        gpu_stats = self.stats[0]
        header = ''
        if len(self.stats) > 1:
            header += ('{} ').format(len(self.stats))
        if same_name:
            header += ('{} {}').format('GPU', gpu_stats['name'])
        else:
            header += ('{}').format('GPU')
        msg = header[:17]
        ret.append(self.curse_add_line(msg, 'TITLE'))
        if len(self.stats) == 1 or args.meangpu:
            ret.append(self.curse_new_line())
            try:
                mean_proc = sum(s['proc'] for s in self.stats if s is not None) / len(self.stats)
            except TypeError:
                mean_proc_msg = ('{:>4}').format('N/A')
            else:
                mean_proc_msg = ('{:>3.0f}%').format(mean_proc)

            if len(self.stats) > 1:
                msg = ('{:13}').format('proc mean:')
            else:
                msg = ('{:13}').format('proc:')
            ret.append(self.curse_add_line(msg))
            ret.append(self.curse_add_line(mean_proc_msg, self.get_views(item=gpu_stats[self.get_key()], key='proc', option='decoration')))
            ret.append(self.curse_new_line())
            try:
                mean_mem = sum(s['mem'] for s in self.stats if s is not None) / len(self.stats)
            except TypeError:
                mean_mem_msg = ('{:>4}').format('N/A')
            else:
                mean_mem_msg = ('{:>3.0f}%').format(mean_mem)

            if len(self.stats) > 1:
                msg = ('{:13}').format('mem mean:')
            else:
                msg = ('{:13}').format('mem:')
            ret.append(self.curse_add_line(msg))
            ret.append(self.curse_add_line(mean_mem_msg, self.get_views(item=gpu_stats[self.get_key()], key='mem', option='decoration')))
        else:
            for gpu_stats in self.stats:
                ret.append(self.curse_new_line())
                id_msg = ('{}').format(gpu_stats['gpu_id'])
                try:
                    proc_msg = ('{:>3.0f}%').format(gpu_stats['proc'])
                except ValueError:
                    proc_msg = ('{:>4}').format('N/A')

                try:
                    mem_msg = ('{:>3.0f}%').format(gpu_stats['mem'])
                except ValueError:
                    mem_msg = ('{:>4}').format('N/A')

                msg = ('{}: {} mem: {}').format(id_msg, proc_msg, mem_msg)
                ret.append(self.curse_add_line(msg))

        return ret

    def get_device_handles(self):
        """
        Returns a list of NVML device handles, one per device.  Can throw NVMLError.
        """
        return [ pynvml.nvmlDeviceGetHandleByIndex(i) for i in range(pynvml.nvmlDeviceGetCount()) ]

    def get_device_stats(self):
        """Get GPU stats"""
        stats = []
        for index, device_handle in enumerate(self.device_handles):
            device_stats = {}
            device_stats['key'] = self.get_key()
            device_stats['gpu_id'] = index
            device_stats['name'] = self.get_device_name(device_handle)
            device_stats['mem'] = self.get_mem(device_handle)
            device_stats['proc'] = self.get_proc(device_handle)
            stats.append(device_stats)

        return stats

    def get_device_name(self, device_handle):
        """Get GPU device name"""
        try:
            return pynvml.nvmlDeviceGetName(device_handle)
        except pynvml.NVMlError:
            return 'NVIDIA'

    def get_mem(self, device_handle):
        """Get GPU device memory consumption in percent"""
        try:
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(device_handle)
            return memory_info.used * 100.0 / memory_info.total
        except pynvml.NVMLError:
            return

        return

    def get_proc(self, device_handle):
        """Get GPU device CPU consumption in percent"""
        try:
            return pynvml.nvmlDeviceGetUtilizationRates(device_handle).gpu
        except pynvml.NVMLError:
            return

        return

    def exit(self):
        """Overwrite the exit method to close the GPU API"""
        if self.nvml_ready:
            try:
                pynvml.nvmlShutdown()
            except Exception as e:
                logger.debug(('pynvml failed to shutdown correctly ({})').format(e))

        super(Plugin, self).exit()