# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/flexirest/defaults.py
# Compiled at: 2009-10-12 15:27:32
"""Modules indentation intentionally bad."""
from flexirest.rendering import all_writers
templates = {'html': '%(html_prolog)s\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%(lang)s" lang="%(lang)s">\n<head>\n%(html_head)s\n</head>\n<body>\n%(html_body)s\n</body>\n</html>\n'}
for writer_name in all_writers():
    if writer_name not in templates:
        templates[writer_name] = '%(whole)s'