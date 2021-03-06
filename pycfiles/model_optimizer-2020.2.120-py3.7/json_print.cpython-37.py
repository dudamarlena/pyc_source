# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/analysis/json_print.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2305 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import logging as log, json, sys, numpy as np
from extensions.front.user_data_repack import UserDataRepack
from mo.graph.graph import Graph
from mo.middle.passes.convert_data_type import np_data_type_to_precision
from mo.utils.model_analysis import AnalyzeAction, AnalysisCollectorAnchor, AnalysisResults

def prepare_obj_for_dump(obj: object):
    if isinstance(obj, dict):
        return {k:prepare_obj_for_dump(v) for k, v in obj.items()}
    if isinstance(obj, np.ndarray):
        if obj.ndim == 0:
            return obj.item()
        return [prepare_obj_for_dump(elem) for elem in obj]
    else:
        if isinstance(obj, list):
            return [prepare_obj_for_dump(elem) for elem in obj]
            if isinstance(obj, type):
                try:
                    return np_data_type_to_precision(obj)
                except:
                    log.error('Unsupported data type: {}'.format(str(obj)))
                    return str(obj)

        else:
            if isinstance(obj, np.generic):
                return obj.item()
            return str(obj)


class AnalysisJSONPrint(AnalyzeAction):
    __doc__ = '\n    The action prints the analysis results in JSON format.\n    '
    enabled = False
    id = 'ANALYSIS_JSON_PRINT'

    def run_before(self):
        return [
         UserDataRepack]

    def run_after(self):
        return [
         AnalysisCollectorAnchor]

    def analyze(self, graph: Graph):
        analysis_results = AnalysisResults()
        if analysis_results.get_result() is not None:
            try:
                print(json.dumps(prepare_obj_for_dump(analysis_results.get_result())))
            except Exception as e:
                try:
                    log.error('Cannot serialize to JSON: %s', str(e))
                    sys.exit(1)
                finally:
                    e = None
                    del e

        sys.exit(0)