# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/web/wsgi.py
# Compiled at: 2015-09-05 21:24:22
"""dossier.web.wsgi

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

This is a WSGI compatible Python script that can be used to make
``dossier.web`` run with WSGI servers like ``gunicorn`` and ``uwsgi``.
"""
from dossier.web.run import default_app
_, application = default_app()