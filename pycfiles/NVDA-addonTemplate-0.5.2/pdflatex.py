# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\pdflatex.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.pdflatex

Tool-specific initialization for pdflatex.
Generates .pdf files from .latex or .ltx files

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/pdflatex.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Util, SCons.Tool.pdf, SCons.Tool.tex
PDFLaTeXAction = None

def PDFLaTeXAuxFunction(target=None, source=None, env=None):
    global PDFLaTeXAction
    result = SCons.Tool.tex.InternalLaTeXAuxAction(PDFLaTeXAction, target, source, env)
    if result != 0:
        SCons.Tool.tex.check_file_error_message(env['PDFLATEX'])
    return result


PDFLaTeXAuxAction = None

def generate(env):
    """Add Builders and construction variables for pdflatex to an Environment."""
    global PDFLaTeXAction
    global PDFLaTeXAuxAction
    if PDFLaTeXAction is None:
        PDFLaTeXAction = SCons.Action.Action('$PDFLATEXCOM', '$PDFLATEXCOMSTR')
    if PDFLaTeXAuxAction is None:
        PDFLaTeXAuxAction = SCons.Action.Action(PDFLaTeXAuxFunction, strfunction=SCons.Tool.tex.TeXLaTeXStrFunction)
    env.AppendUnique(LATEXSUFFIXES=SCons.Tool.LaTeXSuffixes)
    import pdf
    pdf.generate(env)
    bld = env['BUILDERS']['PDF']
    bld.add_action('.ltx', PDFLaTeXAuxAction)
    bld.add_action('.latex', PDFLaTeXAuxAction)
    bld.add_emitter('.ltx', SCons.Tool.tex.tex_pdf_emitter)
    bld.add_emitter('.latex', SCons.Tool.tex.tex_pdf_emitter)
    SCons.Tool.tex.generate_common(env)
    return


def exists(env):
    SCons.Tool.tex.generate_darwin(env)
    return env.Detect('pdflatex')