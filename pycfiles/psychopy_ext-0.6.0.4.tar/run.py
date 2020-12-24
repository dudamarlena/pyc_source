# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Dropbox\experiments\psychopy_ext\psychopy_ext\demos\run.py
# Compiled at: 2013-12-12 11:17:53
import sys
try:
    import psychopy_ext
except:
    try:
        sys.path.insert(0, '../psychopy_ext')
        import psychopy_ext
    except:
        sys.path.insert(0, '../../')

from psychopy_ext import ui
__author__ = 'Jonas Kubilius'
__version__ = '0.1'
exp_choices = [
 ui.Choices('scripts.trivial', name='Quick demo'),
 ui.Choices('scripts.main', name='Simple exp.', alias='main', order=['exp', 'analysis']),
 ui.Choices('scripts.twotasks', name='Two tasks', order=['exp', 'analysis']),
 ui.Choices('scripts.staircase', name='Staircase', order=['exp', 'analysis']),
 ui.Choices('scripts.perclearn', name='Advanced', order=['exp', 'analysis']),
 ui.Choices('scripts.mouse_resp', name='Mouse responses', order=['exp', 'analysis']),
 ui.Choices('scripts.fmri', name='fMRI')]
ui.Control(exp_choices, title='Demo Project', size=(560, 550))