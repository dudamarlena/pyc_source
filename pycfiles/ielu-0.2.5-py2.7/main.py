# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ielu/main.py
# Compiled at: 2016-03-02 19:12:22
from traitsui.api import toolkit
from traits.trait_base import ETSConfig
from gselu import iEEGCoregistrationFrame
from utils import crash_if_freesurfer_is_not_sourced
import signal

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    crash_if_freesurfer_is_not_sourced()
    iEEGCoregistrationFrame().configure_traits()