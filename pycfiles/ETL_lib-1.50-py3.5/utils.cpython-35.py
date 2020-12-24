# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\utils.py
# Compiled at: 2020-02-12 12:39:31
# Size of source mod 2**32: 2859 bytes
import hashlib, inspect, os, sys, psutil
from pytz import timezone
from contextlib import contextmanager
from datetime import datetime

def log(msg):
    """Print message with easter time.

  Parameters
  ----------
  msg: str
  """
    pad = 150 - len(msg)
    print(msg + datetime.now(timezone('US/Eastern')).strftime('%d/%m/%Y %H:%M:%S').rjust(pad, ' '))


def build_path(config, zone, folder):
    """

  Parameters
  ----------
  config: ETL.Config
  zone: str
  folder: str

  Returns
  -------
  str
  """
    return '{}/{}/{}'.format(config.get_mount_name_from_zone_name(zone), config.data_source, folder)


def get_hash_from_string(algorithm, string, salt=''):
    """Hash a string

  Examples
  ________
  get_hash_from_string('sha256', 'tomate', salt='8f5add0ee4a')

  For spark, use their sha2 method:

  df.withColumn('name', sha2(concat(col('name'), lit(str.encode(salt))), 256))

  Parameters
  ----------
  algorithm: str
  string: str
  salt: str, optional

  Returns
  -------
  str
  """
    return getattr(hashlib, algorithm.lower())(str.encode(string) + str.encode(salt)).hexdigest()


def remove_empty_strings(df):
    return df.replace('', None)


def construct_sql_values(lst):
    values = ''
    for i, path in enumerate(lst):
        comma = ',' if i != 0 else ''
        values += comma + "'" + '/'.join(path.split('/')[-2:]) + "'"

    return values


def df_empty(df):
    """Low-cost check for empty df"
  
  Parameters
  ----------
  df: pyspark.sql.DataFrame

  Returns
  -------
  bool
  """
    head = df.head(1)
    return len(head) == 0 or len(head[0]) == 0


def has_handle(fpath):
    """Check if a file is in use by some process

  Parameters
  ----------
  fpath: str

  Returns
  -------
  bool
  """
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True

        except Exception:
            pass

    return False


@contextmanager
def suppress_stdout():
    with open(os.devnull, 'w') as (devnull):
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def get_function_arg_or_kwarg_by_name(arg_name, func, args, kwargs):
    try:
        return kwargs.get(arg_name) or args[list(inspect.signature(func).parameters).index(arg_name)]
    except ValueError as e:
        raise ValueError("Function {} was not passed any parameter '{}'".format(func.__name__, arg_name)) from e