# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dojo\_base.py
# Compiled at: 2013-06-09 05:52:53
__doc__ = ' Functionality that formally was contained in the base dojo/dojo module.\n\nThe dojo/_base directory contains modules with basic functionality, such as \narray operations. Typically, if a function or class exists within the dojo \nnamespace directly (e.g. dojo.forEach()) then it is defined in dojo/_base\n\nThe dojo/_base files will be maintained until the 2.0 release.\n\n'
from pyojo.js.code import Code
from mixins import ArrayMixin

class Dojo(Code):
    """ Base class for Dojo javascript parts.
    
        The require list allows to Require and Define to know what to ask to
        the AMD loader. 
    """
    loc = ''
    function = ''
    require = []

    def requires(self, *args):
        """ Require this AMD module too.
        """
        if getattr(self, '_require', None) is None:
            self._require = []
        for module in args:
            self._require.append(module)

        return self

    def get_requires(self):
        return self.require + getattr(self, '_require', [])


class kernel(object):
    """ The bootstrap kernel that generates the dojo namespace.
    """


class config(object):
    """ Configures Dojo and loads the default platform configuration.
    
    To override certain global settings that control how the framework 
    operates.
    """


class loader(object):
    """ The legacy and AMD module loader for Dojo.
    """


class lang(Dojo):
    """ Contains functions for supporting Polymorphism and other language 
    constructs that are fundemental to the rest of the toolkit.
    """
    require = [
     'dojo/_base/lang']


class declare(Dojo):
    """ JavaScript uses prototype-based inheritance, not class-based 
    inheritance (which is used by most programming languages).
    """
    require = [
     'dojo/_base/declare']


class array(Dojo, ArrayMixin):
    """ A bunch of useful methods to deal with arrays.
    """
    require = [
     'dojo/_base/array']


class window(object):
    """Use the window, document, and document.body global variables, 
      or equivalent variables for the frame that you want to operate on.
    """


class Color(Dojo):
    """ A unified way to store RGBA colors.
    """
    require = [
     'dojo/_base/Color']


class fx(Dojo):
    """ The legacy and AMD module loader for Dojo.
    """
    require = [
     'dojo/_base/fx']

    def animateProperty(self):
        pass

    def fadeIn(self):
        pass

    def fadeOut(self):
        pass


class unload(object):
    """ Registers a function to be called when the page unloads.
    """

    def addOnUnload(self):
        pass

    def addOnWindowUnload(self):
        pass