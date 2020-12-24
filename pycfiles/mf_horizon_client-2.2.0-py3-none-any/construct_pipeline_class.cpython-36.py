# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/client/pipelines/construct_pipeline_class.py
# Compiled at: 2020-05-09 07:13:20
# Size of source mod 2**32: 749 bytes
from mf_horizon_client.data_structures.dataset_summary import DatasetSummary
from mf_horizon_client.data_structures.pipeline import Pipeline
from mf_horizon_client.data_structures.pipeline_summary import PipelineSummary
from mf_horizon_client.data_structures.stage import Stage
from mf_horizon_client.utils.string_case_converters import convert_dict_from_camel_to_snake

def construct_pipeline_class(pipeline) -> Pipeline:
    stages = [Stage(**convert_dict_from_camel_to_snake(stage)) for stage in pipeline['stages']]
    return Pipeline(summary=PipelineSummary(**convert_dict_from_camel_to_snake(pipeline['summary'])),
      stages=stages,
      dataset=DatasetSummary(**convert_dict_from_camel_to_snake(pipeline['dataset'])))