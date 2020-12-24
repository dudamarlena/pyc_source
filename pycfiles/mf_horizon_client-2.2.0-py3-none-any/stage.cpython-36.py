# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/data_structures/stage.py
# Compiled at: 2020-05-09 07:13:20
# Size of source mod 2**32: 864 bytes
import enum
from dataclasses import dataclass
from mf_horizon_client.data_structures.configs.stage_config import StageConfig
from mf_horizon_client.data_structures.configs.stage_status import StageStatus
from mf_horizon_client.schemas.configs import ConfigMultiplexSchema

class StageRunMode(enum.Enum):
    __doc__ = '\n    Defines the current run mode of the stage.\n    Full -  The stage will run normally\n    Preview - The stage will run in a quick preview mode\n    '
    FULL = 'full'
    PREVIEW = 'preview'


@dataclass
class Stage:
    __doc__ = '\n    Python client representation of a Horizon Stage\n    '

    def __post_init__(self):
        self.config = ConfigMultiplexSchema().load(self.config)

    status: StageStatus
    id_: int
    type: str
    config: StageConfig
    run_mode: StageRunMode