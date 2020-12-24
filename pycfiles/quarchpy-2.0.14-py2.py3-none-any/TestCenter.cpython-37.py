# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\utilities\TestCenter.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 5030 bytes
"""
Implements the standard TestCenter API for Python, allowing a Python script to execute all TestCenter functions.
This is Quarch internal use only.  Each function uses the stdin/stdout to communicate with the TestCenter process
as such, communication is based on simple strings
"""
from inspect import getframeinfo, stack
import sys

def setup(interface_name, *command_params):
    """
    Sets up a test interface, passing the interface parameters onto TestCenter to process
    
    Parameters
    ----------
    interface_name : str
        Name of the interface to setup
    command_params : iterable object
        List of parameter strings to be passed to the setup function    
        
    Returns
    -------
    setup_response : str
        String returned from setup function. Generally "1" or "0" as a boolean success flag    

    """
    caller = getframeinfo(stack()[1][0])
    sys.stdout.write('SETUP,' + str(caller.filename) + ',' + str(caller.lineno) + ',' + interface_name + ',')
    for index, item in enumerate(command_params):
        if index < len(command_params) - 1:
            sys.stdout.write('"' + item + '"' + ',')
        else:
            sys.stdout.write('"' + item)

    sys.stdout.write('\n')
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def testPoint(command_name, *command_params):
    """
    Runs a test point from the testcenter library functions
    
    Parameters
    ----------
    command_name : str
        In the form InterfaceName.TestName
    command_params : iterable object
        List of parameter strings to be passed to the test function    
        
    Returns
    -------
    test_response : str
        String returned from test function. This varies based on the TestPoint spec    

    """
    try:
        caller = getframeinfo(stack()[2][0])
    except:
        caller = getframeinfo(stack()[1][0])

    sys.stdout.write('TEST,' + str(caller.filename) + ',' + str(caller.lineno) + ',' + command_name + ',')
    for x in command_params:
        sys.stdout.write('"' + x + '"' + ',')

    sys.stdout.write('\n')
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def endTest():
    """
    Orders the end of the test.  This will terminate the test parser and disponse of any resources
    held by the test libraries (including quarch module connections)      

    """
    caller = getframeinfo(stack()[1][0])
    sys.stdout.write('ENDTEST,' + str(caller.filename) + ',' + str(caller.lineno))
    sys.stdout.write('\n')
    sys.stdout.flush()


def beginTestBlock(message_text):
    """
    Notes the start of a block of tests.  This allows multiple nested layers of related tests
    to improve readability of the results.  This has no effect on the test execution, only
    on the reporting of the results.
    
    Parameters
    ----------
    message_text : str
        User message describing the test block.  This will be shown in the results    
        
    Returns
    -------
    test_response : str
        String returned from test function. This will be "1" on success and "0" on error     
            
    """
    caller = getframeinfo(stack()[1][0])
    sys.stdout.write('BLOCK_START,' + str(caller.filename) + ',' + str(caller.lineno) + ',' + '"' + message_text + '"')
    sys.stdout.write('\n')
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def endTestBlock():
    """
    Notes the end of a block of tests.  This allows multiple nested layers of related tests
    to improve readability of the results.  This has no effect on the test execution, only
    on the reporting of the results. 

    Returns
    -------
    test_response : str
        String returned from test function. This will be "1" on success and "0" on error      
            
    """
    caller = getframeinfo(stack()[1][0])
    sys.stdout.write('BLOCK_END,' + str(caller.filename) + ',' + str(caller.lineno) + ',' + '"')
    sys.stdout.write('\n')
    sys.stdout.flush()
    return sys.stdin.readline().strip()