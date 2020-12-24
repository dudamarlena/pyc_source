# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/container.py
# Compiled at: 2013-02-11 04:58:46
from ztfy.utils.unicode import translateString

def getContentName(container, base_name, translate=True, max_length=30):
    """Get a real name for a given base name and a container
    
    Target name will be suffixed with an index if base name already exists
    """
    if translate:
        base_name = translateString(base_name, escapeSlashes=True, spaces='-')
    if max_length:
        base_name = base_name[0:max_length]
    if base_name not in container:
        return base_name
    index = 2
    name = '%s-%02d' % (base_name, index)
    while name in container:
        index += 1
        name = '%s-%02d' % (base_name, index)

    return name