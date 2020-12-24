# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\__main__.py
# Compiled at: 2018-10-08 16:43:40
# Size of source mod 2**32: 2415 bytes
from .disassembler import EvmBytecode
from . import registry
import sys, os, logging
logger = logging.getLogger(__name__)

def main():
    nerrors = 0
    logging.basicConfig(format='%(levelname)-7s - %(message)s', level=logging.WARNING)
    from optparse import OptionParser
    parser = OptionParser()
    loglevels = ['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET']
    parser.add_option('-v', '--verbosity', default='critical', help='available loglevels: %s [default: %%default]' % ','.join(l.lower() for l in loglevels))
    parser.add_option('-l', '--list', action='store_true', help='list instructions')
    parser.add_option('-d', '--disassemble', action='store_true', help='disassemble input')
    options, args = parser.parse_args()
    if options.verbosity.upper() in loglevels:
        options.verbosity = getattr(logging, options.verbosity.upper())
        logger.setLevel(options.verbosity)
    else:
        parser.error('invalid verbosity selected. please check --help')
    if options.list:
        print('  %-2s | %-20s %-20s %-20s' % ('op', 'instruction', 'category', 'gas'))
        print('=' * 60)
        for instr in sorted(registry.INSTRUCTIONS_BY_OPCODE.values(), key=lambda o: o.opcode):
            line = '0x%-2x | %-20s %-20s %-20s' % (instr.opcode, str(instr).strip('\x00'), instr.category, instr.gas)
            if args and any(a.lower() in line.lower() for a in args):
                print(line)
            elif not args:
                print(line)

    else:
        if options.disassemble:
            if not sys.stdin.isatty():
                args.append(sys.stdin.read().strip())
            for a in args:
                if os.path.isfile(a):
                    with open(a, 'r') as (f):
                        a = f.read()
                bytecode = EvmBytecode(a)
                disassembly = bytecode.disassemble()
                nerrors = len(disassembly.errors)
                print(disassembly.as_string)
                if nerrors:
                    logger.warning('Disassembler finished with %d errors' % nerrors)

        else:
            parser.error('not implemented. check --help')
            nerrors = -1
    sys.exit(nerrors)


if __name__ == '__main__':
    main()