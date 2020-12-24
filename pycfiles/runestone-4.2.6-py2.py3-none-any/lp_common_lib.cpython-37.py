# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/server/lp_common_lib.py
# Compiled at: 2019-08-13 16:05:20
# Size of source mod 2**32: 6487 bytes
import os.path, io, json

def commentForExt(file_name):
    return {'.py':'# ', 
     '.c':'// ', 
     '.h':'// ', 
     '.js':'// ', 
     '.s':'; ', 
     '.rst':'', 
     '.css':'/* ', 
     '.ini':'; '}[os.path.splitext(file_name)[1]]


STUDENT_SOURCE_PATH = '../student_source'
BUILD_SYSTEM_PATH = '../build_system'
SPHINX_CONFIG_NAME = 'sphinx_settings.json'

def read_sphinx_config(dir_='.'):
    try:
        with io.open((os.path.join(dir_, SPHINX_CONFIG_NAME)), encoding='utf-8') as (f):
            return json.loads(f.read())
    except IOError:
        return


def code_here_comment(file_name):
    return _add_line_comment_delimiter(CODE_HERE_STRING, file_name) + '\n'


CODE_HERE_STRING = '``*******************************************``\nAdd your code after this line.\n\nAdd your code before this line.\n``*******************************************``'

def _add_line_comment_delimiter(str_, file_name):
    delim = commentForExt(file_name)
    str_ = str_.replace('\n', '\n' + delim)
    return delim + str_


def get_sim_str_sim30(sim_mcu, elf_file, uart_out_file):
    return 'LD {}\nLC {}\nIO nul {}\nRP\nBS done\nE 10000\nQ\n'.format(sim_mcu, elf_file, uart_out_file)


def get_sim_str_mdb(sim_mcu, elf_file, uart_out_file, optional_commands=''):
    return 'device {}\nhwtool sim\nset uart1io.output file\nset uart1io.uartioenabled true\nset uart1io.outputfile "{}"\nset oscillator.frequency 1\nset oscillator.frequencyunit Mega\nprogram "{}"\nbreak done\n{}\nrun\nwait 6000\nquit\n'.format(sim_mcu, uart_out_file, elf_file, optional_commands)