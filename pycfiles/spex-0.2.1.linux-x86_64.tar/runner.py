# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/greg/work/spex/env/lib64/python2.7/site-packages/spex/runner.py
# Compiled at: 2015-07-14 13:38:06
from __future__ import print_function
import os, sys, logging
logger = logging.getLogger('spex')
from .artifact_server import ArtifactServer
from .utils import establish_spark_home, honor_logging

def driver(application, application_args, spex_conf, verbose=False):
    """Runs the spex in driver mode, creating the actual application from its entry point with PySpark configuration

    Parameters
    ----------
    args : dict-like
        The arguments presented to the spex application, used for configuring PySpark and booting the driver.
    prog : str
        The name of the spex application that is running the PySpark jobs
    """
    honor_logging(verbose)
    spex_conf = establish_spark_home(spex_conf)
    sys.path.append(spex_conf.spex_root)
    from .context import SpexContext
    with ArtifactServer(os.getcwd()) as (artifact_server):
        artifact_resolver = artifact_server.artifact_uri_resolver()
        logger.info('Started artifact server [%s]', artifact_server)
        with SpexContext(spex_conf, artifact_resolver) as (spex_context):
            logger.debug('Application in use is [%s]', application)
            application.configure_spark_context(application_args, spex_context.spark_config)
            logger.info('Starting spark application from spex file')
            application.run(spex_context)


def daemon():
    """Runs the spex in daemon mode, booting the environment ready for PySpark to manipulate it for operation"""
    try:
        import pyspark.daemon
        pyspark.daemon.manager()
    except ImportError:
        raise ImportError('PySpark not correctly setup?')