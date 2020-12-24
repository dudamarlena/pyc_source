# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\dbfs_utils.py
# Compiled at: 2020-02-01 19:28:22
# Size of source mod 2**32: 2390 bytes
from pyspark.sql.types import *
from .spark_init import get_spark_dbutils

def get_dbfs_mounts():
    _, dbutils = get_spark_dbutils()
    return [obj.path.split('dbfs:')[1].rstrip('/') for obj in dbutils.fs.ls('/mnt/adls/')]


def install_py_lib(library, version=None):
    """Install pypi library if on databricks and do not raise if called locally.

  Just a safe way to install python library for both databricks connect and notebooks.

  Parameters
  ----------
  library: str
  version: str, optional
  """
    _, dbutils = get_spark_dbutils()
    if hasattr(dbutils, 'library'):
        dbutils_library = dbutils.__getattr__('library')
        if not any(library in lib for lib in dbutils_library.list()):
            if version is not None:
                dbutils_library.installPyPI(library, version)
    else:
        dbutils_library.installPyPI(library)


def table_exists(table_name, database_name='default'):
    """Check if table exists

  Parameters
  ----------
  table_name: str
  database_name: str, optional

  Returns
  -------
  bool
  """
    spark, _ = get_spark_dbutils()
    return len(spark.sql("SHOW DATABASES LIKE '{}'".format(database_name)).collect()) > 0 and len(spark.sql("SHOW TABLES IN {} LIKE '{}'".format(database_name, table_name)).collect()) > 0


def get_empty_df(schema=None):
    """

  Parameters
  ----------
  schema: pyspark.sql.types.StructType, optional

  Returns
  -------
  pyspark.sql.DataFrame
  """
    spark, _ = get_spark_dbutils()
    return spark.createDataFrame([], schema or StructType())


def directory_empty(directory_path):
    """Check that the dir path exists and has files.

  Spark fails to read if either of those conditions aren't fulfilled.

  Parameters
  ----------
  directory_path: str

  Returns
  -------
  bool
  """
    _, dbutils = get_spark_dbutils()
    has_folder = any([e.name.strip('/') == directory_path.split('/')[(-1)] for e in dbutils.fs.ls(directory_path + '/..')])
    has_files = len(dbutils.fs.ls(directory_path)) > 0
    return not has_folder or not has_files


def exists(path):
    _, dbutils = get_spark_dbutils()
    try:
        dbutils.fs.ls(path)
    except Exception as e:
        if 'FileNotFoundException' in e.__str__():
            return False

    return True