# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\dvipdf.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.dvipdf

Tool-specific initialization for dvipdf.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/dvipdf.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Defaults, SCons.Tool.pdf, SCons.Tool.tex, SCons.Util
_null = SCons.Scanner.LaTeX._null

def DviPdfPsFunction(XXXDviAction, target=None, source=None, env=None):
    """A builder for DVI files that sets the TEXPICTS environment
       variable before running dvi2ps or dvipdf."""
    try:
        abspath = source[0].attributes.path
    except AttributeError:
        abspath = ''

    saved_env = SCons.Scanner.LaTeX.modify_env_var(env, 'TEXPICTS', abspath)
    result = XXXDviAction(target, source, env)
    if saved_env is _null:
        try:
            del env['ENV']['TEXPICTS']
        except KeyError:
            pass

    else:
        env['ENV']['TEXPICTS'] = saved_env
    return result


def DviPdfFunction(target=None, source=None, env=None):
    global PDFAction
    result = DviPdfPsFunction(PDFAction, target, source, env)
    return result


def DviPdfStrFunction(target=None, source=None, env=None):
    """A strfunction for dvipdf that returns the appropriate
    command string for the no_exec options."""
    if env.GetOption('no_exec'):
        result = env.subst('$DVIPDFCOM', 0, target, source)
    else:
        result = ''
    return result


PDFAction = None
DVIPDFAction = None

def PDFEmitter(target, source, env):
    """Strips any .aux or .log files from the input source list.
    These are created by the TeX Builder that in all likelihood was
    used to generate the .dvi file we're using as input, and we only
    care about the .dvi file.
    """

    def strip_suffixes(n):
        return SCons.Util.splitext(str(n))[1] not in ('.aux', '.log')

    source = list(filter(strip_suffixes, source))
    return (target, source)


def generate(env):
    """Add Builders and construction variables for dvipdf to an Environment."""
    global DVIPDFAction
    global PDFAction
    if PDFAction is None:
        PDFAction = SCons.Action.Action('$DVIPDFCOM', '$DVIPDFCOMSTR')
    if DVIPDFAction is None:
        DVIPDFAction = SCons.Action.Action(DviPdfFunction, strfunction=DviPdfStrFunction)
    import pdf
    pdf.generate(env)
    bld = env['BUILDERS']['PDF']
    bld.add_action('.dvi', DVIPDFAction)
    bld.add_emitter('.dvi', PDFEmitter)
    env['DVIPDF'] = 'dvipdf'
    env['DVIPDFFLAGS'] = SCons.Util.CLVar('')
    env['DVIPDFCOM'] = 'cd ${TARGET.dir} && $DVIPDF $DVIPDFFLAGS ${SOURCE.file} ${TARGET.file}'
    env['PDFCOM'] = [
     '$DVIPDFCOM']
    return


def exists(env):
    SCons.Tool.tex.generate_darwin(env)
    return env.Detect('dvipdf')