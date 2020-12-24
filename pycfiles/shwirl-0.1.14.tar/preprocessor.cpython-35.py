# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/gloo/preprocessor.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 2298 bytes
import re
from .. import glsl
from ..util import logger

def remove_comments(code):
    """Remove C-style comment from GLSL code string."""
    pattern = '(\\".*?\\"|\\\'.*?\\\')|(/\\*.*?\\*/|//[^\\r\\n]*\\n)'
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def do_replace(match):
        if match.group(2) is not None:
            return ''
        else:
            return match.group(1)

    return regex.sub(do_replace, code)


def merge_includes(code):
    """Merge all includes recursively."""
    pattern = '\\#\\s*include\\s*"(?P<filename>[a-zA-Z0-9\\_\\-\\.\\/]+)"'
    regex = re.compile(pattern)
    includes = []

    def replace(match):
        filename = match.group('filename')
        if filename not in includes:
            includes.append(filename)
            path = glsl.find(filename)
            if not path:
                logger.critical('"%s" not found' % filename)
                raise RuntimeError('File not found', filename)
            text = '\n// --- start of "%s" ---\n' % filename
            with open(path) as (fh):
                text += fh.read()
            text += '// --- end of "%s" ---\n' % filename
            return text
        return ''

    for i in range(10):
        if re.search(regex, code):
            code = re.sub(regex, replace, code)
        else:
            break

    return code


def preprocess(code):
    """Preprocess a code by removing comments, version and merging includes."""
    if code:
        code = merge_includes(code)
    return code