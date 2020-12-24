# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/utils/guess_framework.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 2272 bytes
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
import re
from argparse import Namespace
from mo.utils.error import Error
from mo.utils.utils import refer_to_faq_msg

def deduce_framework_by_namespace(argv: Namespace):
    if not argv.framework:
        if getattr(argv, 'saved_model_dir', None) or getattr(argv, 'input_meta_graph', None):
            argv.framework = 'tf'
        else:
            if getattr(argv, 'input_symbol', None) or getattr(argv, 'pretrained_model_name', None):
                argv.framework = 'mxnet'
            else:
                if getattr(argv, 'input_proto', None):
                    argv.framework = 'caffe'
                else:
                    if argv.input_model is None:
                        raise Error('Path to input model is required: use --input_model.')
                    else:
                        argv.framework = guess_framework_by_ext(argv.input_model)
        if not argv.framework:
            raise Error('Framework name can not be deduced from the given options: {}={}. Use --framework to choose one of caffe, tf, mxnet, kaldi, onnx', '--input_model', argv.input_model, refer_to_faq_msg(15))
    return map(lambda x: argv.framework == x, ['tf', 'caffe', 'mxnet', 'kaldi', 'onnx'])


def guess_framework_by_ext(input_model_path: str) -> int:
    if re.match('^.*\\.caffemodel$', input_model_path):
        return 'caffe'
    if re.match('^.*\\.pb$', input_model_path):
        return 'tf'
    if re.match('^.*\\.pbtxt$', input_model_path):
        return 'tf'
    if re.match('^.*\\.params$', input_model_path):
        return 'mxnet'
    if re.match('^.*\\.nnet$', input_model_path):
        return 'kaldi'
    if re.match('^.*\\.mdl', input_model_path):
        return 'kaldi'
    if re.match('^.*\\.onnx$', input_model_path):
        return 'onnx'