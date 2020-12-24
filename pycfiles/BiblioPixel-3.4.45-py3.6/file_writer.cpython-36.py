# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/image/file_writer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1303 bytes
import importlib, itertools, os, tempfile
MODULE = '.'.join(__name__.split('.')[:-1])
COLORS_PER_LINE = 12
SUFFIXES = ('.directory', '.gif', '.mp4', '.yml')

def file_writer(movie_writer):
    suffix = movie_writer.suffix or '.directory'
    if suffix not in SUFFIXES:
        raise ValueError('Cannot write %s files' % suffix)
    module = importlib.import_module(MODULE + suffix)
    return module.Writer(movie_writer)


class FileWriter:
    __doc__ = 'Base for classes that write a specific type of movie file'

    def __init__(self, writer):
        self.writer = writer
        self.frame_files = []
        if self.writer.gif_dir:
            self.gif_dir = self.writer.gif_dir
            os.makedirs((self.gif_dir), exist_ok=True)
        else:
            self.tmp_holder = tempfile.TemporaryDirectory()
            self.gif_dir = self.tmp_holder.name

    def step(self):
        frame_name = '%s%04d.png' % (self.writer.basename, self.writer.frame)
        filename = os.path.join(self.gif_dir, frame_name)
        self.writer.render().save(filename)
        self.frame_files.append(filename)

    def write(self):
        fps = self.writer.scaled_fps
        ff, self.frame_files = self.frame_files, []
        if ff:
            (self._write)((self.writer.filename), ff, fps, **(self.writer).options)