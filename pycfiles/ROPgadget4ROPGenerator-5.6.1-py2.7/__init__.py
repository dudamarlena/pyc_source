# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/__init__.py
# Compiled at: 2018-03-17 16:59:29
import ropgadget.args, ropgadget.binary, ropgadget.core, ropgadget.gadgets, ropgadget.options, ropgadget.rgutils, ropgadget.updateAlert, ropgadget.version, ropgadget.loaders, ropgadget.ropchain

def main():
    import sys
    from ropgadget.args import Args
    from ropgadget.core import Core
    sys.exit(Core(Args().getArgs()).analyze())