# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/site_tools/ldf_compiler.py
# Compiled at: 2015-03-19 14:45:48
import SCons.Builder, SCons.Action, os.path, sys, utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from pymomo.utilities.paths import convert_path

def ldf_generator(source, target, env, for_signature):
    """
        Create an command line to drive the LDF compiler using the parameter defined in 
        the environment
        """
    chip = env['ARCH']
    types = chip.property('type_package', None)
    if types is None:
        args = [
         'momo --norc SystemLog LogDefinitionMap']
    else:
        args = [
         'momo --norc import_types "%s" SystemLog LogDefinitionMap' % types]
    for src in source:
        args.append('add_ldf "%s"' % str(src))

    args.append('generate_header "%s"' % str(target[0]))
    return SCons.Action.Action((' ').join(args), 'Compiling Log Definitions into %s' % str(target[0]))


_ldf_obj = SCons.Builder.Builder(generator=ldf_generator, suffix='.h')

def generate(env):
    env['BUILDERS']['ldf_compiler'] = _ldf_obj


def exists(env):
    return 1