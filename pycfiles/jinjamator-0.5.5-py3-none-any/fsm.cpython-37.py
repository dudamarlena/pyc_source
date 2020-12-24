# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator-oss/jinjamator/plugins/content/fsm/fsm.py
# Compiled at: 2020-04-06 16:53:41
# Size of source mod 2**32: 2006 bytes
from netmiko import ConnectHandler
import textfsm, os
try:
    from textfsm import clitable
except ImportError:
    import clitable

def _clitable_to_dict(cli_table):
    """Convert TextFSM cli_table object to list of dictionaries."""
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element

        objs.append(temp_dict)

    return objs


def fsm_process(device_type=None, command=None, data=None):
    """Return the structured data based on the output from a network device."""
    cli_table = clitable.CliTable('index', '{0}/fsmtemplates'.format(os.path.dirname(os.path.abspath(__file__))))
    attrs = dict(Command=command,
      Platform=device_type)
    try:
        cli_table.ParseCmd(data, attrs)
        structured_data = _clitable_to_dict(cli_table)
    except clitable.CliTableError as e:
        try:
            if _parent._args.best_effort:
                _parent._log.error('Unable to parse command "%s" on platform %s - %s' % (
                 command, device_type, str(e)))
                return []
            raise Exception('Unable to parse command "%s" on platform %s - %s' % (
             command, device_type, str(e)))
        finally:
            e = None
            del e

    except textfsm.TextFSMError as e:
        try:
            if _parent._args.best_effort:
                _parent._log.error('Unable to parse command "%s" on platform %s - %s' % (
                 command, device_type, str(e)))
                return []
            raise Exception('Unable to parse command "%s" on platform %s - %s' % (
             command, device_type, str(e)))
        finally:
            e = None
            del e

    return structured_data