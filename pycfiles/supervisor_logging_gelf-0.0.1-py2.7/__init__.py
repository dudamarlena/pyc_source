# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/supervisor_logging_gelf/__init__.py
# Compiled at: 2016-09-15 21:33:05
"""
Send received events to graylog over GELF/UDP.
"""
from __future__ import print_function
import logging, logging.handlers, os, sys, re, graypy
level_match_expr = '^.*?: ([A-Z]+)\\/.*?\\] (.*)$'

def get_headers(line):
    """
    Parse Supervisor message headers.
    """
    return dict([ x.split(':') for x in line.split() ])


def eventdata(payload):
    """
    Parse a Supervisor event.
    """
    headerinfo, data = payload.split('\n', 1)
    headers = get_headers(headerinfo)
    return (headers, data)


def supervisor_events(stdin, stdout):
    """
    An event stream from Supervisor.
    """
    while True:
        stdout.write('READY\n')
        stdout.flush()
        line = stdin.readline()
        headers = get_headers(line)
        payload = stdin.read(int(headers['len']))
        event_headers, event_data = eventdata(payload)
        yield (
         event_headers, event_data)
        stdout.write('RESULT 2\nOK')
        stdout.flush()


def split_msg_and_get_log_level(event_data, level_match):
    """
    Strip out syslog timestamp and try to match the level to the syslog level
    """
    match_obj = level_match.match(event_data)
    try:
        if match_obj.group(1) in ('DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL',
                                  'FATAL'):
            level = eval('logging.' + match_obj.group(1))
        else:
            level = logging.INFO
    except:
        level = logging.INFO

    try:
        body = match_obj.group(2)
    except:
        body = event_data

    return (
     level, body)


def main():
    env = os.environ
    try:
        host = env['GRAYLOG_SERVER']
        port = int(env['GRAYLOG_PORT'])
    except KeyError:
        sys.exit('GRAYLOG_SERVER and GRAYLOG_PORT are required.')

    sys.stderr.write('Starting with host: %s, port: %d' % (host, port))
    sys.stderr.flush()
    handler = graypy.GELFHandler(host, port)
    level_match = re.compile(level_match_expr)
    for event_headers, event_data in supervisor_events(sys.stdin, sys.stdout):
        level, body = split_msg_and_get_log_level(event_data, level_match)
        event = logging.LogRecord(name=event_headers['processname'], level=level, pathname=None, lineno=0, msg=body, args=(), exc_info=None)
        event.process = int(event_headers['pid'])
        event.processName = event_headers['groupname']
        handler.handle(event)

    return


if __name__ == '__main__':
    main()