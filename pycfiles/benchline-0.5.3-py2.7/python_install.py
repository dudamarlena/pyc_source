# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/python_install.py
# Compiled at: 2014-03-25 13:48:40
"""
Installs the changes to a python project to the local machine.

Just a convenience script.
"""
import benchline.args, benchline.command

def validate_args(parser, options, args):
    pass


def main():
    options, args = benchline.args.go(__doc__, validate_args=validate_args)
    if options.doctest:
        benchline.command.run('python setup.py test')
        benchline.command.run('python3 setup.py test')
    benchline.command.run('sudo python3 setup.py install')
    benchline.command.run('sudo python setup.py install')


if __name__ == '__main__':
    main()