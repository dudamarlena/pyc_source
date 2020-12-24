# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/example_parser_configuration_test.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 2775 bytes
"""Tests for ExampleParserConfiguration."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from google.protobuf import text_format
from tensorflow.core.example import example_parser_configuration_pb2
from tensorflow.python.client import session
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import parsing_ops
from tensorflow.python.platform import test
from tensorflow.python.util.example_parser_configuration import extract_example_parser_configuration
BASIC_PROTO = '\nfeature_map {\n  key: "x"\n  value {\n    fixed_len_feature {\n      dtype: DT_FLOAT\n      shape {\n        dim {\n          size: 1\n        }\n      }\n      default_value {\n        dtype: DT_FLOAT\n        tensor_shape {\n          dim {\n            size: 1\n          }\n        }\n        float_val: 33.0\n      }\n      values_output_tensor_name: "ParseExample/ParseExample:3"\n    }\n  }\n}\nfeature_map {\n  key: "y"\n  value {\n    var_len_feature {\n      dtype: DT_STRING\n      values_output_tensor_name: "ParseExample/ParseExample:1"\n      indices_output_tensor_name: "ParseExample/ParseExample:0"\n      shapes_output_tensor_name: "ParseExample/ParseExample:2"\n    }\n  }\n}\n'

class ExampleParserConfigurationTest(test.TestCase):

    def testBasic(self):
        golden_config = example_parser_configuration_pb2.ExampleParserConfiguration()
        text_format.Parse(BASIC_PROTO, golden_config)
        with session.Session() as (sess):
            examples = array_ops.placeholder(dtypes.string, shape=[1])
            feature_to_type = {'x': parsing_ops.FixedLenFeature([1], dtypes.float32, 33.0), 
             'y': parsing_ops.VarLenFeature(dtypes.string)}
            _ = parsing_ops.parse_example(examples, feature_to_type)
            parse_example_op = sess.graph.get_operation_by_name('ParseExample/ParseExample')
            config = extract_example_parser_configuration(parse_example_op, sess)
            self.assertProtoEquals(golden_config, config)


if __name__ == '__main__':
    test.main()