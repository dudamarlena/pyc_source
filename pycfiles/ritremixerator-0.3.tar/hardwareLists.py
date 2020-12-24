# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/../dorrie/comps/hardwareLists.py
# Compiled at: 2012-01-23 15:46:01
import string
langDict = {}
lines = open('/usr/share/system-config-language/locale-list', 'r').readlines()
for line in lines:
    tokens = string.split(line)
    if '.' in tokens[0]:
        langBase = string.split(tokens[0], '.')
        langBase = langBase[0]
    else:
        if '@' in tokens[0]:
            langBase = string.split(tokens[0], '@')
            langBase = langBase[0]
        else:
            langBase = tokens[0]
        name = ''
        for token in tokens[3:]:
            name = name + ' ' + token

    name = string.strip(name)
    langDict[name] = langBase