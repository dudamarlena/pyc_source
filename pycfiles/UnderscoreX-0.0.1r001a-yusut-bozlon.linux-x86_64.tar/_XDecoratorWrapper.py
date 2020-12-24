# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/UnderscoreX/_XDecoratorWrapper.py
# Compiled at: 2012-09-10 22:34:33
__DOC__ = '\n_XDecoratorWrapper.py\n\n  DecoratorClass used to parse **Kargs and handle Warning and exception thru Missing Attribute by adding\n  @_XDecoratorWrapper.Kargs2AttrPreException and creatinf a function having this decorator being called:\n  @_XDecoratorWrapper.ObjectClassRaiser( ObjectAttributeHolder , ExceptionClass )\n\n\n### see the example:\n\n### This example assuming having following module being available  :\n### ------------------------------------------------\n### from optparse import OptionParser\n### import sets\n### from sets import Set\n### \n### ------------------------------------------------\n\nGeneric Exception class model:\n\nWe need 2 Class to store attribute:\n\nclass ObjectGenericWarningHolder( object ):\n\n  def __init__( self ):\n    print "Add Current Object Attribute %s" % self.__class__.__name__\n\nclass ObjectGenericAttrHolder( object ):\n\n  def __init__( self ):\n    print "Add Current Object Attribute %s" % self.__class__.__name__\n\n\nWe Need a Generic Exception class like this one.\n\n\nclass ExceptionGenericAttrMissing( Exception ):\n  \n  msg                             =\'__GENERIC_EXCEPTION_MESSAGES__\'\n  AttrCurrentExceptionHandled     = None\n  HadDecoderTypeList              = False \n\n  def __Init__Attr( self , value ):\n    self.AttrCurrentExceptionHandled = value\n    DictListTemplateKey="%sList" % ( value )\n    IsListTemplateKey="Had%sList" % ( value )\n    if hasattr( self, IsListTemplateKey  ):\n      if getattr( self, IsListTemplateKey ) == True:\n        Exception.__init__( self, self.MsgDict[DictListTemplateKey] % ( self.AttrCurrentExceptionHandled ,\n                                                                        getattr( self, DictListTemplateKey ) ) )\n      else:\n        Exception.__init__( self, self.MsgDict[self.AttrCurrentExceptionHandled]  % ( self.AttrCurrentExceptionHandled ) )\n    \n\n  @_XDecoratorWrapper.Kargs2Attr( ObjectWarningHolder )\n  def __init__( self, **Kargs ):\n    if hasattr( self, \'ListAttrFuncAccess\' ):\n      print "Available message for following Attr:[ %s ]" % ( self.ListAttrFuncAccess ) \n    self.RaisedExceptionByAttr = False\n    for ExceptionByAttr in self.ListAttrFuncAccess:\n      if hasattr( self, ExceptionByAttr ):\n        self.RaisedExceptionByAttr = True\n        getattr( self, "__Init__Attr")( ExceptionByAttr )\n\n\nMain class:\n\nclass GenericTest( object ):\n\n  MsgDict = {\n    \'AppsName\'        :\'Internal Value AppsName not used, You should at least Specified an AppsName Value.\',\n    \'ActionHelper\'    :\'Internal Value ActionHelper not used, You should at least Specified an ActionHelper Value.\',\n    \'HelperSwitch\'    :\'Internal Value HelperSwitch not used, You should at least Specified an HelperSwitch Value.\',\n  }  \n\n  OptionListDiscovery=list()\n  TempOptionList=list()\n  ErrorHandler = iterpipes.CalledProcessError\n\n  ListAttrFuncAccess        = [ \'AppsName\', \'ActionHelper\', \'HelperSwitch\' ]\n  parser = OptionParser()\n\n  def __start_cmdline_parser__( self ):\n    \n    self.parser.add_option("-A", "--AppsName",\n                      dest="StrAppsName",\n                      help="Add AppsName in your Class")\n    self.parser.add_option("-J", "--ActionHelper",\n                      dest="StrActionHelper",\n                      help="Add ActionHelper in your Class")\n    self.parser.add_option("-S", "--HelperSwitch",\n                      dest="StrHelperSwitch",\n                      help="Add HelperSwitch in your Class ")\n\n\n  @_XDecoratorWrapper.Kargs2AttrPreException( ObjectIterAppsFilter )\n  def __init__( self , **Kargs ):\n    self.__start_cmdline_parser__()\n    (self.options, self.args ) = self.parser.parse_args() \n    self.ErrorRaiser( )\n### ...\n\n\n  @_XDecoratorWrapper.ObjectClassRaiser( ObjectGenericAttrHolder , ExceptionGenericAttrMissing )\n  def ErrorRaiser( self ):\n    print "Inspecting Missing Attribute."\n\n\n\n### Some Instantiation statement:\n\nif __name__.__eq__( \'__main__\' ):\n  _XDecoratorWrapper.ErrorClassReceivedAttrListName = \'ListAttrFuncAccess\'\n  ExceptionGenericAttrMissing.ListAttrFuncAccess    = ItertAppsFilter.ListAttrFuncAccess\n  ExceptionGenericAttrMissing.MsgDict               = ItertAppsFilter.MsgDict\n\nAnd We have Correct basic model of Attribute filtering thru the **kargs and will raise any Warning or exception\nupon definition of your class inside the Object Raiser inside _XDecoratorWrapper :\n--------\n@_XDecoratorWrapper.ObjectClassRaiser( __ANY_EXCEPTION_OR_WARNING_OBJECT__ , ExceptionGenericAttrMissing )\ndef ErrorRaiser( self ):\n pass \n--------\n'
import sys, os, re, cStringIO, time, datetime, iterpipes
try:
    from iterpipes import cmd, bincmd, linecmd, run, call, check_call, cmdformat, compose
except ImportError:
    from iterpipes import cmd, bincmd, linecmd, run, call, check_call, compose

try:
    getcontext().prec = 36
except NameError:
    import decimal
    from decimal import *
    getcontext().prec = 36

try:
    ThisSetTest = Set(['1', '2', '3'])
except NameError:
    import sets
    from sets import Set

class _XDecoratorWrapper:
    DisplayKargs2AttrItemAdded = False
    DictAttrRefferal = 'DictAttrAdd'
    DictAttrRefferalType = list
    DictAttrRefferalAdd = 'append'
    ErrorClassReceivedAttrList = None
    ErrorClassReceivedAttrListName = None

    @staticmethod
    def Kargs2AttrPreException(ClassTinyDecl):
        """
    This Decorator Will:
     Read the *args key but do not consume it or affect any variable at this times . 
     Reaf **kwargs key and add it to current Object-class ClassTinyDecl under current
     name readed from **kwargs key name. 
            
    """

        def decorator(func):

            def inner(*args, **kwargs):
                AttrContainer = getattr(AttributeGenerationDecor, 'DictAttrRefferalType')()
                setattr(ClassTinyDecl, AttributeGenerationDecor.DictAttrRefferal, AttrContainer)
                for ItemName in kwargs.keys():
                    if AttributeGenerationDecor.DisplayKargs2AttrItemAdded == True:
                        print 'Processing Key, value : < %s, "%s" >' % (ItemName, kwargs[ItemName])
                    setattr(ClassTinyDecl, ItemName, kwargs[ItemName])
                    getattr(getattr(ClassTinyDecl, AttributeGenerationDecor.DictAttrRefferal), AttributeGenerationDecor.DictAttrRefferalAdd)(ItemName)

                func(*args, **kwargs)

            return inner

        return decorator

    @staticmethod
    def Kargs2Attr(ClassTinyDecl):
        """
    This Decorator Will:
     Read the *args key but do not consume it or affect any variable at this times . 
     Reaf **kwargs key and add it to current Object-class ClassTinyDecl under current
     name readed from **kwargs key name. 
            
    """

        def decorator(func):

            def inner(*args, **kwargs):
                for ItemName in kwargs.keys():
                    if AttributeGenerationDecor.DisplayKargs2AttrItemAdded == True:
                        print 'Processing Key %s, Value: %s' % (ItemName, kwargs[ItemName])
                    setattr(ClassTinyDecl, ItemName, kwargs[ItemName])

                func(*args, **kwargs)

            return inner

        return decorator

    @staticmethod
    def LoopClassFunc(TransportClass, MainClass, FuncList):
        """
    This Decorator Will:
     Read the *args key but do not consume it or affect any variable at this times . 
     Reaf **kwargs key and add it to current Object-class ClassTinyDecl under current
     name readed from **kwargs key name. 
            
    """

        def decorator(func):

            def inner():
                for FuncNameExec in getattr(TransportClass, FuncList):
                    getattr(eval(MainClass), FuncNameExec)()

                func()

            return inner

        return decorator

    @staticmethod
    def ObjectClassRaiser(ClassTinyDecl, ErrorClass):
        """
    This Decorator Will:
     Read the *args key but do not consume it or affect any variable at this times . 
     Reaf **kwargs key and add it to current Object-class ClassTinyDecl under current
     name readed from **kwargs key name. 
            
    """

        def decorator(func):

            def inner(*args):
                func(*args)
                AttrSetListParsed = Set(getattr(ClassTinyDecl, AttributeGenerationDecor.DictAttrRefferal))
                AttrSetMainList = Set(getattr(ErrorClass, AttributeGenerationDecor.ErrorClassReceivedAttrListName))
                MissingAttrSet = AttrSetMainList.difference(AttrSetListParsed)
                try:
                    AttrRaiseName = MissingAttrSet.pop()
                    raise ErrorClass(AttrRaiseName)
                except KeyError:
                    pass

            return inner

        return decorator


class ObjectGenericWarningHolder(object):

    def __init__(self):
        print 'Add Current Object Attribute %s' % self.__class__.__name__


class ObjectGenericAttrHolder(object):

    def __init__(self):
        print 'Add Current Object Attribute %s' % self.__class__.__name__


class ExceptionGenericAttrMissing(Exception):
    msg = '__GENERIC_EXCEPTION_MESSAGES__'
    AttrCurrentExceptionHandled = None
    HadDecoderTypeList = False

    def __Init__Attr(self, value):
        self.AttrCurrentExceptionHandled = value
        DictListTemplateKey = '%sList' % value
        IsListTemplateKey = 'Had%sList' % value
        if hasattr(self, IsListTemplateKey):
            if getattr(self, IsListTemplateKey) == True:
                Exception.__init__(self, self.MsgDict[DictListTemplateKey] % (self.AttrCurrentExceptionHandled,
                 getattr(self, DictListTemplateKey)))
            else:
                Exception.__init__(self, self.MsgDict[self.AttrCurrentExceptionHandled] % self.AttrCurrentExceptionHandled)

    @_XDecoratorWrapper.Kargs2Attr(ObjectGenericWarningHolder)
    def __init__(self, **Kargs):
        if hasattr(self, 'ListAttrFuncAccess'):
            print 'Available message for following Attr:[ %s ]' % self.ListAttrFuncAccess
        self.RaisedExceptionByAttr = False
        for ExceptionByAttr in self.ListAttrFuncAccess:
            if hasattr(self, ExceptionByAttr):
                self.RaisedExceptionByAttr = True
                getattr(self, '__Init__Attr')(ExceptionByAttr)