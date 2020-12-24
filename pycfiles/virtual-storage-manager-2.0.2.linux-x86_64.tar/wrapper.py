# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/rootwrap/wrapper.py
# Compiled at: 2016-06-13 14:11:03
import ConfigParser, logging, logging.handlers, os, string
from vsm.openstack.common.rootwrap import filters

class NoFilterMatched(Exception):
    """This exception is raised when no filter matched."""
    pass


class FilterMatchNotExecutable(Exception):
    """
    This exception is raised when a filter matched but no executable was
    found.
    """

    def __init__(self, match=None, **kwargs):
        self.match = match


class RootwrapConfig(object):

    def __init__(self, config):
        self.filters_path = config.get('DEFAULT', 'filters_path').split(',')
        if config.has_option('DEFAULT', 'exec_dirs'):
            self.exec_dirs = config.get('DEFAULT', 'exec_dirs').split(',')
        else:
            self.exec_dirs = os.environ['PATH'].split(':')
        if config.has_option('DEFAULT', 'syslog_log_facility'):
            v = config.get('DEFAULT', 'syslog_log_facility')
            facility_names = logging.handlers.SysLogHandler.facility_names
            self.syslog_log_facility = getattr(logging.handlers.SysLogHandler, v, None)
            if self.syslog_log_facility is None and v in facility_names:
                self.syslog_log_facility = facility_names.get(v)
            if self.syslog_log_facility is None:
                raise ValueError('Unexpected syslog_log_facility: %s' % v)
        else:
            default_facility = logging.handlers.SysLogHandler.LOG_SYSLOG
            self.syslog_log_facility = default_facility
        if config.has_option('DEFAULT', 'syslog_log_level'):
            v = config.get('DEFAULT', 'syslog_log_level')
            self.syslog_log_level = logging.getLevelName(v.upper())
            if self.syslog_log_level == 'Level %s' % v.upper():
                raise ValueError('Unexepected syslog_log_level: %s' % v)
        else:
            self.syslog_log_level = logging.ERROR
        if config.has_option('DEFAULT', 'use_syslog'):
            self.use_syslog = config.getboolean('DEFAULT', 'use_syslog')
        else:
            self.use_syslog = False
        return


def setup_syslog(execname, facility, level):
    rootwrap_logger = logging.getLogger()
    rootwrap_logger.setLevel(level)
    handler = logging.handlers.SysLogHandler(address='/dev/log', facility=facility)
    handler.setFormatter(logging.Formatter(os.path.basename(execname) + ': %(message)s'))
    rootwrap_logger.addHandler(handler)


def build_filter(class_name, *args):
    """Returns a filter object of class class_name"""
    if not hasattr(filters, class_name):
        logging.warning('Skipping unknown filter class (%s) specified in filter definitions' % class_name)
        return None
    else:
        filterclass = getattr(filters, class_name)
        return filterclass(*args)


def load_filters(filters_path):
    """Load filters from a list of directories"""
    filterlist = []
    for filterdir in filters_path:
        if not os.path.isdir(filterdir):
            continue
        for filterfile in os.listdir(filterdir):
            filterconfig = ConfigParser.RawConfigParser()
            filterconfig.read(os.path.join(filterdir, filterfile))
            for name, value in filterconfig.items('Filters'):
                filterdefinition = [ string.strip(s) for s in value.split(',') ]
                newfilter = build_filter(*filterdefinition)
                if newfilter is None:
                    continue
                newfilter.name = name
                filterlist.append(newfilter)

    return filterlist


def match_filter(filters, userargs, exec_dirs=[]):
    """
    Checks user command and arguments through command filters and
    returns the first matching filter.
    Raises NoFilterMatched if no filter matched.
    Raises FilterMatchNotExecutable if no executable was found for the
    best filter match.
    """
    first_not_executable_filter = None
    for f in filters:
        if f.match(userargs):
            if not f.get_exec(exec_dirs=exec_dirs):
                if not first_not_executable_filter:
                    first_not_executable_filter = f
                continue
            return f

    if first_not_executable_filter:
        raise FilterMatchNotExecutable(match=first_not_executable_filter)
    raise NoFilterMatched()
    return