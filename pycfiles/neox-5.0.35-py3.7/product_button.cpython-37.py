# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/product_button.py
# Compiled at: 2019-10-26 09:38:40
# Size of source mod 2**32: 1419 bytes
import os
from pathlib import Path
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
css_small = 'product_button_small.css'
css_high = 'product_button_hd.css'
root_dir = str(Path(__file__).parent.parent)
__all__ = [
 'ProductButton']

class ProductButton(QPushButton):

    def __init__(self, parent, id, text_up, text_bottom, method, target, size='small'):
        super(ProductButton, self).__init__()
        self.id = id
        styles = []
        if size == 'small':
            css_file_screen = css_small
        else:
            css_file_screen = css_high
        css_file = os.path.join(root_dir, 'css', css_file_screen)
        with open(css_file, 'r') as (infile):
            styles.append(infile.read())
        self.setStyleSheet(''.join(styles))
        self.setObjectName('product_button')
        if len(text_up) > 29:
            text_up = text_up[0:29]
        label1 = QLabel(text_up, self)
        label1.setWordWrap(True)
        label1.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        label1.setObjectName('product_label_up')
        label2 = QLabel(text_bottom, self)
        label2.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        label2.setObjectName('product_label_bottom')
        method = getattr(parent, method)
        if target:
            method = partial(method, target)
        self.clicked.connect(method)