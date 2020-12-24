# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paula/testing/interact.py
# Compiled at: 2008-08-14 09:21:53
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'
import code, sys

def interact(locals=None):
    """Provides an interactive shell aka console inside your testcase.
    
    It looks exact like in a doctestcase and you can copy and paste
    code from the shell into your doctest. The locals in the testcase are 
    available, because you are _in_ the testcase.

    In your testcase or doctest you can invoke the shell at any point by
    calling::
        
        >>> interact( locals() )        
        
    locals -- passed to InteractiveInterpreter.__init__()
    """
    savestdout = sys.stdout
    sys.stdout = sys.stderr
    sys.stderr.write('\n' + '=' * 75)
    console = code.InteractiveConsole(locals)
    console.interact('\nDocTest Interactive Console - (c) BlueDynamics Alliance, Austria, 2006-2008\nNote: You have the same locals available as in your test-case. \nCtrl-D ends session and continues testing.\n')
    sys.stdout.write('\nend of DocTest Interactive Console session\n')
    sys.stdout.write('=' * 75 + '\n')
    sys.stdout = savestdout