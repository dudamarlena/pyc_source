# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/custom_button.py
# Compiled at: 2019-10-26 09:37:45
# Size of source mod 2**32: 3171 bytes
import os
from pathlib import Path
from functools import partial
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QSizePolicy
root_dir = Path(__file__).parent.parent
root_dir = str(root_dir)
css_screens = {'small':'flat_button_small.css', 
 'medium':'flat_button_medium.css', 
 'large':'flat_button_large.css'}
__all__ = [
 'CustomButton']

class CustomButton(QPushButton):

    def __init__(self, parent, id, icon=None, title=None, desc=None, method=None, target=None, size='small', name_style='category_button'):
        """
            Create custom, responsive and nice button flat style,
            with two subsections
                 _ _ _ _ _
                |  ICON   |   -> Title / Icon (Up section)
                |  DESC   |   -> Descriptor section (Optional - bottom section)
                |_ _ _ _ _|

            :id :: Id of button,
            :icon:: A QSvgRenderer object,
            :title :: Name of button,
            :descriptor:: Text name or descriptor of button,
            :method:: Method for connect to clicked signal if it missing '*_pressed'
                will be used instead.
            :target:: ?
            :name_style:: define which type of button style must be rendered.
        """
        super(CustomButton, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        qsize = QSize(50, 50)
        if name_style == 'toolbar_button':
            qsize = QSize(35, 35)
        else:
            self.id = id
            styles = []
            css_file = os.path.join(root_dir, 'css', css_screens[size])
            with open(css_file, 'r') as (infile):
                styles.append(infile.read())
            self.setStyleSheet(''.join(styles))
            self.setObjectName(name_style)
            rows = []
            if icon:
                if not desc:
                    self.setIcon(icon)
                    self.setIconSize(qsize)
                else:
                    pixmap = icon.pixmap(qsize)
                    label_icon = QLabel()
                    label_icon.setObjectName('label_icon')
                    label_icon.setPixmap(pixmap)
                    label_icon.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
                    rows.append(label_icon)
        if title:
            if len(desc) > 29:
                desc = desc[0:29]
            label_title = QLabel(title)
            label_title.setWordWrap(True)
            label_title.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
            label_title.setObjectName('label_title')
            rows.append(label_title)
        if desc:
            if len(desc) > 29:
                desc = desc[0:29]
            label_desc = QLabel(desc, self)
            label_desc.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
            label_desc.setObjectName('label_desc')
            rows.append(label_desc)
        if len(rows) > 1:
            vbox = QVBoxLayout()
            for w in rows:
                vbox.addWidget(w)

            self.setLayout(vbox)
        method = getattr(parent, method)
        if target:
            method = partial(method, target)
        self.clicked.connect(method)