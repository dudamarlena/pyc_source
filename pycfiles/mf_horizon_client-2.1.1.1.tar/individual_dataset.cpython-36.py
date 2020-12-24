# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stanley/PycharmProjects/horizon-python-client/src/mf_horizon_client/data_structures/individual_dataset.py
# Compiled at: 2020-04-13 11:00:26
# Size of source mod 2**32: 315 bytes
from typing import List
from dataclasses import dataclass
from mf_horizon_client.data_structures.column_passport import ColumnPassport
from mf_horizon_client.data_structures.dataset_summary import DatasetSummary

@dataclass
class IndividualDataset:
    analysis: List[ColumnPassport]
    summary: DatasetSummary