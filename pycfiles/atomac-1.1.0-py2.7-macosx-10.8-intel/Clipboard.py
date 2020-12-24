# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/Clipboard.py
# Compiled at: 2012-08-03 19:46:40
import types, AppKit, pprint, logging, Foundation

class Clipboard(object):
    """ Class to represent clipboard-related operations for text """
    utf8encoding = Foundation.NSUTF8StringEncoding
    STRING = AppKit.NSStringPboardType
    RTF = AppKit.NSRTFPboardType
    IMAGE = AppKit.NSTIFFPboardType
    URL = AppKit.NSURLPboardType
    COLOR = AppKit.NSColorPboardType

    @classmethod
    def paste(cls):
        """ Method to get the clipboard data ('Paste')

          Returns: Data (string) retrieved or None if empty.  Exceptions from
          AppKit will be handled by caller.
      """
        data = None
        pb = AppKit.NSPasteboard.generalPasteboard()
        data = pb.stringForType_(cls.STRING)
        return data

    @classmethod
    def copy(cls, data):
        """ Method to set the clipboard data ('Copy')

          Parameters: data to set (string)
          Optional: datatype if it's not a string
          Returns: True / False on successful copy, Any exception raised (like
                   passes the NSPasteboardCommunicationError) should be caught
                   by the caller.
      """
        pp = pprint.PrettyPrinter()
        copyData = 'Data to copy (put in pasteboard): %s'
        logging.debug(copyData % pp.pformat(data))
        cleared = cls.clearAll()
        if not cleared:
            logging.warning('Clipboard could not clear properly')
            return False
        if type(data) is not types.ListType:
            data = [
             data]
        pb = AppKit.NSPasteboard.generalPasteboard()
        pbSetOk = pb.writeObjects_(data)
        return bool(pbSetOk)

    @classmethod
    def clearContents(cls):
        """ Clear contents of general pasteboard

          Future enhancement can include specifying which clipboard to clear
          Returns: True on success; caller should expect to catch exceptions,
                   probably from AppKit (ValueError)
      """
        logMsg = 'Request to clear contents of pasteboard: general'
        logging.debug(logMsg)
        pb = AppKit.NSPasteboard.generalPasteboard()
        pb.clearContents()
        return True

    @classmethod
    def clearProperties(cls):
        """ Clear properties of general pasteboard

          Future enhancement can include specifying which clipboard's properties
          to clear
          Returns: True on success; caller should catch exceptions raised,
                   e.g. from AppKit (ValueError)
      """
        logMsg = 'Request to clear properties of pasteboard: general'
        logging.debug(logMsg)
        pb = AppKit.NSPasteboard.generalPasteboard()
        pb.clearProperties()
        return True

    @classmethod
    def clearAll(cls):
        """ Clear contents and properties of general pasteboard

          Future enhancement can include specifying which clipboard's properties
          to clear
          Returns: Boolean True on success; caller should handle exceptions
      """
        contentsCleared = cls.clearContents()
        propsCleared = cls.clearProperties()
        return True

    @classmethod
    def isEmpty(cls, datatype=None):
        """ Method to test if the general pasteboard is empty or not with respect
          to the type of object you want

          Parameters: datatype (defaults to strings)
          Returns: Boolean True (empty) / False (has contents); Raises
                   exception (passes any raised up)
      """
        if not datatype:
            datatype = AppKit.NSString
        if type(datatype) is not types.ListType:
            datatype = [
             datatype]
        pp = pprint.PrettyPrinter()
        logging.debug('Desired datatypes: %s' % pp.pformat(datatype))
        optDict = {}
        logging.debug('Results filter is: %s' % pp.pformat(optDict))
        try:
            logMsg = 'Request to verify pasteboard is empty'
            logging.debug(logMsg)
            pb = AppKit.NSPasteboard.generalPasteboard()
            itsEmpty = not bool(pb.canReadObjectForClasses_options_(datatype, optDict))
        except ValueError as error:
            logging.error(error)
            raise

        return bool(itsEmpty)