# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/code.py
# Compiled at: 2018-12-02 10:27:40
# Size of source mod 2**32: 3900 bytes
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo
"""
from beampy import document
from beampy.modules.figure import figure
from beampy.modules.core import beampy_module
import tempfile, os
from textwrap import dedent
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import SvgFormatter
    is_pigment = True
except:
    is_pigment = False

class code(beampy_module):
    __doc__ = "\n    Add highlighted code syntax to your presentation. This module require pygments.\n\n    Parameters\n    ----------\n\n    codetext : string\n        Text of the code source to include.\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the code (the default is 'center'). See\n        positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the code (the default is 'auto'). See positioning\n        system of Beampy.\n\n    width : string, optional\n        Width of the code (the default is :py:mod:`document._width`). The value\n        is given as string with a unit accepted by svg syntax.\n\n    language : string or None, optional\n        Language of the source code (the default value is None, which implies\n        that the language is guessed by pygments). See pygments language for\n        available ones.\n\n    size : string, optional\n        Font size used to render the source code (the default is '14px').\n\n\n    .. note::\n       This module is in very draft stage !!!\n\n    "

    def __init__(self, codetext, x='center', y='auto', width=None, language=None, size='14px'):
        self.type = 'svg'
        self.content = dedent(codetext)
        self.x = x
        self.y = y
        if width is None:
            self.width = document._width
        else:
            self.width = width
        self.args = {'language': language, 'font_size': size}
        self.language = language
        self.font_size = size
        if is_pigment:
            self.register()
        else:
            print("Python pygment is not installed, I can't translate code into svg...")

    def code2svg(self):
        """
            function to render code to svg
        """
        inkscapecmd = document._external_cmd['inkscape']
        codein = self.content
        if self.language is None:
            lexer = guess_lexer(codein)
        else:
            lexer = get_lexer_by_name(self.language, stripall=True)
        svgcode = highlight(codein, lexer, SvgFormatter(fontsize=self.font_size, style='tango'))
        tmpfile, tmpname = tempfile.mkstemp(prefix='beampytmp_CODE')
        with open(tmpname + '.svg', 'w') as (f):
            f.write(svgcode)
        cmd = inkscapecmd + ' -z -T -l=%s %s' % (tmpname + '_good.svg', tmpname + '.svg')
        req = os.popen(cmd)
        req.close()
        f = figure(tmpname + '_good.svg', width=self.width.value, height=self.height.value)
        f.positionner = self.positionner
        f.render()
        self.svgout = f.svgout
        self.positionner = f.positionner
        self.width = f.width
        self.height = f.height
        self.update_size(self.width, self.height)
        f.delete()
        os.remove(tmpname + '.svg')
        os.remove(tmpname + '_good.svg')
        os.remove(tmpname)

    def render(self):
        self.code2svg()
        self.rendered = True