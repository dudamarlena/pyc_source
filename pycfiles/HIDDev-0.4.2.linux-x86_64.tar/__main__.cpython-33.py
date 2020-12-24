# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.3/dist-packages/hiddev/__main__.py
# Compiled at: 2013-10-29 20:25:57
# Size of source mod 2**32: 2131 bytes
""" Example HID enumerator """
from . import enumerate_udev, usages

def printField(field):
    result = '    - Field {0.index} ({1})'.format(field, ','.join(field.flags))
    if field.application_usage:
        result += ' application: {0},'.format(usages.getUsageName(field.application_usage, True))
    if field.physical_usage or field.physical_range[0] != field.physical_range[1]:
        result += ' physical: {0} ({2}-{3} {1}),'.format(usages.getUsageName(field.physical_usage), field.unit, *field.physical_range)
    if field.logical_usage or field.logical_range[0] != field.logical_range[1]:
        result += ' logical: {0} ({1}-{2}),'.format(usages.getUsageName(field.logical_usage, True), *field.logical_range)
    if 'buffered_bytes' not in field.flags:
        usage_iterator = (('{0}'.format(usages.getUsageName(x, True)) if x else '0') for x in field.usages)
        if len(field.usages) > 3:
            first_usage = field.usages[0]
            if all(x == first_usage for x in field.usages):
                print(result + ' usages [{0} x {1}]'.format(len(field.usages), usages.getUsageName(field.usages[0], True)))
            else:
                print(result + ' usages [\n        ' + '\n        '.join(usage_iterator) + '\n      ]')
        else:
            print(result + ' usages [{0}]'.format(', '.join(usage_iterator)))
    else:
        print(result + ' usages [{0} x {1}]'.format(len(field.usages), usages.getUsageName(field.usages[0], True)))


for dev in enumerate_udev():
    print(dev.device_node + ':', dev.get_name())
    print('  Applications:', ', '.join(usages.getUsageName(x) for x in dev.applications))
    print()
    for report in sorted(dev.inputs(), key=lambda x: x.id):
        print('  Input {0.id}:'.format(report))
        for field in report:
            printField(field)

    print()
    for report in sorted(dev.outputs(), key=lambda x: x.id):
        print('  Output {0.id}:'.format(report))
        for field in report:
            printField(field)

    print()
    for report in sorted(dev.features(), key=lambda x: x.id):
        print('  Feature {0.id}:'.format(report))
        for field in report:
            printField(field)

    print()