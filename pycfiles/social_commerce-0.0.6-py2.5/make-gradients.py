# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/media/make-gradients.py
# Compiled at: 2009-10-31 23:19:40
import sys
sys.path.append('../utils')
from gradient import *
write_png('heading.png', 1, 80, gradient([
 (
  1.0, (0, 17, 51), (0, 85, 119))]))
write_png('form-shadow.png', 1, 25, gradient([
 (
  0.33, (221, 221, 221), (243, 243, 243)),
 (
  1.0, (243, 243, 243), (243, 243, 243))]))