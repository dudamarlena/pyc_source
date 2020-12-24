# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\run.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 5698 bytes
"""
This module allows specific quarchpy utilities and embedded applications to be run from the command line
using the format:
> python -m quarchpy.run [option]
"""
import quarchpy.debug.SystemTest as systemTestMain
import quarchpy.disk_test.driveTestCore as driveTestCoreMain
import quarchpy.calibration.calibrationUtil as calibrationUtilMain
from quarchpy.qis.qisFuncs import startLocalQis
from quarchpy.qps.qpsFuncs import startLocalQps
import quarchpy.debug.upgrade_quarchpy as uprade_quarchpy_main
from quarchpy.user_interface import *
import sys

def main(args):
    """
    Main function parses the arguments from the run command only
    """
    _parse_run_options(args)


def _parse_run_options(args):
    """
    Parses the command line argument supplied via the quarchpy.run command line option

    Parameters
    ----------
    args : list[str]
        List of arguments to process

    """
    found = False
    if len(args) > 0:
        run_options = _get_run_options()
        main_arg = args[0]
        for item in run_options:
            if item[0] == main_arg or item[1] == main_arg:
                found = True
                item[2](args[1:])

    if found == False:
        print('')
        print('ERROR - Command line argument not recognised')
        print('')
        _run_help_function()


def _get_run_options():
    """
    Gets the list of options for quarch.run commands which can be called.  This is used internally to access the available commands
    
    Returns
    -------
    options_list : list[list[object]]
        List of call parameters, each of which is a list of objects making up the function description

    """
    run_options = []
    run_options.append(['debug_info', 'debug', _run_debug_function, 'Runs system tests which displays useful information for debugging'])
    run_options.append([None, 'qcs', _run_qcs_function, 'Launches Quarch Compliance Suite server'])
    run_options.append(['calibration_tool', 'calibration', _run_calibration_function, 'Runs The Quarch power module calibration tool'])
    run_options.append([None, 'qis', _run_qis_function, 'Launches Quarch Instrument Server for communication with Quarch Power Modules'])
    run_options.append([None, 'qps', _run_qps_function, 'Launches Quarch Power Studios, for power capture and analysis'])
    run_options.append(['upgrade_quarchpy', 'upgrade', _run_upgrade_function, 'Detects if an update of Quarchpy is available and assists in the upgrade process'])
    run_options.append(['h', 'help', _run_help_function, 'Displays the help screen with a list of commands supported'])
    return run_options


def _run_debug_function(args=None):
    """
    Executes the python debug/system test option, returning details of the installation to the user
    for debug purposes

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    systemTestMain(args)


def _run_qcs_function(args=None):
    """
    Executes the QCS server back end process

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    driveTestCoreMain(args)


def _run_qis_function(args=None):
    """
    Executes Quarch Instrumentation Server

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    startLocalQis(args=args)


def _run_qps_function(args=None):
    """
    Executes Quarch Power Studio

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    startLocalQps(args=args)


def _run_calibration_function(args=None):
    """
    Executes the calibration utility for power modules

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    calibrationUtilMain(args)


def _run_upgrade_function(args=None):
    """
    Checks for updates to quarchpy and runs the update process if required

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    uprade_quarchpy_main(args)


def _run_help_function(args=None):
    """
    Shows the quarchpy.run help screen

    Parameters
    ----------
    args : list[str]
        List of sub arguments to process

    """
    print('quarch.run - Available commands')
    run_options = _get_run_options()
    display_options = []
    for item in run_options:
        short_name = item[1]
        description = item[3]
        display_options.append([short_name, description])

    displayTable(display_options, align='l', tableHeaders=['Name', 'Description'])


if __name__ == '__main__':
    main(sys.argv[1:])