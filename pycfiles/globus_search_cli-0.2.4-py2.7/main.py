# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/parsing/main.py
# Compiled at: 2018-12-11 21:16:05
from globus_search_cli.parsing.click_wrappers import globus_group

def main_func(f):
    """
    Wrap root command func in common opts and make it a command group
    """
    f = globus_group('search-client', help='CLI Client to the Globus Search API')(f)
    return f