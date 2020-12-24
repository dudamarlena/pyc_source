# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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