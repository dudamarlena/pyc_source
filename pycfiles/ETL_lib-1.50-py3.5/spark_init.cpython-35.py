# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\spark_init.py
# Compiled at: 2020-01-28 15:17:26
# Size of source mod 2**32: 1316 bytes


def get_spark_dbutils():
    """Get dbutils and spark objects.

  Do not put this at module scope to prevent spark initialisation on import.

  Spark / dbutils are not the same on notebooks vs on databricks-connect,
  and instanciating them via databricks-connect takes some time.

  The point of this helper function is thus to allow control over when
  to launch this initialisation. This is needed in order to use some of the library's
  functions without having to wait for that spark init unless needed.

  Returns
  -------
  (pyspark.sql.session.SparkSession, pyspark.dbutils.DBUtils)
  """
    if 'spark' not in locals():
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.config('spark.driver.host', '127.0.0.1').config('spark.driver.bindAddress', '127.0.0.1').config('spark.executor.extraJavaOptions', '-Xss4m').config('spark.driver.extraJavaOptions', '-Xss4m').getOrCreate()
        spark.sparkContext.setLogLevel('WARN')
        try:
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        except ImportError:
            import IPython
            dbutils = IPython.get_ipython().user_ns['dbutils']

        return (
         spark, dbutils)
    return (locals()['spark'], locals()['dbutils'])