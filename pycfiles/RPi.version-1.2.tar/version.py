# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: RPi/version.py
# Compiled at: 2015-02-04 06:32:34
_memory = [
 256,
 512,
 1024]
_manufacturer = [
 'SONY',
 'EGOMAN',
 'EMBEST',
 'UNKNOWN',
 'EMBEST']
_processor = [
 2835,
 2836]
_type = [
 'Model A',
 'Model B',
 'Model A+',
 'Model B+',
 'Model B Pi 2',
 'Alpha',
 'Compute Module']
_model = [
 'A',
 'B',
 'A',
 'B',
 'B',
 None,
 'CM']
_version = [
 1,
 1,
 1,
 1,
 2,
 1,
 1]
_cpuinfo = open('/proc/cpuinfo').read()
_cpuinfo = _cpuinfo.replace('\t', '')
_cpuinfo = _cpuinfo.split('\n')
_cpuinfo = filter(len, _cpuinfo)
_cpuinfo = dict(item.split(': ') for item in _cpuinfo)
_revision = int(_cpuinfo['Revision'], 16)
_scheme = (_revision & 8388608) >> 23
memory = 0
manufacturer = None
processor = None
type = None
model = None
version = 0
revision = 0
info = {}
if _scheme:
    memory = _memory[((_revision & 7340032) >> 20)]
    manufacturer = _manufacturer[((_revision & 983040) >> 16)]
    processor = _processor[((_revision & 61440) >> 12)]
    type = _type[((_revision & 4080) >> 4)]
    version = _version[((_revision & 4080) >> 4)]
    model = _model[((_revision & 4080) >> 4)]
    revision = _revision & 15
    info = {'memory': memory, 
       'manufacturer': manufacturer, 
       'processor': processor, 
       'type': type, 
       'revision': revision, 
       'model': model, 
       'revision': revision}
if __name__ == '__main__':
    if scheme:
        print ('Type:\t\t{}').format(type)
        print ('RAM:\t\t{}').format(memory)
        print ('CPU:\t\t{}').format(processor)
        print ('Manufacturer:\t{}').format(manufacturer)
        print ('Revision:\t{}').format(rev)
    else:
        print 'Old scheme detected'
        print ('Revision: {}').format(revision)