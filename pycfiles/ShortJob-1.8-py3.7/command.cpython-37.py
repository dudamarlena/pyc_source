# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ShortJob/command.py
# Compiled at: 2020-04-28 04:54:31
# Size of source mod 2**32: 2696 bytes
import os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

default = {'cxx':'root -l -b -q', 
 'C':'root -l -b -q', 
 'c':'root -l -b -q', 
 'cc':'root -l -b -q', 
 'cpp':'root -l -b -q', 
 'c++':'root -l -b -q', 
 'py':'python', 
 'sh':'bash', 
 'csh':'tcsh'}

def introduction():
    """dir: default, the default execute commands associated with one special type.

    @key: file type, "C", "cxx", "cc", "cpp", "c++", "py", "sh", "csh"

    @value: the execute commands, "root -l -b -q", "bash"

    list: rootType

    You can modify the command free in the file ~/.ShortJob/command
    we define those type file belong to "ROOT"

    ["cxx", "C", "cc", "c++", "c"]
    * in python3 the module "ConfigParser" is named as "configparser"
    """
    pass


class MyConfigParser(ConfigParser.ConfigParser):
    __doc__ = 'set ConfigParser options for case sensitive.'

    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


localConfigFile = os.path.expanduser('~/.ShortJob/command')

def initConfig(execommand):
    """init the ConfigParser file, the commands is stored in ~/.ShortJob/command
    Args:
       execommand(dir): take the file type as key and the command as value
    Returns:
        void
    """
    local_config = MyConfigParser()
    local_config.add_section('command')
    for k in execommand:
        local_config.set('command', k, execommand[k])

    if not os.path.exists(os.path.expanduser('~/.ShortJob')):
        os.mkdir(os.path.expanduser('~/.ShortJob'))
    localFile = os.path.expanduser(localConfigFile)
    with open(localFile, 'w') as (configFile):
        local_config.write(configFile)


def init(configfile):
    if not os.path.exists(configfile):
        initConfig(default)


def ReadConfig(configfile):
    init(configfile)
    local_config = MyConfigParser()
    local_config.read(configfile)
    d = {}
    for item in local_config.items('command'):
        d[item[0]] = item[1]

    return d


exe = ReadConfig(localConfigFile)
rootType = ['cxx', 'C', 'cc', 'c++', 'c']
if __name__ == '__main__':
    for i in exe:
        print('{} --> {}'.format(i, exe[i]))