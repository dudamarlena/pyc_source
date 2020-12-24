# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/error_explainer/colon_statements.py
# Compiled at: 2020-04-06 02:33:21
# Size of source mod 2**32: 473 bytes
"""
Map of statements tha are followed by a colon and their parso node counterparts
"""
import parso
colon_statements = {'if':parso.python.tree.IfStmt, 
 'try':parso.python.tree.TryStmt, 
 'while':parso.python.tree.WhileStmt, 
 'for':parso.python.tree.ForStmt, 
 'def':parso.python.tree.Function, 
 'class':parso.python.tree.Class, 
 'with':parso.python.tree.WithStmt, 
 'else':parso.python.tree.IfStmt, 
 'elif':parso.python.tree.IfStmt}