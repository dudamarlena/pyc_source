# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/server/inference/inference_base.py
# Compiled at: 2019-10-31 06:52:53
# Size of source mod 2**32: 3026 bytes
from typing import List, Union, Any, Callable
import numpy as np
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.offset.sequence import Sequence
from tokenizer_tools.tagset.exceptions import TagSetDecodeError
decoder = BILUOSequenceEncoderDecoder()

class InferenceBase(object):

    def __init__(self, model_path, *args, **kwargs):
        self.model_path = model_path
        self.predict_fn = None
        self.load_prediction_fn()

    def load_prediction_fn(self):
        self.predict_fn = self.instance_predict_fn()

    def instance_predict_fn(self) -> Callable:
        raise NotImplementedError

    def infer(self, input_text: str):
        input_text_list = [input_text]
        infer_result = self.do_infer(input_text_list)
        return infer_result[0]

    def batch_infer(self, input_text: List[str]):
        return self.do_infer(input_text)

    def preprocess(self, msg_list: List[List[str]]) -> Union[(np.ndarray, List[List[str]])]:
        raise NotImplementedError

    def encode_input_feature(self, msg_list: Union[(np.ndarray, List[List[str]])]) -> Any:
        raise NotImplementedError

    def decode_output_feature(self, response: Any) -> Any:
        raise NotImplementedError

    def postprocess(self, input_: Any) -> List[List[str]]:
        raise NotImplementedError

    def decode_ner_tag_sequence(self, ner_tag_sequence: List[List[str]], std_msg_list: List[List[str]], raw_msg_list: List[str]):
        infer_result = []
        for raw_msg, std_msg, ner_tags in zip(raw_msg_list, std_msg_list, ner_tag_sequence):
            failed = False
            try:
                seq = decoder.to_offset(ner_tags, std_msg)
            except TagSetDecodeError as e:
                print(e)
                seq = Sequence(std_msg)
                failed = True

            infer_result.append((raw_msg, seq, ner_tags, failed))

        return infer_result

    def do_infer(self, input_list: List[str]):
        std_input_list = [[i for i in text] for text in input_list]
        preprocessed_msg = self.preprocess(std_input_list)
        encoded_input_feature = self.encode_input_feature(preprocessed_msg)
        raw_predictions = self.predict_fn(encoded_input_feature)
        predictions = self.decode_output_feature(raw_predictions)
        ner_tag_sequence = self.postprocess(predictions)
        result = self.decode_ner_tag_sequence(ner_tag_sequence, std_input_list, input_list)
        return result