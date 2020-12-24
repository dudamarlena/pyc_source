# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sysadmin/src/malt/malt/ext/malt_markdown.py
# Compiled at: 2017-05-12 18:30:51
# Size of source mod 2**32: 804 bytes
import malt
try:
    import markdown
except ImportError:
    markdown = None

if markdown:
    settings = malt.site.config.get('markdown', {})
    renderer = (markdown.Markdown)(**settings)

    @malt.renderers.register('md')
    def render(text):
        return renderer.reset().convert(text)