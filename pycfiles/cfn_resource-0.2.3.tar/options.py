# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cfn_pyplates/options.py
# Compiled at: 2016-03-13 18:27:04
from collections import defaultdict
prompt_str = 'Key "{0}" not found in the supplied options mapping.\nYou can enter it now (or leave blank for None/null):\n> '

class OptionsMapping(defaultdict):

    def __init__(self, *args, **kwargs):
        super(OptionsMapping, self).__init__(None, *args, **kwargs)
        return

    def __missing__(self, key):
        try:
            value = raw_input(prompt_str.format(key))
        except KeyboardInterrupt:
            raise SystemExit

        if not value:
            value = None
        self[key] = value
        return value