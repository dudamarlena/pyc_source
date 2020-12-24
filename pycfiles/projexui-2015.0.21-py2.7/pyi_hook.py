# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/pyi_hook.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' Defines the hook required for the PyInstaller to use projex with it. '
import os, projex.pyi
hiddenimports, datas = projex.pyi.collect(os.path.dirname(__file__))
hiddenimports.append('smtplib')