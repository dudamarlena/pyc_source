# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/trainer/paddle_train.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 2339 bytes
from ioflow.corpus import Corpus
from ioflow.task_status import get_task_status_class
from ioflow.model_saver import ModelSaver
from ioflow.performance_metrics import get_performance_metrics_class
from ioflow.configure import read_configure
from seq2annotation.input_paddle import build_input_func, generate_tagset
from seq2annotation.model_paddle import Model

class Train(object):

    def train(self, addition_config=None, *args, **kwargs):
        raw_config = read_configure(*args, **kwargs)
        if addition_config:
            raw_config.update(addition_config)
        model = Model(raw_config)
        config = model.get_default_config()
        config.update(raw_config)
        task_status_class = get_task_status_class(config)
        task_status = task_status_class(config)
        corpus = Corpus(config)
        corpus.prepare()
        train_data_generator_func = corpus.get_generator_func(corpus.TRAIN)
        eval_data_generator_func = corpus.get_generator_func(corpus.EVAL)
        corpus_meta_data = corpus.get_meta_info()
        config['tags_data'] = generate_tagset(corpus_meta_data['tags'])
        task_status.send_status(task_status.START)
        train_input_func = build_input_func(train_data_generator_func, config)
        eval_input_func = build_input_func(eval_data_generator_func, config)
        evaluate_result, export_results, final_saved_model = model.train_and_eval_then_save(train_input_func, eval_input_func, config)
        task_status.send_status(task_status.DONE)
        if evaluate_result:
            performance_metrics_class = get_performance_metrics_class(config)
            performance_metrics = performance_metrics_class(config)
            performance_metrics.set_metrics('test_loss', evaluate_result['loss'])
            performance_metrics.set_metrics('test_acc', evaluate_result['acc'])
        model_saver = ModelSaver(config)
        model_saver.save_model(final_saved_model)
        return final_saved_model


if __name__ == '__main__':
    train = Train()
    train.train()