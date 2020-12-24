# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/greg/work/spex/env/lib64/python2.7/site-packages/spex/context.py
# Compiled at: 2015-07-08 19:54:16
import os, sys, json
from spex.utils import print_banner, ArtifactResolver
try:
    import py4j
    from pyspark import SparkConf, SparkContext, SQLContext, HiveContext
except ImportError:
    raise ImportError('You attempted to import the spex.context module _before_ the sys.path was fixed up for spark')

from .config import SpexConfig
_SPARK_CONTEXT = None
_STARTUP_SCRIPT = '\ntry:\n    from spex.context import current\n    spex_context = current()\nexcept ImportError:\n    import sys\n    sys.path = %(path)s\n    from spex.context import current\n    spex_context = current("""%(context)s""")\nsc = spex_context.sc\nsql_ctx = spex_context.sql_ctx\ndel current\n'

class SpexContext(object):

    def __init__(self, spex_conf, artifact_resolver):
        global _SPARK_CONTEXT
        assert _SPARK_CONTEXT is None, 'Cannot have two spark contexts at once in the same process'
        _SPARK_CONTEXT = self
        self.spex_conf = spex_conf
        self.artifact_resolver = artifact_resolver
        os.environ['PYSPARK_PYTHON'] = './%s.spex' % spex_conf.spex_name
        self._spark_config = None
        self._spex_startup = None
        self._spark_context = None
        self._sql_context = None
        return

    @property
    def sc(self):
        spark_context = self._spark_context or SparkContext(conf=self.spark_config)
        if not self.spex_conf.spex_file is not None:
            raise AssertionError('The spex builder must be broken I do not know my spex conf!')
            spark_context.addFile(self.spex_conf.spex_file)
            for py_file in self.spex_conf.spark_config.py_files:
                spark_context.addPyFile(py_file)

            for file in self.spex_conf.spark_config.files:
                spark_context.addFile(file)

            for jar in self.spex_conf.spark_config.jars:
                spark_context.addFile(jar)

            self._spark_context = spark_context
            print_banner(self)
        return self._spark_context

    @property
    def sql_ctx(self):
        if not self._sql_context:
            spark_context = self.sc
            try:
                spark_context._jvm.org.apache.hadoop.hive.conf.HiveConf()
                self._sql_context = HiveContext(spark_context)
            except py4j.protocol.Py4JError:
                self._sql_context = SQLContext(spark_context)

        return self._sql_context

    @property
    def spark_config(self):
        if self._spark_config is None:
            os.environ['SPARK_SUBMIT_CLASSPATH'] = (',').join(self.spex_conf.spark_config.jars)
            conf = SparkConf()
            conf.setAppName(self.spex_conf.spark_config.name)
            conf.setMaster(self.spex_conf.spark_config.master)
            conf.set('spark.rdd.compress', 'true')
            conf.set('spark.io.compression.codec', 'lz4')
            conf.set('spark.mesos.coarse', 'true' if self.spex_conf.spark_config.coarse_mode else 'false')
            self._spark_config = conf
        config = self._spark_config
        config.set('spark.executor.uri', self.artifact_resolver(self.spex_conf.spark_distro))
        config.setExecutorEnv(key='PYSPARK_PYTHON', value='./%s daemon' % self.spex_conf.spex_name)
        return config

    @property
    def startup_script(self):
        if self._spex_startup is None:
            spex_startup = os.path.join(self.spex_conf.spex_root, 'spex_startup.py')
            with open(spex_startup, 'w') as (startup_script):
                startup_script.write(_STARTUP_SCRIPT % dict(path=sys.path, context=self.dumps()))
            self._spex_startup = spex_startup
        return self._spex_startup

    def dumps(self):
        return json.dumps({'spex_conf': self.spex_conf.to_dict(), 
           'artifact_resolver': self.artifact_resolver.to_dict(), 
           'sys.path': sys.path})

    @classmethod
    def loads(cls, raw_data):
        data = json.loads(raw_data)
        spex_conf = SpexConfig.from_dict(data['spex_conf'])
        artifact_resolver = ArtifactResolver.from_dict(data['artifact_resolver'])
        return cls(spex_conf, artifact_resolver)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        if self._spark_context:
            self._spark_context.stop()


def current(serialised_context=None):
    if _SPARK_CONTEXT:
        return _SPARK_CONTEXT
    else:
        if serialised_context:
            return SpexContext.loads(serialised_context)
        return