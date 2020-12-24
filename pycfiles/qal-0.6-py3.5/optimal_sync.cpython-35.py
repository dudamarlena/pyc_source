# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/tools/optimal_sync.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 3539 bytes
"""
    ************
    Optimal Sync
    ************
    
    Optimal Sync is a tool that helps with creating and scripting replication jobs.
    Is is a stand-alone tool facilitates data replication and merging with some basic transformation features. 
    It uses a definition file and an SQL compliant database for the Transformation.
    
    :copyright: Copyright 2010-2015 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details.
"""
import os
__version__ = '0.9'
__release__ = '0.9.0'
__copyright__ = '2010-2014, Nicklas Boerjesson'
import json, sys, getopt
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from qal.transformation.merge import Merge
from qal.tools.gui.main_tk_replicator import ReplicatorMain
_help_msg = '\nUsage: optimal_sync.py [OPTION]... -d [DEFINITION FILE]... -l [LOG LEVEL]\nMerge data in using a definition file.\n\nThis stand-alone tool facilitates data replication and merging with some basic transformation features. \nIt uses a definition file and an SQL compliant database for the Transformation.\n\n    -d, --definitionfile    Provide the path to an JSON definition file to describe the Transformation\n    -e,                     Initialize editor\n    -l, --log_level         Log level\n    \n    --help     display this help and exit\n    --version  output version information and exit\n\nAlways back up your data!\n\n'

def init(_definitionfile):
    """Loads the definition file and extracts settings"""
    pass


def main():
    """Main program function"""
    _definitionfile = None
    _edit = None
    _log_level = None
    try:
        _opts = None
        _args = None
        _opts, _args = getopt.getopt(sys.argv[1:], 'ed:l:', ['help', 'version', 'definitionfile=*.json', 'log_level='])
    except getopt.GetoptError as err:
        print(str(err) + '\n' + _help_msg + '\n Arguments: ' + str(_args))
        sys.exit(2)

    if _opts:
        for _opt, _arg in _opts:
            if _opt == '-e':
                _edit = True
            elif _opt in ('-d', '--definitionfile'):
                _definitionfile = _arg
            else:
                if _opt in ('-l', '--log_level'):
                    _log_level = _arg
                else:
                    if _opt == '--help':
                        print(_help_msg)
                        sys.exit()
                    elif _opt == '--version':
                        print(__version__)
                        sys.exit()

        if _definitionfile:
            print(_definitionfile)
            with open(_definitionfile, 'r') as (f):
                _merge = Merge(_json=json.load(f), _base_path=os.path.dirname(_definitionfile))
        else:
            _merge = Merge()
        if _log_level:
            _merge.destination_log_level = int(_log_level)
        if _edit or not _definitionfile:
            ReplicatorMain(_merge=_merge, _filename=_definitionfile)
        else:
            _dataset, _log, _deletes, _inserts, _updates = _merge.execute()
            print(str(_log))
    else:
        print('Error: No options provided.\n' + _help_msg)


if __name__ == '__main__':
    main()