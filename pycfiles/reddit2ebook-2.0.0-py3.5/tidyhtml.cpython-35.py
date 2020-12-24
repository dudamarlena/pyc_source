# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reddit2ebook/ebooklib_patched/plugins/tidyhtml.py
# Compiled at: 2016-05-13 06:16:04
# Size of source mod 2**32: 2242 bytes
import six, subprocess
from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

def tidy_cleanup(content, **extra):
    cmd = []
    for k, v in six.iteritems(extra):
        cmd.append('--%s' % k)
        if v:
            cmd.append(v)

    try:
        p = subprocess.Popen(['tidy'] + cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    except OSError:
        return (3, None)

    p.stdin.write(content)
    cont, p_err = p.communicate()
    return (
     p.returncode, cont)


class TidyPlugin(BasePlugin):
    NAME = 'Tidy HTML'
    OPTIONS = {'utf8': None, 
     'tidy-mark': 'no'}

    def __init__(self, extra={}):
        self.options = dict(self.OPTIONS)
        self.options.update(extra)

    def html_before_write(self, book, chapter):
        if not chapter.content:
            return
        _, chapter.content = tidy_cleanup(chapter.content, **self.options)
        return chapter.content

    def html_after_read(self, book, chapter):
        if not chapter.content:
            return
        _, chapter.content = tidy_cleanup(chapter.content, **self.options)
        return chapter.content