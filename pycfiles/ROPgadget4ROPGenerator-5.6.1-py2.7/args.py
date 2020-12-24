# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/args.py
# Compiled at: 2018-03-17 16:59:29
import argparse, sys
from ropgadget.updateAlert import UpdateAlert
from ropgadget.version import *

class Args(object):

    def __init__(self, arguments=None):
        self.__args = None
        custom_arguments_provided = True
        if not arguments:
            arguments = sys.argv[1:]
            custom_arguments_provided = False
        self.__parse(arguments, custom_arguments_provided)
        return

    def __parse(self, arguments, custom_arguments_provided=False):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='description:\n  ROPgadget lets you search your gadgets on a binary. It supports several \n  file formats and architectures and uses the Capstone disassembler for\n  the search engine.\n\nformats supported: \n  - ELF\n  - PE\n  - Mach-O\n  - Raw\n\narchitectures supported:\n  - x86\n  - x86-64\n  - ARM\n  - ARM64\n  - MIPS\n  - PowerPC\n  - Sparc\n', epilog='examples:\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 \n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --ropchain\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --depth 3\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --string "main"\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --string "m..n"\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --opcode c9c3\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --only "mov|ret"\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --only "mov|pop|xor|ret"\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --filter "xchg|add|sub"\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --norop --nosys\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --range 0x08041000-0x08042000\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --string main --range 0x080c9aaa-0x080c9aba\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --memstr "/bin/sh"\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --console\n  ROPgadget.py --binary ./test-suite-binaries/elf-Linux-x86 --badbytes "00|01-1f|7f|42"\n  ROPgadget.py --binary ./test-suite-binaries/Linux_lib64.so --offset 0xdeadbeef00000000\n  ROPgadget.py --binary ./test-suite-binaries/elf-ARMv7-ls --depth 5\n  ROPgadget.py --binary ./test-suite-binaries/elf-ARM64-bash --depth 5\n  ROPgadget.py --binary ./test-suite-binaries/raw-x86.raw --rawArch=x86 --rawMode=32')
        parser.add_argument('-v', '--version', action='store_true', help="Display the ROPgadget's version")
        parser.add_argument('-c', '--checkUpdate', action='store_true', help='Checks if a new version is available')
        parser.add_argument('--binary', type=str, metavar='<binary>', help='Specify a binary filename to analyze')
        parser.add_argument('--opcode', type=str, metavar='<opcodes>', help='Search opcode in executable segment')
        parser.add_argument('--string', type=str, metavar='<string>', help='Search string in readable segment')
        parser.add_argument('--memstr', type=str, metavar='<string>', help='Search each byte in all readable segment')
        parser.add_argument('--depth', type=int, metavar='<nbyte>', default=10, help='Depth for search engine (default 10)')
        parser.add_argument('--only', type=str, metavar='<key>', help='Only show specific instructions')
        parser.add_argument('--filter', type=str, metavar='<key>', help='Suppress specific instructions')
        parser.add_argument('--range', type=str, metavar='<start-end>', default='0x0-0x0', help='Search between two addresses (0x...-0x...)')
        parser.add_argument('--badbytes', type=str, metavar='<byte>', help="Rejects specific bytes in the gadget's address")
        parser.add_argument('--rawArch', type=str, metavar='<arch>', help='Specify an arch for a raw file')
        parser.add_argument('--rawMode', type=str, metavar='<mode>', help='Specify a mode for a raw file')
        parser.add_argument('--re', type=str, metavar='<re>', help='Regular expression')
        parser.add_argument('--offset', type=str, metavar='<hexaddr>', help='Specify an offset for gadget addresses')
        parser.add_argument('--ropchain', action='store_true', help='Enable the ROP chain generation')
        parser.add_argument('--thumb', action='store_true', help='Use the thumb mode for the search engine (ARM only)')
        parser.add_argument('--console', action='store_true', help='Use an interactive console for search engine')
        parser.add_argument('--norop', action='store_true', help='Disable ROP search engine')
        parser.add_argument('--nojop', action='store_true', help='Disable JOP search engine')
        parser.add_argument('--callPreceded', action='store_true', help='Only show gadgets which are call-preceded')
        parser.add_argument('--nosys', action='store_true', help='Disable SYS search engine')
        parser.add_argument('--multibr', action='store_true', help='Enable multiple branch gadgets')
        parser.add_argument('--all', action='store_true', help='Disables the removal of duplicate gadgets')
        parser.add_argument('--dump', action='store_true', help='Outputs the gadget bytes')
        self.__args = parser.parse_args(arguments)
        if self.__args.version:
            self.__printVersion()
            sys.exit(0)
        elif self.__args.checkUpdate:
            UpdateAlert().checkUpdate()
            sys.exit(0)
        elif self.__args.depth < 2:
            print '[Error] The depth must be >= 2'
            sys.exit(-1)
        elif not custom_arguments_provided and not self.__args.binary and not self.__args.console:
            print '[Error] Need a binary filename (--binary/--console or --help)'
            sys.exit(-1)
        elif self.__args.range:
            try:
                rangeS = int(self.__args.range.split('-')[0], 16)
                rangeE = int(self.__args.range.split('-')[1], 16)
            except:
                print '[Error] A range must be set in hexadecimal. Ex: 0x08041000-0x08042000'
                sys.exit(-1)

            if rangeS > rangeE:
                print '[Error] The start value must be greater than end value'
                sys.exit(-1)

    def __printVersion(self):
        print 'Version:        %s' % PYROPGADGET_VERSION
        print 'Author:         Jonathan Salwan'
        print 'Author page:    https://twitter.com/JonathanSalwan'
        print 'Project page:   http://shell-storm.org/project/ROPgadget/'

    def getArgs(self):
        return self.__args