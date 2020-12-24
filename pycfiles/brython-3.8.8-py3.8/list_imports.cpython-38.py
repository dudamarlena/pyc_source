# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\brython\list_imports.py
# Compiled at: 2020-02-18 10:46:58
# Size of source mod 2**32: 478 bytes
imports = []
with open('imports.txt') as (f):
    for line in f:
        if line.startswith('sympy/'):
            module = line.strip().replace('/', '.')
            if module.endswith('.__init__.py'):
                module = module[:-len('.__init__.py')]
            else:
                if module.endswith('.py'):
                    module = module[:-3]
            imports.append(module)
    else:
        if '404' in line:
            imports.pop()

print('imports', imports, len(imports))