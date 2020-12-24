# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/modeling/hyperparams/base_config.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 11663 bytes
"""Base configurations to standardize experiments."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy, functools
from typing import Any, List, Mapping, Optional, Type
import dataclasses, tensorflow as tf, yaml
from official.modeling.hyperparams import params_dict

@dataclasses.dataclass
class Config(params_dict.ParamsDict):
    __doc__ = "The base configuration class that supports YAML/JSON based overrides.\n\n  * It recursively enforces a whitelist of basic types and container types, so\n    it avoids surprises with copy and reuse caused by unanticipated types.\n  * It converts dict to Config even within sequences,\n    e.g. for config = Config({'key': [([{'a': 42}],)]),\n         type(config.key[0][0][0]) is Config rather than dict.\n  "
    IMMUTABLE_TYPES = (
     str, int, float, bool, type(None))
    SEQUENCE_TYPES = (
     list, tuple)
    default_params = None
    default_params: dataclasses.InitVar[Optional[Mapping[(str, Any)]]]
    restrictions = None
    restrictions: dataclasses.InitVar[Optional[List[str]]]

    @classmethod
    def _isvalidsequence(cls, v):
        """Check if the input values are valid sequences.

    Args:
      v: Input sequence.

    Returns:
      True if the sequence is valid. Valid sequence includes the sequence
      type in cls.SEQUENCE_TYPES and element type is in cls.IMMUTABLE_TYPES or
      is dict or ParamsDict.
    """
        if not isinstance(v, cls.SEQUENCE_TYPES):
            return False
        return all((isinstance(e, cls.IMMUTABLE_TYPES) for e in v)) or all((isinstance(e, dict) for e in v)) or all((isinstance(e, params_dict.ParamsDict) for e in v))

    @classmethod
    def _import_config(cls, v, subconfig_type):
        """Returns v with dicts converted to Configs, recursively."""
        if not issubclass(subconfig_type, params_dict.ParamsDict):
            raise TypeError('Subconfig_type should be subclass of ParamsDict, found {!r}'.format(subconfig_type))
        if isinstance(v, cls.IMMUTABLE_TYPES):
            return v
        if isinstance(v, cls.SEQUENCE_TYPES):
            if not cls._isvalidsequence(v):
                raise TypeError('Invalid sequence: only supports single level {!r} of {!r} or dict or ParamsDict found: {!r}'.format(cls.SEQUENCE_TYPES, cls.IMMUTABLE_TYPES, v))
            import_fn = functools.partial((cls._import_config),
              subconfig_type=subconfig_type)
            return type(v)(map(import_fn, v))
        if isinstance(v, params_dict.ParamsDict):
            return copy.deepcopy(v)
        if isinstance(v, dict):
            return subconfig_type(v)
        raise TypeError('Unknown type: {!r}'.format(type(v)))

    @classmethod
    def _export_config(cls, v):
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, cls.IMMUTABLE_TYPES):
            return v
        elif isinstance(v, cls.SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
            if isinstance(v, params_dict.ParamsDict):
                return v.as_dict()
            if isinstance(v, dict):
                raise TypeError('dict value not supported in converting.')
        else:
            raise TypeError('Unknown type: {!r}'.format(type(v)))

    @classmethod
    def _get_subconfig_type(cls, k) -> Type[params_dict.ParamsDict]:
        """Get element type by the field name.

    Args:
      k: the key/name of the field.

    Returns:
      Config as default. If a type annotation is found for `k`,
      1) returns the type of the annotation if it is subtype of ParamsDict;
      2) returns the element type if the annotation of `k` is List[SubType]
         or Tuple[SubType].
    """
        subconfig_type = Config
        if k in cls.__annotations__:
            type_annotation = cls.__annotations__[k]
            if isinstance(type_annotation, type) and issubclass(type_annotation, Config):
                subconfig_type = cls.__annotations__[k]
            else:
                field_type = getattr(type_annotation, '__origin__', type(None))
                if isinstance(field_type, type):
                    if issubclass(field_type, cls.SEQUENCE_TYPES):
                        element_type = getattr(type_annotation, '__args__', [type(None)])[0]
                        subconfig_type = element_type if issubclass(element_type, params_dict.ParamsDict) else subconfig_type
        return subconfig_type

    def __post_init__(self, default_params, restrictions, *args, **kwargs):
        (super().__init__)(args, default_params=default_params, restrictions=restrictions, **kwargs)

    def _set(self, k, v):
        """Overrides same method in ParamsDict.

    Also called by ParamsDict methods.

    Args:
      k: key to set.
      v: value.

    Raises:
      RuntimeError
    """
        subconfig_type = self._get_subconfig_type(k)
        if isinstance(v, dict):
            if not k not in self.__dict__:
                self.__dict__[k] = self.__dict__[k] or subconfig_type(v)
            else:
                self.__dict__[k].override(v)
        else:
            self.__dict__[k] = self._import_config(v, subconfig_type)

    def __setattr__(self, k, v):
        if k not in self.RESERVED_ATTR:
            if getattr(self, '_locked', False):
                raise ValueError('The Config has been locked. No change is allowed.')
        self._set(k, v)

    def _override(self, override_dict, is_strict=True):
        """Overrides same method in ParamsDict.

    Also called by ParamsDict methods.

    Args:
      override_dict: dictionary to write to .
      is_strict: If True, not allows to add new keys.

    Raises:
      KeyError: overriding reserved keys or keys not exist (is_strict=True).
    """
        for k, v in sorted(override_dict.items()):
            if k in self.RESERVED_ATTR:
                raise KeyError('The key {!r} is internally reserved. Can not be overridden.'.format(k))
            else:
                if k not in self.__dict__:
                    if is_strict:
                        raise KeyError('The key {!r} does not exist in {!r}. To extend the existing keys, use `override` with `is_strict` = False.'.format(k, type(self)))
                    else:
                        self._set(k, v)
            if isinstance(v, dict) and self.__dict__[k]:
                self.__dict__[k]._override(v, is_strict)
            elif isinstance(v, params_dict.ParamsDict) and self.__dict__[k]:
                self.__dict__[k]._override(v.as_dict(), is_strict)
            else:
                self._set(k, v)

    def as_dict(self):
        """Returns a dict representation of params_dict.ParamsDict.

    For the nested params_dict.ParamsDict, a nested dict will be returned.
    """
        return {k:self._export_config(v) for k, v in self.__dict__.items() if k not in self.RESERVED_ATTR}

    def replace(self, **kwargs):
        """Like `override`, but returns a copy with the current config unchanged."""
        params = self.__class__(self)
        params.override(kwargs, is_strict=True)
        return params

    @classmethod
    def from_yaml(cls, file_path: str):
        with tf.io.gfile.GFile(file_path, 'r') as (f):
            loaded = yaml.load(f)
            config = cls()
            config.override(loaded)
            return config

    @classmethod
    def from_json(cls, file_path: str):
        """Wrapper for `from_yaml`."""
        return cls.from_yaml(file_path)

    @classmethod
    def from_args(cls, *args, **kwargs):
        """Builds a config from the given list of arguments."""
        attributes = list(cls.__annotations__.keys())
        default_params = {a:p for a, p in zip(attributes, args)}
        default_params.update(kwargs)
        return cls(default_params)


@dataclasses.dataclass
class RuntimeConfig(Config):
    __doc__ = "High-level configurations for Runtime.\n\n  These include parameters that are not directly related to the experiment,\n  e.g. directories, accelerator type, etc.\n\n  Attributes:\n    distribution_strategy: e.g. 'mirrored', 'tpu', etc.\n    enable_xla: Whether or not to enable XLA.\n    per_gpu_thread_count: thread count per GPU.\n    gpu_threads_enabled: Whether or not GPU threads are enabled.\n    gpu_thread_mode: Whether and how the GPU device uses its own threadpool.\n    dataset_num_private_threads: Number of threads for a private threadpool\n      created for all datasets computation.\n    tpu: The address of the TPU to use, if any.\n    num_gpus: The number of GPUs to use, if any.\n    worker_hosts: comma-separated list of worker ip:port pairs for running\n      multi-worker models with DistributionStrategy.\n    task_index: If multi-worker training, the task index of this worker.\n    all_reduce_alg: Defines the algorithm for performing all-reduce.\n    num_packs: Sets `num_packs` in the cross device ops used in\n      MirroredStrategy.  For details, see tf.distribute.NcclAllReduce.\n    loss_scale: The type of loss scale. This is used when setting the mixed\n      precision policy.\n    run_eagerly: Whether or not to run the experiment eagerly.\n\n  "
    distribution_strategy = 'mirrored'
    distribution_strategy: str
    enable_xla = False
    enable_xla: bool
    gpu_threads_enabled = False
    gpu_threads_enabled: bool
    gpu_thread_mode = None
    gpu_thread_mode: Optional[str]
    dataset_num_private_threads = None
    dataset_num_private_threads: Optional[int]
    per_gpu_thread_count = 0
    per_gpu_thread_count: int
    tpu = None
    tpu: Optional[str]
    num_gpus = 0
    num_gpus: int
    worker_hosts = None
    worker_hosts: Optional[str]
    task_index = -1
    task_index: int
    all_reduce_alg = None
    all_reduce_alg: Optional[str]
    num_packs = 1
    num_packs: int
    loss_scale = None
    loss_scale: Optional[str]
    run_eagerly = False
    run_eagerly: bool


@dataclasses.dataclass
class TensorboardConfig(Config):
    __doc__ = 'Configuration for Tensorboard.\n\n  Attributes:\n    track_lr: Whether or not to track the learning rate in Tensorboard. Defaults\n      to True.\n    write_model_weights: Whether or not to write the model weights as\n      images in Tensorboard. Defaults to False.\n\n  '
    track_lr = True
    track_lr: bool
    write_model_weights = False
    write_model_weights: bool


@dataclasses.dataclass
class CallbacksConfig(Config):
    __doc__ = 'Configuration for Callbacks.\n\n  Attributes:\n    enable_checkpoint_and_export: Whether or not to enable checkpoints as a\n      Callback. Defaults to True.\n    enable_tensorboard: Whether or not to enable Tensorboard as a Callback.\n      Defaults to True.\n    enable_time_history: Whether or not to enable TimeHistory Callbacks.\n      Defaults to True.\n\n  '
    enable_checkpoint_and_export = True
    enable_checkpoint_and_export: bool
    enable_tensorboard = True
    enable_tensorboard: bool
    enable_time_history = True
    enable_time_history: bool