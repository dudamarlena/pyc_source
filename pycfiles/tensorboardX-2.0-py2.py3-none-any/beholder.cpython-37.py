# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dexter/git/tensorboardX/tensorboardX/beholder/beholder.py
# Compiled at: 2019-08-01 11:57:19
# Size of source mod 2**32: 8355 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from proto.summary_pb2 import Summary
from proto.summary_pb2 import SummaryMetadata
from proto.tensor_pb2 import TensorProto
from proto.tensor_shape_pb2 import TensorShapeProto
import os, time, numpy as np
from .file_system_tools import read_pickle, write_pickle, write_file
from .shared_config import PLUGIN_NAME, TAG_NAME, SUMMARY_FILENAME, DEFAULT_CONFIG, CONFIG_FILENAME, SUMMARY_COLLECTION_KEY_NAME, SECTION_INFO_FILENAME
from . import video_writing

class Beholder(object):

    def __init__(self, logdir):
        self.PLUGIN_LOGDIR = logdir + '/plugins/' + PLUGIN_NAME
        self.is_recording = False
        self.video_writer = video_writing.VideoWriter((self.PLUGIN_LOGDIR),
          outputs=[
         video_writing.FFmpegVideoOutput, video_writing.PNGVideoOutput])
        self.last_image_shape = []
        self.last_update_time = time.time()
        self.config_last_modified_time = -1
        self.previous_config = dict(DEFAULT_CONFIG)
        if not os.path.exists(self.PLUGIN_LOGDIR + '/config.pkl'):
            os.makedirs(self.PLUGIN_LOGDIR)
            write_pickle(DEFAULT_CONFIG, '{}/{}'.format(self.PLUGIN_LOGDIR, CONFIG_FILENAME))

    def _get_config(self):
        """Reads the config file from disk or creates a new one."""
        filename = '{}/{}'.format(self.PLUGIN_LOGDIR, CONFIG_FILENAME)
        modified_time = os.path.getmtime(filename)
        if modified_time != self.config_last_modified_time:
            config = read_pickle(filename, default=(self.previous_config))
            self.previous_config = config
        else:
            config = self.previous_config
        self.config_last_modified_time = modified_time
        return config

    def _write_summary(self, frame):
        """Writes the frame to disk as a tensor summary."""
        path = '{}/{}'.format(self.PLUGIN_LOGDIR, SUMMARY_FILENAME)
        smd = SummaryMetadata()
        tensor = TensorProto(dtype='DT_FLOAT',
          float_val=(frame.reshape(-1).tolist()),
          tensor_shape=TensorShapeProto(dim=[
         TensorShapeProto.Dim(size=(frame.shape[0])),
         TensorShapeProto.Dim(size=(frame.shape[1])),
         TensorShapeProto.Dim(size=(frame.shape[2]))]))
        summary = Summary(value=[
         Summary.Value(tag=TAG_NAME,
           metadata=smd,
           tensor=tensor)]).SerializeToString()
        write_file(summary, path)

    @staticmethod
    def stats(tensor_and_name):
        imgstats = []
        for img, name in tensor_and_name:
            immax = img.max()
            immin = img.min()
            imgstats.append({'height':img.shape[0], 
             'max':str(immax), 
             'mean':str(img.mean()), 
             'min':str(immin), 
             'name':name, 
             'range':str(immax - immin), 
             'shape':str((img.shape[1], img.shape[2]))})

        return imgstats

    def _get_final_image(self, config, trainable=None, arrays=None, frame=None):
        if config['values'] == 'frames':
            final_image = frame
        else:
            if config['values'] == 'arrays':
                final_image = np.concatenate([arr for arr, _ in arrays])
                stat = self.stats(arrays)
                write_pickle(stat, '{}/{}'.format(self.PLUGIN_LOGDIR, SECTION_INFO_FILENAME))
            else:
                if config['values'] == 'trainable_variables':
                    final_image = np.concatenate([arr for arr, _ in trainable])
                    stat = self.stats(trainable)
                    write_pickle(stat, '{}/{}'.format(self.PLUGIN_LOGDIR, SECTION_INFO_FILENAME))
        if len(final_image.shape) == 2:
            final_image = np.expand_dims(final_image, -1)
        return final_image

    def _enough_time_has_passed(self, FPS):
        """For limiting how often frames are computed."""
        if FPS == 0:
            return False
        earliest_time = self.last_update_time + 1.0 / FPS
        return time.time() >= earliest_time

    def _update_frame(self, trainable, arrays, frame, config):
        final_image = self._get_final_image(config, trainable, arrays, frame)
        self._write_summary(final_image)
        self.last_image_shape = final_image.shape
        return final_image

    def _update_recording(self, frame, config):
        """Adds a frame to the current video output."""
        should_record = config['is_recording']
        if should_record:
            if not self.is_recording:
                self.is_recording = True
                print('Starting recording using %s', self.video_writer.current_output().name())
            self.video_writer.write_frame(frame)
        else:
            if self.is_recording:
                self.is_recording = False
                self.video_writer.finish()
                print('Finished recording')

    def update(self, trainable=None, arrays=None, frame=None):
        """Creates a frame and writes it to disk.

        Args:
            trainable: a list of namedtuple (tensors, name).
            arrays: a list of namedtuple (tensors, name).
            frame: lalala
        """
        new_config = self._get_config()
        if True or self._enough_time_has_passed(self.previous_config['FPS']):
            self.last_update_time = time.time()
            final_image = self._update_frame(trainable, arrays, frame, new_config)
            self._update_recording(final_image, new_config)


class BeholderHook:
    pass