# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/check-stackeffect.py
# Compiled at: 2017-09-21 14:36:10
import opcode_33
exec open('/src/external-vcs/bitbucket/maynard/maynard/stackeffect.py', 'r').read()
for i in range(255):
    my_effect = opcode_33.oppush[i] - opcode_33.oppop[i]
    if my_effect != opcode_stack_effect[i]:
        if my_effect <= -8 or opcode_stack_effect[i] == -9:
            continue
        print '%s should have effect %d, got %d' % (opcode_33.opname[i], opcode_stack_effect[i], my_effect)