# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/interfaces/project.py
# Compiled at: 2010-03-14 14:30:45
"""
all interfaces about project.
"""
from zope.interface import Interface
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'
__docformat__ = 'plaintext'

class IPPMProject(Interface):
    """
    defines the interfaces for a project. empty for now.
    """
    __module__ = __name__


class IPPMStory(Interface):
    """
    the interface for a story.
    """
    __module__ = __name__


class IPPMIteration(Interface):
    """
    the marker interface for a interation.
    """
    __module__ = __name__


class IPPMMetadata(Interface):
    """
    the marker interace for a metadata
    """
    __module__ = __name__


class IPPMUseCase(Interface):
    """
    the marker interace for a use case
    """
    __module__ = __name__