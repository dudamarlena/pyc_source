# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\yacc.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.yacc

Tool-specific initialization for yacc.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/yacc.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path, SCons.Defaults, SCons.Tool, SCons.Util
YaccAction = SCons.Action.Action('$YACCCOM', '$YACCCOMSTR')

def _yaccEmitter(target, source, env, ysuf, hsuf):
    yaccflags = env.subst('$YACCFLAGS', target=target, source=source)
    flags = SCons.Util.CLVar(yaccflags)
    targetBase, targetExt = os.path.splitext(SCons.Util.to_String(target[0]))
    if '.ym' in ysuf:
        target = [
         targetBase + '.m']
    if '-d' in flags:
        target.append(targetBase + env.subst(hsuf, target=target, source=source))
    if '-g' in flags:
        base, ext = os.path.splitext(SCons.Util.to_String(source[0]))
        target.append(base + env.subst('$YACCVCGFILESUFFIX'))
    if '-v' in flags:
        env.SideEffect(targetBase + '.output', target[0])
        env.Clean(target[0], targetBase + '.output')
    fileGenOptions = [
     '--defines=', '--graph=']
    for option in flags:
        for fileGenOption in fileGenOptions:
            l = len(fileGenOption)
            if option[:l] == fileGenOption:
                fileName = option[l:].strip()
                target.append(fileName)

    return (
     target, source)


def yEmitter(target, source, env):
    return _yaccEmitter(target, source, env, ['.y', '.yacc'], '$YACCHFILESUFFIX')


def ymEmitter(target, source, env):
    return _yaccEmitter(target, source, env, ['.ym'], '$YACCHFILESUFFIX')


def yyEmitter(target, source, env):
    return _yaccEmitter(target, source, env, ['.yy'], '$YACCHXXFILESUFFIX')


def generate(env):
    """Add Builders and construction variables for yacc to an Environment."""
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)
    c_file.add_action('.y', YaccAction)
    c_file.add_emitter('.y', yEmitter)
    c_file.add_action('.yacc', YaccAction)
    c_file.add_emitter('.yacc', yEmitter)
    c_file.add_action('.ym', YaccAction)
    c_file.add_emitter('.ym', ymEmitter)
    cxx_file.add_action('.yy', YaccAction)
    cxx_file.add_emitter('.yy', yyEmitter)
    env['YACC'] = env.Detect('bison') or 'yacc'
    env['YACCFLAGS'] = SCons.Util.CLVar('')
    env['YACCCOM'] = '$YACC $YACCFLAGS -o $TARGET $SOURCES'
    env['YACCHFILESUFFIX'] = '.h'
    env['YACCHXXFILESUFFIX'] = '.hpp'
    env['YACCVCGFILESUFFIX'] = '.vcg'


def exists(env):
    return env.Detect(['bison', 'yacc'])