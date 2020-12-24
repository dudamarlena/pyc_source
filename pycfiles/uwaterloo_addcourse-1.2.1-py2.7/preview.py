# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/preview.py
# Compiled at: 2015-04-26 11:14:38
import tempfile, time, webbrowser

def preview_page(html):
    """Preview the HTML code html in your browser."""
    with tempfile.NamedTemporaryFile(mode='w+t') as (f):
        f.write(str(html))
        f.flush()
        webbrowser.open('file://' + f.name)
        time.sleep(5)