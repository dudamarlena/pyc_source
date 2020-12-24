# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autolabel/cli.py
# Compiled at: 2020-04-03 05:01:17
# Size of source mod 2**32: 1212 bytes
import sys
from itertools import chain
from pathlib import Path
import click
from more_itertools import grouper
from .classifier import classifier

@click.command()
@click.argument('images', type=(click.Path()), nargs=(-1))
@click.option('--batch-size', default=1, type=(click.INT))
@click.option('--sep', default=' ', help='Separator')
@click.option('--top', default=1)
@click.option('--output', '-o', help='Output file', type=(click.File('w')))
@click.option('--model', '-m', type=(click.Choice(classifier.keys())), default='resnet50')
def main(images, batch_size, sep, top, output, model):
    from .image import ImageListDataset
    if not sys.stdin.isatty():
        stdin_iter = (Path(x.rstrip('\n')) for x in click.get_text_stream('stdin').readlines())
        iterator = chain(stdin_iter, images)
    else:
        iterator = images
    c = classifier[model]()
    for im_paths in grouper(iterator, batch_size):
        dataset = ImageListDataset(im_paths)
        res = c.predict(dataset, top=top)
        for p, decoded in res.items():
            for label in decoded:
                s = (
                 p, label[0], label[1])
                print((sep.join(map(str, s))), file=output)