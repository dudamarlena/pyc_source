# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/__init__.py
# Compiled at: 2014-11-03 07:40:40
# Size of source mod 2**32: 999 bytes
"""beehive is behaviour-driven development, Python style

Behavior-driven development (or BDD) is an agile software development
technique that encourages collaboration between developers, QA and
non-technical or business participants in a software project.

*beehive* uses tests written in a natural language style, backed up by Python
code.

To get started, we recommend the `tutorial`_ and then the `test language`_ and
`api`_ references.

.. _`tutorial`: tutorial.html
.. _`test language`: gherkin.html
.. _`api`: api.html
"""
__version__ = '1.0'
import sys
from beehive.step_registry import given, when, then, step, Given, When, Then, Step
from beehive.matchers import use_step_matcher, step_matcher, register_type
__step_names = (
 given, when, then, step, Given, When, Then, Step)
__all__ = __step_names + (use_step_matcher, step_matcher, register_type)
if 'behave' not in sys.modules:
    sys.modules['behave'] = sys.modules['beehive']