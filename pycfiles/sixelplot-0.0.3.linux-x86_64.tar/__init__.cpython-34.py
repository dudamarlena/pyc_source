# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kikutake/.pyenv/versions/3.4.4/lib/python3.4/site-packages/sixelplot/__init__.py
# Compiled at: 2016-05-27 01:49:49
# Size of source mod 2**32: 246 bytes
import matplotlib, matplotlib.pyplot as plt, sixel, sys, io

def show(output=sys.stdout):
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    writer = sixel.SixelWriter()
    writer.draw(buf, output=output)