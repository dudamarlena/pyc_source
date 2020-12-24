# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_to_gcs_transfer_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1072 bytes
import warnings
from airflow.contrib.operators.gcp_transfer_operator import S3ToGoogleCloudStorageTransferOperator
warnings.warn('This module is deprecated. Please use `airflow.contrib.operators.gcp_transfer_operator`', DeprecationWarning)