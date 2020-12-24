# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\delete.py
# Compiled at: 2020-02-28 08:30:33
# Size of source mod 2**32: 1928 bytes
from . import curated_control, curated_tables, raw_control
from .utils import log
from .dbfs_utils import table_exists
from .spark_init import get_spark_dbutils
from .exceptions import NoTablesDefinedException

def delete(config, zones=None, tables=None, hard=False, check_tables=True):
    """Delete tables and control tables data at every zones.

  Parameters
  ----------
  config: ETL.Config
  zones: list or str, optional
  tables: list or str, optional
  hard: bool, optional
    Rarely any point in deleting the table itself. Simply delete contents.
    May be needed after many tests resulting in a ballooning delta table size.
  check_tables: bool, optional
    If false, can delete folders / tables with different names than in params.
  """
    spark, dbutils = get_spark_dbutils()
    zones = config.validate_zone_names(zones)
    if check_tables:
        tables = config.validate_table_names(tables)
        if len(tables) == 0:
            raise NoTablesDefinedException(delete)
    if 'raw' in zones and table_exists(config.raw_control_table_name, config.data_source):
        if hard:
            spark.sql('DROP TABLE IF EXISTS {}.{}'.format(config.data_source, config.raw_control_table_name))
    else:
        for table in tables:
            raw_control.delete(config, table)

    if 'curated' in zones:
        if hard:
            spark.sql('DROP TABLE IF EXISTS {}.{}'.format(config.data_source, config.curated_control_table_name))
        for table in tables:
            curated_tables.delete(config, table, drop=hard)
            curated_control.delete(config, table)

    if 'trusted' in zones and hard:
        mount = config.get_mount_name_from_zone_name('trusted')
        for table in tables:
            path = '{}/{}/{}'.format(mount, config.data_source, table)
            dbutils.fs.rm(path, True)

    log('Done.')