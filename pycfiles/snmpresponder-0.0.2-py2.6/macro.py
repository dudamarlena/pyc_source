# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpresponder/macro.py
# Compiled at: 2019-01-13 12:56:28


def expandMacro(option, context):
    for k in context:
        pat = '${%s}' % k
        if option and '${' in option:
            option = option.replace(pat, str(context[k]))

    return option


def expandMacros(options, context):
    options = list(options)
    for (idx, option) in enumerate(options):
        options[idx] = expandMacro(option, context)

    return options