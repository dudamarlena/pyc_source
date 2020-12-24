# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/latex/render.py
# Compiled at: 2006-12-26 17:18:03
__doc__ = '\n    pocoo.pkg.latex.render\n    ~~~~~~~~~~~~~~~~~~~~~~\n\n    Render LaTeX and create images. Needs dvipng.\n    And documentation.\n\n\n    :copyright: 2006 by Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
import sha, os
from os import path
import tempfile, shutil
DOCUMENT = '\n\\documentclass{article}\n\\usepackage[utf-8]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{amsthm}\n\\usepackage{amssymb}\n\\usepackage{amsfonts}\n\\usepackage{bm}\n\\pagestyle{empty}\n\\begin{document}\n\\[ %s \\]\n\\end{document}\n'
BLACKLIST = ('include', 'def', 'command', 'loop', 'repeat', 'open', 'toks', 'output',
             'line', 'input', 'catcode', 'mathcode', 'name', 'item', 'section')

class LatexRender(object):
    __module__ = __name__

    def __init__(self, fmlpath):
        self.fmlpath = fmlpath
        if not path.isdir(fmlpath):
            os.makedirs(fmlpath)

    def render(self, fml):
        """
        Render ``fml`` as LaTeX math mode markup and return a tuple
        ``(filename of PNG file, error message)``.
        """
        shasum = sha.new(fml).hexdigest()
        fn = '%s.png' % shasum
        fnpath = path.join(self.fmlpath, fn)
        if path.isfile(fnpath):
            return (fn, '')
        for cmd in BLACKLIST:
            if '\\' + cmd in fml:
                return ('', 'the %s command is blacklisted' % cmd)

        if '^^' in fml or '\\$\\$' in fml:
            return ('', '^^ and $$ are blacklisted')
        if len(fml) > 1000:
            return ('', 'formula exceeds 1000 characters')
        fml = fml.replace('\n', '\\]\n\\[')
        tex = DOCUMENT % fml
        (tf, texfile) = tempfile.mkstemp('.tex')
        os.write(tf, tex)
        os.close(tf)
        basename = texfile[:-4]
        dirname = path.dirname(basename)
        ret = os.system('latex --interaction=nonstopmode --output-directory="%s" %s' % (dirname, texfile))
        if ret != 0:
            self._cleanup(basename)
            return ('', 'latex failed')
        cmd = 'dvipng -T tight -x 1200 -z 9 -bg transparent ' + '-o %s.png %s.dvi' % (basename, basename)
        ret = os.system(cmd)
        if ret != 0:
            self._cleanup(basename)
            return ('', 'dvipng failed')
        shutil.copyfile(basename + '.png', fnpath)
        self._cleanup(basename)
        return (
         fn, '')

    def _cleanup(self, basename):
        """Delete temporary files."""
        for suffix in ('.tex', '.aux', '.log', '.dvi', '.png'):
            try:
                os.unlink(basename + suffix)
            except:
                pass

        return ''