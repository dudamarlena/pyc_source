# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/timeseries/rrd.py
# Compiled at: 2010-10-14 14:04:22
"""
Time Series: RRD

Implementation of timeseries backend methods for RRDTool.

TODO(g): Optionally ensure a ramdisk is created for the RRD file, so no disk
    performance is lost.  Create the file using less storage space, if you
    are capturing a lot of data points with fine granularity, or accept
    sacraficing the memory to remove any IO hits.
TODO(g): Add in adjustable information for saving space.  Set by MB or time,
    or either?  Return both, if so...
"""
import os, time, logging
from unidist.log import log
from unidist.run import Run

def GetRrdLastUpdateTime(filename):
    """Returns: int, epooch time, last time RRD was updated"""
    updated = 0
    if not os.path.isfile(filename):
        Exception('RRD Does not exist: %s' % filename)
    cmd = 'rrdtool last %s' % filename
    (status, output, output_error) = Run(cmd)
    if status == 0:
        updated = int(output.strip())
    else:
        log('RRD File failed to find last update: %s: %s' % (filename, output_error), logging.ERROR)
    return updated


def StoreInRrd(filename, interval, occurred, fields):
    if not os.path.isfile(filename):
        raise Exception('RRD file not found: %s' % filename)
    occurred_orig = occurred
    occurred = int(occurred)
    offset = occurred % interval
    if offset != 0:
        occurred -= offset
    cmd = 'rrdtool update %s %s:' % (filename, occurred)
    columns = fields.keys()
    columns.sort()
    for column in columns:
        if column in fields:
            value = fields[column]
            if value == None:
                cmd += 'U:'
            else:
                cmd += '%s:' % value
        else:
            cmd += 'U:'

    cmd = cmd[:-1]
    (status, output, output_error) = Run(cmd)
    if output_error:
        log('Cmd: %s  Error: %s' % (cmd, output_error))
        rrd_last_update_time = GetRrdLastUpdateTime(filename)
    return


def CreateRrd(filename, interval, create_fields, defaults, start=0):
    log('Creating RRD file: %s: %s seconds: %s' % (filename, interval, create_fields.keys()))
    cmd = 'rrdtool create %s --start %s --step %s ' % (filename, int(start - interval), interval)
    columns = create_fields.keys()
    columns.sort()
    for column in columns:
        column_data = create_fields[column]
        info = dict(defaults['column_default'])
        info.update(column_data)
        cmd += 'DS:%s:%s:%s:%s:%s ' % (column, info['type'], info['heartbeat'], info['range_bottom'], info['range_top'])

    for rra in defaults['rra']:
        cmd += 'RRA:%s:%s:%s:%s ' % (rra[0], rra[1], rra[2], rra[3])

    (status, output, output_error) = Run(cmd)
    if output_error:
        log('Failed to created RRD: %s: %s' % (cmd, output_error))
    return status


def GraphRrd(filename, image_path, create_fields, graph_fields, method, title, label_vertical, defaults, duration=600):
    log('Graphing RRD: %s  (%s)' % (filename, duration))
    temp_image_path = '%s.part' % image_path
    cmd = 'rrdtool graph %s ' % temp_image_path
    cmd += '--title "%s" ' % title
    cmd += '--vertical-label "%s" ' % label_vertical
    cmd += '-w 400 -h 100 '
    cmd += '--start -%ss ' % duration
    columns = {}
    for column in graph_fields:
        column_data = dict(defaults['column_default'])
        column_data.update(create_fields[column])
        columns[column] = column_data

    range_bottom = columns.get('range_bottom', 0)
    if range_bottom != None:
        cmd += '-l %d ' % range_bottom
    graph_top = columns.get('graph_top', None)
    if graph_top != None:
        cmd += '-u %d ' % graph_top
    for column in graph_fields:
        column_data = dict(defaults['column_default'])
        column_data.update(create_fields[column])
        cmd += 'DEF:%s=%s:%s:AVERAGE ' % (column, filename, column)

    line = 1
    line_stack = []
    for column in graph_fields:
        column_data = dict(defaults['column_default'])
        column_data.update(create_fields[column])
        line_stack.append(column)
        line_items = (',').join(line_stack)
        line_items += ',+' * (len(line_stack) - 1)
        cmd += 'CDEF:Ln%d=%s ' % (line, line_items)
        line += 1

    line = 1
    line_stack = []
    for column in graph_fields:
        column_data = dict(defaults['column_default'])
        column_data.update(create_fields[column])
        line_stack.append(column)
        line_items = (',').join(line_stack)
        line_items += ',+' * (len(line_stack) - 1)
        if line == 1:
            line_label = column
        else:
            line_label = '%s:STACK' % column
        cmd += 'AREA:%s%s:%s ' % (column, defaults['colors']['area'][(line - 1)], line_label)
        line += 1

    line = 1
    line_stack = []
    for column in graph_fields:
        cmd += 'LINE1:Ln%d%s ' % (line, defaults['colors']['line'][(line - 1)])
        line += 1

    cmd += '"COMMENT:\\n" '
    cmd += '"COMMENT:%s\\n" ' % time.asctime(time.localtime()).replace(':', '\\:')
    for column in graph_fields:
        cmd += '"GPRINT:%s:LAST:Last %s\\: %%2.1lf" ' % (column, column)

    (status, _, _) = Run(cmd)
    if status == 0:
        try:
            os.rename(temp_image_path, image_path)
        except Exception, e:
            log('Renaming the RRD graph from %s to %s failed: %s' % (temp_image_path, image_path, e))

    return


def FetchFromRrd(filename, start_time, consolidation='AVERAGE'):
    """Returns dict of dicts, keyed on time, keyed on column names, then values."""
    cmd = 'rrdtool fetch %s %s -s %s' % (filename, consolidation, start_time)
    data = {}
    (status, output, output_error) = Run(cmd)
    if output_error:
        raise Exception('Failed to fetch from RRD: %s: %s' % (cmd, output_error))
    else:
        lines = output.split('\n')
        header = lines[0].strip()
        while '  ' in header:
            header = header.replace('  ', ' ')

        columns = header.split(' ')
    for line in lines[1:]:
        if ':' in line:
            (occurred, values) = line.split(':', 1)
            values = values.strip().split(' ')
            item = {}
            for count in range(0, len(columns)):
                number_value = float(str(values[count]))
                item[columns[count]] = number_value

            data[occurred] = item

    return data


def Test():
    import yaml
    fp = open('timeseries_rrd_defaults.yaml')
    defaults = yaml.load(fp)
    fp.close()
    filename = 'cpu_test.rrd'
    graph_filename = 'cpu_test.png'
    interval = 5
    create_fields = {}
    create_fields['user'] = {'type': 'GAUGE', 'range_top': 'U', 'range_bottom': 0, 'heartbeat': 120}
    create_fields['system'] = {'type': 'GAUGE', 'range_top': 'U', 'range_bottom': 0, 'heartbeat': 120}
    create_fields['idle'] = {'type': 'GAUGE', 'range_top': 'U', 'range_bottom': 0, 'heartbeat': 120}
    if not os.path.exists(filename):
        CreateRrd(filename, interval, create_fields, defaults)
    print GetRrdLastUpdateTime(filename)
    fields = {'user': 68, 'system': 22, 'idle': 33}
    StoreInRrd(filename, interval, time.time(), fields)
    fields = {'user': 56, 'system': 6, 'idle': 38}
    StoreInRrd(filename, interval, time.time() + 5, fields)
    fields = {'user': 36, 'system': 16, 'idle': 48}
    StoreInRrd(filename, interval, time.time() + 10, fields)
    print GetRrdLastUpdateTime(filename)
    fields = [
     'system', 'user', 'idle']
    start_time = -60
    fetched = FetchFromRrd(filename, fields, start_time)
    print 'Fetched'
    import pprint
    pprint.pprint(fetched)
    sys.exit(0)
    create_fields = {}
    create_fields['user'] = {'type': 'GAUGE', 'range_top': 'U', 'range_bottom': 0, 'heartbeat': 120}
    create_fields['system'] = {'type': 'GAUGE', 'range_top': 'U', 'range_bottom': 0, 'heartbeat': 120}
    create_fields['idle'] = {'type': 'GAUGE', 'range_top': 'U', 'range_bottom': 0, 'heartbeat': 120}
    method = 'STACK'
    title = 'CPU Test'
    label_vertical = '% Used'
    graph_fields = ['system', 'user', 'idle']
    GraphRrd(filename, graph_filename, create_fields, graph_fields, method, title, label_vertical, defaults)


if __name__ == '__main__':
    Test()