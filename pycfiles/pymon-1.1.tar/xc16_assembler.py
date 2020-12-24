# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/site_tools/xc16_assembler.py
# Compiled at: 2015-03-19 14:45:48
import SCons.Builder, SCons.Action, SCons.Scanner, os.path, sys, utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from pymomo.utilities.paths import convert_path

def xc16_generator(source, target, env, for_signature):
    """
        Create an XC16 command line using the parameter defined in 
        the environment
        """
    arch = env['ARCH']
    args = [
     'xc16-gcc']
    args.extend(['-mcpu=%s' % arch.property('chip')])
    args.extend(['-c'])
    args.append(str(source[0]))
    args.extend(['-o %s' % str(target[0])])
    args.extend(utilities.build_includes(arch.includes()))
    args.extend(utilities.build_defines(arch.property('defines', default={})))
    args.extend(arch.property('asflags', default=[]))
    return SCons.Action.Action((' ').join(args), 'Assembling %s' % str(source[0]))


_xc16_obj = SCons.Builder.Builder(generator=xc16_generator, suffix='.o')

def generate(env):
    env['BUILDERS']['xc16_as'] = _xc16_obj


def exists(env):
    return 1