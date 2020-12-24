# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/utils/tensorboard_utils.py
# Compiled at: 2020-03-04 08:08:01
# Size of source mod 2**32: 937 bytes
import os
from typing import Any, Dict, Tuple
from tensorboardX import SummaryWriter

class TensorboardSummaryWriter:

    def __init__(self, output_path: str) -> None:
        self.output_path = output_path
        self.writers = {}

    def ensure_writer_exists(self, name: str) -> None:
        if name not in self.writers.keys():
            writer_path = os.path.join(self.output_path, name)
            self.writers[name] = SummaryWriter(writer_path)

    def save_to_tensorboard(self, results: Dict[(Tuple[(str, str)], float)], n_epoch: int) -> None:
        for (role, metric), value in results.items():
            metric_with_role = '_'.join([metric, role])
            self.ensure_writer_exists(metric_with_role)
            self.writers[metric_with_role].add_scalar(metric, value, n_epoch)

    def close_all_writers(self) -> None:
        for writer in self.writers.values():
            writer.close()