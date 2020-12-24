# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adversarials/core/config.py
# Compiled at: 2018-12-21 01:06:52
# Size of source mod 2**32: 6494 bytes
"""Configuration file for Adversarial package.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Software Engineer.
     Email: javafolabi@gmail.com | victor.afolabi@zephyrtel.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: config.py.py
     Created on 20 December, 2018 @ 07:07 PM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
import os, json, pickle, configparser
from abc import ABCMeta
from typing import Callable, Any
import yaml
from easydict import EasyDict
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__all__ = [
 'Config']

class Config(metaclass=ABCMeta):

    @staticmethod
    def from_yaml(file: str):
        """Load configuration from a YAML file.

        Args:
            file (str): A `.yml` or `.yaml` filename.

        Raises:
            AssertionError: File is not a YAML file.
            FileNotFoundError: `file` was not found.

        Returns:
            easydict.EasyDict: config dictionary object.
        """
        if not file.endswith('yaml'):
            if not file.endswith('yml'):
                raise AssertionError('File is not a YAML file.')
        if not os.path.isfile(file):
            raise FileNotFoundError('{} was not found'.format(file))
        with open(file, mode='r') as (f):
            cfg = EasyDict(yaml.load(f, Loader=Loader))
        return cfg

    @staticmethod
    def from_cfg(file: str, ext: str='cfg'):
        """Load configuration from an cfg file.

        Args:
            file (str): An cfg filename.
            ext (str, optional): Defaults to 'cfg'. Config file extension.

        Raises:
            AssertionError: File is not an `${ext}` file.
            FileNotFoundError: `file` was not found.

        Returns:
            easydict.EasyDict: config dictionary object.
        """
        assert file.endswith(ext), f"File is not a/an `{ext}` file."
        if not os.path.isfile(file):
            raise FileNotFoundError('{} was not found'.format(file))
        cfg = configparser.ConfigParser(dict_type=EasyDict)
        cfg.read(file)
        return cfg

    @staticmethod
    def from_json(file: str):
        """Load configuration from a json file.

        Args:
            file (str): A JSON filename.

        Raises:
            AssertionError: File is not a JSON file.
            FileNotFoundError: `file` was not found.

        Returns:
            easydict.EasyDict: config dictionary object.
        """
        assert file.endswith('json'), 'File is not a `JSON` file.'
        if not os.path.isfile(file):
            raise FileNotFoundError('{} was not found'.format(file))
        with open(file, mode='r') as (f):
            cfg = EasyDict(json.load(f))
        return cfg

    @staticmethod
    def to_yaml(cfg: EasyDict, file: str, **kwargs):
        """Save configuration object into a YAML file.

        Args:
            cfg (EasyDict): Configuration: as a dictionary instance.
            file (str): Path to write the configuration to.

        Keyword Args:
            Passed into `dumper`.

        Raises:
            AssertionError: `dumper` must be callable.
        """
        kwargs.setdefault('Dumper', Dumper)
        (Config._to_file)(cfg=cfg, file=file, dumper=yaml.dump, **kwargs)

    @staticmethod
    def to_json(cfg: EasyDict, file: str, **kwargs):
        """Save configuration object into a JSON file.

        Args:
            cfg (EasyDict): Configuration: as dictionary instance.
            file (str): Path to write the configuration to.

        Keyword Args:
            Passed into `dumper`.

        Raises:
            AssertionError: `dumper` must be callable.
        """
        (Config._to_file)(cfg=cfg, file=file, dumper=json.dump, **kwargs)

    @staticmethod
    def to_cfg(cfg: EasyDict, file: str, **kwargs):
        """Save configuration object into a cfg or ini file.

        Args:
            cfg (Any): Configuration: as dictionary instance.
            file (str): Path to write the configuration to.

        Keyword Args:
            Passed into `dumper`.
        """
        print(cfg, file, **kwargs)
        return NotImplemented

    @staticmethod
    def to_pickle(cfg: Any, file: str, **kwargs):
        """Save configuration object into a pickle file.

        Args:
            cfg (Any): Configuration: as dictionary instance.
            file (str): Path to write the configuration to.

        Keyword Args:
            Passed into `dumper`.

        Raises:
            AssertionError: `dumper` must be callable.
        """
        (Config._to_file)(cfg=cfg, file=file, dumper=pickle.dump, **kwargs)

    @staticmethod
    def _to_file(cfg: Any, file: str, dumper: Callable, **kwargs):
        """Save configuration object into a file as allowed by `dumper`.

        Args:
            cfg (Any): Configuration: as dictionary instance.
            file (str): Path to write the configuration to.
            dumper (Callable): Function/callable handler to save object to disk.

        Keyword Args:
            Passed into `dumper`.

        Raises:
            AssertionError: `dumper` must be callable.
        """
        assert callable(dumper), '`dumper` must be callable.'
        if not os.path.isdir(file):
            os.makedirs(file)
        with open(file, mode='wb', encoding='utf-8') as (f):
            dumper(cfg, f, **kwargs)