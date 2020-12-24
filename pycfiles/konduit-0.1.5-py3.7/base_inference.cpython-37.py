# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\konduit\base_inference.py
# Compiled at: 2020-04-20 03:25:17
# Size of source mod 2**32: 120638 bytes
import enum
from konduit.json_utils import empty_type_dict, DictWrapper, ListWrapper

class TensorDataTypesConfig(object):
    __doc__ = 'TensorDataTypesConfig\n\n    Configures TensorDataTypes for inputs and outputs of a step.\n\n    :param input_data_types: List of input konduit.TensorDataType\n    :param output_data_types: List of output konduit.TensorDataType\n    '
    _types_map = {'inputDataTypes':{'type':dict, 
      'subtype':None}, 
     'outputDataTypes':{'type':dict, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, input_data_types=None, output_data_types=None):
        self._TensorDataTypesConfig__input_data_types = input_data_types
        self._TensorDataTypesConfig__output_data_types = output_data_types

    def _get_input_data_types(self):
        return self._TensorDataTypesConfig__input_data_types

    def _set_input_data_types(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputDataTypes must be type')
        self._TensorDataTypesConfig__input_data_types = value

    input_data_types = property(_get_input_data_types, _set_input_data_types)

    def _get_output_data_types(self):
        return self._TensorDataTypesConfig__output_data_types

    def _set_output_data_types(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputDataTypes must be type')
        self._TensorDataTypesConfig__output_data_types = value

    output_data_types = property(_get_output_data_types, _set_output_data_types)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._TensorDataTypesConfig__input_data_types is not None:
            d['inputDataTypes'] = self._TensorDataTypesConfig__input_data_types.as_dict() if hasattr(self._TensorDataTypesConfig__input_data_types, 'as_dict') else self._TensorDataTypesConfig__input_data_types
        if self._TensorDataTypesConfig__output_data_types is not None:
            d['outputDataTypes'] = self._TensorDataTypesConfig__output_data_types.as_dict() if hasattr(self._TensorDataTypesConfig__output_data_types, 'as_dict') else self._TensorDataTypesConfig__output_data_types
        return d


class SavedModelConfig(object):
    __doc__ = 'SavedModelConfig\n\n    SavedModel Configuration for TensorFlow models\n\n    :param saved_model_path: path to the saved model\n    :param model_tag: a tag to give the model, e.g. "serve"\n    :param signature_key: TensorFlow SignatureDef key, e.g. "incr_counter_by"\n    :param saved_model_input_order: list of input variables in order\n    :param save_model_output_order: list of output variables in order\n    '
    _types_map = {'savedModelPath':{'type':str, 
      'subtype':None}, 
     'modelTag':{'type':str, 
      'subtype':None}, 
     'signatureKey':{'type':str, 
      'subtype':None}, 
     'savedModelInputOrder':{'type':list, 
      'subtype':str}, 
     'saveModelOutputOrder':{'type':list, 
      'subtype':str}}
    _formats_map = {'savedModelInputOrder':'table', 
     'saveModelOutputOrder':'table'}

    def __init__(self, saved_model_path=None, model_tag=None, signature_key=None, saved_model_input_order=None, save_model_output_order=None):
        self._SavedModelConfig__saved_model_path = saved_model_path
        self._SavedModelConfig__model_tag = model_tag
        self._SavedModelConfig__signature_key = signature_key
        self._SavedModelConfig__saved_model_input_order = saved_model_input_order
        self._SavedModelConfig__save_model_output_order = save_model_output_order

    def _get_saved_model_path(self):
        return self._SavedModelConfig__saved_model_path

    def _set_saved_model_path(self, value):
        if not isinstance(value, str):
            raise TypeError('savedModelPath must be str')
        self._SavedModelConfig__saved_model_path = value

    saved_model_path = property(_get_saved_model_path, _set_saved_model_path)

    def _get_model_tag(self):
        return self._SavedModelConfig__model_tag

    def _set_model_tag(self, value):
        if not isinstance(value, str):
            raise TypeError('modelTag must be str')
        self._SavedModelConfig__model_tag = value

    model_tag = property(_get_model_tag, _set_model_tag)

    def _get_signature_key(self):
        return self._SavedModelConfig__signature_key

    def _set_signature_key(self, value):
        if not isinstance(value, str):
            raise TypeError('signatureKey must be str')
        self._SavedModelConfig__signature_key = value

    signature_key = property(_get_signature_key, _set_signature_key)

    def _get_saved_model_input_order(self):
        return self._SavedModelConfig__saved_model_input_order

    def _set_saved_model_input_order(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('savedModelInputOrder must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('savedModelInputOrder list valeus must be str')
        self._SavedModelConfig__saved_model_input_order = value

    saved_model_input_order = property(_get_saved_model_input_order, _set_saved_model_input_order)

    def _get_save_model_output_order(self):
        return self._SavedModelConfig__save_model_output_order

    def _set_save_model_output_order(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('saveModelOutputOrder must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('saveModelOutputOrder list valeus must be str')
        self._SavedModelConfig__save_model_output_order = value

    save_model_output_order = property(_get_save_model_output_order, _set_save_model_output_order)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._SavedModelConfig__saved_model_path is not None:
            d['savedModelPath'] = self._SavedModelConfig__saved_model_path.as_dict() if hasattr(self._SavedModelConfig__saved_model_path, 'as_dict') else self._SavedModelConfig__saved_model_path
        if self._SavedModelConfig__model_tag is not None:
            d['modelTag'] = self._SavedModelConfig__model_tag.as_dict() if hasattr(self._SavedModelConfig__model_tag, 'as_dict') else self._SavedModelConfig__model_tag
        if self._SavedModelConfig__signature_key is not None:
            d['signatureKey'] = self._SavedModelConfig__signature_key.as_dict() if hasattr(self._SavedModelConfig__signature_key, 'as_dict') else self._SavedModelConfig__signature_key
        if self._SavedModelConfig__saved_model_input_order is not None:
            d['savedModelInputOrder'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._SavedModelConfig__saved_model_input_order]
        if self._SavedModelConfig__save_model_output_order is not None:
            d['saveModelOutputOrder'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._SavedModelConfig__save_model_output_order]
        return d


class ParallelInferenceConfig(object):
    __doc__ = 'ParallelInferenceConfig\n\n    Configuration for parallel inference.\n\n    :param queue_limit:\n    :param queue_limit:\n    :param batch_limit:\n    :param workers:\n    :param max_train_epochs:\n    :param inference_mode:\n    :param vertx_config_json:\n    '
    _inferenceMode_enum = enum.Enum('_inferenceMode_enum',
      'SEQUENTIAL BATCHED INPLACE', module=__name__)
    _types_map = {'queueLimit':{'type':int, 
      'subtype':None}, 
     'batchLimit':{'type':int, 
      'subtype':None}, 
     'workers':{'type':int, 
      'subtype':None}, 
     'maxTrainEpochs':{'type':int, 
      'subtype':None}, 
     'inferenceMode':{'type':str, 
      'subtype':None}, 
     'vertxConfigJson':{'type':str, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, queue_limit=None, batch_limit=None, workers=None, max_train_epochs=None, inference_mode=None, vertx_config_json=None):
        self._ParallelInferenceConfig__queue_limit = queue_limit
        self._ParallelInferenceConfig__batch_limit = batch_limit
        self._ParallelInferenceConfig__workers = workers
        self._ParallelInferenceConfig__max_train_epochs = max_train_epochs
        self._ParallelInferenceConfig__inference_mode = inference_mode
        self._ParallelInferenceConfig__vertx_config_json = vertx_config_json

    def _get_queue_limit(self):
        return self._ParallelInferenceConfig__queue_limit

    def _set_queue_limit(self, value):
        if not isinstance(value, int):
            raise TypeError('queueLimit must be int')
        self._ParallelInferenceConfig__queue_limit = value

    queue_limit = property(_get_queue_limit, _set_queue_limit)

    def _get_batch_limit(self):
        return self._ParallelInferenceConfig__batch_limit

    def _set_batch_limit(self, value):
        if not isinstance(value, int):
            raise TypeError('batchLimit must be int')
        self._ParallelInferenceConfig__batch_limit = value

    batch_limit = property(_get_batch_limit, _set_batch_limit)

    def _get_workers(self):
        return self._ParallelInferenceConfig__workers

    def _set_workers(self, value):
        if not isinstance(value, int):
            raise TypeError('workers must be int')
        self._ParallelInferenceConfig__workers = value

    workers = property(_get_workers, _set_workers)

    def _get_max_train_epochs(self):
        return self._ParallelInferenceConfig__max_train_epochs

    def _set_max_train_epochs(self, value):
        if not isinstance(value, int):
            raise TypeError('maxTrainEpochs must be int')
        self._ParallelInferenceConfig__max_train_epochs = value

    max_train_epochs = property(_get_max_train_epochs, _set_max_train_epochs)

    def _get_inference_mode(self):
        return self._ParallelInferenceConfig__inference_mode

    def _set_inference_mode(self, value):
        if not isinstance(value, str):
            raise TypeError('inferenceMode must be str')
        elif value in self._inferenceMode_enum.__members__:
            self._ParallelInferenceConfig__type = value
        else:
            raise ValueError('Value {} not in _inferenceMode_enum list'.format(value))

    inference_mode = property(_get_inference_mode, _set_inference_mode)

    def _get_vertx_config_json(self):
        return self._ParallelInferenceConfig__vertx_config_json

    def _set_vertx_config_json(self, value):
        if not isinstance(value, str):
            raise TypeError('vertxConfigJson must be str')
        self._ParallelInferenceConfig__vertx_config_json = value

    vertx_config_json = property(_get_vertx_config_json, _set_vertx_config_json)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ParallelInferenceConfig__queue_limit is not None:
            d['queueLimit'] = self._ParallelInferenceConfig__queue_limit.as_dict() if hasattr(self._ParallelInferenceConfig__queue_limit, 'as_dict') else self._ParallelInferenceConfig__queue_limit
        if self._ParallelInferenceConfig__batch_limit is not None:
            d['batchLimit'] = self._ParallelInferenceConfig__batch_limit.as_dict() if hasattr(self._ParallelInferenceConfig__batch_limit, 'as_dict') else self._ParallelInferenceConfig__batch_limit
        if self._ParallelInferenceConfig__workers is not None:
            d['workers'] = self._ParallelInferenceConfig__workers.as_dict() if hasattr(self._ParallelInferenceConfig__workers, 'as_dict') else self._ParallelInferenceConfig__workers
        if self._ParallelInferenceConfig__max_train_epochs is not None:
            d['maxTrainEpochs'] = self._ParallelInferenceConfig__max_train_epochs.as_dict() if hasattr(self._ParallelInferenceConfig__max_train_epochs, 'as_dict') else self._ParallelInferenceConfig__max_train_epochs
        if self._ParallelInferenceConfig__inference_mode is not None:
            d['inferenceMode'] = self._ParallelInferenceConfig__inference_mode.as_dict() if hasattr(self._ParallelInferenceConfig__inference_mode, 'as_dict') else self._ParallelInferenceConfig__inference_mode
        if self._ParallelInferenceConfig__vertx_config_json is not None:
            d['vertxConfigJson'] = self._ParallelInferenceConfig__vertx_config_json.as_dict() if hasattr(self._ParallelInferenceConfig__vertx_config_json, 'as_dict') else self._ParallelInferenceConfig__vertx_config_json
        return d


class ModelConfigType(object):
    __doc__ = "ModelConfigType\n\n    This model configuration has meta data for a model loader, which\n    includes the model loading path and the model type. It's used in\n    konduit.ModelConfig.\n\n    :param model_type: Can be any of 'DL4J',\n        'PMML', 'TENSORFLOW', 'KERAS', and 'SAMEDIFF'.\n    :param model_loading_path: path to the model file\n    "
    _modelType_enum = enum.Enum('_modelType_enum',
      'DL4J PMML TENSORFLOW KERAS SAMEDIFF', module=__name__)
    _types_map = {'modelType':{'type':str, 
      'subtype':None}, 
     'modelLoadingPath':{'type':str, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, model_type=None, model_loading_path=None):
        self._ModelConfigType__model_type = model_type
        self._ModelConfigType__model_loading_path = model_loading_path

    def _get_model_type(self):
        return self._ModelConfigType__model_type

    def _set_model_type(self, value):
        if not isinstance(value, str):
            raise TypeError('modelType must be str')
        elif value in self._modelType_enum.__members__:
            self._ModelConfigType__type = value
        else:
            raise ValueError('Value {} not in _modelType_enum list'.format(value))

    model_type = property(_get_model_type, _set_model_type)

    def _get_model_loading_path(self):
        return self._ModelConfigType__model_loading_path

    def _set_model_loading_path(self, value):
        if not isinstance(value, str):
            raise TypeError('modelLoadingPath must be str')
        self._ModelConfigType__model_loading_path = value

    model_loading_path = property(_get_model_loading_path, _set_model_loading_path)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ModelConfigType__model_type is not None:
            d['modelType'] = self._ModelConfigType__model_type.as_dict() if hasattr(self._ModelConfigType__model_type, 'as_dict') else self._ModelConfigType__model_type
        if self._ModelConfigType__model_loading_path is not None:
            d['modelLoadingPath'] = self._ModelConfigType__model_loading_path.as_dict() if hasattr(self._ModelConfigType__model_loading_path, 'as_dict') else self._ModelConfigType__model_loading_path
        return d


class ModelConfig(object):
    __doc__ = 'ModelConfig\n\n    Model configurations hold the TensorDataTypeConfig and the\n    .ModelConfigType of the model you want to serve.\n\n    :param tensor_data_types_config: konduit.TensorDataTypeConfig\n    :param model_config_type: konduit.ModelConfigType\n    '
    _types_map = {'tensorDataTypesConfig':{'type':TensorDataTypesConfig, 
      'subtype':None}, 
     'modelConfigType':{'type':ModelConfigType, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, tensor_data_types_config=None, model_config_type=None):
        self._ModelConfig__tensor_data_types_config = tensor_data_types_config
        self._ModelConfig__model_config_type = model_config_type

    def _get_tensor_data_types_config(self):
        return self._ModelConfig__tensor_data_types_config

    def _set_tensor_data_types_config(self, value):
        if not isinstance(value, TensorDataTypesConfig):
            raise TypeError('tensorDataTypesConfig must be TensorDataTypesConfig')
        self._ModelConfig__tensor_data_types_config = value

    tensor_data_types_config = property(_get_tensor_data_types_config, _set_tensor_data_types_config)

    def _get_model_config_type(self):
        return self._ModelConfig__model_config_type

    def _set_model_config_type(self, value):
        if not isinstance(value, ModelConfigType):
            raise TypeError('modelConfigType must be ModelConfigType')
        self._ModelConfig__model_config_type = value

    model_config_type = property(_get_model_config_type, _set_model_config_type)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ModelConfig__tensor_data_types_config is not None:
            d['tensorDataTypesConfig'] = self._ModelConfig__tensor_data_types_config.as_dict() if hasattr(self._ModelConfig__tensor_data_types_config, 'as_dict') else self._ModelConfig__tensor_data_types_config
        if self._ModelConfig__model_config_type is not None:
            d['modelConfigType'] = self._ModelConfig__model_config_type.as_dict() if hasattr(self._ModelConfig__model_config_type, 'as_dict') else self._ModelConfig__model_config_type
        return d


class TensorDataType(object):
    __doc__ = 'TensorDataType\n\n    Possible data types for tensors. Comes with conversions from TensorFlow\n    and Python and between ND4J types. Choose from\n\n    INVALID, FLOAT, DOUBLE, INT32, UINT8, INT16, INT8, STRING, COMPLEX64,\n    INT64, BOOL, QINT8, QUINT8, QINT32, BFLOAT16, QINT16, QUINT16, UINT16,\n    COMPLEX128, HALF, RESOURCE, VARIANT, UINT32, UINT64\n    '
    _types_map = {}
    _formats_map = {}

    def __init__(self):
        pass

    def as_dict(self):
        d = empty_type_dict(self)
        return d


class ObjectDetectionConfig(object):
    __doc__ = 'ObjectDetectionConfig\n\n     Configuration for object detection output of models.\n\n    :param threshold: cut-off threshold for detected objects, defaults to 0.5\n    :param num_labels: the number of labels to predict with your model.\n    :param labels_path: Path to file containing the labels\n    :param priors: list of bounding box priors (list of list of floating point numbers)\n    :param input_shape: input shape of the data\n    '
    _types_map = {'threshold':{'type':float, 
      'subtype':None}, 
     'numLabels':{'type':int, 
      'subtype':None}, 
     'labelsPath':{'type':str, 
      'subtype':None}, 
     'priors':{'type':list, 
      'subtype':list}, 
     'inputShape':{'type':list, 
      'subtype':int}}
    _formats_map = {'priors':'table', 
     'inputShape':'table'}

    def __init__(self, threshold=None, num_labels=None, labels_path=None, priors=None, input_shape=None):
        self._ObjectDetectionConfig__threshold = threshold
        self._ObjectDetectionConfig__num_labels = num_labels
        self._ObjectDetectionConfig__labels_path = labels_path
        self._ObjectDetectionConfig__priors = priors
        self._ObjectDetectionConfig__input_shape = input_shape

    def _get_threshold(self):
        return self._ObjectDetectionConfig__threshold

    def _set_threshold(self, value):
        if not isinstance(value, float):
            raise TypeError('threshold must be float')
        self._ObjectDetectionConfig__threshold = value

    threshold = property(_get_threshold, _set_threshold)

    def _get_num_labels(self):
        return self._ObjectDetectionConfig__num_labels

    def _set_num_labels(self, value):
        if not isinstance(value, int):
            raise TypeError('numLabels must be int')
        self._ObjectDetectionConfig__num_labels = value

    num_labels = property(_get_num_labels, _set_num_labels)

    def _get_labels_path(self):
        return self._ObjectDetectionConfig__labels_path

    def _set_labels_path(self, value):
        if not isinstance(value, str):
            raise TypeError('labelsPath must be str')
        self._ObjectDetectionConfig__labels_path = value

    labels_path = property(_get_labels_path, _set_labels_path)

    def _get_priors(self):
        return self._ObjectDetectionConfig__priors

    def _set_priors(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('priors must be list')
        if not all((isinstance(i, list) for i in value)):
            raise TypeError('priors list valeus must be list')
        self._ObjectDetectionConfig__priors = value

    priors = property(_get_priors, _set_priors)

    def _get_input_shape(self):
        return self._ObjectDetectionConfig__input_shape

    def _set_input_shape(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputShape must be list')
        if not all((isinstance(i, int) for i in value)):
            raise TypeError('inputShape list valeus must be int')
        self._ObjectDetectionConfig__input_shape = value

    input_shape = property(_get_input_shape, _set_input_shape)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ObjectDetectionConfig__threshold is not None:
            d['threshold'] = self._ObjectDetectionConfig__threshold.as_dict() if hasattr(self._ObjectDetectionConfig__threshold, 'as_dict') else self._ObjectDetectionConfig__threshold
        if self._ObjectDetectionConfig__num_labels is not None:
            d['numLabels'] = self._ObjectDetectionConfig__num_labels.as_dict() if hasattr(self._ObjectDetectionConfig__num_labels, 'as_dict') else self._ObjectDetectionConfig__num_labels
        if self._ObjectDetectionConfig__labels_path is not None:
            d['labelsPath'] = self._ObjectDetectionConfig__labels_path.as_dict() if hasattr(self._ObjectDetectionConfig__labels_path, 'as_dict') else self._ObjectDetectionConfig__labels_path
        if self._ObjectDetectionConfig__priors is not None:
            d['priors'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ObjectDetectionConfig__priors]
        if self._ObjectDetectionConfig__input_shape is not None:
            d['inputShape'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ObjectDetectionConfig__input_shape]
        return d


class SchemaType(object):
    __doc__ = "SchemaType\n\n    Type of an input or output to a pipeline step. Can be any of:\n\n    'String', 'Integer', 'Long', 'Double', 'Float', 'Categorical', 'Time', 'Bytes',\n    'Boolean', 'NDArray', 'Image'.\n    "
    _types_map = {}
    _formats_map = {}

    def __init__(self):
        pass

    def as_dict(self):
        d = empty_type_dict(self)
        return d


class Input(object):
    __doc__ = "Input\n\n    Used for specifying various kinds of configuration about inputs\n    for the server. Input.DataFormat defines in which data format\n    an input variable is expected to be specified. Can be any of\n\n    'NUMPY', 'JSON', 'ND4J', 'IMAGE', or 'ARROW'\n    "
    _types_map = {}
    _formats_map = {}

    def __init__(self):
        pass

    def as_dict(self):
        d = empty_type_dict(self)
        return d


class Output(object):
    __doc__ = 'Output\n\n    Used for specifying various kinds of configuration about outputs\n    for the server. Outnput.DataFormat defines in which data format\n    an input variable is expected to be specified. Can be any of\n\n    \'NUMPY\', \'JSON\', \'ND4J\', or \'ARROW\'.\n\n    Additionally, Output.PredictionType defines the type of prediction\n    you want to specify for your pipeline. The prediction type determines\n    which "output adapter" is used to transform the output. Currently you\n    can choose from the following values:\n\n    \'CLASSIFICATION\', \'YOLO\', \'SSD\', \'RCNN\', \'RAW\', \'REGRESSION\'\n    '
    _types_map = {}
    _formats_map = {}

    def __init__(self):
        pass

    def as_dict(self):
        d = empty_type_dict(self)
        return d


class KerasConfig(object):
    _types_map = {'tensorDataTypesConfig':{'type':TensorDataTypesConfig, 
      'subtype':None}, 
     'modelConfigType':{'type':ModelConfigType, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, tensor_data_types_config=None, model_config_type=None):
        self._KerasConfig__tensor_data_types_config = tensor_data_types_config
        self._KerasConfig__model_config_type = model_config_type

    def _get_tensor_data_types_config(self):
        return self._KerasConfig__tensor_data_types_config

    def _set_tensor_data_types_config(self, value):
        if not isinstance(value, TensorDataTypesConfig):
            raise TypeError('tensorDataTypesConfig must be TensorDataTypesConfig')
        self._KerasConfig__tensor_data_types_config = value

    tensor_data_types_config = property(_get_tensor_data_types_config, _set_tensor_data_types_config)

    def _get_model_config_type(self):
        return self._KerasConfig__model_config_type

    def _set_model_config_type(self, value):
        if not isinstance(value, ModelConfigType):
            raise TypeError('modelConfigType must be ModelConfigType')
        self._KerasConfig__model_config_type = value

    model_config_type = property(_get_model_config_type, _set_model_config_type)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._KerasConfig__tensor_data_types_config is not None:
            d['tensorDataTypesConfig'] = self._KerasConfig__tensor_data_types_config.as_dict() if hasattr(self._KerasConfig__tensor_data_types_config, 'as_dict') else self._KerasConfig__tensor_data_types_config
        if self._KerasConfig__model_config_type is not None:
            d['modelConfigType'] = self._KerasConfig__model_config_type.as_dict() if hasattr(self._KerasConfig__model_config_type, 'as_dict') else self._KerasConfig__model_config_type
        return d


class DL4JConfig(object):
    _types_map = {'tensorDataTypesConfig':{'type':TensorDataTypesConfig, 
      'subtype':None}, 
     'modelConfigType':{'type':ModelConfigType, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, tensor_data_types_config=None, model_config_type=None):
        self._DL4JConfig__tensor_data_types_config = tensor_data_types_config
        self._DL4JConfig__model_config_type = model_config_type

    def _get_tensor_data_types_config(self):
        return self._DL4JConfig__tensor_data_types_config

    def _set_tensor_data_types_config(self, value):
        if not isinstance(value, TensorDataTypesConfig):
            raise TypeError('tensorDataTypesConfig must be TensorDataTypesConfig')
        self._DL4JConfig__tensor_data_types_config = value

    tensor_data_types_config = property(_get_tensor_data_types_config, _set_tensor_data_types_config)

    def _get_model_config_type(self):
        return self._DL4JConfig__model_config_type

    def _set_model_config_type(self, value):
        if not isinstance(value, ModelConfigType):
            raise TypeError('modelConfigType must be ModelConfigType')
        self._DL4JConfig__model_config_type = value

    model_config_type = property(_get_model_config_type, _set_model_config_type)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._DL4JConfig__tensor_data_types_config is not None:
            d['tensorDataTypesConfig'] = self._DL4JConfig__tensor_data_types_config.as_dict() if hasattr(self._DL4JConfig__tensor_data_types_config, 'as_dict') else self._DL4JConfig__tensor_data_types_config
        if self._DL4JConfig__model_config_type is not None:
            d['modelConfigType'] = self._DL4JConfig__model_config_type.as_dict() if hasattr(self._DL4JConfig__model_config_type, 'as_dict') else self._DL4JConfig__model_config_type
        return d


class PmmlConfig(object):
    __doc__ = 'PmmlConfig\n\n    Configuration for models in PMML format\n\n    :param tensor_data_types_config: konduit.TensorDataTypesConfig\n    :param model_config_type: konduit.ModelConfigType\n    :param evaluator_factory_name: defaults to "org.jpmml.evaluator.ModelEvaluatorFactory". Custom extensions\n           have to be written in Java.\n    '
    _types_map = {'tensorDataTypesConfig':{'type':TensorDataTypesConfig, 
      'subtype':None}, 
     'modelConfigType':{'type':ModelConfigType, 
      'subtype':None}, 
     'evaluatorFactoryName':{'type':str, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, tensor_data_types_config=None, model_config_type=None, evaluator_factory_name=None):
        self._PmmlConfig__tensor_data_types_config = tensor_data_types_config
        self._PmmlConfig__model_config_type = model_config_type
        self._PmmlConfig__evaluator_factory_name = evaluator_factory_name

    def _get_tensor_data_types_config(self):
        return self._PmmlConfig__tensor_data_types_config

    def _set_tensor_data_types_config(self, value):
        if not isinstance(value, TensorDataTypesConfig):
            raise TypeError('tensorDataTypesConfig must be TensorDataTypesConfig')
        self._PmmlConfig__tensor_data_types_config = value

    tensor_data_types_config = property(_get_tensor_data_types_config, _set_tensor_data_types_config)

    def _get_model_config_type(self):
        return self._PmmlConfig__model_config_type

    def _set_model_config_type(self, value):
        if not isinstance(value, ModelConfigType):
            raise TypeError('modelConfigType must be ModelConfigType')
        self._PmmlConfig__model_config_type = value

    model_config_type = property(_get_model_config_type, _set_model_config_type)

    def _get_evaluator_factory_name(self):
        return self._PmmlConfig__evaluator_factory_name

    def _set_evaluator_factory_name(self, value):
        if not isinstance(value, str):
            raise TypeError('evaluatorFactoryName must be str')
        self._PmmlConfig__evaluator_factory_name = value

    evaluator_factory_name = property(_get_evaluator_factory_name, _set_evaluator_factory_name)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._PmmlConfig__tensor_data_types_config is not None:
            d['tensorDataTypesConfig'] = self._PmmlConfig__tensor_data_types_config.as_dict() if hasattr(self._PmmlConfig__tensor_data_types_config, 'as_dict') else self._PmmlConfig__tensor_data_types_config
        if self._PmmlConfig__model_config_type is not None:
            d['modelConfigType'] = self._PmmlConfig__model_config_type.as_dict() if hasattr(self._PmmlConfig__model_config_type, 'as_dict') else self._PmmlConfig__model_config_type
        if self._PmmlConfig__evaluator_factory_name is not None:
            d['evaluatorFactoryName'] = self._PmmlConfig__evaluator_factory_name.as_dict() if hasattr(self._PmmlConfig__evaluator_factory_name, 'as_dict') else self._PmmlConfig__evaluator_factory_name
        return d


class SameDiffConfig(object):
    __doc__ = 'SameDiffConfig\n\n    Extension of ModelConfig to DL4J SameDiff models\n\n    :param tensor_data_types_config: konduit.TensorDataTypesConfig\n    :param model_config_type: konduit.ModelConfigType\n    '
    _types_map = {'tensorDataTypesConfig':{'type':TensorDataTypesConfig, 
      'subtype':None}, 
     'modelConfigType':{'type':ModelConfigType, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, tensor_data_types_config=None, model_config_type=None):
        self._SameDiffConfig__tensor_data_types_config = tensor_data_types_config
        self._SameDiffConfig__model_config_type = model_config_type

    def _get_tensor_data_types_config(self):
        return self._SameDiffConfig__tensor_data_types_config

    def _set_tensor_data_types_config(self, value):
        if not isinstance(value, TensorDataTypesConfig):
            raise TypeError('tensorDataTypesConfig must be TensorDataTypesConfig')
        self._SameDiffConfig__tensor_data_types_config = value

    tensor_data_types_config = property(_get_tensor_data_types_config, _set_tensor_data_types_config)

    def _get_model_config_type(self):
        return self._SameDiffConfig__model_config_type

    def _set_model_config_type(self, value):
        if not isinstance(value, ModelConfigType):
            raise TypeError('modelConfigType must be ModelConfigType')
        self._SameDiffConfig__model_config_type = value

    model_config_type = property(_get_model_config_type, _set_model_config_type)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._SameDiffConfig__tensor_data_types_config is not None:
            d['tensorDataTypesConfig'] = self._SameDiffConfig__tensor_data_types_config.as_dict() if hasattr(self._SameDiffConfig__tensor_data_types_config, 'as_dict') else self._SameDiffConfig__tensor_data_types_config
        if self._SameDiffConfig__model_config_type is not None:
            d['modelConfigType'] = self._SameDiffConfig__model_config_type.as_dict() if hasattr(self._SameDiffConfig__model_config_type, 'as_dict') else self._SameDiffConfig__model_config_type
        return d


class TensorFlowConfig(object):
    __doc__ = 'TensorFlowConfig\n\n    TensorFlow extension of konduit.ModelConfig used to define model steps\n    with TensorFlow models.\n\n    :param tensor_data_types_config: konduit.TensorDataTypesConfig\n    :param model_config_type: konduit.ModelConfigType\n    :param config_proto_path: path to the TensorFlow ProtoBuf model file.\n    :param saved_model_config: konduit.SavedModelConfig\n    '
    _types_map = {'tensorDataTypesConfig':{'type':TensorDataTypesConfig, 
      'subtype':None}, 
     'modelConfigType':{'type':ModelConfigType, 
      'subtype':None}, 
     'configProtoPath':{'type':str, 
      'subtype':None}, 
     'savedModelConfig':{'type':SavedModelConfig, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, tensor_data_types_config=None, model_config_type=None, config_proto_path=None, saved_model_config=None):
        self._TensorFlowConfig__tensor_data_types_config = tensor_data_types_config
        self._TensorFlowConfig__model_config_type = model_config_type
        self._TensorFlowConfig__config_proto_path = config_proto_path
        self._TensorFlowConfig__saved_model_config = saved_model_config

    def _get_tensor_data_types_config(self):
        return self._TensorFlowConfig__tensor_data_types_config

    def _set_tensor_data_types_config(self, value):
        if not isinstance(value, TensorDataTypesConfig):
            raise TypeError('tensorDataTypesConfig must be TensorDataTypesConfig')
        self._TensorFlowConfig__tensor_data_types_config = value

    tensor_data_types_config = property(_get_tensor_data_types_config, _set_tensor_data_types_config)

    def _get_model_config_type(self):
        return self._TensorFlowConfig__model_config_type

    def _set_model_config_type(self, value):
        if not isinstance(value, ModelConfigType):
            raise TypeError('modelConfigType must be ModelConfigType')
        self._TensorFlowConfig__model_config_type = value

    model_config_type = property(_get_model_config_type, _set_model_config_type)

    def _get_config_proto_path(self):
        return self._TensorFlowConfig__config_proto_path

    def _set_config_proto_path(self, value):
        if not isinstance(value, str):
            raise TypeError('configProtoPath must be str')
        self._TensorFlowConfig__config_proto_path = value

    config_proto_path = property(_get_config_proto_path, _set_config_proto_path)

    def _get_saved_model_config(self):
        return self._TensorFlowConfig__saved_model_config

    def _set_saved_model_config(self, value):
        if not isinstance(value, SavedModelConfig):
            raise TypeError('savedModelConfig must be SavedModelConfig')
        self._TensorFlowConfig__saved_model_config = value

    saved_model_config = property(_get_saved_model_config, _set_saved_model_config)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._TensorFlowConfig__tensor_data_types_config is not None:
            d['tensorDataTypesConfig'] = self._TensorFlowConfig__tensor_data_types_config.as_dict() if hasattr(self._TensorFlowConfig__tensor_data_types_config, 'as_dict') else self._TensorFlowConfig__tensor_data_types_config
        if self._TensorFlowConfig__model_config_type is not None:
            d['modelConfigType'] = self._TensorFlowConfig__model_config_type.as_dict() if hasattr(self._TensorFlowConfig__model_config_type, 'as_dict') else self._TensorFlowConfig__model_config_type
        if self._TensorFlowConfig__config_proto_path is not None:
            d['configProtoPath'] = self._TensorFlowConfig__config_proto_path.as_dict() if hasattr(self._TensorFlowConfig__config_proto_path, 'as_dict') else self._TensorFlowConfig__config_proto_path
        if self._TensorFlowConfig__saved_model_config is not None:
            d['savedModelConfig'] = self._TensorFlowConfig__saved_model_config.as_dict() if hasattr(self._TensorFlowConfig__saved_model_config, 'as_dict') else self._TensorFlowConfig__saved_model_config
        return d


class PythonConfig(object):
    __doc__ = 'PythonConfig\n\n    Extension of konduit.ModelConfig for custom Python code. Provide your Python\n    code either as string to `python_code` or as path to a Python script to `python_code_path`.\n    Additionally, you can modify or extend your Python path by setting `python_path` accordingly.\n\n    :param tensor_data_types_config: konduit.TensorDataTypesConfig\n    :param model_config_type: konduit.ModelConfigType\n    :param python_code: Python code as str\n    :param python_code_path: full qualifying path to the Python script you want to run, as str\n    :param python_inputs: list of Python input variable names\n    :param python_outputs: list of Python output variable names\n    :param extra_inputs: potential extra input variables\n    :param python_path: your desired Python PATH as str\n    :param return_all_inputs: whether or not to return all inputs additionally to outputs\n    :param setup_and_run: whether or not to use the setup-and-run schematics, defaults to False.\n    '
    _types_map = {'pythonCode':{'type':str, 
      'subtype':None}, 
     'pythonCodePath':{'type':str, 
      'subtype':None}, 
     'pythonPath':{'type':str, 
      'subtype':None}, 
     'pythonInputs':{'type':dict, 
      'subtype':None}, 
     'pythonOutputs':{'type':dict, 
      'subtype':None}, 
     'extraInputs':{'type':dict, 
      'subtype':None}, 
     'returnAllInputs':{'type':bool, 
      'subtype':None}, 
     'setupAndRun':{'type':bool, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, python_code=None, python_code_path=None, python_path=None, python_inputs=None, python_outputs=None, extra_inputs=None, return_all_inputs=None, setup_and_run=False):
        self._PythonConfig__python_code = python_code
        self._PythonConfig__python_code_path = python_code_path
        self._PythonConfig__python_path = python_path
        self._PythonConfig__python_inputs = python_inputs
        self._PythonConfig__python_outputs = python_outputs
        self._PythonConfig__extra_inputs = extra_inputs
        self._PythonConfig__return_all_inputs = return_all_inputs
        self._PythonConfig__setup_and_run = setup_and_run

    def _get_python_code(self):
        return self._PythonConfig__python_code

    def _set_python_code(self, value):
        if not isinstance(value, str):
            raise TypeError('pythonCode must be str')
        self._PythonConfig__python_code = value

    python_code = property(_get_python_code, _set_python_code)

    def _get_python_code_path(self):
        return self._PythonConfig__python_code_path

    def _set_python_code_path(self, value):
        if not isinstance(value, str):
            raise TypeError('pythonCodePath must be str')
        self._PythonConfig__python_code_path = value

    python_code_path = property(_get_python_code_path, _set_python_code_path)

    def _get_python_path(self):
        return self._PythonConfig__python_path

    def _set_python_path(self, value):
        if not isinstance(value, str):
            raise TypeError('pythonPath must be str')
        self._PythonConfig__python_path = value

    python_path = property(_get_python_path, _set_python_path)

    def _get_python_inputs(self):
        return self._PythonConfig__python_inputs

    def _set_python_inputs(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('pythonInputs must be type')
        self._PythonConfig__python_inputs = value

    python_inputs = property(_get_python_inputs, _set_python_inputs)

    def _get_python_outputs(self):
        return self._PythonConfig__python_outputs

    def _set_python_outputs(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('pythonOutputs must be type')
        self._PythonConfig__python_outputs = value

    python_outputs = property(_get_python_outputs, _set_python_outputs)

    def _get_extra_inputs(self):
        return self._PythonConfig__extra_inputs

    def _set_extra_inputs(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('extraInputs must be type')
        self._PythonConfig__extra_inputs = value

    extra_inputs = property(_get_extra_inputs, _set_extra_inputs)

    def _get_return_all_inputs(self):
        return self._PythonConfig__return_all_inputs

    def _set_return_all_inputs(self, value):
        if not isinstance(value, bool):
            raise TypeError('returnAllInputs must be bool')
        self._PythonConfig__return_all_inputs = value

    return_all_inputs = property(_get_return_all_inputs, _set_return_all_inputs)

    def _get_setup_and_run(self):
        return self._PythonConfig__setup_and_run

    def _set_setup_and_run(self, value):
        if not isinstance(value, bool):
            raise TypeError('setupAndRun must be bool')
        self._PythonConfig__setup_and_run = value

    setup_and_run = property(_get_setup_and_run, _set_setup_and_run)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._PythonConfig__python_code is not None:
            d['pythonCode'] = self._PythonConfig__python_code.as_dict() if hasattr(self._PythonConfig__python_code, 'as_dict') else self._PythonConfig__python_code
        if self._PythonConfig__python_code_path is not None:
            d['pythonCodePath'] = self._PythonConfig__python_code_path.as_dict() if hasattr(self._PythonConfig__python_code_path, 'as_dict') else self._PythonConfig__python_code_path
        if self._PythonConfig__python_path is not None:
            d['pythonPath'] = self._PythonConfig__python_path.as_dict() if hasattr(self._PythonConfig__python_path, 'as_dict') else self._PythonConfig__python_path
        if self._PythonConfig__python_inputs is not None:
            d['pythonInputs'] = self._PythonConfig__python_inputs.as_dict() if hasattr(self._PythonConfig__python_inputs, 'as_dict') else self._PythonConfig__python_inputs
        if self._PythonConfig__python_outputs is not None:
            d['pythonOutputs'] = self._PythonConfig__python_outputs.as_dict() if hasattr(self._PythonConfig__python_outputs, 'as_dict') else self._PythonConfig__python_outputs
        if self._PythonConfig__extra_inputs is not None:
            d['extraInputs'] = self._PythonConfig__extra_inputs.as_dict() if hasattr(self._PythonConfig__extra_inputs, 'as_dict') else self._PythonConfig__extra_inputs
        if self._PythonConfig__return_all_inputs is not None:
            d['returnAllInputs'] = self._PythonConfig__return_all_inputs.as_dict() if hasattr(self._PythonConfig__return_all_inputs, 'as_dict') else self._PythonConfig__return_all_inputs
        if self._PythonConfig__setup_and_run is not None:
            d['setupAndRun'] = self._PythonConfig__setup_and_run.as_dict() if hasattr(self._PythonConfig__setup_and_run, 'as_dict') else self._PythonConfig__setup_and_run
        return d


class ServingConfig(object):
    __doc__ = "ServingConfig\n\n    A serving configuration collects all properties needed to serve your\n    model pipeline within a konduit.InferenceConfig.\n\n    :param http_port: HTTP port of the konduit.Server\n    :param listen_host: host of the konduit.Server, defaults to 'localhost'\n    :param output_data_format: Output data format, see konduit.Output for more information\n    :param uploads_directory: to which directory to store file uploads to, defaults to 'file-uploads/'\n    :param log_timings: whether to log timings for this config, defaults to False\n    :param metric_types: the types of metrics logged for your ServingConfig can currently only be configured and\n           extended from Java. don't modify this property.\n    "
    _outputDataFormat_enum = enum.Enum('_outputDataFormat_enum',
      'NUMPY JSON ND4J ARROW', module=__name__)
    _types_map = {'httpPort':{'type':int, 
      'subtype':None}, 
     'listenHost':{'type':str, 
      'subtype':None}, 
     'outputDataFormat':{'type':str, 
      'subtype':None}, 
     'uploadsDirectory':{'type':str, 
      'subtype':None}, 
     'logTimings':{'type':bool, 
      'subtype':None}, 
     'createLoggingEndpoints':{'type':bool, 
      'subtype':None}, 
     'metricTypes':{'type':list, 
      'subtype':str}}
    _formats_map = {'metricTypes': 'table'}

    def __init__(self, http_port=None, listen_host='localhost', output_data_format='NUMPY', uploads_directory='file-uploads/', log_timings=False, create_logging_endpoints=False, metric_types=None):
        self._ServingConfig__http_port = http_port
        self._ServingConfig__listen_host = listen_host
        self._ServingConfig__output_data_format = output_data_format
        self._ServingConfig__uploads_directory = uploads_directory
        self._ServingConfig__log_timings = log_timings
        self._ServingConfig__create_logging_endpoints = create_logging_endpoints
        self._ServingConfig__metric_types = metric_types

    def _get_http_port(self):
        return self._ServingConfig__http_port

    def _set_http_port(self, value):
        if not isinstance(value, int):
            raise TypeError('httpPort must be int')
        self._ServingConfig__http_port = value

    http_port = property(_get_http_port, _set_http_port)

    def _get_listen_host(self):
        return self._ServingConfig__listen_host

    def _set_listen_host(self, value):
        if not isinstance(value, str):
            raise TypeError('listenHost must be str')
        self._ServingConfig__listen_host = value

    listen_host = property(_get_listen_host, _set_listen_host)

    def _get_output_data_format(self):
        return self._ServingConfig__output_data_format

    def _set_output_data_format(self, value):
        if not isinstance(value, str):
            raise TypeError('outputDataFormat must be str')
        elif value in self._outputDataFormat_enum.__members__:
            self._ServingConfig__type = value
        else:
            raise ValueError('Value {} not in _outputDataFormat_enum list'.format(value))

    output_data_format = property(_get_output_data_format, _set_output_data_format)

    def _get_uploads_directory(self):
        return self._ServingConfig__uploads_directory

    def _set_uploads_directory(self, value):
        if not isinstance(value, str):
            raise TypeError('uploadsDirectory must be str')
        self._ServingConfig__uploads_directory = value

    uploads_directory = property(_get_uploads_directory, _set_uploads_directory)

    def _get_log_timings(self):
        return self._ServingConfig__log_timings

    def _set_log_timings(self, value):
        if not isinstance(value, bool):
            raise TypeError('logTimings must be bool')
        self._ServingConfig__log_timings = value

    log_timings = property(_get_log_timings, _set_log_timings)

    def _get_create_logging_endpoints(self):
        return self._ServingConfig__create_logging_endpoints

    def _set_create_logging_endpoints(self, value):
        if not isinstance(value, bool):
            raise TypeError('createLoggingEndpoints must be bool')
        self._ServingConfig__create_logging_endpoints = value

    create_logging_endpoints = property(_get_create_logging_endpoints, _set_create_logging_endpoints)

    def _get_metric_types(self):
        return self._ServingConfig__metric_types

    def _set_metric_types(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('metricTypes must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('metricTypes list valeus must be str')
        self._ServingConfig__metric_types = value

    metric_types = property(_get_metric_types, _set_metric_types)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ServingConfig__http_port is not None:
            d['httpPort'] = self._ServingConfig__http_port.as_dict() if hasattr(self._ServingConfig__http_port, 'as_dict') else self._ServingConfig__http_port
        if self._ServingConfig__listen_host is not None:
            d['listenHost'] = self._ServingConfig__listen_host.as_dict() if hasattr(self._ServingConfig__listen_host, 'as_dict') else self._ServingConfig__listen_host
        if self._ServingConfig__output_data_format is not None:
            d['outputDataFormat'] = self._ServingConfig__output_data_format.as_dict() if hasattr(self._ServingConfig__output_data_format, 'as_dict') else self._ServingConfig__output_data_format
        if self._ServingConfig__uploads_directory is not None:
            d['uploadsDirectory'] = self._ServingConfig__uploads_directory.as_dict() if hasattr(self._ServingConfig__uploads_directory, 'as_dict') else self._ServingConfig__uploads_directory
        if self._ServingConfig__log_timings is not None:
            d['logTimings'] = self._ServingConfig__log_timings.as_dict() if hasattr(self._ServingConfig__log_timings, 'as_dict') else self._ServingConfig__log_timings
        if self._ServingConfig__create_logging_endpoints is not None:
            d['createLoggingEndpoints'] = self._ServingConfig__create_logging_endpoints.as_dict() if hasattr(self._ServingConfig__create_logging_endpoints, 'as_dict') else self._ServingConfig__create_logging_endpoints
        if self._ServingConfig__metric_types is not None:
            d['metricTypes'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ServingConfig__metric_types]
        return d


class PipelineStep(object):
    __doc__ = 'PipelineStep\n\n    PipelineStep collects all ETL and model related properties (input schema,\n    normalization and transform steps, output schema, potential pre-\n    or post-processing etc.). This config is passed to the respective\n    verticle along with konduit.ServingConfig.\n\n    :param input_schemas: dictionary of konduit.SchemaType for input names\n    :param output_schemas: dictionary of konduit.SchemaType for output names\n    :param input_names: list on step input names\n    :param output_names: list of step output names\n    :param input_column_names: dictionary mapping input names to lists of names of your columnar data (e.g.\n           { "input_1": ["col1", "col2"]}\n    :param output_column_names: dictionary mapping output names to lists of names of your columnar data (e.g.\n           { "output_1": ["col1", "col2"]}\n    '
    _types_map = {'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}, 
     'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputNames':{'type':list, 
      'subtype':str}}
    _formats_map = {'outputNames':'table', 
     'inputNames':'table'}

    def __init__(self, input_column_names=None, output_column_names=None, input_schemas=None, output_schemas=None, output_names=None, input_names=None):
        self._PipelineStep__input_column_names = input_column_names
        self._PipelineStep__output_column_names = output_column_names
        self._PipelineStep__input_schemas = input_schemas
        self._PipelineStep__output_schemas = output_schemas
        self._PipelineStep__output_names = output_names
        self._PipelineStep__input_names = input_names

    def _get_input_column_names(self):
        return self._PipelineStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._PipelineStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._PipelineStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._PipelineStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def _get_input_schemas(self):
        return self._PipelineStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._PipelineStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._PipelineStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._PipelineStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_output_names(self):
        return self._PipelineStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._PipelineStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_names(self):
        return self._PipelineStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._PipelineStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._PipelineStep__input_column_names is not None:
            d['inputColumnNames'] = self._PipelineStep__input_column_names.as_dict() if hasattr(self._PipelineStep__input_column_names, 'as_dict') else self._PipelineStep__input_column_names
        if self._PipelineStep__output_column_names is not None:
            d['outputColumnNames'] = self._PipelineStep__output_column_names.as_dict() if hasattr(self._PipelineStep__output_column_names, 'as_dict') else self._PipelineStep__output_column_names
        if self._PipelineStep__input_schemas is not None:
            d['inputSchemas'] = self._PipelineStep__input_schemas.as_dict() if hasattr(self._PipelineStep__input_schemas, 'as_dict') else self._PipelineStep__input_schemas
        if self._PipelineStep__output_schemas is not None:
            d['outputSchemas'] = self._PipelineStep__output_schemas.as_dict() if hasattr(self._PipelineStep__output_schemas, 'as_dict') else self._PipelineStep__output_schemas
        if self._PipelineStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._PipelineStep__output_names]
        if self._PipelineStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._PipelineStep__input_names]
        return d


class TextConfig(object):
    _types_map = {}
    _formats_map = {}

    def __init__(self):
        pass

    def as_dict(self):
        d = empty_type_dict(self)
        return d


class BasePipelineStep(PipelineStep):
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None):
        self._BasePipelineStep__input_schemas = input_schemas
        self._BasePipelineStep__output_schemas = output_schemas
        self._BasePipelineStep__input_names = input_names
        self._BasePipelineStep__output_names = output_names
        self._BasePipelineStep__input_column_names = input_column_names
        self._BasePipelineStep__output_column_names = output_column_names

    def _get_input_schemas(self):
        return self._BasePipelineStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._BasePipelineStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._BasePipelineStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._BasePipelineStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._BasePipelineStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._BasePipelineStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._BasePipelineStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._BasePipelineStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._BasePipelineStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._BasePipelineStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._BasePipelineStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._BasePipelineStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._BasePipelineStep__input_schemas is not None:
            d['inputSchemas'] = self._BasePipelineStep__input_schemas.as_dict() if hasattr(self._BasePipelineStep__input_schemas, 'as_dict') else self._BasePipelineStep__input_schemas
        if self._BasePipelineStep__output_schemas is not None:
            d['outputSchemas'] = self._BasePipelineStep__output_schemas.as_dict() if hasattr(self._BasePipelineStep__output_schemas, 'as_dict') else self._BasePipelineStep__output_schemas
        if self._BasePipelineStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._BasePipelineStep__input_names]
        if self._BasePipelineStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._BasePipelineStep__output_names]
        if self._BasePipelineStep__input_column_names is not None:
            d['inputColumnNames'] = self._BasePipelineStep__input_column_names.as_dict() if hasattr(self._BasePipelineStep__input_column_names, 'as_dict') else self._BasePipelineStep__input_column_names
        if self._BasePipelineStep__output_column_names is not None:
            d['outputColumnNames'] = self._BasePipelineStep__output_column_names.as_dict() if hasattr(self._BasePipelineStep__output_column_names, 'as_dict') else self._BasePipelineStep__output_column_names
        return d


class NormalizationConfig(object):
    __doc__ = 'NormalizationConfig\n\n    Configuration for data normalization in the ETL part of your pipeline.\n\n    :param config: dictionary of str values defining you normalization step.\n    '
    _types_map = {'config': {'type':dict,  'subtype':None}}
    _formats_map = {}

    def __init__(self, config=None):
        self._NormalizationConfig__config = config

    def _get_config(self):
        return self._NormalizationConfig__config

    def _set_config(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('config must be type')
        self._NormalizationConfig__config = value

    config = property(_get_config, _set_config)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._NormalizationConfig__config is not None:
            d['config'] = self._NormalizationConfig__config.as_dict() if hasattr(self._NormalizationConfig__config, 'as_dict') else self._NormalizationConfig__config
        return d


class PythonStep(PipelineStep):
    __doc__ = 'PythonStep\n\n    PythonStep defines a custom Python konduit.PipelineStep from a konduit.PythonConfig.\n\n    :param input_schemas: Input konduit.SchemaTypes, see konduit.PipelineStep.\n    :param output_schemas: Output konduit.SchemaTypes, see konduit.PipelineStep.\n    :param input_names: list of step input names, see konduit.PipelineStep.\n    :param output_names: list of step input names, see konduit.PipelineStep.\n    :param input_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param output_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param python_configs: konduit.PythonConfig\n    '
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}, 
     'pythonConfigs':{'type':dict, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None, python_configs=None):
        self._PythonStep__input_schemas = input_schemas
        self._PythonStep__output_schemas = output_schemas
        self._PythonStep__input_names = input_names
        self._PythonStep__output_names = output_names
        self._PythonStep__input_column_names = input_column_names
        self._PythonStep__output_column_names = output_column_names
        self._PythonStep__python_configs = python_configs

    def _get_input_schemas(self):
        return self._PythonStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._PythonStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._PythonStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._PythonStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._PythonStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._PythonStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._PythonStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._PythonStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._PythonStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._PythonStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._PythonStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._PythonStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def _get_python_configs(self):
        return self._PythonStep__python_configs

    def _set_python_configs(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('pythonConfigs must be type')
        self._PythonStep__python_configs = value

    python_configs = property(_get_python_configs, _set_python_configs)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._PythonStep__input_schemas is not None:
            d['inputSchemas'] = self._PythonStep__input_schemas.as_dict() if hasattr(self._PythonStep__input_schemas, 'as_dict') else self._PythonStep__input_schemas
        if self._PythonStep__output_schemas is not None:
            d['outputSchemas'] = self._PythonStep__output_schemas.as_dict() if hasattr(self._PythonStep__output_schemas, 'as_dict') else self._PythonStep__output_schemas
        if self._PythonStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._PythonStep__input_names]
        if self._PythonStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._PythonStep__output_names]
        if self._PythonStep__input_column_names is not None:
            d['inputColumnNames'] = self._PythonStep__input_column_names.as_dict() if hasattr(self._PythonStep__input_column_names, 'as_dict') else self._PythonStep__input_column_names
        if self._PythonStep__output_column_names is not None:
            d['outputColumnNames'] = self._PythonStep__output_column_names.as_dict() if hasattr(self._PythonStep__output_column_names, 'as_dict') else self._PythonStep__output_column_names
        if self._PythonStep__python_configs is not None:
            d['pythonConfigs'] = self._PythonStep__python_configs.as_dict() if hasattr(self._PythonStep__python_configs, 'as_dict') else self._PythonStep__python_configs
        return d


class TransformProcessStep(PipelineStep):
    __doc__ = 'TransformProcessStep\n\n    TransformProcessStep defines a konduit.PipelineStep from a DataVec TransformProcess\n\n    :param input_schemas: Input konduit.SchemaTypes, see konduit.PipelineStep.\n    :param output_schemas: Output konduit.SchemaTypes, see konduit.PipelineStep.\n    :param input_names: list of step input names, see konduit.PipelineStep.\n    :param output_names: list of step input names, see konduit.PipelineStep.\n    :param input_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param output_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param transform_processes: DataVec TransformProcess\n    '
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}, 
     'transformProcesses':{'type':dict, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None, transform_processes=None):
        self._TransformProcessStep__input_schemas = input_schemas
        self._TransformProcessStep__output_schemas = output_schemas
        self._TransformProcessStep__input_names = input_names
        self._TransformProcessStep__output_names = output_names
        self._TransformProcessStep__input_column_names = input_column_names
        self._TransformProcessStep__output_column_names = output_column_names
        self._TransformProcessStep__transform_processes = transform_processes

    def _get_input_schemas(self):
        return self._TransformProcessStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._TransformProcessStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._TransformProcessStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._TransformProcessStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._TransformProcessStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._TransformProcessStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._TransformProcessStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._TransformProcessStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._TransformProcessStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._TransformProcessStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._TransformProcessStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._TransformProcessStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def _get_transform_processes(self):
        return self._TransformProcessStep__transform_processes

    def _set_transform_processes(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('transformProcesses must be type')
        self._TransformProcessStep__transform_processes = value

    transform_processes = property(_get_transform_processes, _set_transform_processes)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._TransformProcessStep__input_schemas is not None:
            d['inputSchemas'] = self._TransformProcessStep__input_schemas.as_dict() if hasattr(self._TransformProcessStep__input_schemas, 'as_dict') else self._TransformProcessStep__input_schemas
        if self._TransformProcessStep__output_schemas is not None:
            d['outputSchemas'] = self._TransformProcessStep__output_schemas.as_dict() if hasattr(self._TransformProcessStep__output_schemas, 'as_dict') else self._TransformProcessStep__output_schemas
        if self._TransformProcessStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._TransformProcessStep__input_names]
        if self._TransformProcessStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._TransformProcessStep__output_names]
        if self._TransformProcessStep__input_column_names is not None:
            d['inputColumnNames'] = self._TransformProcessStep__input_column_names.as_dict() if hasattr(self._TransformProcessStep__input_column_names, 'as_dict') else self._TransformProcessStep__input_column_names
        if self._TransformProcessStep__output_column_names is not None:
            d['outputColumnNames'] = self._TransformProcessStep__output_column_names.as_dict() if hasattr(self._TransformProcessStep__output_column_names, 'as_dict') else self._TransformProcessStep__output_column_names
        if self._TransformProcessStep__transform_processes is not None:
            d['transformProcesses'] = self._TransformProcessStep__transform_processes.as_dict() if hasattr(self._TransformProcessStep__transform_processes, 'as_dict') else self._TransformProcessStep__transform_processes
        return d


class ModelStep(PipelineStep):
    __doc__ = 'ModelStep\n\n    ModelStep extends konduit.PipelineStep and is the base class for all pipeline steps\n    involving machine learning models.\n\n    :param input_schemas: Input konduit.SchemaTypes, see konduit.PipelineStep.\n    :param output_schemas: Output konduit.SchemaTypes, see konduit.PipelineStep.\n    :param input_names: list of step input names, see konduit.PipelineStep.\n    :param output_names: list of step input names, see konduit.PipelineStep.\n    :param input_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param output_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param model_config: konduit.ModelConfig\n    :param parallel_inference_config: konduit.ParallelInferenceConfig\n    :param normalization_config: konduit.NormalizationConfig\n    '
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}, 
     'modelConfig':{'type':ModelConfig, 
      'subtype':None}, 
     'parallelInferenceConfig':{'type':ParallelInferenceConfig, 
      'subtype':None}, 
     'normalizationConfig':{'type':NormalizationConfig, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None, model_config=None, parallel_inference_config=None, normalization_config=None):
        self._ModelStep__input_schemas = input_schemas
        self._ModelStep__output_schemas = output_schemas
        self._ModelStep__input_names = input_names
        self._ModelStep__output_names = output_names
        self._ModelStep__input_column_names = input_column_names
        self._ModelStep__output_column_names = output_column_names
        self._ModelStep__model_config = model_config
        self._ModelStep__parallel_inference_config = parallel_inference_config
        self._ModelStep__normalization_config = normalization_config

    def _get_input_schemas(self):
        return self._ModelStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._ModelStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._ModelStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._ModelStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._ModelStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._ModelStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._ModelStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._ModelStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._ModelStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._ModelStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._ModelStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._ModelStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def _get_model_config(self):
        return self._ModelStep__model_config

    def _set_model_config(self, value):
        if not isinstance(value, ModelConfig):
            raise TypeError('modelConfig must be ModelConfig')
        self._ModelStep__model_config = value

    model_config = property(_get_model_config, _set_model_config)

    def _get_parallel_inference_config(self):
        return self._ModelStep__parallel_inference_config

    def _set_parallel_inference_config(self, value):
        if not isinstance(value, ParallelInferenceConfig):
            raise TypeError('parallelInferenceConfig must be ParallelInferenceConfig')
        self._ModelStep__parallel_inference_config = value

    parallel_inference_config = property(_get_parallel_inference_config, _set_parallel_inference_config)

    def _get_normalization_config(self):
        return self._ModelStep__normalization_config

    def _set_normalization_config(self, value):
        if not isinstance(value, NormalizationConfig):
            raise TypeError('normalizationConfig must be NormalizationConfig')
        self._ModelStep__normalization_config = value

    normalization_config = property(_get_normalization_config, _set_normalization_config)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ModelStep__input_schemas is not None:
            d['inputSchemas'] = self._ModelStep__input_schemas.as_dict() if hasattr(self._ModelStep__input_schemas, 'as_dict') else self._ModelStep__input_schemas
        if self._ModelStep__output_schemas is not None:
            d['outputSchemas'] = self._ModelStep__output_schemas.as_dict() if hasattr(self._ModelStep__output_schemas, 'as_dict') else self._ModelStep__output_schemas
        if self._ModelStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ModelStep__input_names]
        if self._ModelStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ModelStep__output_names]
        if self._ModelStep__input_column_names is not None:
            d['inputColumnNames'] = self._ModelStep__input_column_names.as_dict() if hasattr(self._ModelStep__input_column_names, 'as_dict') else self._ModelStep__input_column_names
        if self._ModelStep__output_column_names is not None:
            d['outputColumnNames'] = self._ModelStep__output_column_names.as_dict() if hasattr(self._ModelStep__output_column_names, 'as_dict') else self._ModelStep__output_column_names
        if self._ModelStep__model_config is not None:
            d['modelConfig'] = self._ModelStep__model_config.as_dict() if hasattr(self._ModelStep__model_config, 'as_dict') else self._ModelStep__model_config
        if self._ModelStep__parallel_inference_config is not None:
            d['parallelInferenceConfig'] = self._ModelStep__parallel_inference_config.as_dict() if hasattr(self._ModelStep__parallel_inference_config, 'as_dict') else self._ModelStep__parallel_inference_config
        if self._ModelStep__normalization_config is not None:
            d['normalizationConfig'] = self._ModelStep__normalization_config.as_dict() if hasattr(self._ModelStep__normalization_config, 'as_dict') else self._ModelStep__normalization_config
        return d


class ArrayConcatenationStep(PipelineStep):
    __doc__ = 'ArrayConcatenationStep\n\n    konduit.PipelineStep that concatenates two or more arrays along the specified dimensions.\n\n    :param input_schemas: Input konduit.SchemaTypes, see konduit.PipelineStep.\n    :param output_schemas: Output konduit.SchemaTypes, see konduit.PipelineStep.\n    :param input_names: list of step input names, see konduit.PipelineStep.\n    :param output_names: list of step input names, see konduit.PipelineStep.\n    :param input_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param output_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param concat_dimensions: dictionary of array indices to concatenation dimension\n    '
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}, 
     'concatDimensions':{'type':dict, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None, concat_dimensions=None):
        self._ArrayConcatenationStep__input_schemas = input_schemas
        self._ArrayConcatenationStep__output_schemas = output_schemas
        self._ArrayConcatenationStep__input_names = input_names
        self._ArrayConcatenationStep__output_names = output_names
        self._ArrayConcatenationStep__input_column_names = input_column_names
        self._ArrayConcatenationStep__output_column_names = output_column_names
        self._ArrayConcatenationStep__concat_dimensions = concat_dimensions

    def _get_input_schemas(self):
        return self._ArrayConcatenationStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._ArrayConcatenationStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._ArrayConcatenationStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._ArrayConcatenationStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._ArrayConcatenationStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._ArrayConcatenationStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._ArrayConcatenationStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._ArrayConcatenationStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._ArrayConcatenationStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._ArrayConcatenationStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._ArrayConcatenationStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._ArrayConcatenationStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def _get_concat_dimensions(self):
        return self._ArrayConcatenationStep__concat_dimensions

    def _set_concat_dimensions(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('concatDimensions must be type')
        self._ArrayConcatenationStep__concat_dimensions = value

    concat_dimensions = property(_get_concat_dimensions, _set_concat_dimensions)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ArrayConcatenationStep__input_schemas is not None:
            d['inputSchemas'] = self._ArrayConcatenationStep__input_schemas.as_dict() if hasattr(self._ArrayConcatenationStep__input_schemas, 'as_dict') else self._ArrayConcatenationStep__input_schemas
        if self._ArrayConcatenationStep__output_schemas is not None:
            d['outputSchemas'] = self._ArrayConcatenationStep__output_schemas.as_dict() if hasattr(self._ArrayConcatenationStep__output_schemas, 'as_dict') else self._ArrayConcatenationStep__output_schemas
        if self._ArrayConcatenationStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ArrayConcatenationStep__input_names]
        if self._ArrayConcatenationStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ArrayConcatenationStep__output_names]
        if self._ArrayConcatenationStep__input_column_names is not None:
            d['inputColumnNames'] = self._ArrayConcatenationStep__input_column_names.as_dict() if hasattr(self._ArrayConcatenationStep__input_column_names, 'as_dict') else self._ArrayConcatenationStep__input_column_names
        if self._ArrayConcatenationStep__output_column_names is not None:
            d['outputColumnNames'] = self._ArrayConcatenationStep__output_column_names.as_dict() if hasattr(self._ArrayConcatenationStep__output_column_names, 'as_dict') else self._ArrayConcatenationStep__output_column_names
        if self._ArrayConcatenationStep__concat_dimensions is not None:
            d['concatDimensions'] = self._ArrayConcatenationStep__concat_dimensions.as_dict() if hasattr(self._ArrayConcatenationStep__concat_dimensions, 'as_dict') else self._ArrayConcatenationStep__concat_dimensions
        return d


class JsonExpanderTransformStep(PipelineStep):
    __doc__ = 'JsonExpanderTransformStep\n\n    Executes expansion of JSON objects in to "real" objects.\n    This is needed when integrating with PipelineStepRunner\n    that may output {@link Text} with json arrays or json objects.\n    This kind of output is generally expected from Python or PMML based pipelines\n    which have a lot more complicated output and schema based values\n    rather than straight NDArrays like\n    most deep learning pipelines will be.\n\n    :param input_schemas: Input konduit.SchemaTypes, see konduit.PipelineStep.\n    :param output_schemas: Output konduit.SchemaTypes, see konduit.PipelineStep.\n    :param input_names: list of step input names, see konduit.PipelineStep.\n    :param output_names: list of step input names, see konduit.PipelineStep.\n    :param input_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param output_column_names: Input name to column name mapping, see konduit.PipelineStep.\n        '
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None):
        self._JsonExpanderTransformStep__input_schemas = input_schemas
        self._JsonExpanderTransformStep__output_schemas = output_schemas
        self._JsonExpanderTransformStep__input_names = input_names
        self._JsonExpanderTransformStep__output_names = output_names
        self._JsonExpanderTransformStep__input_column_names = input_column_names
        self._JsonExpanderTransformStep__output_column_names = output_column_names

    def _get_input_schemas(self):
        return self._JsonExpanderTransformStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._JsonExpanderTransformStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._JsonExpanderTransformStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._JsonExpanderTransformStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._JsonExpanderTransformStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._JsonExpanderTransformStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._JsonExpanderTransformStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._JsonExpanderTransformStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._JsonExpanderTransformStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._JsonExpanderTransformStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._JsonExpanderTransformStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._JsonExpanderTransformStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._JsonExpanderTransformStep__input_schemas is not None:
            d['inputSchemas'] = self._JsonExpanderTransformStep__input_schemas.as_dict() if hasattr(self._JsonExpanderTransformStep__input_schemas, 'as_dict') else self._JsonExpanderTransformStep__input_schemas
        if self._JsonExpanderTransformStep__output_schemas is not None:
            d['outputSchemas'] = self._JsonExpanderTransformStep__output_schemas.as_dict() if hasattr(self._JsonExpanderTransformStep__output_schemas, 'as_dict') else self._JsonExpanderTransformStep__output_schemas
        if self._JsonExpanderTransformStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._JsonExpanderTransformStep__input_names]
        if self._JsonExpanderTransformStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._JsonExpanderTransformStep__output_names]
        if self._JsonExpanderTransformStep__input_column_names is not None:
            d['inputColumnNames'] = self._JsonExpanderTransformStep__input_column_names.as_dict() if hasattr(self._JsonExpanderTransformStep__input_column_names, 'as_dict') else self._JsonExpanderTransformStep__input_column_names
        if self._JsonExpanderTransformStep__output_column_names is not None:
            d['outputColumnNames'] = self._JsonExpanderTransformStep__output_column_names.as_dict() if hasattr(self._JsonExpanderTransformStep__output_column_names, 'as_dict') else self._JsonExpanderTransformStep__output_column_names
        return d


class ImageLoadingStep(PipelineStep):
    __doc__ = 'ImageLoadingStep\n\n    Loads an input image into an NDArray.\n\n    :param input_schemas: Input konduit.SchemaTypes, see konduit.PipelineStep.\n    :param output_schemas: Output konduit.SchemaTypes, see konduit.PipelineStep.\n    :param input_names: list of step input names, see konduit.PipelineStep.\n    :param output_names: list of step input names, see konduit.PipelineStep.\n    :param input_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param output_column_names: Input name to column name mapping, see konduit.PipelineStep.\n    :param original_image_height: input image height in pixels\n    :param original_image_width: input image width in pixels\n    :param update_ordering_before_transform: boolean, defaults to False\n    :param dimensions_configs: dictionary defining input shapes per input name, e.g. {"input", [28,28,3]}\n    :param image_processing_required_layout: desired channel ordering after this pipeline step has been applied,\n           either "NCHW" or "NHWC", defaults to the prior\n    :param image_processing_initial_layout: channel ordering before processing, either\n           "NCHW" or "NHWC", defaults to the prior\n    :param image_transform_processes: a DataVec ImageTransformProcess\n    :param object_detection_config: konduit.ObjectDetectionConfig\n    '
    _types_map = {'inputSchemas':{'type':dict, 
      'subtype':None}, 
     'outputSchemas':{'type':dict, 
      'subtype':None}, 
     'inputNames':{'type':list, 
      'subtype':str}, 
     'outputNames':{'type':list, 
      'subtype':str}, 
     'inputColumnNames':{'type':dict, 
      'subtype':None}, 
     'outputColumnNames':{'type':dict, 
      'subtype':None}, 
     'originalImageHeight':{'type':int, 
      'subtype':None}, 
     'originalImageWidth':{'type':int, 
      'subtype':None}, 
     'updateOrderingBeforeTransform':{'type':bool, 
      'subtype':None}, 
     'dimensionsConfigs':{'type':dict, 
      'subtype':None}, 
     'imageProcessingRequiredLayout':{'type':str, 
      'subtype':None}, 
     'imageProcessingInitialLayout':{'type':str, 
      'subtype':None}, 
     'imageTransformProcesses':{'type':dict, 
      'subtype':None}, 
     'objectDetectionConfig':{'type':ObjectDetectionConfig, 
      'subtype':None}}
    _formats_map = {'inputNames':'table', 
     'outputNames':'table'}

    def __init__(self, input_schemas=None, output_schemas=None, input_names=None, output_names=None, input_column_names=None, output_column_names=None, original_image_height=None, original_image_width=None, update_ordering_before_transform=None, dimensions_configs=None, image_processing_required_layout=None, image_processing_initial_layout=None, image_transform_processes=None, object_detection_config=None):
        self._ImageLoadingStep__input_schemas = input_schemas
        self._ImageLoadingStep__output_schemas = output_schemas
        self._ImageLoadingStep__input_names = input_names
        self._ImageLoadingStep__output_names = output_names
        self._ImageLoadingStep__input_column_names = input_column_names
        self._ImageLoadingStep__output_column_names = output_column_names
        self._ImageLoadingStep__original_image_height = original_image_height
        self._ImageLoadingStep__original_image_width = original_image_width
        self._ImageLoadingStep__update_ordering_before_transform = update_ordering_before_transform
        self._ImageLoadingStep__dimensions_configs = dimensions_configs
        self._ImageLoadingStep__image_processing_required_layout = image_processing_required_layout
        self._ImageLoadingStep__image_processing_initial_layout = image_processing_initial_layout
        self._ImageLoadingStep__image_transform_processes = image_transform_processes
        self._ImageLoadingStep__object_detection_config = object_detection_config

    def _get_input_schemas(self):
        return self._ImageLoadingStep__input_schemas

    def _set_input_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputSchemas must be type')
        self._ImageLoadingStep__input_schemas = value

    input_schemas = property(_get_input_schemas, _set_input_schemas)

    def _get_output_schemas(self):
        return self._ImageLoadingStep__output_schemas

    def _set_output_schemas(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputSchemas must be type')
        self._ImageLoadingStep__output_schemas = value

    output_schemas = property(_get_output_schemas, _set_output_schemas)

    def _get_input_names(self):
        return self._ImageLoadingStep__input_names

    def _set_input_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('inputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('inputNames list valeus must be str')
        self._ImageLoadingStep__input_names = value

    input_names = property(_get_input_names, _set_input_names)

    def _get_output_names(self):
        return self._ImageLoadingStep__output_names

    def _set_output_names(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('outputNames must be list')
        if not all((isinstance(i, str) for i in value)):
            raise TypeError('outputNames list valeus must be str')
        self._ImageLoadingStep__output_names = value

    output_names = property(_get_output_names, _set_output_names)

    def _get_input_column_names(self):
        return self._ImageLoadingStep__input_column_names

    def _set_input_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('inputColumnNames must be type')
        self._ImageLoadingStep__input_column_names = value

    input_column_names = property(_get_input_column_names, _set_input_column_names)

    def _get_output_column_names(self):
        return self._ImageLoadingStep__output_column_names

    def _set_output_column_names(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('outputColumnNames must be type')
        self._ImageLoadingStep__output_column_names = value

    output_column_names = property(_get_output_column_names, _set_output_column_names)

    def _get_original_image_height(self):
        return self._ImageLoadingStep__original_image_height

    def _set_original_image_height(self, value):
        if not isinstance(value, int):
            raise TypeError('originalImageHeight must be int')
        self._ImageLoadingStep__original_image_height = value

    original_image_height = property(_get_original_image_height, _set_original_image_height)

    def _get_original_image_width(self):
        return self._ImageLoadingStep__original_image_width

    def _set_original_image_width(self, value):
        if not isinstance(value, int):
            raise TypeError('originalImageWidth must be int')
        self._ImageLoadingStep__original_image_width = value

    original_image_width = property(_get_original_image_width, _set_original_image_width)

    def _get_update_ordering_before_transform(self):
        return self._ImageLoadingStep__update_ordering_before_transform

    def _set_update_ordering_before_transform(self, value):
        if not isinstance(value, bool):
            raise TypeError('updateOrderingBeforeTransform must be bool')
        self._ImageLoadingStep__update_ordering_before_transform = value

    update_ordering_before_transform = property(_get_update_ordering_before_transform, _set_update_ordering_before_transform)

    def _get_dimensions_configs(self):
        return self._ImageLoadingStep__dimensions_configs

    def _set_dimensions_configs(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('dimensionsConfigs must be type')
        self._ImageLoadingStep__dimensions_configs = value

    dimensions_configs = property(_get_dimensions_configs, _set_dimensions_configs)

    def _get_image_processing_required_layout(self):
        return self._ImageLoadingStep__image_processing_required_layout

    def _set_image_processing_required_layout(self, value):
        if not isinstance(value, str):
            raise TypeError('imageProcessingRequiredLayout must be str')
        self._ImageLoadingStep__image_processing_required_layout = value

    image_processing_required_layout = property(_get_image_processing_required_layout, _set_image_processing_required_layout)

    def _get_image_processing_initial_layout(self):
        return self._ImageLoadingStep__image_processing_initial_layout

    def _set_image_processing_initial_layout(self, value):
        if not isinstance(value, str):
            raise TypeError('imageProcessingInitialLayout must be str')
        self._ImageLoadingStep__image_processing_initial_layout = value

    image_processing_initial_layout = property(_get_image_processing_initial_layout, _set_image_processing_initial_layout)

    def _get_image_transform_processes(self):
        return self._ImageLoadingStep__image_transform_processes

    def _set_image_transform_processes(self, value):
        if not isinstance(value, dict):
            if not isinstance(value, DictWrapper):
                if not isinstance(value, DictWrapper):
                    raise TypeError('imageTransformProcesses must be type')
        self._ImageLoadingStep__image_transform_processes = value

    image_transform_processes = property(_get_image_transform_processes, _set_image_transform_processes)

    def _get_object_detection_config(self):
        return self._ImageLoadingStep__object_detection_config

    def _set_object_detection_config(self, value):
        if not isinstance(value, ObjectDetectionConfig):
            raise TypeError('objectDetectionConfig must be ObjectDetectionConfig')
        self._ImageLoadingStep__object_detection_config = value

    object_detection_config = property(_get_object_detection_config, _set_object_detection_config)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._ImageLoadingStep__input_schemas is not None:
            d['inputSchemas'] = self._ImageLoadingStep__input_schemas.as_dict() if hasattr(self._ImageLoadingStep__input_schemas, 'as_dict') else self._ImageLoadingStep__input_schemas
        if self._ImageLoadingStep__output_schemas is not None:
            d['outputSchemas'] = self._ImageLoadingStep__output_schemas.as_dict() if hasattr(self._ImageLoadingStep__output_schemas, 'as_dict') else self._ImageLoadingStep__output_schemas
        if self._ImageLoadingStep__input_names is not None:
            d['inputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ImageLoadingStep__input_names]
        if self._ImageLoadingStep__output_names is not None:
            d['outputNames'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._ImageLoadingStep__output_names]
        if self._ImageLoadingStep__input_column_names is not None:
            d['inputColumnNames'] = self._ImageLoadingStep__input_column_names.as_dict() if hasattr(self._ImageLoadingStep__input_column_names, 'as_dict') else self._ImageLoadingStep__input_column_names
        if self._ImageLoadingStep__output_column_names is not None:
            d['outputColumnNames'] = self._ImageLoadingStep__output_column_names.as_dict() if hasattr(self._ImageLoadingStep__output_column_names, 'as_dict') else self._ImageLoadingStep__output_column_names
        if self._ImageLoadingStep__original_image_height is not None:
            d['originalImageHeight'] = self._ImageLoadingStep__original_image_height.as_dict() if hasattr(self._ImageLoadingStep__original_image_height, 'as_dict') else self._ImageLoadingStep__original_image_height
        if self._ImageLoadingStep__original_image_width is not None:
            d['originalImageWidth'] = self._ImageLoadingStep__original_image_width.as_dict() if hasattr(self._ImageLoadingStep__original_image_width, 'as_dict') else self._ImageLoadingStep__original_image_width
        if self._ImageLoadingStep__update_ordering_before_transform is not None:
            d['updateOrderingBeforeTransform'] = self._ImageLoadingStep__update_ordering_before_transform.as_dict() if hasattr(self._ImageLoadingStep__update_ordering_before_transform, 'as_dict') else self._ImageLoadingStep__update_ordering_before_transform
        if self._ImageLoadingStep__dimensions_configs is not None:
            d['dimensionsConfigs'] = self._ImageLoadingStep__dimensions_configs.as_dict() if hasattr(self._ImageLoadingStep__dimensions_configs, 'as_dict') else self._ImageLoadingStep__dimensions_configs
        if self._ImageLoadingStep__image_processing_required_layout is not None:
            d['imageProcessingRequiredLayout'] = self._ImageLoadingStep__image_processing_required_layout.as_dict() if hasattr(self._ImageLoadingStep__image_processing_required_layout, 'as_dict') else self._ImageLoadingStep__image_processing_required_layout
        if self._ImageLoadingStep__image_processing_initial_layout is not None:
            d['imageProcessingInitialLayout'] = self._ImageLoadingStep__image_processing_initial_layout.as_dict() if hasattr(self._ImageLoadingStep__image_processing_initial_layout, 'as_dict') else self._ImageLoadingStep__image_processing_initial_layout
        if self._ImageLoadingStep__image_transform_processes is not None:
            d['imageTransformProcesses'] = self._ImageLoadingStep__image_transform_processes.as_dict() if hasattr(self._ImageLoadingStep__image_transform_processes, 'as_dict') else self._ImageLoadingStep__image_transform_processes
        if self._ImageLoadingStep__object_detection_config is not None:
            d['objectDetectionConfig'] = self._ImageLoadingStep__object_detection_config.as_dict() if hasattr(self._ImageLoadingStep__object_detection_config, 'as_dict') else self._ImageLoadingStep__object_detection_config
        return d


class MemMapConfig(object):
    __doc__ = 'MemMapConfig\n\n    Configuration for managing serving of memory-mapped files. The goal is to mem-map\n    and serve a large array stored in "array_path" and get slices of this array on demand\n    by index. If an index is specified that does not match an index of the mem-mapped array,\n    an default or "unknown" vector is inserted into the slice instead, which is stored in\n    "unk_vector_path".\n\n    For instance, let\'s say we want to mem-map [[1, 2, 3], [4, 5, 6]], a small array with two\n    valid slices. Our unknown vector is simply [0, 0, 0] in this example. Now, if we query for\n    the indices {-2, 1} we\'d get [[0, 0, 0], [4, 5, 6]].\n\n    :param array_path: path: path to the file containing the large array you want to memory-map\n    :param unk_vector_path: path to the file containing the "unknown" vector / slice\n    :param initial_memmap_size: size of the mem-map, defaults to 1000000000\n    :param work_space_name: DL4J \'WorkSpace\' name, defaults to \'memMapWorkspace\'\n    '
    _types_map = {'arrayPath':{'type':str, 
      'subtype':None}, 
     'unkVectorPath':{'type':str, 
      'subtype':None}, 
     'initialMemmapSize':{'type':int, 
      'subtype':None}, 
     'workSpaceName':{'type':str, 
      'subtype':None}}
    _formats_map = {}

    def __init__(self, array_path=None, unk_vector_path=None, initial_memmap_size=None, work_space_name=None):
        self._MemMapConfig__array_path = array_path
        self._MemMapConfig__unk_vector_path = unk_vector_path
        self._MemMapConfig__initial_memmap_size = initial_memmap_size
        self._MemMapConfig__work_space_name = work_space_name

    def _get_array_path(self):
        return self._MemMapConfig__array_path

    def _set_array_path(self, value):
        if not isinstance(value, str):
            raise TypeError('arrayPath must be str')
        self._MemMapConfig__array_path = value

    array_path = property(_get_array_path, _set_array_path)

    def _get_unk_vector_path(self):
        return self._MemMapConfig__unk_vector_path

    def _set_unk_vector_path(self, value):
        if not isinstance(value, str):
            raise TypeError('unkVectorPath must be str')
        self._MemMapConfig__unk_vector_path = value

    unk_vector_path = property(_get_unk_vector_path, _set_unk_vector_path)

    def _get_initial_memmap_size(self):
        return self._MemMapConfig__initial_memmap_size

    def _set_initial_memmap_size(self, value):
        if not isinstance(value, int):
            raise TypeError('initialMemmapSize must be int')
        self._MemMapConfig__initial_memmap_size = value

    initial_memmap_size = property(_get_initial_memmap_size, _set_initial_memmap_size)

    def _get_work_space_name(self):
        return self._MemMapConfig__work_space_name

    def _set_work_space_name(self, value):
        if not isinstance(value, str):
            raise TypeError('workSpaceName must be str')
        self._MemMapConfig__work_space_name = value

    work_space_name = property(_get_work_space_name, _set_work_space_name)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._MemMapConfig__array_path is not None:
            d['arrayPath'] = self._MemMapConfig__array_path.as_dict() if hasattr(self._MemMapConfig__array_path, 'as_dict') else self._MemMapConfig__array_path
        if self._MemMapConfig__unk_vector_path is not None:
            d['unkVectorPath'] = self._MemMapConfig__unk_vector_path.as_dict() if hasattr(self._MemMapConfig__unk_vector_path, 'as_dict') else self._MemMapConfig__unk_vector_path
        if self._MemMapConfig__initial_memmap_size is not None:
            d['initialMemmapSize'] = self._MemMapConfig__initial_memmap_size.as_dict() if hasattr(self._MemMapConfig__initial_memmap_size, 'as_dict') else self._MemMapConfig__initial_memmap_size
        if self._MemMapConfig__work_space_name is not None:
            d['workSpaceName'] = self._MemMapConfig__work_space_name.as_dict() if hasattr(self._MemMapConfig__work_space_name, 'as_dict') else self._MemMapConfig__work_space_name
        return d


class InferenceConfiguration(object):
    __doc__ = 'InferenceConfiguration\n\n    This configuration object brings together all properties to serve a set of\n    pipeline steps for inference.\n\n    :param steps: list of konduit.PipelineStep\n    :param serving_config: a konduit.ServingConfig\n    :param mem_map_config: a konduit.MemMapConfig\n    '
    _types_map = {'steps':{'type':list, 
      'subtype':PipelineStep}, 
     'servingConfig':{'type':ServingConfig, 
      'subtype':None}, 
     'memMapConfig':{'type':MemMapConfig, 
      'subtype':None}}
    _formats_map = {'steps': 'table'}

    def __init__(self, steps=None, serving_config=None, mem_map_config=None):
        self._InferenceConfiguration__steps = steps
        self._InferenceConfiguration__serving_config = serving_config
        self._InferenceConfiguration__mem_map_config = mem_map_config

    def _get_steps(self):
        return self._InferenceConfiguration__steps

    def _set_steps(self, value):
        if not isinstance(value, list):
            if not isinstance(value, ListWrapper):
                raise TypeError('steps must be list')
        if not all((isinstance(i, PipelineStep) for i in value)):
            raise TypeError('steps list valeus must be PipelineStep')
        self._InferenceConfiguration__steps = value

    steps = property(_get_steps, _set_steps)

    def _get_serving_config(self):
        return self._InferenceConfiguration__serving_config

    def _set_serving_config(self, value):
        if not isinstance(value, ServingConfig):
            raise TypeError('servingConfig must be ServingConfig')
        self._InferenceConfiguration__serving_config = value

    serving_config = property(_get_serving_config, _set_serving_config)

    def _get_mem_map_config(self):
        return self._InferenceConfiguration__mem_map_config

    def _set_mem_map_config(self, value):
        if not isinstance(value, MemMapConfig):
            raise TypeError('memMapConfig must be MemMapConfig')
        self._InferenceConfiguration__mem_map_config = value

    mem_map_config = property(_get_mem_map_config, _set_mem_map_config)

    def as_dict(self):
        d = empty_type_dict(self)
        if self._InferenceConfiguration__steps is not None:
            d['steps'] = [p.as_dict() if hasattr(p, 'as_dict') else p for p in self._InferenceConfiguration__steps]
        if self._InferenceConfiguration__serving_config is not None:
            d['servingConfig'] = self._InferenceConfiguration__serving_config.as_dict() if hasattr(self._InferenceConfiguration__serving_config, 'as_dict') else self._InferenceConfiguration__serving_config
        if self._InferenceConfiguration__mem_map_config is not None:
            d['memMapConfig'] = self._InferenceConfiguration__mem_map_config.as_dict() if hasattr(self._InferenceConfiguration__mem_map_config, 'as_dict') else self._InferenceConfiguration__mem_map_config
        return d