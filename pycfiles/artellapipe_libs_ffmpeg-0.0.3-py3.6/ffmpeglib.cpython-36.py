# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/ffmpeg/core/ffmpeglib.py
# Compiled at: 2020-05-02 23:49:33
# Size of source mod 2**32: 6530 bytes
"""
Utility module that contains useful utilities and classes related with FFMpeg
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, fileseq, logging, ffmpeg
from ffmpeg import nodes
from tpDcc.libs.python import python, path as path_utils
from artellapipe.libs import ffmpeg as ffmpeg_lib
LOGGER = logging.getLogger()

def launch_stream(ffmpeg_stream, overwrite=True):
    """
    Executes all the FFMpeg operations of the given FFMpeg stream
    :param ffmpeg_stream: ffmpeg.nodes.Stream
    :param overwrite: bool
    """
    if not ffmpeg_stream:
        LOGGER.warning('Given FFMpeg stream to store is not valid! Aborting stream launch operation ...')
        return
    ffmpeg_executable = ffmpeg_lib.get_ffmpeg_executable()
    if not ffmpeg_executable or not os.path.isfile(ffmpeg_executable):
        return
    ffmpeg.run(ffmpeg_stream, cmd=ffmpeg_executable, overwrite_output=overwrite, quiet=True)


def get_file_input--- This code section failed: ---

 L.  54         0  LOAD_FAST                'input_file'
                2  POP_JUMP_IF_FALSE    66  'to 66'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'input_file'
                8  LOAD_GLOBAL              str
               10  LOAD_GLOBAL              unicode
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    66  'to 66'

 L.  55        18  LOAD_FAST                'check_file_path'
               20  POP_JUMP_IF_FALSE    50  'to 50'

 L.  56        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                path
               26  LOAD_ATTR                isfile
               28  LOAD_FAST                'input_file'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  POP_JUMP_IF_FALSE    64  'to 64'

 L.  57        34  LOAD_GLOBAL              ffmpeg
               36  LOAD_ATTR                input
               38  LOAD_FAST                'input_file'
               40  BUILD_TUPLE_1         1 
               42  LOAD_FAST                'kwargs'
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  RETURN_VALUE     
             48_0  COME_FROM            32  '32'
               48  JUMP_ABSOLUTE        98  'to 98'
               50  ELSE                     '64'

 L.  59        50  LOAD_GLOBAL              ffmpeg
               52  LOAD_ATTR                input
               54  LOAD_FAST                'input_file'
               56  BUILD_TUPLE_1         1 
               58  LOAD_FAST                'kwargs'
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  RETURN_VALUE     
               64  JUMP_FORWARD         98  'to 98'
             66_0  COME_FROM             2  '2'

 L.  60        66  LOAD_GLOBAL              isinstance
               68  LOAD_FAST                'input_file'
               70  LOAD_GLOBAL              nodes
               72  LOAD_ATTR                FilterableStream
               74  CALL_FUNCTION_2       2  '2 positional arguments'
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L.  61        78  LOAD_FAST                'input_file'
               80  RETURN_END_IF    
             82_0  COME_FROM            76  '76'

 L.  63        82  LOAD_GLOBAL              LOGGER
               84  LOAD_ATTR                warning
               86  LOAD_STR                 'Given video file "{}" is not valid!'
               88  LOAD_ATTR                format
               90  LOAD_FAST                'input_file'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  POP_TOP          
             98_0  COME_FROM            64  '64'

Parse error at or near `POP_TOP' instruction at offset 96


def save_to_file(ffmpeg_stream, output_path, run_stream=False, overwrite=True):
    """
    Stores given FFMpeg stream object into given output path
    :param ffmpeg_stream: ffmpeg.nodes.Stream
    :param output_path: str
    :param run_stream: bool
    :param overwrite: bool
    """
    if not ffmpeg_stream:
        LOGGER.warning('Given FFMpeg stream to store is not valid! Aborting stream store operation ...')
        return
    save = ffmpeg.output(ffmpeg_stream, output_path, loglevel='quiet')
    if not run_stream:
        return save
    launch_stream(save, overwrite=overwrite)


def draw_text(input_file, text, x=0, y=0, font_color=None, font_file=None, font_size=16, escape_text=False):
    input_file = get_file_input(input_file)
    if not font_color:
        font_color = 'white'
    new_text = ffmpeg.drawtext(input_file,
      text, x=x, y=y, fontcolor=font_color, fontfile=font_file, fontsize=font_size, escape_text=escape_text)
    return new_text


def overlay_inputs(input_1, input_2, x=0, y=0):
    """
    Function that overlays input_1 on top of input_2
    :param input_1: str or ffmpeg.nodes.FilterableStream
    :param input_2: str or ffmpeg.nodes.FilterableStream
    :param x: int
    :param y: int
    :return: ffmpeg.nodes.FilterableStream
    """
    stream_1 = get_file_input(input_1)
    stream_2 = get_file_input(input_2)
    if not stream_1 or not stream_2:
        return False
    else:
        overlay = ffmpeg.overlay(stream_1, stream_2, x=x, y=y)
        return overlay


def draw_timestamp_on_video(video_file, text=None, x=0, y=0, font_color=None, font_file=None, font_size=16, escape_text=False, timecode='00:00:00:00', timecode_rate=24):
    input_file = get_file_input(video_file)
    if not font_color:
        font_color = 'white'
    if text is None:
        text = ''
    draw_text = ffmpeg.drawtext(input_file,
      text, timecode=timecode, x=x, y=y, fontcolor=font_color, fontfile=font_file, fontsize=font_size, escape_text=escape_text,
      timecode_rate=timecode_rate)
    return draw_text


def create_video_from_sequence_file(file_in_sequence, output_file, sequence_number_padding=2, framerate=24, video_codec='libx264', run_stream=True):
    if not file_in_sequence or not os.path.isfile(file_in_sequence):
        return
    sequence = fileseq.FileSequence(file_in_sequence)
    frame_fill = str(sequence.zfill()).zfill(sequence_number_padding)
    frame_file = sequence.frame('#')
    frame_file = path_utils.clean_path(frame_file.replace'.#.''.%{}d.'.format(frame_fill))
    sequence_input = get_file_input(frame_file,
      check_file_path=False, start_number=(sequence.start()), framerate=framerate)
    output = ffmpeg.output(sequence_input,
      output_file, vcodec=video_codec, framerate=framerate)
    if not run_stream:
        return output
    launch_stream(output)


def create_video_from_list_of_files(list_of_files, output_file, framerate=24, video_codec='libx264', run_stream=True):
    list_of_files = [get_file_input(input_file) for input_file in list_of_files]
    if not list_of_files:
        return
    concatenate = (ffmpeg.concat)(*list_of_files)
    output = ffmpeg.output(concatenate, output_file, vcodec=video_codec, framerate=framerate)
    if not run_stream:
        return output
    launch_stream(output)


def run_multiples_outputs_at_once(outputs_to_run, max_operations=15):
    """
    Run all the given outputs at once
    :param outputs_to_run: list
    :param max_operations: int
    :return:
    """
    operations_to_run = list()
    current_op = 0
    for op in outputs_to_run:
        operations_to_run.append(op)
        current_op += 1
        if current_op >= max_operations:
            merge = (ffmpeg.merge_outputs)(*operations_to_run)
            try:
                launch_stream(merge)
            except Exception as exc:
                for opt_to_run in operations_to_run:
                    launch_stream(opt_to_run)

            python.clear_list(operations_to_run)
            current_op = 0

    if operations_to_run:
        merge = (ffmpeg.merge_outputs)(*operations_to_run)
        try:
            launch_stream(merge)
        except Exception as exc:
            for opt_to_run in operations_to_run:
                launch_stream(opt_to_run)


def scale_video(video_file, new_width=None, new_height=None):
    if new_width is None and new_height is None:
        LOGGER.warning('Impossible to scale video because no given new dimensiones are valid!')
        return False
    else:
        video_input = get_file_input(video_file)
        if not video_input:
            return False
        scale = ffmpeg.filter(video_input, 'scale', width=new_width, height=new_height)
        return scale