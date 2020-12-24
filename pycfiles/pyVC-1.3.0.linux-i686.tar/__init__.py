# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/__init__.py
# Compiled at: 2007-08-31 18:49:27
__revision__ = '$Revision: 273 $'
__all__ = [
 'Helpers', 'Networks', 'Specifications', 'VirtualMachines',
 'Machine', 'Disks']

class Config(dict):
    __revision__ = '$Revision: 273 $'

    def __init__(self):
        import ConfigParser, os
        dict.__init__(self)
        configpaths = [
         '/etc/pyVC.ini', os.path.expanduser('~/.pyVC.ini')]
        config = ConfigParser.SafeConfigParser()
        self.configfiles = tuple(config.read(configpaths))
        if config.sections() == []:
            raise ValueError, 'ERROR: could not locate ini file. \n Looked in %s. \n Try copying and editing the example in etc/pyVC.ini' % configpaths
        for section in config.sections():
            if section not in self:
                self[section] = {}
            for option in config.options(section):
                try:
                    self[section][option] = config.get(section, option)
                except ConfigParser.InterpolationSyntaxError:
                    raise ValueError, 'ERROR: could not read the INI value for %s. \n Please check the files in %s for any errors.' % (option, self.configfiles)