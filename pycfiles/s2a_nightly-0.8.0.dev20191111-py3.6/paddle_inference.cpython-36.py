# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/server/paddle_inference.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 1711 bytes
import os, numpy as np, paddle.fluid as fluid
from seq2annotation.input_paddle import read_vocabulary
from tokenizer_tools.tagset.NER.BILUO import BILUOSequenceEncoderDecoder

class Inference(object):

    def __init__(self, model_path):
        self.place = fluid.CPUPlace()
        self.exe = fluid.Executor(self.place)
        self.inference_program, self.feed_target_names, self.fetch_targets = fluid.io.load_inference_model(dirname=model_path, executor=(self.exe))
        self.vocabulary = read_vocabulary(os.path.join(model_path, 'data/vocabulary.txt'))
        self.tag = read_vocabulary(os.path.join(model_path, 'data/tags.txt'))
        self.decoder = BILUOSequenceEncoderDecoder()

    def infer(self, input_text):
        data = [self.vocabulary.lookup(i) for i in input_text]
        print(data)
        word = fluid.create_lod_tensor([data], [[len(data)]], self.place)
        results, = self.exe.run((self.inference_program),
          feed={self.feed_target_names[0]: word},
          fetch_list=(self.fetch_targets),
          return_numpy=False)
        result = np.array(results).reshape([-1]).tolist()
        print(result)
        output_tag = [self.tag.id_to_str(i) for i in result]
        print(output_tag)
        result = self.decoder.to_offset(output_tag, input_text)
        return result


if __name__ == '__main__':
    inference = Inference('/Users/howl/PyCharmProjects/seq2annotation/results/saved_model/1557904173')
    result = inference.infer('查这几天的天气。')
    print(result)