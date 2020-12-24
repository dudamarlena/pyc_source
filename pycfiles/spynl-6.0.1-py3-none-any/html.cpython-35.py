# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/serial/html.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 551 bytes
"""If needed, Spynl can return an HTML response."""
from spynl.main.serial.xml import prettify_xml
DOCTYPE = '<!DOCTYPE html>'

def dumps(content, pretty=False):
    """format an HTML response"""
    if pretty and '<html><' in content and '<body><' in content:
        tags = ['<' + e for e in content.split('<') if e != '']
        content = ''.join(prettify_xml(tags))
    if not content.lstrip().startswith('<!DOCTYPE'):
        content = DOCTYPE + content
    return '{}{}'.format(pretty * '\n', content)