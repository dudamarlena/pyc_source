# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/hwlib/sysfs.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 3727 bytes
import logging, os
log = logging.getLogger(__name__)

def parse_cookie(path):
    try:
        with open(path) as (cookie_file):
            return cookie_file.read().strip()
    except IOError as ioerror:
        log.debug('Problem reading sysfs file %s [%s]' % (path, ioerror))
        return ''


def convert_bool(data):
    if not data:
        return False
    try:
        return bool(int(data))
    except ValueError:
        log.warning('Problem coercing data to int, probably not a bool : {}'.format(data))
        return bool(data)


def append_sys(path):
    return os.path.join('/sys', path.lstrip('/'))


class SysFSBase(object):

    def __init__(self):
        self.base_path = ''

    def get_cookie(self, name):
        path = os.path.join(append_sys(self.base_path), name)
        return parse_cookie(path)


class NetClass(SysFSBase):
    class_path = 'class/net'

    def __init__(self, devname):
        super(NetClass, self).__init__()
        self.devname = devname
        self.base_path = os.path.join(self.class_path, self.devname)

    @property
    def address(self):
        return self.get_cookie('address')

    @property
    def carrier(self):
        return convert_bool(self.get_cookie('carrier'))

    @property
    def dev_port(self):
        return self.get_cookie('dev_port')

    @property
    def dev_id(self):
        return self.get_cookie('dev_id')

    @property
    def duplex(self):
        return self.get_cookie('duplex')

    @property
    def speed(self):
        return self.get_cookie('speed')

    @property
    def ifindex(self):
        return self.get_cookie('ifindex')

    @classmethod
    def list_interfaces(cls, exclude_loopback=True):
        path = append_sys(cls.class_path)
        interfaces = os.listdir(path)
        if exclude_loopback:
            if 'lo' in interfaces:
                interfaces.remove('lo')
        return interfaces


class DMI(SysFSBase):
    __doc__ = "    Since class/dmi is unlikely to change, we'll build attributes off fs objects\n    "
    class_path = 'class/dmi/id'

    def __init__(self):
        super(DMI, self).__init__()
        self.base_path = self.class_path
        self.elements = list()
        self._DMI__build_attributes()

    def __build_attributes(self):
        ld = os.listdir(append_sys(self.base_path))
        for f in ld:
            sys_path = os.path.join(self.base_path, f)
            if os.path.isfile(append_sys(sys_path)):
                self.elements.append(f)
                self.__setattr__(f, self.get_cookie(f))

    def __getattr__(self, item):
        """        This is only here to shut up pycharm inspections. In version 4.5, it now does not complain about missing
        attributes if __getattr__ is defined in new style classes
        """
        raise AttributeError('Attribute lookup failed for %s' % item)

    def dump(self):
        """        Dump a dictionary of dmi elements as key/value pairs
        """
        _d = {}
        for element in self.elements:
            _d[element] = getattr(self, element)

        return _d