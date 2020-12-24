# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autofunccli/__init__.py
# Compiled at: 2020-05-04 16:20:57
# Size of source mod 2**32: 319 bytes
from .analysis import FunctionArgParser as cmdfunc
from .analysis import UnsupportedTypeException
from .analysis import WrongInputTypeException
from .analysis import NonHomogenousEnumTypeException
from .analysis import EnumHasNoTypeException
from .analysis import IsNotAFunctionException
from .cmdclass import cmdfusion