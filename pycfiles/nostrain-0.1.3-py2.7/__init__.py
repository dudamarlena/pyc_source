# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/nostrain/__init__.py
# Compiled at: 2014-02-17 14:57:29
import os.path

def sphinx_theme_path():
    """Use this method in conf.py

        html_theme = 'nostrain'
        import nostrain
        html_theme_path = [nostrain.sphinx_theme_path()]
    """
    root = os.path.dirname(__file__)
    return os.path.join(root, 'sphinx')