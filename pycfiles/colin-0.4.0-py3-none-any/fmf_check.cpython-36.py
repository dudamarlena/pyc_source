# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/checks/fmf_check.py
# Compiled at: 2018-09-03 10:17:54
# Size of source mod 2**32: 2920 bytes
"""
Module with FMF abstract check class
"""
import logging, inspect, os
from .abstract_check import AbstractCheck
from ..fmf_extension import ExtendedTree
logger = logging.getLogger(__name__)

def receive_fmf_metadata(name, path, object_list=False):
    """
    search node identified by name fmfpath

    :param path: path to filesystem
    :param name: str - name as pattern to search - "/name" (prepended hierarchy item)
    :param object_list: bool, if true, return whole list of found items
    :return: Tree Object or list
    """
    output = {}
    fmf_tree = ExtendedTree(path)
    logger.debug('get FMF metadata for test (path:%s name=%s)', path, name)
    items = [x for x in fmf_tree.climb() if x.name.endswith('/' + name) if '@' not in x.name]
    if object_list:
        return items
    else:
        if len(items) == 1:
            output = items[0]
        else:
            if len(items) > 1:
                raise Exception('There is more FMF test metadata for item by name:{}({}) {}'.format(name, len(items), [x.name for x in items]))
            else:
                if not items:
                    raise Exception('Unable to get FMF metadata for: {}'.format(name))
        return output


class FMFAbstractCheck(AbstractCheck):
    __doc__ = '\n    Abstract class for checks and loading metadata from FMF format\n    '
    metadata = None
    name = None
    fmf_metadata_path = None

    def __init__(self):
        if not self.metadata:
            if not self.fmf_metadata_path:
                logger.info('setting self.fmf_metadata_path by class location. DO NOT use it in this way. Metadata are set in colin.core.loader (use proper path)')
                self.fmf_metadata_path = os.path.dirname(inspect.getfile(self.__class__))
            self.metadata = receive_fmf_metadata(name=(self.name), path=(self.fmf_metadata_path))
        master_class = super(FMFAbstractCheck, self)
        kwargs = {}
        try:
            args_names = [argument for argument in inspect.signature(master_class.__init__).parameters]
        except NameError:
            args_names = inspect.getargspec(master_class.__init__).args

        for arg in args_names:
            try:
                kwargs[arg] = self.metadata.data[arg]
            except KeyError:
                pass

        try:
            (master_class.__init__)(**kwargs)
        except TypeError as error:
            logger.debug('missing argument (%s) in FMF metadata key (%s): %s', error, self.metadata.name, self.metadata.data)