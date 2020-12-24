# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/zclient/settings.py
# Compiled at: 2012-02-10 13:22:17
import ConfigParser, os, io

def getall(conf_file):

    def config_map(section):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint('skip: %s' % option)
            except:
                print 'exception on %s!' % option
                dict1[option] = None

        return dict1

    config = ConfigParser.ConfigParser()
    config.read(conf_file)
    settings = {}
    for sec in config.sections():
        settings[sec] = config_map(sec)

    return settings