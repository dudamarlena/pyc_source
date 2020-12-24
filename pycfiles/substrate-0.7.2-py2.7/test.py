# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/local/substrate/manage/substrate_manage/commands/test.py
# Compiled at: 2012-06-22 10:46:07
""" Run tests using unittest2 'discover' """
import logging, os, sys, tempfile
from google.appengine.api import yaml_errors
from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main
__unittest = True
try:
    from unittest2.main import main_ as main
except ImportError:
    from unittest.main import main

config = matcher = None
try:
    config, matcher, from_cache = dev_appserver.LoadAppConfig('.', {})
except yaml_errors.EventListenerError as e:
    logging.error('Fatal error when loading application configuration:\n' + str(e))
except dev_appserver.InvalidAppConfigError as e:
    logging.error('Application configuration file invalid:\n%s', e)

args = dev_appserver_main.DEFAULT_ARGS.copy()
args[dev_appserver_main.ARG_CLEAR_DATASTORE] = True
args[dev_appserver_main.ARG_BLOBSTORE_PATH] = os.path.join(tempfile.gettempdir(), 'dev_appserver.test.blobstore')
args[dev_appserver_main.ARG_DATASTORE_PATH] = os.path.join(tempfile.gettempdir(), 'dev_appserver.test.datastore')
args[dev_appserver_main.ARG_PROSPECTIVE_SEARCH_PATH] = os.path.join(tempfile.gettempdir(), 'dev_appserver.test.matcher')
args[dev_appserver_main.ARG_HISTORY_PATH] = os.path.join(tempfile.gettempdir(), 'dev_appserver.test.datastore.history')
dev_appserver.SetupStubs(config.application, **args)
sys.path.insert(0, os.path.abspath(os.path.curdir))
if __name__ == '__main__':
    argv = [
     'unit2', 'discover', '--start-directory', 'tests']
    argv.extend(sys.argv[1:])
    sys.argv = argv
    main()