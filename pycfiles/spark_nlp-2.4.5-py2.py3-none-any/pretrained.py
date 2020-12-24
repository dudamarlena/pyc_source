# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maziyar/Desktop/Work/JohnSnowLabs/spark-nlp/python/build/lib/sparknlp/pretrained.py
# Compiled at: 2020-02-26 05:14:58
import sparknlp.internal as _internal, threading, time
from pyspark.sql import DataFrame
from sparknlp.annotator import *
from sparknlp.base import LightPipeline
from pyspark.ml import PipelineModel

def printProgress(stop):
    states = [
     ' | ', ' / ', ' — ', ' \\ ']
    nextc = 0
    while True:
        sys.stdout.write(('\r[{}]').format(states[nextc]))
        sys.stdout.flush()
        time.sleep(2.5)
        nextc = nextc + 1 if nextc < 3 else 0
        if stop():
            sys.stdout.write(('\r[{}]').format('OK!'))
            sys.stdout.flush()
            break

    sys.stdout.write('\n')


class ResourceDownloader(object):

    @staticmethod
    def downloadModel(reader, name, language, remote_loc=None, j_dwn='PythonResourceDownloader'):
        print name + ' download started this may take some time.'
        file_size = _internal._GetResourceSize(name, language, remote_loc).apply()
        if file_size == '-1':
            print 'Can not find the model to download please check the name!'
        else:
            print 'Approximate size to download ' + file_size
            stop_threads = False
            t1 = threading.Thread(target=printProgress, args=(lambda : stop_threads,))
            t1.start()
            try:
                j_obj = _internal._DownloadModel(reader.name, name, language, remote_loc, j_dwn).apply()
            finally:
                stop_threads = True
                t1.join()

            return reader(classname=None, java_model=j_obj)
        return

    @staticmethod
    def downloadPipeline(name, language, remote_loc=None):
        print name + ' download started this may take some time.'
        file_size = _internal._GetResourceSize(name, language, remote_loc).apply()
        if file_size == '-1':
            print 'Can not find the model to download please check the name!'
        else:
            print 'Approx size to download ' + file_size
            stop_threads = False
            t1 = threading.Thread(target=printProgress, args=(lambda : stop_threads,))
            t1.start()
            try:
                j_obj = _internal._DownloadPipeline(name, language, remote_loc).apply()
                jmodel = PipelineModel._from_java(j_obj)
            finally:
                stop_threads = True
                t1.join()

            return jmodel

    @staticmethod
    def clearCache(name, language, remote_loc=None):
        _internal._ClearCache(name, language, remote_loc).apply()

    @staticmethod
    def showPublicModels():
        print 'test'
        _internal._ShowPublicModels().apply()

    @staticmethod
    def showPublicPipelines():
        _internal._ShowPublicPipelines().apply()

    @staticmethod
    def showUnCategorizedResources():
        _internal._ShowUnCategorizedResources().apply()


class PretrainedPipeline:

    def __init__(self, name, lang='en', remote_loc=None, parse_embeddings=False, disk_location=None):
        if not disk_location:
            self.model = ResourceDownloader().downloadPipeline(name, lang, remote_loc)
        else:
            self.model = PipelineModel.load(disk_location)
        self.light_model = LightPipeline(self.model, parse_embeddings)

    @staticmethod
    def from_disk(path, parse_embeddings=False):
        return PretrainedPipeline(None, None, None, parse_embeddings, path)

    def annotate(self, target, column=None):
        if type(target) is DataFrame:
            if not column:
                raise Exception('annotate() column arg needed when targeting a DataFrame')
            return self.model.transform(target.withColumnRenamed(column, 'text'))
        if type(target) is list or type(target) is str:
            pipeline = self.light_model
            return pipeline.annotate(target)
        raise Exception('target must be either a spark DataFrame, a list of strings or a string')

    def fullAnnotate(self, target, column=None):
        if type(target) is DataFrame:
            if not column:
                raise Exception('annotate() column arg needed when targeting a DataFrame')
            return self.model.transform(target.withColumnRenamed(column, 'text'))
        if type(target) is list or type(target) is str:
            pipeline = self.light_model
            return pipeline.fullAnnotate(target)
        raise Exception('target must be either a spark DataFrame, a list of strings or a string')

    def transform(self, data):
        return self.model.transform(data)