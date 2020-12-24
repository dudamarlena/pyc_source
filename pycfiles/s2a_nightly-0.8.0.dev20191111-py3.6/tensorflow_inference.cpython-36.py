# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/server/tensorflow_inference.py
# Compiled at: 2019-10-31 06:52:53
# Size of source mod 2**32: 2370 bytes
from typing import List
import keras
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder
from tokenizer_tools.tagset.offset.sequence import Sequence
from tensorflow.contrib import predictor
from tokenizer_tools.tagset.exceptions import TagSetDecodeError
decoder = BILUOSequenceEncoderDecoder()

class Inference(object):

    def __init__(self, model_path):
        self.model_dir = model_path
        self.predict_fn = predictor.from_saved_model(model_path)

    def infer(self, input_text: str):
        infer_result = self._infer(input_text)
        return infer_result[0]

    def batch_infer(self, input_text: List[str]):
        return self._infer(input_text)

    def _infer(self, input_text):
        if isinstance(input_text, str):
            input_list = [
             input_text]
        else:
            input_list = input_text
        raw_sequences = [[i for i in text] for text in input_list]
        sentence = keras.preprocessing.sequence.pad_sequences(raw_sequences,
          dtype='object', padding='post',
          truncating='post',
          value=['<pad>']).tolist()
        input_feature = {'words':[[i for i in text] for text in sentence], 
         'words_len':[len(text) for text in raw_sequences]}
        predictions = self.predict_fn(input_feature)
        tags_list = predictions['tags']
        infer_result = []
        for raw_input_text, raw_text, normalized_text, tags in zip(input_list, raw_sequences, sentence, tags_list):
            tags_seq = [i.decode() for i in tags]
            failed = False
            try:
                seq = decoder.to_offset(tags_seq, raw_text)
            except TagSetDecodeError as e:
                print(e)
                seq = Sequence(input_text)
                failed = True

            infer_result.append((raw_input_text, seq, tags_seq, failed))

        return infer_result