# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\substitutions\factory.py
# Compiled at: 2016-09-29 05:35:35
# Size of source mod 2**32: 1819 bytes
from flap.substitutions.commons import FileWrapper
from flap.substitutions.misc import EndInput
from flap.substitutions.comments import CommentsRemover
from flap.substitutions.files import Input, SubFileExtractor, SubFile, Include, IncludeOnly
from flap.substitutions.graphics import GraphicsPath, IncludeGraphics, IncludeSVG, Overpic
from flap.substitutions.bibliography import Bibliography

class ProcessorFactory:
    __doc__ = '\n    Create chains of processors\n    '

    @staticmethod
    def chain(proxy, source, processors):
        pipeline = source
        for eachProcessor in processors:
            pipeline = eachProcessor(pipeline, proxy)

        return pipeline

    def input_merger(self, file, proxy):
        return ProcessorFactory.chain(proxy, CommentsRemover(FileWrapper(file)), [
         SubFileExtractor, SubFile, Input, EndInput])

    def flap_pipeline(self, proxy, file):
        return ProcessorFactory.chain(proxy, self.input_merger(file, proxy), [
         Include, IncludeOnly, GraphicsPath, IncludeGraphics, IncludeSVG, Overpic, Bibliography])