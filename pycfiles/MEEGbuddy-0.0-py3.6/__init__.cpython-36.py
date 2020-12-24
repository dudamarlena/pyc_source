# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/MEEGbuddy/__init__.py
# Compiled at: 2019-02-12 17:24:49
# Size of source mod 2**32: 281 bytes
""" MEEG Resources for MGH Division of Neurotherapeutics """
from .meeg import MEEGbuddy, Comparator, create_demi_events, loadMEEGbuddies
from . import pci
from .psd_multitaper_plot_tools import DraggableResizeableRectangle, ButtonClickProcessor
from .gif_combine import combine_gifs