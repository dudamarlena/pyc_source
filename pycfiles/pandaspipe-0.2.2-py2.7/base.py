# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pandaspipe/base.py
# Compiled at: 2016-04-07 04:27:16
import abc, logging
_log = logging.getLogger(__name__)
__all__ = [
 'PipelineEntity', 'PipelineUnsupportedOperation']

class PipelineEntity:
    """
    Test
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.env = {}
        self.priority = None
        self.type = 'node'
        self.input_channels = []
        self.output_channels = []
        self.external_dependencies = []
        return

    @abc.abstractmethod
    def register(self, pipeline):
        """
        Test
        :param pipeline:
        :return:
        """
        pass


class PipelineUnsupportedOperation(Exception):
    """
    Test
    """
    pass