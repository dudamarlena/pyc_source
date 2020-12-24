# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/sanitize.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 616 bytes
from dexy.filter import DexyFilter
try:
    import bleach
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

class Bleach(DexyFilter):
    __doc__ = '\n    Runs the Bleach HTML sanitizer. <https://github.com/jsocol/bleach>\n    '
    aliases = ['bleach']
    _settings = {'added-in-version':'0.9.9.6', 
     'input-extensions':[
      '.html', '.txt'], 
     'output-extensions':[
      '.html', '.txt']}

    def is_active(self):
        return AVAILABLE

    def process_text(self, input_text):
        return bleach.clean(input_text)