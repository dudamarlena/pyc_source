# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/parsers/markdown.py
# Compiled at: 2012-11-21 04:46:57
import misaka as m

class Render(m.HtmlRenderer):
    pass


class Parser:

    def parse(self, markdown):
        html = m.Markdown(Render())
        return html.render(markdown)