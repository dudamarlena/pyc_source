# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/collector/filesystem.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 2923 bytes
import re, os
from prometheus_client.core import GaugeMetricFamily
from .namespace import NAMESPACE
from .collector import Collector
defIgnoredMountPoints = '^/(dev|proc|sys|var/lib/docker/.+)($|/)'
defIgnoredFSTypes = '^(autofs|binfmt_misc|bpf|cgroup2?|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|iso9660|mqueue|nsfs|overlay|proc|procfs|pstore|rpc_pipefs|securityfs|selinuxfs|squashfs|sysfs|tracefs)$'

def parseFilesystemLabels(fslines):
    lines = map(lambda l: l.split(' '), fslines)
    lines = filter(lambda l: re.match(defIgnoredFSTypes, l[2]) is None, lines)
    lines = filter(lambda l: re.match(defIgnoredMountPoints, l[1]) is None, lines)
    return list(map(lambda l: {'device':l[0],  'mountPoint':l[1],  'fsType':l[2], 
     'options':l[3]}, lines))


def generateFilesystemMetrics(subsystem):
    return [
     GaugeMetricFamily(name=('{}_{}_{}'.format(NAMESPACE, subsystem, 'size_bytes')), labels=['device', 'mountpoint', 'fstype'], documentation=''),
     GaugeMetricFamily(name=('{}_{}_{}'.format(NAMESPACE, subsystem, 'free_bytes')), labels=[
      'device', 'mountpoint', 'fstype'],
       documentation=''),
     GaugeMetricFamily(name=('{}_{}_{}'.format(NAMESPACE, subsystem, 'avail_bytes')), labels=[
      'device', 'mountpoint', 'fstype'],
       documentation=''),
     GaugeMetricFamily(name=('{}_{}_{}'.format(NAMESPACE, subsystem, 'files')), labels=[
      'device', 'mountpoint', 'fstype'],
       documentation=''),
     GaugeMetricFamily(name=('{}_{}_{}'.format(NAMESPACE, subsystem, 'files_free')), labels=[
      'device', 'mountpoint', 'fstype'],
       documentation='')]


class FilesystemCollector(Collector):
    name = 'filesystem'

    def collect(self):
        metrics = generateFilesystemMetrics(self.name)
        with open('/proc/1/mounts', 'r') as (f):
            for labels in parseFilesystemLabels(f.readlines()):
                st = os.statvfs(labels['mountPoint'])
                metrics[0].add_metric([labels['device'], labels['mountPoint'],
                 labels['fsType']], float(st.f_blocks * st.f_bsize))
                metrics[1].add_metric([labels['device'], labels['mountPoint'],
                 labels['fsType']], float(st.f_bfree * st.f_bsize))
                metrics[2].add_metric([labels['device'], labels['mountPoint'],
                 labels['fsType']], float(st.f_bavail * st.f_bsize))
                metrics[3].add_metric([labels['device'], labels['mountPoint'],
                 labels['fsType']], st.f_files)
                metrics[4].add_metric([labels['device'], labels['mountPoint'],
                 labels['fsType']], st.f_files * st.f_ffree)

        for m in metrics:
            (yield m)