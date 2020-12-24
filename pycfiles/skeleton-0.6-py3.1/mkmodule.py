# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dinoboff/Documents/workspace/skeleton/src/build/lib/skeleton/examples/mkmodule.py
# Compiled at: 2010-05-11 18:08:22
"""
Basic script to create an empty python package containing one module
"""
from skeleton import Skeleton, Var

class BasicModule(Skeleton):
    """
    Create an empty module with its etup script and a README file.
    """
    src = 'basic-module'
    variables = [
     Var('module_name'),
     Var('author'),
     Var('author_email')]


def main():
    """Basic command line bootstrap for the BasicModule Skeleton"""
    BasicModule.cmd()


if __name__ == '__main__':
    main()