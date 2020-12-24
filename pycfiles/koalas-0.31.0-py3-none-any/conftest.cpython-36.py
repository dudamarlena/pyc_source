# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/conftest.py
# Compiled at: 2019-11-07 14:25:58
# Size of source mod 2**32: 3117 bytes
import pytest, numpy, tempfile, atexit, os, shutil, uuid, logging
from distutils.version import LooseVersion
import pandas as pd, pyarrow as pa, matplotlib.pyplot as plt
from pyspark import __version__
from databricks import koalas
from databricks.koalas import utils
if LooseVersion(__version__) >= LooseVersion('3.0.0'):
    session = utils.default_session({'spark.jars.packages': 'io.delta:delta-core_2.12:0.1.0'})
else:
    if LooseVersion(__version__) >= LooseVersion('2.4.2'):
        session = utils.default_session({'spark.jars.packages': 'io.delta:delta-core_2.11:0.1.0'})
    else:
        session = utils.default_session()

@pytest.fixture(scope='session', autouse=True)
def session_termination():
    yield
    session.stop()


@pytest.fixture(autouse=True)
def add_ks(doctest_namespace):
    doctest_namespace['ks'] = koalas


@pytest.fixture(autouse=True)
def add_pd(doctest_namespace):
    if os.getenv('PANDAS_VERSION', None) is not None:
        if not pd.__version__ == os.getenv('PANDAS_VERSION'):
            raise AssertionError
    doctest_namespace['pd'] = pd


@pytest.fixture(autouse=True)
def add_pa(doctest_namespace):
    if os.getenv('PYARROW_VERSION', None) is not None:
        if not pa.__version__ == os.getenv('PYARROW_VERSION'):
            raise AssertionError
    doctest_namespace['pa'] = pa


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace['np'] = numpy


@pytest.fixture(autouse=True)
def add_path(doctest_namespace):
    path = tempfile.mkdtemp()
    atexit.register(lambda : shutil.rmtree(path, ignore_errors=True))
    doctest_namespace['path'] = path


@pytest.fixture(autouse=True)
def add_db(doctest_namespace):
    db_name = 'db%s' % str(uuid.uuid4()).replace('-', '')
    session.sql('CREATE DATABASE %s' % db_name)
    atexit.register(lambda : session.sql('DROP DATABASE IF EXISTS %s CASCADE' % db_name))
    doctest_namespace['db'] = db_name


@pytest.fixture(autouse=(os.getenv('KOALAS_USAGE_LOGGER', None) is not None))
def add_caplog(caplog):
    with caplog.at_level((logging.INFO), logger='databricks.koalas.usage_logger'):
        yield


@pytest.fixture(autouse=True)
def close_figs():
    yield
    plt.close('all')