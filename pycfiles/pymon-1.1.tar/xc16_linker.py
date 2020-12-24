# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/site_tools/xc16_linker.py
# Compiled at: 2015-03-19 14:45:48
import SCons.Builder, SCons.Action, os.path, sys, utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from pymomo.utilities.paths import convert_path

def get_map_file(targetdir, env):
    return os.path.join(targetdir, env['ARCH'].output_name() + '.map')


def xc16_generator(source, target, env, for_signature):
    """
        Create an XC16 command line using the parameter defined in 
        the environment
        """
    arch = env['ARCH']
    targetdir = str(target[0].get_dir())
    args = [
     'xc16-gcc']
    args.extend(['-mcpu=%s' % arch.property('chip')])
    args.extend([ str(x) for x in source ])
    args.extend(['-o %s' % str(target[0])])
    args.extend(utilities.build_libdirs(arch.property('libdirs', default=[])))
    args.extend(utilities.build_staticlibs(arch.property('libraries', default=[]), arch))
    args.extend(['-Wl,-Map=%s' % get_map_file(targetdir, env)])
    args.extend(arch.property('ldflags', default=[]))
    linker_script = arch.property('linker', default=None)
    if linker_script is not None:
        args.append('-T%s' % linker_script)
    return SCons.Action.Action((' ').join(args), 'Linking %s' % str(target[0]))


def xc16_emitter(target, source, env):
    targetdir = str(target[0].get_dir())
    target += [get_map_file(targetdir, env)]
    return (
     target, source)


_xc16_obj = SCons.Builder.Builder(generator=xc16_generator, emitter=xc16_emitter, suffix='.o')

def generate(env):
    env['BUILDERS']['xc16_ld'] = _xc16_obj


def exists(env):
    return 1