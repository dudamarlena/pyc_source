# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smilectl/__init__.py
# Compiled at: 2018-09-22 01:53:44
"""Main script for SMILECTL."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import subprocess, simplejson as json
from six.moves import range
import smile as sm
from smile import flags
from smile import logging
import _jsonnet
from .api import login_prompt, NBAPI
from .utils import libsm_abs_path
with flags.Subcommand('up', dest='command'):
    flags.DEFINE_string('config_file', '', 'The config path.', required=True)
    flags.DEFINE_string('vars', '', 'External variables for the script. Example: --vars home=/smile/,num=1')
    flags.DEFINE_string('api_host', '', 'API Host.')
with flags.Subcommand('runlocal', dest='command'):
    flags.DEFINE_string('config_file', '', 'The config path.', required=True)
    flags.DEFINE_string('vars', '', 'External variables for the script. Example: --vars home=/smile/,num=1')
    flags.DEFINE_bool('dry_run', False, 'If this command is specified, instead of running the command, print out the entire job object.')
FLAGS = flags.FLAGS

def path_import_callback(dir_path, rel):
    """Path import callback function. Used for JSONNET evaluation."""
    full_path = libsm_abs_path(dir_path, rel)
    if full_path:
        with open(full_path, 'r') as (fobj):
            content = fobj.read()
        return (full_path, content)
    raise RuntimeError('File not found')


def parse_config_file(config_file, vars_string=''):
    """Parse the smile configuration file into Python dictionory object."""
    vars_dict = [ part.split('=', 1) for part in vars_string.split(',') if '=' in part ]
    vars_dict = {k:v for k, v in vars_dict}
    json_result = _jsonnet.evaluate_file(config_file, import_callback=path_import_callback, ext_vars=vars_dict)
    jsonobj = json.loads(json_result)
    return jsonobj


def _do_runlocal(jsonobj):
    """Bring up a single given job locally."""
    logging.debug('Running job %s...' % jsonobj['name'])
    logging.debug('Command: %s' % jsonobj['cmd'])
    subprocess.Popen(jsonobj['cmd'], shell=True).wait()


def _do_up(jsonobj, **kwargs):
    """Bring up a single NB cluster task."""
    api_stub = kwargs['api_stub']
    logging.info('Creating job %s...' % jsonobj['name'])
    logging.info('Command: %s' % jsonobj['cmd'])
    for idx in range(3):
        if idx > 0:
            logging.error('Retrying (%d-th times)...' % (idx + 1))
        res = api_stub.create_job(jsonobj)
        if res is not None:
            logging.info('Job %s submitted.' % jsonobj['name'])
            return res

    return


HANDLERS = {'runlocal': _do_runlocal, 'up': _do_up}

def _do_job_submit():
    """Job related commands. Currently `up` and `runlocal`."""
    jsonobj = parse_config_file(FLAGS.config_file, FLAGS.vars)
    job_handler = HANDLERS.get(FLAGS.command, None)
    if FLAGS.command == 'runlocal' and FLAGS.dry_run:
        print(json.dumps(jsonobj, sort_keys=True, indent=2, separators=(',', ': ')))
        return
    else:
        kwargs = {}
        if FLAGS.command in ('up', ):
            username, password = login_prompt()
            api_stub = NBAPI(username, password, api_host=FLAGS.api_host)
            kwargs['api_stub'] = api_stub
            if api_stub.login() is None:
                return
            logging.info('Login succeeded.')
        if isinstance(jsonobj, list):
            for j in jsonobj:
                job_handler(j, **kwargs)

        else:
            job_handler(jsonobj, **kwargs)
        return


def main(_):
    """Main entry function."""
    if FLAGS.command in ('up', 'runlocal'):
        _do_job_submit()
    else:
        logging.error('Invalid command.')
        return


def app_main():
    """The entry function of the script."""
    sm.app.run(main=main)