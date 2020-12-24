# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/iniutils.py
# Compiled at: 2010-12-12 22:28:56
import ConfigParser, string, sys
_ConfigDefault = {'database.dbms': 'mysql', 
   'database.name': '', 
   'database.user': 'root', 
   'database.password': '', 
   'database.host': '127.0.0.1'}

def LoadConfig(file, config={}):
    """
    returns a dictionary with keys of the form
    <section>.<option> and the corresponding values
    """
    config = config.copy()
    cp = ConfigParser.ConfigParser()
    cp.read(file)
    for sec in cp.sections():
        name = string.lower(sec)
        for opt in cp.options(sec):
            config[name + '.' + string.lower(opt)] = string.strip(cp.get(sec, opt))

    return config


if __name__ == '__main__':
    newConfig = LoadConfig('fileConverter.ini', _ConfigDefault)