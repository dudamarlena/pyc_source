# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oebakery/misc.py
# Compiled at: 2009-11-02 08:05:00
from __future__ import with_statement

def get_simple_config_line(filename, variable):
    if os.path.exists(filename):
        regex = re.compile(variable + '\\s*=\\s*["\'](.*)["\']')
        with open(filename) as (file):
            for line in file.readlines():
                match = regex.match(line)
                if match:
                    return match.group(1)

    return


def version_str_to_tuple(str):
    dash = str.rfind('-')
    if dash >= 0:
        str = str[dash + 1:]
    list = string.split(str, '.')
    tuple = ()
    for number in list:
        tuple = tuple + (int(number),)

    return tuple