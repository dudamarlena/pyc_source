# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/repl.py
# Compiled at: 2015-09-07 06:11:28
from Queue import Empty
from scheme import debug
__author__ = 'perkins'
from scheme.parser import Parser
import scheme.processer
processer = scheme.processer.processer
import sys
Es = []

def repl(f=sys.stdin, prompt='schemepy> ', of=sys.stdout):
    global parser
    parser = Parser(f)
    while True:
        sys.stdout.write(prompt)
        try:
            ast = parser.ast
        except Exception as e:
            print e
            continue

        if ast:
            try:
                r = processer.doProcess(ast)
            except Empty as e:
                if hasattr(e, 'ret'):
                    r = e.ret
                else:
                    import traceback
                    traceback.print_exc()
                    raise e
            except Exception as e:
                if debug.getDebug('repl'):
                    Es.append(e)
                    import traceback
                    print traceback.format_exc()
                    print processer.ast
                    if processer.children:
                        print processer.children[(-1)].ast
                    print scheme.processer.current_processer.ast
                r = e

            if r is not None and of:
                print >> of, r
        else:
            break

    return