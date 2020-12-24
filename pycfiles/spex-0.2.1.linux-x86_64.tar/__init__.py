# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/greg/work/spex/env/lib64/python2.7/site-packages/spex/__init__.py
# Compiled at: 2015-07-08 19:54:16
"""
spex
~~~~~~~~~~~~~~~~~~~
PEX for PySpark
:copyright: (c) 2015 urx
"""
import logging, sys, tempfile, os
logging.getLogger('spex').addHandler(logging.NullHandler())
__title__ = 'spex'
__summary__ = 'PEX for PySpark'
__uri__ = 'https://github.com/URXTech/spex'
__version__ = '0.1.0'
__author__ = 'Greg Bowyer'
__email__ = 'bowyer@urx.com'
__license__ = 'Proprietary'
__copyright__ = 'Copyright 2015 urx'
from .entrypoint import SparkApplication

def spex(args=None, spex_conf=None):
    """Run stub that boots pyspark based on the environment provided by pex"""
    from .args import create_parser
    from .runner import daemon, driver
    from .config import load_spex_config, SparkConfig
    from .entrypoint import get_entry_points, DaemonApplication
    bootstrap_spex_config = spex_conf if spex_conf else load_spex_config()
    entry_points = get_entry_points()
    parser = create_parser(entry_points, bootstrap_spex_config)
    args = parser.parse_args(args)
    if args.application == DaemonApplication:
        daemon()
    else:
        if args.spark_home is None:
            args.spark_home = os.environ.get('SPARK_HOME', None)
        if args.spark_home is None:
            print 'You must specify the spark home either with arguments (--spark-home) or as the env variable SPARK_HOME'
            sys.exit(1)
        if args.local_dir is None:
            args.local_dir = os.path.join(tempfile.gettempdir(), args.name)
        spark_config = SparkConfig(**{k:v for k, v in args.__dict__.items() if k in SparkConfig._fields})
        spex_config = bootstrap_spex_config._replace(spark_config=spark_config)
        application = args.application()
        driver(application, args.application_args, spex_config, verbose=args.verbose)
    return


__all__ = ('spex', 'SparkApplication')