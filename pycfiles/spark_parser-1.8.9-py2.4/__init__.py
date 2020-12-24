# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spark_parser/__init__.py
# Compiled at: 2017-02-25 04:47:06
import sys
from spark_parser.version import VERSION
__version__ = 'SPARK-%s Python2 and Python3 compatible' % VERSION
__docformat__ = 'restructuredtext'
PYTHON3 = sys.version_info >= (3, 0)
from spark_parser.ast import AST
from spark_parser.ast import GenericASTTraversal
from spark_parser.ast import GenericASTTraversalPruningException
from spark_parser.spark import DEFAULT_DEBUG
from spark_parser.spark import GenericParser
from spark_parser.spark import GenericASTBuilder
from spark_parser.scanner import GenericScanner
from spark_parser.scanner import GenericToken