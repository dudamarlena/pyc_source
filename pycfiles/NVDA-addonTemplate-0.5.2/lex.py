# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\lex.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.lex

Tool-specific initialization for lex.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/lex.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path, SCons.Action, SCons.Tool, SCons.Util
LexAction = SCons.Action.Action('$LEXCOM', '$LEXCOMSTR')

def lexEmitter(target, source, env):
    sourceBase, sourceExt = os.path.splitext(SCons.Util.to_String(source[0]))
    if sourceExt == '.lm':
        target = [
         sourceBase + '.m']
    fileGenOptions = [
     '--header-file=', '--tables-file=']
    lexflags = env.subst('$LEXFLAGS', target=target, source=source)
    for option in SCons.Util.CLVar(lexflags):
        for fileGenOption in fileGenOptions:
            l = len(fileGenOption)
            if option[:l] == fileGenOption:
                fileName = option[l:].strip()
                target.append(fileName)

    return (
     target, source)


def generate(env):
    """Add Builders and construction variables for lex to an Environment."""
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)
    c_file.add_action('.l', LexAction)
    c_file.add_emitter('.l', lexEmitter)
    c_file.add_action('.lex', LexAction)
    c_file.add_emitter('.lex', lexEmitter)
    cxx_file.add_action('.lm', LexAction)
    cxx_file.add_emitter('.lm', lexEmitter)
    cxx_file.add_action('.ll', LexAction)
    cxx_file.add_emitter('.ll', lexEmitter)
    env['LEX'] = env.Detect('flex') or 'lex'
    env['LEXFLAGS'] = SCons.Util.CLVar('')
    env['LEXCOM'] = '$LEX $LEXFLAGS -t $SOURCES > $TARGET'


def exists(env):
    return env.Detect(['flex', 'lex'])