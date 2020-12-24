# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/ide.py
# Compiled at: 2016-03-01 18:44:57
# Size of source mod 2**32: 7271 bytes
"""IDE for model machine."""
import warnings, sys
from modelmachine.cpu import CPU_LIST
from modelmachine.cu import HALTED
from modelmachine import asm
POS = [
 0, 0]
MAX_POS = [20, 20]
INSTRUCTION = 'Enter\n  `(s)tep [count]` to start execution\n  `(c)ontinue` to continue the program until the end\n  `(p)rint` registers state\n  `(m)emory <begin> <end>` to view random access memory\n  `(q)uit` to quit\n'

def exec_step(cpu, step, command):
    """Exec debug step command."""
    need_help = False
    if cpu.control_unit.get_status() == HALTED:
        print('cannot execute command: machine halted')
    else:
        command = command.split()
    try:
        if len(command) == 2:
            count = int(command[1], 0)
        else:
            if len(command) == 1:
                count = 1
            else:
                raise ValueError()
    except ValueError:
        need_help = True
        count = None
    else:
        for i in range(count):
            i = i
            step += 1
            cpu.control_unit.step()
            print('step {step}:'.format(step=step))
            exec_print(cpu, step)
            if cpu.control_unit.get_status() == HALTED:
                print('machine halted')
                break

    return (
     step, need_help, False)


def exec_continue(cpu, step):
    """Exec debug continue command."""
    if cpu.control_unit.get_status() == HALTED:
        print('cannot execute command: machine halted')
    else:
        cpu.control_unit.run()
        print('machine halted')
    return (step, False, False)


def exec_print(cpu, step):
    """Print contents of registers."""
    print('RAM access count:', cpu.ram.access_count)
    print('Registers state:')
    registers = sorted(list(cpu.registers.keys()))
    for reg in registers:
        size = cpu.registers.register_sizes[reg]
        data = '0x' + hex(cpu.registers[reg])[2:].rjust(size // 4, '0')
        print('  ' + reg + ' : ' + data)

    return (step, False, False)


def exec_memory(cpu, step, command):
    """Print contents of RAM."""
    need_help = False
    command = command.split()
    if len(command) == 3:
        try:
            begin = int(command[1], 0)
            end = int(command[2], 0)
        except ValueError:
            need_help = True
        else:
            print(cpu.io_unit.store_hex(begin, (end - begin) * cpu.ram.word_size))
    else:
        need_help = True
    return (step, need_help, False)


def exec_command(cpu, step, command):
    """Exec one command and generate step, need_help and need_quit variables."""
    if command[0] == 's':
        return exec_step(cpu, step, command)
    else:
        if command[0] == 'c':
            return exec_continue(cpu, step)
        if command[0] == 'p':
            return exec_print(cpu, step)
        if command[0] == 'm':
            return exec_memory(cpu, step, command)
        if command[0] == 'q':
            return (step, False, True)
        return (step, True, False)


def debug(cpu):
    """Debug cycle."""
    import readline
    readline = readline
    print('Wellcome to interactive debug mode.\nBeware: now every error breaks the debugger.')
    need_quit = False
    need_help = True
    step = 0
    while not need_quit:
        if need_help:
            print(INSTRUCTION)
            need_help = False
        try:
            command = input('> ') + ' '
        except EOFError:
            command = 'quit'
            print(command)

        try:
            with warnings.catch_warnings(record=True) as (warns):
                warnings.simplefilter('always')
                step, need_help, need_quit = exec_command(cpu, step, command)
                for warn in warns:
                    print('Warning:', warn.message)

        except Exception as error:
            print('Error:', error.args[0])
            cpu.alu.halt()
            print('machine has halted')


def get_cpu(source, protect_memory):
    """Return empty cpu or raise the ValueError."""
    arch = source[0].strip()
    if arch in CPU_LIST:
        cpu = CPU_LIST[arch](protect_memory)
        return cpu
    raise ValueError('Unexpected arch (found in first line): {arch}'.format(arch=arch))


def get_program(filename, protect_memory):
    """Read model machine program."""
    with open(filename, 'r') as (source_file):
        source = source_file.readlines()
        cpu = get_cpu(source, protect_memory)
        cpu.load_program(source)
        return cpu


def assemble(input_filename, output_filename):
    """Assemble input_filename and wrote output_filename."""
    with open(input_filename, 'r') as (input_file):
        input_data = input_file.read()
    error_list, code = asm.parse(input_data)
    if error_list != []:
        print('Compilation aborted with errors:')
        for error in error_list:
            print(error, file=sys.stderr)
            exit(1)

    else:
        print('Success compilation.')
        with open(output_filename, 'w') as (output_file):
            print(code, file=output_file)