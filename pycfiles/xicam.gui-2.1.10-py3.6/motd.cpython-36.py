# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\widgets\motd.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 3269 bytes
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from xicam.gui.static import path

class MOTD(QScrollArea):

    def __init__(self, parent=None):
        super(MOTD, self).__init__()
        text = f"""\n        <div align='center'>\n           <br />\n           <br />\n           <img src='{path('images/camera.jpg')}\' width=\'200\'/>\n           <h1 style=\'font-family:Zero Threes;\'>\n               Welcome to Xi-cam\n           </h1>\n           <br />\n           Please cite Xi-cam in published work: <br />\n           Pandolfi, R., Kumar, D., Venkatakrishnan, S., Krishnan, H., Hexemer, A.\n           (under preparation)\n    \n        </div>\n        \n        <table cellspacing="10"><tr><td>\n            Ronald J. Pandolfi<sup>a</sup><br />\n            Daniel B. Allan<sup>e</sup> <br />\n            Elke Arenholz<sup>a</sup> <br />\n            Luis Barroso-Luque<sup>a</sup><br />\n            Stuart I. Campbell<sup>e</sup><br />\n            Thomas A. Caswell<sup>e</sup><br />\n            Austin Blair<sup>a</sup><br />\n            Francesco De Carlo<sup>c</sup><br />\n            Sean Fackler<sup>a</sup><br />\n            Amanda P. Fournier<sup>b</sup><br />\n            Guillaume Freychet<sup>a</sup><br />\n            Masafumi Fukuto<sup>e</sup><br />\n            Dŏga G̈ursoy<sup>ch</sup><br />\n            Zhang Jiang<sup>c</sup><br />\n            Harinarayan Krishnan<sup>a</sup><br />\n            Dinesh Kumar<sup>a</sup><br />\n            R. Joseph Kline<sup>g</sup><br />\n            Ruipeng Li<sup>e</sup><br />\n            Christopher Liman<sup>g</sup><br />\n        </td><td>\n            Stefano Marchesini<sup>a</sup><br />\n            Apurva Mehta<sup>b</sup><br />\n            Alpha T. N’Diaye<sup>a</sup><br />\n            Dilworth (Dula) Y. Parkinson<sup>a</sup><br />\n            Holden Parks<sup>a</sup><br />\n            Lenson A. Pellouchoud<sup>a</sup><br />\n            Talita Perciano<sup>a</sup><br />\n            Fang Ren<sup>b</sup><br />\n            Shreya Sahoo<sup>a</sup><br />\n            Joseph Strzalka<sup>c</sup><br />\n            Daniel Sunday<sup>g</sup><br />\n            Christopher J. Tassone<sup>a</sup><br />\n            Daniela Ushizima<sup>a</sup><br />\n            Singanallur Venkatakrishnan<sup>d</sup><br />\n            Kevin G. Yager<sup>f</sup><br />\n            James A. Sethian<sup>a</sup><br />\n            Alexander Hexemer<sup>a</sup>\n        </td><td>\n            <sup>a</sup>Lawrence Berkeley National Laboratory<br />\n            <sup>b</sup>Stanford Synchrotron Radiation Lightsource<br />\n            <sup>c</sup>Advanced Photon Source, Argonne National Laboratory<br />\n            <sup>d</sup>Oak Ridge National Laboratory<br />\n            <sup>e</sup>National Synchrotron Light Source II<br />\n            <sup>f</sup>Center for Functional Nanomaterials<br />\n            <sup>g</sup>National Institute of Standards and Technology<br />\n            <sup>h</sup>Department of Electrical Engineering<br />and Computer Science, Northwestern University<br />\n        </td></tr></table>\n        \n        """
        label = QLabel()
        label.setText(text)
        self.setWidget(label)