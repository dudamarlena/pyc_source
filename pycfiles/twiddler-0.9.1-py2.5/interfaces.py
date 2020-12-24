# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/interfaces.py
# Compiled at: 2008-07-24 14:48:01
from zope.interface import Interface, Attribute

class IConfigurableComponent(Interface):

    def configureForm():
        """
        This should return a lump of html containing form definitions
        and the like to be inserted into a <form> tag on the Configure
        tab.

        The <form> tag and 'Save Changes' button will already be
        generated.
        """
        pass

    def configure(form):
        """
        This should use information from the supplied form to
        configure this object.

        'form' is a dictionary equivalent to REQUEST.form
        """
        pass


class IInputFactory(Interface):

    def __call__():
        """
        Returns an object implementing twiddler.interfaces.IInput
        """
        pass


class IExecutorFactory(Interface):

    def __call__():
        """
        Returns an object implementing twiddler.interfaces.IExecutor
        """
        pass


class IOutputFactory(Interface):

    def __call__():
        """
        Returns an object implementing twiddler.interfaces.IOutput
        """
        pass


class IFilterFactory(Interface):

    def __call__():
        """
        Returns an object implementing twiddler.interfaces.IFilter
        """
        pass