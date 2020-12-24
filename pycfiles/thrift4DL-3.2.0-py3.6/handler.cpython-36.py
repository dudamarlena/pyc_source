# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/tcp/handler.py
# Compiled at: 2020-01-17 02:28:08
# Size of source mod 2**32: 13329 bytes
from .connectors import Receiver, Deliver, Validator
import multiprocessing
from .protocols import cvt_vision_result_proto
from thrift.Thrift import TType, TMessageType, TApplicationException
import traceback
from queue import Empty
import numpy as np, logging, time
IDLE_QUEUE_BLOCK_TIME_SEC = 10
ERROR_MESSAGE = 'Cannot process the request!'
PREPROCESS_ERROR_MESSAGE = 'Invalid Input'
PREDICT_ERROR_MESSAGE = 'Prediction Error'
SUCCESS_MESSAGE = 'Successful'
SUCCESS_CODE = 0
ERROR_CODE = -1
ERROR_RESPONSE = ''

class Logger:

    @staticmethod
    def get_logger(name, log_file=None):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if log_file is not None:
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        return logger


class BaseHandler:

    def __init__(self, model_path, gpu_id, mem_fraction, client_queue, batch_group_timeout, batch_infer_size):
        pass

    def get_env(self, gpu_id, mem_fraction):
        raise NotImplementedError

    def get_model(self, model_path, env_params):
        raise NotImplementedError

    def preprocess(self, model, input):
        raise NotImplementedError

    def postprocess(self, model, input):
        raise NotImplementedError

    def predict(self, model, input):
        raise NotImplementedError

    def _predict_error_handle(self, args_dict):
        raise NotImplementedError

    def _predict_success_handle(self, result, args_dict):
        raise NotImplementedError

    def _model_process(self, model, image_binary):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class Handler(multiprocessing.Process, BaseHandler):

    def __init__(self, model_path, gpu_id, mem_fraction, client_queue, batch_group_timeout, batch_infer_size, logger=None, log_file=None):
        multiprocessing.Process.__init__(self)
        self.handler_id = int(time.time() * 1000)
        if logger is None:
            self.logger = Logger.get_logger(f"worker_id - {self.handler_id}", log_file)
        else:
            self.logger = logger
        self.logger.info('Init Handler')
        self.client_queue = client_queue
        self.gpu_id = gpu_id
        self.mem_fraction = mem_fraction
        self.model_path = model_path
        self.batch_infer_size = batch_infer_size
        if self.batch_infer_size == 1:
            self.batch_group_timeout = None
        else:
            self.batch_group_timeout = self._milisec_to_sec(batch_group_timeout)
        self.receiver = Receiver()
        self.deliver = Deliver()
        self.validator = Validator()
        self.processing_name = ['predict']

    def _milisec_to_sec(self, sec):
        return sec / 1000

    def get_env(self, gpu_id, mem_fraction):
        env_params = None
        return env_params

    def get_model(self, model_path, env_params):
        model = None
        return model

    def preprocess(self, model, input):
        return input

    def postprocess(self, model, input):
        return input

    def predict(self, model, input):
        raise NotImplementedError

    def _predict_error_handle(self, connection_info, error_message=None):
        error_message = ERROR_MESSAGE if error_message is None else error_message
        connection_info['result'].success = cvt_vision_result_proto(ERROR_CODE, error_message, ERROR_RESPONSE)
        return connection_info

    def _predict_success_handle(self, content, connection_info):
        connection_info['result'].success = cvt_vision_result_proto(SUCCESS_CODE, SUCCESS_MESSAGE, content)
        return connection_info

    def _model_process(self, model, image_binary):
        img_arr = self.preprocess(model, image_binary)
        pred_result = self.predict(model, img_arr)
        pred_result = self.postprocess(model, pred_result)
        return pred_result

    def run(self):
        env_params = self.get_env(self.gpu_id, self.mem_fraction)
        model = self.get_model(self.model_path, env_params)
        while True:
            client = self.client_queue.get()
            connection_info = self.receiver.process(client)
            connection_info = self.validator.process(connection_info)
            image_binary = connection_info['image_binary']
            try:
                pred_response = self._model_process(model, image_binary)
                connection_info = self._predict_success_handle(pred_response, connection_info)
            except Exception as e:
                print(traceback.format_exc())
                connection_info = self._predict_error_handle(connection_info)

            self.deliver.process(connection_info)


class VisionHandler(Handler):

    def get_batch(self):
        """ Block queue for a while to wait incomming request
        """
        batch_input = []
        is_done = False
        is_empty = False
        timeout = IDLE_QUEUE_BLOCK_TIME_SEC
        while True:
            try:
                if is_done:
                    batch_input.clear()
                    is_done = False
                    is_empty = False
                    timeout = IDLE_QUEUE_BLOCK_TIME_SEC
                try:
                    client = self.client_queue.get(block=True, timeout=timeout)
                    connection_info = self.receiver.process(client)
                    connection_info = self.validator.process(connection_info)
                    if connection_info['name'] not in self.processing_name:
                        self.deliver.process(connection_info)
                        continue
                    batch_input.append(connection_info)
                    timeout = self.batch_group_timeout
                except Empty:
                    is_empty = True

                if len(batch_input) >= self.batch_infer_size or is_empty and len(batch_input) > 0:
                    is_done = True
                    self.logger.info(f"Inference-Size: {len(batch_input)}")
                    yield batch_input
            except Exception as e:
                self.logger.error(traceback.format_exc())

    def _get_default_batch_pred_result(self, batch_len):
        return [
         cvt_vision_result_proto(error_code=(-1), error_message='',
           content='')] * batch_len

    def run(self):
        env_params = self.get_env(self.gpu_id, self.mem_fraction)
        model = self.get_model(self.model_path, env_params)
        for batch_connection_info in self.get_batch():
            if len(batch_connection_info) > 0:
                batch_image_binary = []
                batch_pred_result = self._get_default_batch_pred_result(len(batch_connection_info))
                for connection_info in batch_connection_info:
                    try:
                        image_binary = connection_info['image_binary']
                        image_binary = self.preprocess(model, image_binary)
                        batch_image_binary.append(image_binary)
                    except Exception as e:
                        self.logger.error(traceback.format_exc())
                        connection_info = self._predict_error_handle(connection_info, PREPROCESS_ERROR_MESSAGE)
                        self.deliver.process(connection_info)

                if len(batch_image_binary) > 0:
                    try:
                        batch_pred_result = self.predict(model, batch_image_binary)
                        assert isinstance(batch_pred_result, list), ValueError('result from `predict` must be a list')
                        for connection_info, pred_result in zip(batch_connection_info, batch_pred_result):
                            connection_info = self._predict_success_handle(pred_result, connection_info)
                            self.deliver.process(connection_info)

                    except Exception as e:
                        self.logger.error(traceback.format_exc())
                        for connection_info, pred_result in zip(batch_connection_info, batch_pred_result):
                            connection_info = self._predict_error_handle(connection_info,
                              error_message=PREDICT_ERROR_MESSAGE)
                            self.deliver.process(connection_info)

                del batch_image_binary
                del batch_connection_info
                del batch_pred_result


class VisionHandlerV2(VisionHandler):

    def __init__(self, model_path, gpu_id, mem_fraction, processor_pipe_conn, batch_group_timeout, batch_infer_size):
        multiprocessing.Process.__init__(self)
        print('Init Handler')
        self.processor_pipe_conn = processor_pipe_conn
        self.gpu_id = gpu_id
        self.mem_fraction = mem_fraction
        self.model_path = model_path
        self.batch_infer_size = batch_infer_size
        self.batch_group_timeout = self._milisec_to_sec(batch_group_timeout)
        self.receiver = Receiver()
        self.deliver = Deliver()
        self.validator = Validator()
        self._pid = np.random.randint(1000)
        self.processing_name = ['predict']

    def get_batch(self):
        """ Block queue for a while to wait incomming request
        """
        while True:
            try:
                batch_connection_info = []
                batch_clients = self.processor_pipe_conn.recv()
                for client in batch_clients:
                    connection_info = self.receiver.process(client)
                    connection_info = self.validator.process(connection_info)
                    if connection_info['name'] not in self.processing_name:
                        self.deliver.process(connection_info)
                    else:
                        batch_connection_info.append(connection_info)

                yield batch_connection_info
            except Exception as e:
                print(traceback.format_exc())

    def _get_default_batch_pred_result(self, batch_len):
        return [
         cvt_vision_result_proto(error_code=(-1), error_message='',
           content='')] * batch_len

    def run(self):
        env_params = self.get_env(self.gpu_id, self.mem_fraction)
        model = self.get_model(self.model_path, env_params)
        for batch_connection_info in self.get_batch():
            if len(batch_connection_info) > 0:
                batch_image_binary = []
                batch_pred_result = self._get_default_batch_pred_result(len(batch_connection_info))
                for connection_info in batch_connection_info:
                    try:
                        image_binary = connection_info['image_binary']
                        image_binary = self.preprocess(model, image_binary)
                        batch_image_binary.append(image_binary)
                    except Exception as e:
                        print(traceback.format_exc())
                        connection_info = self._predict_error_handle(connection_info)
                        self.deliver.process(connection_info)

                if len(batch_image_binary) > 0:
                    try:
                        batch_pred_result = self.predict(model, batch_image_binary)
                    except Exception as e:
                        print(traceback.format_exc())

                    for connection_info, pred_result in zip(batch_connection_info, batch_pred_result):
                        try:
                            pred_result = self.postprocess(model, pred_result)
                            connection_info = self._predict_success_handle(pred_result, connection_info)
                        except Exception as e:
                            print(traceback.format_exc())
                            connection_info = self._predict_error_handle(connection_info)

                        self.deliver.process(connection_info)

                del batch_image_binary
                del batch_connection_info
                del batch_pred_result