# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_markdown.py
# Compiled at: 2018-10-09 08:32:27
# Size of source mod 2**32: 750 bytes
import ivy
try:
    import markdown
except ImportError:
    markdown = None

if markdown:
    settings = ivy.site.config.get('markdown', {})
    renderer = (markdown.Markdown)(**settings)

    @ivy.renderers.register('md')
    def render(text):
        return renderer.reset().convert(text)