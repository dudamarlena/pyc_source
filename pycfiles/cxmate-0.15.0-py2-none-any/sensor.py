# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cli/commands/sensor.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: sensor.py'
from cxmanage_api.cli import get_tftp, get_nodes, get_node_strings, run_command

def sensor_command(args):
    """read sensor values from a cluster or host"""
    tftp = get_tftp(args)
    nodes = get_nodes(args, tftp)
    if not args.quiet:
        print 'Getting sensor readings...'
    results, errors = run_command(args, nodes, 'get_sensors', args.sensor_name)
    sensors = {}
    for node in nodes:
        if node in results:
            for sensor_name, sensor in results[node].iteritems():
                if sensor_name not in sensors:
                    sensors[sensor_name] = []
                reading = sensor.sensor_reading.replace('(+/- 0) ', '')
                try:
                    value = float(reading.split()[0])
                    suffix = reading.lstrip('%f ' % value)
                    sensors[sensor_name].append((node, value, suffix))
                except ValueError:
                    sensors[sensor_name].append((node, reading, ''))

    node_strings = get_node_strings(args, results, justify=True)
    if node_strings:
        jsize = len(node_strings.itervalues().next())
    for sensor_name, readings in sensors.iteritems():
        print sensor_name
        for node, reading, suffix in readings:
            try:
                print '%s: %.2f %s' % (node_strings[node], reading, suffix)
            except TypeError:
                print '%s: %s' % (node_strings[node], reading)

        try:
            if all(suffix == x[2] for x in readings):
                minimum = min(x[1] for x in readings)
                maximum = max(x[1] for x in readings)
                average = sum(x[1] for x in readings) / len(readings)
                print '%s: %.2f %s' % (('Minimum').ljust(jsize), minimum, suffix)
                print '%s: %.2f %s' % (('Maximum').ljust(jsize), maximum, suffix)
                print '%s: %.2f %s' % (('Average').ljust(jsize), average, suffix)
        except TypeError:
            pass

        print

    if not args.quiet and errors:
        print 'Some errors occured during the command.\n'
    return len(errors) > 0