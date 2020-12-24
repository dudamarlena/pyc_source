# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\latex.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.latex

Tool-specific initialization for LaTeX.
Generates .dvi files from .latex or .ltx files

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/latex.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Defaults, SCons.Scanner.LaTeX, SCons.Util, SCons.Tool, SCons.Tool.tex

def LaTeXAuxFunction(target=None, source=None, env=None):
    result = SCons.Tool.tex.InternalLaTeXAuxAction(SCons.Tool.tex.LaTeXAction, target, source, env)
    if result != 0:
        SCons.Tool.tex.check_file_error_message(env['LATEX'])
    return result


LaTeXAuxAction = SCons.Action.Action(LaTeXAuxFunction, strfunction=SCons.Tool.tex.TeXLaTeXStrFunction)

def generate(env):
    """Add Builders and construction variables for LaTeX to an Environment."""
    env.AppendUnique(LATEXSUFFIXES=SCons.Tool.LaTeXSuffixes)
    import dvi
    dvi.generate(env)
    import pdf
    pdf.generate(env)
    bld = env['BUILDERS']['DVI']
    bld.add_action('.ltx', LaTeXAuxAction)
    bld.add_action('.latex', LaTeXAuxAction)
    bld.add_emitter('.ltx', SCons.Tool.tex.tex_eps_emitter)
    bld.add_emitter('.latex', SCons.Tool.tex.tex_eps_emitter)
    SCons.Tool.tex.generate_common(env)


def exists(env):
    SCons.Tool.tex.generate_darwin(env)
    return env.Detect('latex')