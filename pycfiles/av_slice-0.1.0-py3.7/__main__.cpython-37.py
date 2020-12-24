# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/av_slice/__main__.py
# Compiled at: 2019-06-11 23:51:07
# Size of source mod 2**32: 1033 bytes
from moviepy import editor
import click
from av_slice.audio import quiet_sections
from av_slice.video import remove_sections

@click.command()
@click.option('--output_file', default='', help='filename of output')
@click.argument('file')
@click.option('--threshold', default=0.01, help='threshold under which to make a cut')
def _video_silence(file, output_file, threshold):
    if output_file == '':
        n, *ext = file.split('.')
        output_file = f"{n}_modified.{'.'.join(ext)}"
    click.echo(f"saving result to {output_file}")
    click.echo('calculating removals...')
    inpt = editor.VideoFileClip(file)
    cuts = quiet_sections((inpt.audio), (int(inpt.audio.fps / inpt.fps)), threshold=threshold)
    click.echo(f"making {len(cuts)} cuts")
    final = remove_sections(inpt, cuts)
    final.write_videofile(output_file)


_video_silence()