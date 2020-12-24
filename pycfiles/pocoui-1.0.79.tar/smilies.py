# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/smilies.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.core.smilies\n    ~~~~~~~~~~~~~~~~~~~~~~\n\n    Pocoo smilies parser.\n\n    :copyright: 2006 by Benjamin Wiegand, Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo import Component
from pocoo.utils.html import escape_html

def replace_smilies(ctx, text):
    """
    Replace smilies in ``text``, using all providers listed in the
    board config.
    """
    smiley_providers = ctx.cfg.get('board', 'smiley_providers', ['default'])
    for provider in ctx.get_components(SmileyProvider):
        if provider.name not in smiley_providers:
            continue
        for smiley in provider.smilies:
            text = text.replace(smiley[0], provider.render_smiley(smiley))

    return text


def get_smiley_buttons(ctx):
    """
    Return a list of button dictionaries usable for the BBCodeEditor
    JavaScript app.
    """
    res = []
    smiley_providers = ctx.cfg.get('board', 'smiley_providers', ['default'])
    for provider in ctx.get_components(SmileyProvider):
        if provider.name not in smiley_providers:
            continue
        for smiley in provider.smilies:
            res.append(smiley + (ctx.make_url(provider.smiley_dir),))

    return res


class SmileyProvider(Component):
    """
    A SmileyProvider maps small text strings to images.
    """
    __module__ = __name__
    smilies = []
    smiley_dir = ''

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def render_smiley(self, smiley):
        """
        Render a smiley. This doesn't need to be overridden in normal
        cases.

        :return: HTML for the smiley image.
        """
        return '<img src="%s" alt="%s" />' % (self.ctx.make_url(self.smiley_dir, smiley[1]), escape_html(smiley[0]))


class Default(SmileyProvider):
    """
    Default Pocoo smilies.
    """
    __module__ = __name__
    smilies = [
     (';-)', 'wink.png'), (':(', 'sad.png'), (':-)', 'smile.png'), (':D', 'grin.png')]
    smiley_dir = '!cobalt/core/default/img/smilies/'