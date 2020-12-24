# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\pjjoyce\dropbox\02. james' files\56. lcopt_cv\lcopt_cv\lcopt_cv\bin\lcopt_cv_gui.py
# Compiled at: 2018-02-19 09:00:46
# Size of source mod 2**32: 429 bytes
from lcopt_cv.gui import ImageGui

def main():
    """ to add controls to the gui, import the default controls and use:
        
        controls = list(DEFAULT_CONTROLS)
        controls.append({'name': 'useless', 'type': 'checkbox', 'label': 'A useless checkbox', 'data': {'value': False}})
    
        app = ImageGui(controls=controls)
    """
    app = ImageGui()
    app.run()