# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dog_whistle/__init__.py
# Compiled at: 2017-10-24 11:25:15
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from six import u
import logging
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


import os, re, copy
logging.getLogger(__name__).addHandler(NullHandler())
log = logging.getLogger(__name__)
MAX_LENGTH = 50

def dw_analyze(path):
    """Used to analyze a project structure and output the recommended settings dictionary to be used when used in practice. Run this method, then add the resulting output to your project

    :param str path: The folder path to analyze"""
    log.debug(b'dw_analyze')

    def walk(path):
        """Walks a directory, yields filepaths"""
        for dirName, subdirList, fileList in os.walk(path):
            log.debug(b'Found directory: %s' % dirName)
            for fname in fileList:
                if not fname.startswith(b'.'):
                    log.debug(b'File: \t%s' % fname)
                    val = os.path.join(dirName, fname)
                    yield val

    regex_lf = re.compile(b'(LogFactory.get_instance)')
    regex_log = re.compile(b'\\.(?:info|warn|warning|error|critical)\\(((["\']).*?\\2)')
    regex_inc = re.compile(b'\\.(?:info|warn|warning|error|critical)\\((.*(?:\\+|\\.format\\().*).*\\)')
    regex_com = re.compile(b'((["\']).*?\\2),')
    found_lf = False
    line_cache = []
    unknown_cache = []
    for file in walk(path):
        log.debug(b'checking file ' + file)
        with open(file, b'r') as (f):
            line_number = 1
            for line in f:
                results = regex_lf.findall(line)
                if len(results) > 0:
                    log.debug(b'found log factory use')
                    found_lf = True
                matches = regex_log.findall(line)
                if len(matches) > 0:
                    if len(regex_inc.findall(line)) == 0:
                        log.debug(b'found valid line')
                        line_cache.append((file, str(line_number), line.strip(),
                         matches[0]))
                    else:
                        log.debug(b'found unknown line')
                        unknown_cache.append((file, str(line_number),
                         line.strip(), matches[0]))
                line_number += 1

    if found_lf:
        log.debug(b'LogFactory in use')
        if len(line_cache) > 0:
            print(b'')
            print(b'Valid Lines')
            print(b'-----------')
            curr_file = None
            for item in line_cache:
                if curr_file != item[0]:
                    curr_file = item[0]
                    print(u(item[0]))
                print(b'  ', item[1], b':', u(item[2]))

        else:
            print(b"You don't appear to have any logger statements.")
        if len(unknown_cache) > 0:
            print(b'')
            print(b'Invalid Lines')
            print(b'-------------')
            print(b'')
            print(b'<<<<<<<<<< YOU MUST FIX THESE BEFORE USING THE DOGWHISTLE LIBRARY >>>>>>>>>>>')
            print(b'')
            curr_file = None
            for item in unknown_cache:
                if curr_file != item[0]:
                    curr_file = item[0]
                    print(u(item[0]))
                print(b'  ', item[1], b':', u(item[2]))

        recommended_str = b"\ndw_dict = {\n    'name': '<my_project>',\n    'tags': [\n        # high level tags that everything in your app will have\n        'item:descriptor'\n    ],\n    'metrics': {\n        # By default, everything is a counter using the concatentated log string\n        # the 'counters' key is NOT required, it is shown here for illustration\n        'counters': [\n            # datadog metrics that will use ++"
        for item in line_cache:
            recommended_str += b'\n            (' + item[3][0] + b', "' + _ddify(item[3][0], False) + b'"),'

        recommended_str += b"\n        ],\n        # datadog metrics that have a predefined value like `51`\n        # These metrics override any 'counter' with the same key,\n        # and are shown here for illustration purposes only\n        'gauges': [\n            "
        for item in line_cache:
            if len(regex_com.findall(item[2])) > 0:
                recommended_str += b'\n            (' + item[3][0] + b', "' + _ddify(item[3][0], False) + b'", "<extras.key.path>"),'

        recommended_str += b"\n        ]\n    },\n    'options': {\n        # use statsd for local testing, see docs\n        'statsd_host': 'localhost',\n        'statsd_port': 8125,\n        'local': True,\n    },\n\n}\n\nEnsure the above dictionary is passed into `dw_config()`\n"
        print(b'')
        print(b'Auto-Generated Template Settings')
        print(b'--------------------------------')
        print(recommended_str)
    else:
        print(b'It does not appear like the LogFactory is used in this project')
    return


def dw_config(settings):
    """Set up the datadog callback integration

    :param dict settings: The settings dict containing the `dw_analyze()` configuration
    :raises: :class:`Exception` if configuration is missing"""
    global _dw_configuration
    global _dw_init
    global _dw_local
    global _dw_stats
    log.debug(b'dw_config called')
    if not _dw_init:
        _dw_configuration = settings
        log.debug(b'init settings ' + str(_dw_configuration))
        if b'name' not in _dw_configuration:
            log.error(b'Unknown application name')
            raise Exception(b"'name' key required in dog_whistle config")
        if b'options' not in _dw_configuration:
            log.debug(b'no options provided')
            _dw_configuration[b'options'] = {}
        if b'metrics' not in _dw_configuration:
            log.debug(b'no metrics provided')
            _dw_configuration[b'metrics'] = {b'counters': [], b'gauges': []}
        if b'tags' not in _dw_configuration:
            log.debug(b'no tags provided')
            _dw_configuration[b'tags'] = []
        if b'allow_extra_tags' not in _dw_configuration:
            log.debug(b'defaulting to no extra tags')
            _dw_configuration[b'allow_extra_tags'] = False
        if b'local' in _dw_configuration[b'options'] and _dw_configuration[b'options'][b'local'] == True:
            from statsd import StatsClient
            if b'statsd_host' not in _dw_configuration[b'options'] or b'statsd_port' not in _dw_configuration[b'options']:
                log.error(b'Unknown statsd config for local setup')
                raise Exception(b'Unknown statsd config for local setup')
            statsd = StatsClient(_dw_configuration[b'options'][b'statsd_host'], _dw_configuration[b'options'][b'statsd_port'])
            _dw_stats = statsd
            _dw_stats.increment = statsd.incr
            _dw_local = True
        else:
            from datadog import initialize, statsd
            if b'statsd_host' not in _dw_configuration[b'options'] or b'statsd_port' not in _dw_configuration[b'options']:
                log.error(b'Unknown statsd config for DataDog setup')
                raise Exception(b'Unknown statsd config for DataDog setup')
            initialize(**_dw_configuration[b'options'])
            _dw_stats = statsd
        _dw_configuration[b'metrics'][b'c_mapper'] = {}
        _dw_configuration[b'metrics'][b'g_mapper'] = {}
        if b'counters' in _dw_configuration[b'metrics']:
            for item in _dw_configuration[b'metrics'][b'counters']:
                _dw_configuration[b'metrics'][b'c_mapper'][item[0]] = item[1]

            del _dw_configuration[b'metrics'][b'counters']
        if b'gauges' in _dw_configuration[b'metrics']:
            for item in _dw_configuration[b'metrics'][b'gauges']:
                _dw_configuration[b'metrics'][b'g_mapper'][item[0]] = []
                if isinstance(item[1], list):
                    log.debug(b'received multi gauge setup')
                    _dw_configuration[b'metrics'][b'g_mapper'][item[0]] = []
                    for part in item[1]:
                        obj_part = {b'name': part[0], b'value': part[1]}
                        _dw_configuration[b'metrics'][b'g_mapper'][item[0]].append(obj_part)

                else:
                    log.debug(b'received single gauge setup')
                    _dw_configuration[b'metrics'][b'g_mapper'][item[0]].append({b'name': item[1], 
                       b'value': item[2]})

            del _dw_configuration[b'metrics'][b'gauges']
        _dw_init = True
    else:
        log.warning(b'tried to configure DogWhistle more than once within app')


def dw_callback(message, extras):
    """The actual callback method passed to the logger

    :param str message: The log message
    :param dict extras: The extras dictionary from the logger"""
    log.debug(b'dw_callback called')
    if _dw_init:
        log.debug(b'inside callback ' + message + b' ' + str(extras))
        if message in _dw_configuration[b'metrics'][b'g_mapper']:
            log.debug(b'executing gauge log to datadog')
            for item in _dw_configuration[b'metrics'][b'g_mapper'][message]:
                value = _get_value(extras, item[b'value'])
                if value is None:
                    log.warning(b'Could not find key ' + item[b'value'] + b' inside extras')
                else:
                    the_msg = _ddify(item[b'name'])
                    if b'tags' in extras and _dw_configuration[b'allow_extra_tags']:
                        _gauge(the_msg, value, tags=_dw_configuration[b'tags'] + extras[b'tags'])
                    else:
                        _gauge(the_msg, value, tags=_dw_configuration[b'tags'])

        else:
            if message in _dw_configuration[b'metrics'][b'c_mapper']:
                the_msg = _ddify(_dw_configuration[b'metrics'][b'c_mapper'][message])
            else:
                the_msg = _ddify(message)
            if b'tags' in extras and _dw_configuration[b'allow_extra_tags']:
                _increment(the_msg, tags=_dw_configuration[b'tags'] + extras[b'tags'])
            else:
                _increment(the_msg, tags=_dw_configuration[b'tags'])
    else:
        log.warning(b'Tried to increment attribute before configuration')
    return


def _ddify(message, prepend=True):
    """Datadogifys and normalizes a log message into a datadog key

    :param str message: The message to concatentate
    :param bool prepend: prepend the application name to the metric
    :returns: the final datado string result
    """
    global MAX_LENGTH
    if prepend:
        message = (b'{}.{}').format(_dw_configuration[b'name'], message)
    message = re.sub(b'[^0-9a-zA-Z_. ]', b'', message)
    return message.rstrip(b'.').lower().replace(b' ', b'_').replace(b'"', b'')[:MAX_LENGTH]


def _get_value(item, key):
    """Grabs a nested value within a dict

    :param dict item: the dictionary
    :param str key: the nested key to find
    :returns: the value if found, otherwise None
    """
    keys = key.split(b'.', 1)
    if isinstance(item, dict):
        if len(keys) == 2:
            if keys[0] in item:
                return _get_value(item[keys[0]], keys[1])
        elif keys[0] in item:
            return copy.deepcopy(item[keys[0]])


def _increment(name, tags):
    """Increments a counter

    :param str name: The name of the stats
    :param list tag: A list of tags"""
    tags = _normalize_tags(tags)
    if _dw_local:
        _dw_stats.increment(stat=name)
    else:
        _dw_stats.increment(metric=name, tags=tags)
    log.info(b'incremented counter ' + name)


def _gauge(name, value, tags):
    """Increments a gauge

    :param str name: The name of the stats
    :param int value: The value of the gauge
    :param list tag: A list of tags"""
    tags = _normalize_tags(tags)
    if _dw_local:
        _dw_stats.gauge(stat=name, value=value)
    else:
        _dw_stats.gauge(metric=name, value=value, tags=tags)
    log.info(b'metric guage ' + name)


def _normalize_tags(tags):
    return [ t.lower() for t in tags ]


def _get_dw_stats():
    """Returns the statsd implementation in use"""
    return _dw_stats


def _get_config():
    """Returns the current configuration of the module"""
    return _dw_configuration


def _reset():
    """Resets the module configuration to the defaults"""
    global _dw_configuration
    global _dw_init
    global _dw_local
    global _dw_stats
    _dw_configuration = None
    _dw_init = False
    _dw_stats = None
    _dw_local = False
    return


_reset()