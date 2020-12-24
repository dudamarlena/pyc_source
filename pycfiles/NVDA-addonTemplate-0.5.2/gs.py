# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\gs.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.gs

Tool-specific initialization for Ghostscript.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/gs.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Platform, SCons.Util
platform = SCons.Platform.platform_default()
if platform == 'os2':
    gs = 'gsos2'
elif platform == 'win32':
    gs = 'gswin32c'
else:
    gs = 'gs'
GhostscriptAction = None

def generate(env):
    """Add Builders and construction variables for Ghostscript to an
    Environment."""
    global GhostscriptAction
    try:
        if GhostscriptAction is None:
            GhostscriptAction = SCons.Action.Action('$GSCOM', '$GSCOMSTR')
        import pdf
        pdf.generate(env)
        bld = env['BUILDERS']['PDF']
        bld.add_action('.ps', GhostscriptAction)
    except ImportError as e:
        pass

    gsbuilder = SCons.Builder.Builder(action=SCons.Action.Action('$GSCOM', '$GSCOMSTR'))
    env['BUILDERS']['Gs'] = gsbuilder
    env['GS'] = gs
    env['GSFLAGS'] = SCons.Util.CLVar('-dNOPAUSE -dBATCH -sDEVICE=pdfwrite')
    env['GSCOM'] = '$GS $GSFLAGS -sOutputFile=$TARGET $SOURCES'
    return


def exists(env):
    if 'PS2PDF' in env:
        return env.Detect(env['PS2PDF'])
    else:
        return env.Detect(gs) or SCons.Util.WhereIs(gs)