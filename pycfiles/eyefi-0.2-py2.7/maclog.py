# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/maclog.py
# Compiled at: 2010-11-28 09:39:53
import os

def mac_fmt(mac):
    return (':').join(mac[2 * i:2 * i + 2] for i in range(6))


def eyefi_parse(logfile):
    photos, aps = {}, {}
    for line in open(logfile):
        power_secs, secs, event = line.strip().split(',', 2)
        event = event.split(',')
        event, args = event[0], event[1:]
        if event == 'POWERON':
            yield (
             photos, aps)
            photos, aps = {}, {}
        elif event in ('AP', 'NEWAP'):
            mac, strength, data = args
            aps.setdefault(mac, []).append({'power_secs': int(power_secs), 
               'secs': int(secs), 
               'signal_to_noise': int(strength), 
               'data': int(data, 16)})
        elif event == 'NEWPHOTO':
            filename, size = args
            photos[filename] = {'power_secs': int(power_secs), 
               'secs': int(secs), 
               'size': int(size)}
        else:
            raise ValueError, 'unknown event %s' % line
        yield (
         photos, aps)


def photo_macs(photo, aps):
    t = photo['power_secs']
    macs = []
    for mac in aps:
        seen = min([ (abs(m['power_secs'] - t), m['signal_to_noise']) for m in aps[mac]
                   ], key=lambda a: a[0])
        if seen[0] <= 3600:
            macs.append({'mac_address': mac_fmt(mac), 'age': seen[0] * 1000, 
               'signal_to_noise': seen[1]})

    return macs