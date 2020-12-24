# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ui/DeepBrainSegUI_support.py
# Compiled at: 2019-11-11 08:44:12
# Size of source mod 2**32: 2189 bytes
import sys
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global progress_bar
    global selectedButton
    progress_bar = tk.IntVar()
    selectedButton = tk.StringVar()


def Aboutus():
    print('DeepBrainSeg1_support.Aboutus')
    sys.stdout.flush()


def AxialScroll(*args):
    print('DeepBrainSeg1_support.AxialScroll')
    sys.stdout.flush()


def CorronalScroll(*args):
    print('DeepBrainSeg1_support.CorronalScroll')
    sys.stdout.flush()


def FlairView():
    print('DeepBrainSeg1_support.FlairView')
    sys.stdout.flush()


def GetRadiomics():
    print('DeepBrainSeg1_support.GetRadiomics')
    sys.stdout.flush()


def Get_Segmentation():
    print('DeepBrainSeg1_support.Get_Segmentation')
    sys.stdout.flush()


def Load_Flair():
    print('DeepBrainSeg1_support.Load_Flair')
    sys.stdout.flush()


def Load_T1():
    print('DeepBrainSeg1_support.Load_T1')
    sys.stdout.flush()


def Load_T1ce():
    print('DeepBrainSeg1_support.Load_T1ce')
    sys.stdout.flush()


def Load_T2():
    print('DeepBrainSeg1_support.Load_T2')
    sys.stdout.flush()


def SagitalScroll(*args):
    print('DeepBrainSeg1_support.SagitalScroll')
    sys.stdout.flush()


def SegmentationOverlay():
    print('DeepBrainSeg1_support.SegmentationOverlay')
    sys.stdout.flush()


def T1View():
    print('DeepBrainSeg1_support.T1View')
    sys.stdout.flush()


def T1ceView():
    print('DeepBrainSeg1_support.T1ceView')
    sys.stdout.flush()


def T2View():
    print('DeepBrainSeg1_support.T2View')
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global root
    global top_level
    global w
    w = gui
    top_level = top
    root = top


def destroy_window():
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import DeepBrainSeg
    DeepBrainSeg.vp_start_gui()