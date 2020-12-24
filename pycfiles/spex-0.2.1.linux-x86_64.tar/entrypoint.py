# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/greg/work/spex/env/lib64/python2.7/site-packages/spex/entrypoint.py
# Compiled at: 2015-07-08 19:54:16
import os, argparse, pkg_resources
from abc import ABCMeta, abstractmethod

class SparkApplication(object):
    """Abstract base class gives allows the running of spark based programs in spex"""
    __metaclass__ = ABCMeta

    @staticmethod
    def configure_arg_parser(arg_parser):
        """Can be implemented to allow spark programs the ability to offer additional command line arguments

        These arguments exist on the end of the application after the spex arguments as a subparser.

        Parameters
        ----------
        arg_parser : argparse.ArgumentParser
            The argument parser to configure
        """
        pass

    @staticmethod
    def help():
        """Implemented to allow spark applications the ability to offer detailed help information in --help

        Returns
        -------
        help : str
            A string detailing what the application is about
        """
        return 'Hey ! implement help() in your SparkApplication / entrypoint to make this info better !'

    def configure_spark_context(self, args, spark_config):
        """Can be implemented to allow spark programs the ability to do additional configuration to the spark context

        The following properties are managed by spex and cannot be altered by programs (spex will simply overwrite
        any changes):
            * spark.executor.uri - This is set to allow spex to correctly download a spark distribution

        Parameters
        ----------
        args : dict-like arguments
            The arguments that are provided to the application on the command line, if custom arguments are desired
            overload `get_arg_parser`
        spark_config : pyspark.SparkConfig
            The spark configuration that will be used to boot the pyspark application
        """
        pass

    @abstractmethod
    def run(self, spex_context):
        """Called to run the actual spark application

        Parameters
        ----------
        spex_context : spex.context.SpexContext
            The spex context for this application, from which items like the spark context will be lazily initialised
        """
        raise NotImplementedError()

    def __call__(self, spex_context):
        """Utility function, basically calls run"""
        self.run(spex_context)


class BareScriptApplication(SparkApplication):
    """Entrypoint that runs a python script"""

    @staticmethod
    def configure_arg_parser(arg_parser):
        arg_parser.add_argument('scripts', nargs=1, help='The main script file to run through the driver')

    def configure_spark_context(self, args, spark_config):
        self.scripts = args.scripts

    @staticmethod
    def help():
        return 'Run a driver using the given script file'

    def run(self, spex_context):
        for script_file in self.scripts:
            with open(script_file) as (script):
                code = compile(script.read(), script_file, 'exec')
                exec code in dict(sc=spex_context.sc, sql_ctx=spex_context.sql_ctx, spexCtx=spex_context)


class DaemonApplication(SparkApplication):
    """Application entrypoint that runs pyspark.daemon"""

    @staticmethod
    def help():
        return argparse.SUPPRESS

    def run(self, spex_context):
        raise ValueError('This is a special entrypoint that should not be called from the driver runner! [%s]' % spex_context)


class IPythonApplication(SparkApplication):
    """Application entrypoint that, after configuring PySpark handles control over to IPython"""

    @staticmethod
    def configure_arg_parser(arg_parser):
        arg_parser.add_argument('args', nargs=argparse.REMAINDER)

    def configure_spark_context(self, args, spark_config):
        self.args = args.args

    @staticmethod
    def help():
        return 'See ipython --help'

    def run(self, spex_context):
        startup_script = spex_context.startup_script
        os.environ['PYTHONSTARTUP'] = startup_script
        from IPython import start_ipython
        start_ipython(argv=self.args)


def get_entry_points():
    """Use the magics to get an entrypoint for the given spex program to run

    Parameters
    ----------
    args : dict-like
        The arguments that were parsed on the command line for the spex-application

    Returns
    -------
    entry_point : SparkApplication
        An entrypoint that honors the spark application ABC
    """
    to_ret = {'driver': BareScriptApplication, 
       'repl': IPythonApplication, 
       'pyspark.daemon': DaemonApplication}
    for entry_point in pkg_resources.iter_entry_points(group='spark_application', name=None):
        if entry_point.name in to_ret:
            raise ValueError("Multiple packages are defining the same spark_application, check setup.py's")
        app = entry_point.load()
        SparkApplication.register(app)
        to_ret[entry_point.name] = app

    return to_ret