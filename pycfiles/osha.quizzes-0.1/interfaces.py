# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/osha.quizzes/src/osha/quizzes/interfaces.py
# Compiled at: 2012-10-19 05:44:19
"""Module where all interfaces, events and exceptions live."""
from Products.PloneFormGen.interfaces.actionAdapter import IPloneFormGenActionAdapter

class IPFGCorrectAnswersAdapter(IPloneFormGenActionAdapter):
    """Calculate the percentage of correct answers"""
    pass