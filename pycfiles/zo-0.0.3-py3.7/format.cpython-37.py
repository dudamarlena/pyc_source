# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/log/format.py
# Compiled at: 2020-04-03 03:49:59
# Size of source mod 2**32: 1467 bytes
from loguru import logger
import sys, traceback, re

def _custom_format(record):
    frames = [_ for _ in traceback.extract_stack() if not re.search('(/log/|/loguru/|/env|/Library)', _.filename)]
    stack = []
    for n, f in enumerate(frames):
        if f.filename in ('<string>', ):
            continue
        if re.search('^<', f.filename):
            continue
        filename = f.filename
        filename = re.sub('^.*/(.*?)\\..{1,3}$', '\\g<1>', filename)
        filename = '' if (n and frames[(n - 1)].filename == f.filename) else filename
        name = f.name.replace('<module>', '')
        stack.append(f"{filename}:{name}:{f.lineno}")

    record['extra']['stack'] = ' > '.join(stack)
    return '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level> | <fg #666>{extra[stack]}</>\n'


def add_log_trace():
    logger.add((sys.stderr), format=_custom_format)