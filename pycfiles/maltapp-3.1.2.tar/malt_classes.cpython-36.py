# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sysadmin/src/malt/malt/ext/malt_classes.py
# Compiled at: 2017-05-12 18:30:22
# Size of source mod 2**32: 678 bytes
import malt

@malt.hooks.register('page_classes')
def add_classes(classes, page):
    if page['is_single']:
        if 'classes' in page['record']:
            if isinstance(page['record']['classes'], str):
                for userclass in page['record']['classes'].split(','):
                    classes.append(userclass.strip())

    return classes