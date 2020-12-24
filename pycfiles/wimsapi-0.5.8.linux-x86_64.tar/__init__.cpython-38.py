# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/wimsapi/__init__.py
# Compiled at: 2020-05-04 16:09:45
# Size of source mod 2**32: 387 bytes
from .api import WimsAPI
from .exam import Exam
from .exceptions import AdmRawError, InvalidItemTypeError, InvalidResponseError, NotSavedError, WimsAPIError
from .score import ExamScore, ExerciseScore, SheetScore
from .sheet import Sheet
from .user import User
from .wclass import Class
name = 'wimsapi'
__title__ = 'wimsapi'
__version__ = VERSION = '0.5.8'