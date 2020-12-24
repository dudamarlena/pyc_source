# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\daemon\process.py
# Compiled at: 2018-08-27 17:21:06
import pipeline, numpy as np, os
from PIL import Image
import string

def process(parent, files, experiment, options=dict(remesh=False, findcenter=False, refinecenter=False, cachethumbnail=False, variation=True, savefullres=False)):
    """
    Applies a series of processing steps to a list of files; outputs a nexus file containing all results
    """
    for f in files:
        path = os.path.join(parent, f)
        img, _ = pipeline.loader.loadpath(path)
        if img is not None:
            if options['findcenter']:
                cen = pipeline.center_approx.center_approx(img)
                experiment.setvalue('Center X', cen[0])
                experiment.setvalue('Center Y', cen[1])
            if options['refinecenter']:
                pipeline.center_approx.refinecenter(img, experiment)
            thumb = None
            if options['cachethumbnail']:
                thumb = pipeline.writer.thumbnail(img)
            if options['remesh']:
                img = pipeline.remesh.remesh(img, path, experiment.getGeometry())
            variation = None
            if options['variation']:
                prevpath = pipeline.pathtools.similarframe(path, -1)
                nextpath = pipeline.pathtools.similarframe(path, +1)
                if prevpath is not None and nextpath is not None:
                    variation = pipeline.variation.filevariation(1, prevpath, img, nextpath)
                else:
                    variation = None
            if img is None:
                return
            if not options['savefullres']:
                img = None
            pipeline.writer.writenexus(img, thumb, pipeline.pathtools.path2nexus(path), path, variation)

    return