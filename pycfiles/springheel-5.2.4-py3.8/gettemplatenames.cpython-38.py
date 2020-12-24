# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/gettemplatenames.py
# Compiled at: 2019-12-16 01:56:42
# Size of source mod 2**32: 1515 bytes
import os

def getTemplateNames():
    """Make filenames for site templates."""
    base = 'base-template'
    characters = 'characters-template'
    archive = 'archive-template'
    index = 'index-template'
    extra = 'extras-template'
    strings = 'strings.json'
    patterns = [
     base, characters, archive, index, extra]
    extension = 'html'
    root = 'templates'
    fulls = []
    for pattern in patterns:
        file = '.'.join([pattern, extension])
        full = os.path.join(root, file)
        fulls.append(full)
    else:
        strings_p = os.path.join(root, strings)
        fulls.append(strings_p)
        templates = tuple(fulls)
        return templates