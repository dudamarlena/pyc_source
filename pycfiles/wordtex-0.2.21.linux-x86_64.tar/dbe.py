# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/dbe.py
# Compiled at: 2013-11-12 16:48:22
"""
  This modules makes it so that any importing module will go to pdb on exception
  rather than going to nothing.  Title stands for
  "DeBug on Exception:, naming convention similar to pdb (python debugger)

  Thanks to: Lennart Regebro at
 <http://stackoverflow.com/questions/5515940/trying-to-implement-import-debug-mode-module/5517696#5517696>
"""
import sys, pdb

def except_hook(exctype, value, traceback):
    if previous_except_hook:
        previous_except_hook(exctype, value, traceback)
    pdb.post_mortem(traceback)


previous_except_hook = sys.excepthook
sys.excepthook = except_hook