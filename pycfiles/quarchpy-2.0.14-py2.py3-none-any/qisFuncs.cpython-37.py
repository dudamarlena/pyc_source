# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\qis\qisFuncs.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 5944 bytes
"""
Contains general functions for starting and stopping QIS processes
"""
import os, sys, time, platform
from quarchpy.connection_specific.connection_QIS import QisInterface
import subprocess, logging

def isQisRunning():
    """
    Checks if a local instance of QIS is running and responding
    
    Returns
    -------
    is_running : bool
        True if QIS is running and responding

    """
    qisRunning = False
    myQis = None
    try:
        myQis = QisInterface(connectionMessage=False)
        if myQis is not None:
            qisRunning = True
    except:
        pass

    if qisRunning is False:
        logging.debug('QIS is not running')
        return False
    logging.debug('QIS is running')
    return True


def startLocalQis(terminal=False, headless=False, args=None):
    """
    Executes QIS on the local system, using the version contained within quarchpy
    
    Parameters
    ----------
    terminal : bool, optional
        True if QIS terminal should be shown on startup
    headless : bool, optional
        True if app should be run in headless mode for non graphical environments
    args : list[str], optional
        List of additional parameters to be supplied to QIS on the command line

    """
    QisPath = os.path.dirname(os.path.abspath(__file__))
    QisPath, junk = os.path.split(QisPath)
    QisPath = os.path.join(QisPath, 'connection_specific', 'QPS', 'qis', 'qis.jar')
    if not headless == True:
        if not args is not None or '-headless' in args:
            cmdPrefix = ' -Djava.awt.headless=true '
        else:
            cmdPrefix = ''
    elif terminal == True:
        cmdSuffix = ' -terminal'
    else:
        cmdSuffix = ''
    if args is not None:
        for option in args:
            if option == '-terminal':
                if terminal == True:
                    continue
            if option != '-headless':
                cmdSuffix = cmdSuffix + (' ' + option)

    current_direc = os.getcwd()
    os.chdir(os.path.dirname(QisPath))
    command = cmdPrefix + '-jar qis.jar' + cmdSuffix
    currentOs = platform.system()
    if currentOs == 'Windows':
        command = 'start /high /b javaw ' + command
        os.system(command)
    else:
        if currentOs == 'Linux':
            if sys.version_info[0] < 3:
                os.popen2('java ' + command)
            else:
                os.popen('java ' + command)
        else:
            command = 'start /high /b javaw ' + command
            os.system(command)
    time.sleep(2)
    startTime = time.time()
    currentTime = time.time()
    timeout = 10
    while not isQisRunning():
        time.sleep(0.1)
        currentTime = time.time()
        if currentTime - startTime > timeout:
            raise TimeoutError('QIS failed to launch within timelimit of ' + str(timeout) + ' sec.')
            break

    os.chdir(current_direc)
    try:
        startLocalQis.func_code = (lambda : None).func_code
    except:
        startLocalQis.__code__ = (lambda : None).__code__


def closeQis(host='127.0.0.1', port=9722):
    """
    Helper function to close an instance of QIS.  By default this is the local version, but
    an address can be specified for remote systems.
    
    Parameters
    ----------
    host : str, optional
        Host IP address if not localhost
    port : str, optional
        QIS connection port if set to a value other than the default
        
    """
    myQis = QisInterface(host, port)
    myQis.sendAndReceiveCmd(cmd='$shutdown')


def GetQisModuleSelection(QisConnection):
    """
    Prints a list of modules for user selection
    
    .. deprecated:: 2.0.12
        Use the module selection functions of the QisInterface class instead
    """
    devList = QisConnection.getDeviceList()
    devList = [x for x in devList if 'rest' not in x]
    print('\n ########## STEP 1 - Select a Quarch Module. ########## \n')
    print(' --------------------------------------------')
    print(' |  {:^5}  |  {:^30}|'.format('INDEX', 'MODULE'))
    print(' --------------------------------------------')
    try:
        for idx in xrange(len(devList)):
            print(' |  {:^5}  |  {:^30}|'.format(str(idx + 1), devList[idx]))
            print(' --------------------------------------------')

    except:
        for idx in range(len(devList)):
            print(' |  {:^5}  |  {:^30}|'.format(str(idx + 1), devList[idx]))
            print(' --------------------------------------------')

    try:
        moduleId = int(raw_input('\n>>> Enter the index of the Quarch module: '))
    except NameError:
        moduleId = int(input('\n>>> Enter the index of the Quarch module: '))

    if moduleId > 0 and moduleId <= len(devList):
        myDeviceID = devList[(moduleId - 1)]
    else:
        myDeviceID = None
    return myDeviceID