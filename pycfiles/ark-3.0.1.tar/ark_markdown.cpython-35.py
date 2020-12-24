# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_markdown.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 801 bytes
import ark
try:
    import markdown
except ImportError:
    markdown = None

if markdown:
    settings = ark.site.config.get('markdown', {})
    renderer = markdown.Markdown(**settings)

    @ark.renderers.register('md')
    def render(text):
        return renderer.reset().convert(text)