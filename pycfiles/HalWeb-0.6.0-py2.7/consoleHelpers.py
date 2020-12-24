# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/consoleHelpers.py
# Compiled at: 2011-12-25 05:31:43


def extractAgrs(paramsList):
    return dict(map(lambda x: (x[:x.index('=')], x[x.index('=') + 1:]), paramsList))


def ask(message, validOptions={'y': True, 'n': False}, input=raw_input):
    yesno = ''
    if isinstance(validOptions, str):
        yesno = input(message)
    else:
        yesno = input(message + '(' + ('/').join(validOptions.keys()) + '):')
    while True:
        if validOptions == '*':
            return yesno
        if len(yesno) > 0:
            if validOptions.has_key(yesno):
                return validOptions[yesno]
        print 'Not Valid Input'
        yesno = input(message + '(' + ('/').join(validOptions.keys()) + '):')