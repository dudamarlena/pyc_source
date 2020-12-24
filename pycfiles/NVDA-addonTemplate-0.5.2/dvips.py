# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\dvips.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.dvips

Tool-specific initialization for dvips.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/dvips.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Tool.dvipdf, SCons.Util

def DviPsFunction(target=None, source=None, env=None):
    global PSAction
    result = SCons.Tool.dvipdf.DviPdfPsFunction(PSAction, target, source, env)
    return result


def DviPsStrFunction(target=None, source=None, env=None):
    """A strfunction for dvipdf that returns the appropriate
    command string for the no_exec options."""
    if env.GetOption('no_exec'):
        result = env.subst('$PSCOM', 0, target, source)
    else:
        result = ''
    return result


PSAction = None
DVIPSAction = None
PSBuilder = None

def generate(env):
    """Add Builders and construction variables for dvips to an Environment."""
    global DVIPSAction
    global PSAction
    global PSBuilder
    if PSAction is None:
        PSAction = SCons.Action.Action('$PSCOM', '$PSCOMSTR')
    if DVIPSAction is None:
        DVIPSAction = SCons.Action.Action(DviPsFunction, strfunction=DviPsStrFunction)
    if PSBuilder is None:
        PSBuilder = SCons.Builder.Builder(action=PSAction, prefix='$PSPREFIX', suffix='$PSSUFFIX', src_suffix='.dvi', src_builder='DVI', single_source=True)
    env['BUILDERS']['PostScript'] = PSBuilder
    env['DVIPS'] = 'dvips'
    env['DVIPSFLAGS'] = SCons.Util.CLVar('')
    env['PSCOM'] = 'cd ${TARGET.dir} && $DVIPS $DVIPSFLAGS -o ${TARGET.file} ${SOURCE.file}'
    env['PSPREFIX'] = ''
    env['PSSUFFIX'] = '.ps'
    return


def exists(env):
    SCons.Tool.tex.generate_darwin(env)
    return env.Detect('dvips')