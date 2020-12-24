# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/dashboard.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import webbrowser
from catalyze import cli, config

@cli.command('dashboard')
def dashboard():
    """Open the Catalyze dashboard in your browser"""
    webbrowser.open(config.dashboard_url)