# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uforgecli/utils/extract_id_utils.py
# Compiled at: 2017-03-01 08:38:06


def extractId(url, position=None, operation=True):
    final = []
    tuple = url.split('/')
    for item in tuple:
        try:
            int(item)
            final.append(item)
        except ValueError:
            pass

    final = list(reversed(final))
    if position is None:
        position = 0
    if operation:
        return final[position]
    else:
        return final
        return