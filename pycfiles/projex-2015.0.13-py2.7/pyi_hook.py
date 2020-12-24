# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/pyi_hook.py
# Compiled at: 2016-07-03 23:28:12
""" Defines the hook required for the PyInstaller to use projex with it. """
import os, projex.pyi
hiddenimports, datas = projex.pyi.collect(os.path.dirname(__file__))
hiddenimports.append('smtplib')