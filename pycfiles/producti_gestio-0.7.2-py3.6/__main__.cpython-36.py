# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/__main__.py
# Compiled at: 2018-05-29 14:08:07
# Size of source mod 2**32: 1452 bytes
import producti_gestio.utils.arguments_parser
from producti_gestio.project.generator import generate_code

def main():
    arguments = producti_gestio.utils.arguments_parser.parser()
    generate_code(arguments.name)


if __name__ == '__main__':
    main()