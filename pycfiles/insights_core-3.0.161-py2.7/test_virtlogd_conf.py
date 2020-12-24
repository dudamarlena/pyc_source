# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_virtlogd_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import virtlogd_conf
from insights.tests import context_wrap
VIRTLOGD_CONF = '\n# Master virtlogd daemon configuration file\n#\n\n#################################################################\n#\n# Logging controls\n#\n\n# Logging level: 4 errors, 3 warnings, 2 information, 1 debug\n# basically 1 will log everything possible\n#log_level = 3\n\n# Logging filters:\n# A filter allows to select a different logging level for a given category\n# of logs\n# The format for a filter is one of:\n#    x:name\n#    x:+name\n#      where name is a string which is matched against source file name,\n#      e.g., "remote", "qemu", or "util/json", the optional "+" prefix\n#      tells libvirt to log stack trace for each message matching name,\n#      and x is the minimal level where matching messages should be logged:\n#    1: DEBUG\n#    2: INFO\n#    3: WARNING\n#    4: ERROR\n#\n# Multiple filter can be defined in a single @filters, they just need to be\n# separated by spaces.\n#\n# e.g. to only get warning or errors from the remote layer and only errors\n# from the event layer:\n#log_filters="3:remote 4:event"\n\n# Logging outputs:\n# An output is one of the places to save logging information\n# The format for an output can be:\n#    x:stderr\n#      output goes to stderr\n#    x:syslog:name\n#      use syslog for the output and use the given name as the ident\n#    x:file:file_path\n#      output to a file, with the given filepath\n#    x:journald\n#      ouput to the systemd journal\n# In all case the x prefix is the minimal level, acting as a filter\n#    1: DEBUG\n#    2: INFO\n#    3: WARNING\n#    4: ERROR\n#\n# Multiple output can be defined, they just need to be separated by spaces.\n# e.g. to log all warnings and errors to syslog under the virtlogd ident:\n#log_outputs="3:syslog:virtlogd"\n#\n\n# The maximum number of concurrent client connections to allow\n# over all sockets combined.\n#max_clients = 1024\n\n\n# Maximum file size before rolling over. Defaults to 2 MB\n#max_size = 2097152\n\n# Maximum number of backup files to keep. Defaults to 3,\n# not including the primary active file\nmax_backups = 3\n'

def test_virtlogd_conf():
    conf = virtlogd_conf.VirtlogdConf(context_wrap(VIRTLOGD_CONF, path='/etc/libvirt/virtlogd.conf'))
    assert conf.get('max_backups') == '3'
    conf = virtlogd_conf.VirtlogdConf(context_wrap(VIRTLOGD_CONF.replace('#max_size = 2097152', 'max_size = 12582912')))
    max_size = conf.get('max_size', None)
    assert int(max_size) == 12582912
    return


def test_virtlogd_conf_documentation():
    failed_count, tests = doctest.testmod(virtlogd_conf, globs={'conf': virtlogd_conf.VirtlogdConf(context_wrap(VIRTLOGD_CONF))})
    assert failed_count == 0