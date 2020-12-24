# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\wix.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.wix

Tool-specific initialization for wix, the Windows Installer XML Tool.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
__revision__ = 'src/engine/SCons/Tool/wix.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Builder, SCons.Action, os

def generate(env):
    """Add Builders and construction variables for WiX to an Environment."""
    if not exists(env):
        return
    env['WIXCANDLEFLAGS'] = ['-nologo']
    env['WIXCANDLEINCLUDE'] = []
    env['WIXCANDLECOM'] = '$WIXCANDLE $WIXCANDLEFLAGS -I $WIXCANDLEINCLUDE -o ${TARGET} ${SOURCE}'
    env['WIXLIGHTFLAGS'].append('-nologo')
    env['WIXLIGHTCOM'] = '$WIXLIGHT $WIXLIGHTFLAGS -out ${TARGET} ${SOURCES}'
    env['WIXSRCSUF'] = '.wxs'
    env['WIXOBJSUF'] = '.wixobj'
    object_builder = SCons.Builder.Builder(action='$WIXCANDLECOM', suffix='$WIXOBJSUF', src_suffix='$WIXSRCSUF')
    linker_builder = SCons.Builder.Builder(action='$WIXLIGHTCOM', src_suffix='$WIXOBJSUF', src_builder=object_builder)
    env['BUILDERS']['WiX'] = linker_builder


def exists(env):
    env['WIXCANDLE'] = 'candle.exe'
    env['WIXLIGHT'] = 'light.exe'
    for path in os.environ['PATH'].split(os.pathsep):
        if not path:
            continue
        if path[0] == '"' and path[-1:] == '"':
            path = path[1:-1]
        path = os.path.normpath(path)
        try:
            files = os.listdir(path)
            if env['WIXCANDLE'] in files and env['WIXLIGHT'] in files:
                env.PrependENVPath('PATH', path)
                if 'wixui.wixlib' in files and 'WixUI_en-us.wxl' in files:
                    env['WIXLIGHTFLAGS'] = [
                     os.path.join(path, 'wixui.wixlib'),
                     '-loc',
                     os.path.join(path, 'WixUI_en-us.wxl')]
                else:
                    env['WIXLIGHTFLAGS'] = []
                return 1
        except OSError:
            pass

    return