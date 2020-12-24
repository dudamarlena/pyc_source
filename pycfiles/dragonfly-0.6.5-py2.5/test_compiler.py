# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\test_compiler.py
# Compiled at: 2008-11-19 12:15:14
import rule, elements, compiler, core
l = core.GrammarList('somelist')
element = elements.Seq((
 elements.Lit('good morning'),
 elements.Lst(l)))
r = rule.Rule('test_rule', element, exported=True)
c = compiler.Compiler()
r.compile(c)
output = c.compile()
print 'Compiler state:'
print c.debug_state_string()
print 'Output:'
binary = ('').join([ '%02x' % ord(c) for c in output ])
for index in xrange(0, len(binary), 4):
    if index and not index % 32:
        print
    print binary[index:index + 4],