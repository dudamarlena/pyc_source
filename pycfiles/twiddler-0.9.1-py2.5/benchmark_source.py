# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/benchmark_source.py
# Compiled at: 2008-07-24 14:48:01
from twiddler.twiddler import Twiddler
from time import time
iterations = 10

def benchmark(source, compiler, runner):
    tsum = 0
    for i in range(iterations):
        t1 = time()
        compiled = compiler(source)
        t2 = time()
        tsum += t2 - t1

    t_compile = tsum / iterations
    for i in range(iterations):
        t1 = time()
        runner(compiled)
        t2 = time()
        tsum += t2 - t1

    t_run = tsum / iterations
    return (t_compile, t_run)


def benchmark1(compiler, runner):
    t = Twiddler('\n    <root xmlns:tal="http://namespaces.zope.org/tal">\n    <element name="e">\n    <repeat name="rX" tal:repeat="i range(0,100,10)">\n    <attributes name="aX" tal:attributes="attrib1 string:Attribute Value">\n    <content name="cX" tal:content="string:My Content"/>\n    </attributes>\n    </repeat>\n    </element>\n    </root>\n    ')
    lengths = range(0, 4, 1)
    lengths[0] = 1
    sequences = [ range(i) for i in range(0, 101, 10) ]
    e = t.getByName('e')
    i = 0
    for length in lengths:
        while i < length:
            si = str(i)
            new = e.repeat()
            new.getByName('rX').replace(name='r' + si)
            new.getByName('aX').replace(name='a' + si)
            new.getByName('cX').replace(name='c' + si)
            i += 1

        print t.render()
        print


benchmark1(None, None)