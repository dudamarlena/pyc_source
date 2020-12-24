# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/config.py
# Compiled at: 2012-08-28 05:19:59
import os.path, re, secobj
from ConfigParser import SafeConfigParser
from secobj.localization import _
LIST_PATTERN = re.compile('\\s*("[^"]*"|.*?)\\s*,')
CFG = None

class ConfigParser(SafeConfigParser):

    def getlist(self, section, option):
        value = self.get(section, option)
        return [ x[1:-1] if x[:1] == x[-1:] == '"' else x for x in LIST_PATTERN.findall(value.rstrip(',') + ',')
               ]


def getconfig():
    global CFG
    if CFG is None:
        raise ValueError, _('Configuration is not inizialized')
    return CFG


def initconfig(configfile, *defaultfiles):
    global CFG
    if CFG is None:
        if configfile is not None:
            if not os.path.isfile(configfile):
                raise ValueError, _("Configuration file doesn't exist or is not a file: {name}").format(name=configfile)
            files = [
             configfile]
            files.extend(defaultfiles)
        else:
            files = list(defaultfiles)
        files.reverse()
        CFG = ConfigParser()
        CFG.read(files)
    return