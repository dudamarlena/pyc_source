# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPointer\MessageSource.py
# Compiled at: 2004-01-26 02:40:21
__doc__ = '\nXPointer error codes and messages\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft import TranslateMessage as _
from Ft.Xml.XPointer import XPtrException
g_errorMessages = {XPtrException.INTERNAL_ERROR: _('There is an internal bug in 4Suite. Please make a post to the 4Suite mailing list to report this error message to the developers. Include platform details and info about how to reproduce the error. Info about the mailing list is at http://lists.fourthought.com/mailman/listinfo/4suite. The error code to report is: %s'), XPtrException.SYNTAX_ERROR: _('Syntax error in XPointer expression: %s'), XPtrException.RESOURCE_ERROR: _('Invalid resource, or not well-formed XML: %s'), XPtrException.SUB_RESOURCE_ERROR: _('Expression does not locate a resource')}