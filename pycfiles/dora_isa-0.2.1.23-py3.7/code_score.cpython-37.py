# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dora/template/cp/score/code_score.py
# Compiled at: 2020-01-16 10:25:08
# Size of source mod 2**32: 643 bytes
from pyspark import SparkContext
sc = SparkContext()
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
sc.setLogLevel('ERROR')
from pyspark.sql import HiveContext
spark = HiveContext(sc)
sc._jsc.hadoopConfiguration().set('fs.AbstractFileSystem.s3a.impl', 'org.apache.hadoop.fs.s3a.S3A')