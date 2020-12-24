# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gwfhlang/__main__.py
# Compiled at: 2019-03-25 15:19:12
# Size of source mod 2**32: 550 bytes
from gwfhlang.parser import get_parser
from gwfhlang.compiler import Compiler
from arkhe.controller import Arkhe
from arkhe.debugger import ADB

def main(file, mode='normal'):
    parser = get_parser()
    compiler = Compiler()
    with open(file) as (f):
        content = f.read()
    code = compiler.transform(parser.parse(content))
    vm = Arkhe(code)
    if mode.lower().startswith('d'):
        adb = ADB()
        adb.vm = vm
        adb.run()
    else:
        vm.eval()


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])