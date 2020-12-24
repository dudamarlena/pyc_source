# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\pdftex.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.pdftex

Tool-specific initialization for pdftex.
Generates .pdf files from .tex files

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/pdftex.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, SCons.Action, SCons.Util, SCons.Tool.tex
PDFTeXAction = None
PDFLaTeXAction = None

def PDFLaTeXAuxAction(target=None, source=None, env=None):
    global PDFLaTeXAction
    result = SCons.Tool.tex.InternalLaTeXAuxAction(PDFLaTeXAction, target, source, env)
    return result


def PDFTeXLaTeXFunction(target=None, source=None, env=None):
    """A builder for TeX and LaTeX that scans the source file to
    decide the "flavor" of the source and then executes the appropriate
    program."""
    global PDFTeXAction
    basedir = os.path.split(str(source[0]))[0]
    abspath = os.path.abspath(basedir)
    if SCons.Tool.tex.is_LaTeX(source, env, abspath):
        result = PDFLaTeXAuxAction(target, source, env)
        if result != 0:
            SCons.Tool.tex.check_file_error_message(env['PDFLATEX'])
    else:
        result = PDFTeXAction(target, source, env)
        if result != 0:
            SCons.Tool.tex.check_file_error_message(env['PDFTEX'])
    return result


PDFTeXLaTeXAction = None

def generate(env):
    """Add Builders and construction variables for pdftex to an Environment."""
    global PDFLaTeXAction
    global PDFTeXAction
    global PDFTeXLaTeXAction
    if PDFTeXAction is None:
        PDFTeXAction = SCons.Action.Action('$PDFTEXCOM', '$PDFTEXCOMSTR')
    if PDFLaTeXAction is None:
        PDFLaTeXAction = SCons.Action.Action('$PDFLATEXCOM', '$PDFLATEXCOMSTR')
    if PDFTeXLaTeXAction is None:
        PDFTeXLaTeXAction = SCons.Action.Action(PDFTeXLaTeXFunction, strfunction=SCons.Tool.tex.TeXLaTeXStrFunction)
    env.AppendUnique(LATEXSUFFIXES=SCons.Tool.LaTeXSuffixes)
    import pdf
    pdf.generate(env)
    bld = env['BUILDERS']['PDF']
    bld.add_action('.tex', PDFTeXLaTeXAction)
    bld.add_emitter('.tex', SCons.Tool.tex.tex_pdf_emitter)
    pdf.generate2(env)
    SCons.Tool.tex.generate_common(env)
    return


def exists(env):
    SCons.Tool.tex.generate_darwin(env)
    return env.Detect('pdftex')