# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/pixmaps/compile.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 588 bytes
import numpy as np
from PyQt4 import QtGui
import os, pickle, sys
path = os.path.abspath(os.path.split(__file__)[0])
pixmaps = {}
for f in os.listdir(path):
    if not f.endswith('.png'):
        continue
    print(f)
    img = QtGui.QImage(os.path.join(path, f))
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    arr = np.asarray(ptr).reshape(img.height(), img.width(), 4).transpose(1, 0, 2)
    pixmaps[f] = pickle.dumps(arr)

ver = sys.version_info[0]
fh = open(os.path.join(path, 'pixmapData_%d.py' % ver), 'w')
fh.write('import numpy as np; pixmapData=%s' % repr(pixmaps))