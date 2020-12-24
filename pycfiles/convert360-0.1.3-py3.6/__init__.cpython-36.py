# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/convert360/__init__.py
# Compiled at: 2017-06-24 15:17:18
# Size of source mod 2**32: 1150 bytes
import imageio
from tqdm import tqdm
from convert360.projector import get_projector

def render_many(renderer, reader, writer, total=None):
    for i, frame in tqdm((enumerate(reader)), total=total):
        img = renderer.render_to_image(frame)
        writer.append_data(img)


def render_single(renderer, reader, writer):
    frame = reader.get_data(0)
    img = renderer.render_to_image(frame)
    writer.append_data(img)


def main(input_path, output_path, size, input_type, output_type):
    output_size = (
     size[0] * 3, size[1] * 2)
    reader = imageio.get_reader(input_path)
    metadata = reader.get_meta_data()
    projector = get_projector(input_type, output_type)
    with projector(output_size) as (renderer):
        writer_args = {}
        frames = 1
        if 'fps' in metadata:
            writer_args['fps'] = metadata['fps']
            frames = metadata['nframes']
        with (imageio.get_writer)(output_path, **writer_args) as (writer):
            if frames > 1:
                render_many(renderer, reader, writer, frames)
            else:
                render_single(renderer, reader, writer)