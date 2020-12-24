# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/mcli/press.py
# Compiled at: 2019-02-12 12:07:18
# Size of source mod 2**32: 1187 bytes
import json, yaml
from mercury_sdk.mcli import operations
from mercury_sdk.mcli import output
from mercury_sdk.rpc import job

def configuration_from_yaml(filename):
    """Loads a YAML configuration file.

    :param filename: The filename of the file to load.
    :returns: dict -- A dictionary representing the YAML configuration file
        loaded. If the file can't be loaded, then the empty dict is returned.
    """
    with open(filename) as (infile):
        return yaml.load(infile.read())


def press_server(client, target_query, configuration, wait=False):
    try:
        _job = job.SimpleJob(client, target_query, 'press', job_kwargs={'configuration': configuration_from_yaml(configuration)})
    except (IOError, OSError) as e:
        output.print_and_exit('Could not load configuration file: {}'.format(e), 1)
        return

    _job.start()
    if not wait:
        return json.dumps({'job_id':_job.job_id, 
         'targets':_job.targets},
          indent=2)
    else:
        _job.join(poll_interval=1)
        return json.dumps(_job.tasks)