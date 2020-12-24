# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/plotbox/movie.py
# Compiled at: 2015-12-03 12:20:33
import numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib.patches as patches, matplotlib.path as path, matplotlib.animation as animation
from tempfile import NamedTemporaryFile
from IPython.display import HTML

def to_html(anim, fps=15):
    """
    Given a matplotlib FuncAnimation object, returns a movie clip of the animation embedded in HTML. To be used when running iPython Notebook with pylab inline.

    Parameters
    ----------
    anim : matplotlib FuncAnimation object
            animation object storing all frames of the movie

    Returns
    -------
    html : HTML object
            returns animation as a movie clip embedded in HTML

    """
    plt.close(anim._fig)
    VIDEO_TAG = '<video controls> <source src="data:video/x-m4v;base64,{0}" type="video/mp4"> \n    Your browser does not support the video tag. </video>'
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix='.mp4') as (f):
            anim.save(f.name, fps=fps, extra_args=['-vcodec', 'libx264'])
            video = open(f.name, 'rb').read()
        anim._encoded_video = video.encode('base64')
    return HTML(VIDEO_TAG.format(anim._encoded_video))