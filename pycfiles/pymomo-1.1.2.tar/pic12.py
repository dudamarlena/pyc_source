# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/pic12.py
# Compiled at: 2015-03-19 14:45:48
from SCons.Script import *
from SCons.Environment import Environment
import os, fnmatch, json, sys, os.path
from copy import deepcopy
import utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymomo.utilities import build
from pymomo.mib.config12 import MIB12Processor

def configure_env_for_xc8(env, **kwargs):
    """
        Setup all of the environmental varibles that the xc8 Builder needs in order
        to property configure and build an 8-bit module.  There's a lot of sensitve
        magic here!  Getting the RAM and ROM ranges wrong will cause very subtle but
        deadly bugs as the executive and applications begin to overwite each other's
        variables.  Be careful when you modify this function.
        """
    arch = env['ARCH']
    proc = MIB12Processor('No Name', arch.settings)
    flags = deepcopy(arch.property('xc8_flags', []))
    flags.extend(arch.property('extra_xc8_flags', []))
    defines = deepcopy(arch.property('defines'))
    defines['kFirstApplicationRow'] = proc.first_app_page
    defines['kFlashRowSize'] = proc.row_size
    defines['kFlashMemorySize'] = proc.total_prog_mem
    incs = arch.includes()
    env['MIB_API_BASE'] = proc.api_range[0]
    env['CHIP'] = proc
    if arch.property('is_exec'):
        env['ROMSTART'] = proc.exec_rom[0]
        env['ROMEND'] = proc.exec_rom[1]
        flags += ['-L-Pmibapi=%xh' % env['MIB_API_BASE'], '-L-Papp_vectors=%xh' % proc.app_rom[0]]
        env['RAMEXCLUDE'] = arch.property('application_ram')
    else:
        exec_range = proc.exec_rom
        env['ROMSTART'] = exec_range[1] + 1
        env['ROMEND'] = proc.total_prog_mem - 1
        env['ROMEXCLUDE'] = []
        flags += ['-L-preset_vec=%xh' % (exec_range[1] + 1)]
        mibstart = proc.mib_range[0]
        lnk_cmd = '-L-Pmibblock=%xh' % mibstart
        flags += [lnk_cmd]
        env['RAMEXCLUDE'] = arch.property('executive_ram')
        env['NO_STARTUP'] = True
    env['XC8FLAGS'] = flags
    env['XC8FLAGS'] += utilities.build_defines(defines)
    env['INCLUDE'] = incs


def build_module(name, arch):
    """
        Configure Scons to build an application module for the 8bit pic microchip archicture indicated in arch_name.
        """
    dirs = arch.build_dirs()
    builddir = dirs['build']
    VariantDir(builddir, 'src', duplicate=0)
    env = Environment(tools=['xc8_compiler', 'patch_mib12', 'xc8_symbols'], ENV=os.environ)
    env.AppendENVPath('PATH', '../../tools/scripts')
    env.AppendENVPath('PATH', '../../tools/bin')
    env['ARCH'] = arch
    env['MODULE'] = name
    configure_env_for_xc8(env)
    compile_mib(env)
    Export('env')
    SConscript(os.path.join(builddir, 'SConscript'))
    prods = [
     os.path.join(dirs['build'], 'mib12_app_module.hex'), os.path.join(dirs['build'], 'mib12_app_module_symbols.h'), os.path.join(dirs['build'], 'mib12_app_module_symbols.stb')]
    hexfile = env.InstallAs(os.path.join(dirs['output'], '%s_%s.hex' % (name, arch.arch_name())), prods[0])
    symheader = env.InstallAs(os.path.join(dirs['output'], '%s_symbols_%s.h' % (name, arch.arch_name())), prods[1])
    symtable = env.InstallAs(os.path.join(dirs['output'], '%s_symbols_%s.stb' % (name, arch.arch_name())), prods[2])


def compile_mib(env):
    """
        Given a path to a *.mib file, use mibtool to process it and return a command_map.asm file
        return the path to that file.
        """
    dirs = env['ARCH'].build_dirs()
    mibname = os.path.join('src', 'mib', env['MODULE'] + '.mib')
    cmdmap_path = os.path.join(dirs['build'], 'command_map.asm')
    env['MIBFILE'] = '#' + cmdmap_path
    return env.Command(cmdmap_path, mibname, 'momo-mib gen -o %s $SOURCE' % dirs['build'])