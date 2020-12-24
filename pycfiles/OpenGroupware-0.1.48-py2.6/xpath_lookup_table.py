# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/tables/xpath_lookup_table.py
# Compiled at: 2012-10-12 07:02:39
import logging, inspect, yaml, uuid
from coils.foundation import BLOBManager
from coils.core import *
from table import Table
from lxml import etree
HARD_NAMESPACES = {'dsml': 'http://www.dsml.org/DSML', 'apache': 'http://apache.org/dav/props', 
   'caldav': 'urn:ietf:params:xml:ns:caldav', 
   'carddav': 'urn:ietf:params:xml:ns:carddav', 
   'coils': '57c7fc84-3cea-417d-af54-b659eb87a046', 
   'dav': 'dav', 
   'xhtml': 'http://www.w3.org/1999/xhtml', 
   'mswebdav': 'urn:schemas-microsoft-com'}

class XPathLookupTable(Table):

    def __init__(self, context=None, process=None, scope=None):
        """
        ctor
        
        :param context: Security and operation context for message lookup
        :param process: Proccess to use when resolving message lookup
        :param scope: Scope to use when resolving message lookup
        """
        Table.__init__(self, context=context, process=process, scope=scope)
        self._xmldoc = None
        self._xpath = None
        self._label = None
        self._rfile = None
        self._do_input_upper = False
        self._do_input_strip = False
        self._do_output_upper = False
        self._do_output_strip = False
        self.log = logging.getLogger('OIE.XPathLookupTable')
        return

    def __repr__(self):
        return ('<XPathLookupTable name="{0}" />').format(self.name)

    def set_rfile(self, rfile):
        """
        Directly set the rfile attribute.
        
        
        :param rfile: Provides the table with a file handle to read the document,
           this is used for testing (otherwise the table cannot execute outside
           of a process instance).
        """
        self._rfile = rfile

    def set_description(self, description):
        """
        Load description of the table
        
        :param description: A dict describing the table
        """
        self.c = description
        self._default = self.c.get('defaultValue', None)
        if self.c.get('chainedTable', None):
            self._chained_table = Table.Load(self.c['chainedTable'])
        else:
            self._chained_table = None
        self._xpath = self.c.get('XPath', None)
        if not self._xpath:
            raise CoilsException('No XPath defined for XPath lookup table')
        self._xpath = self._xpath.replace('"?"', '"{}"')
        self._label = self.c.get('messageLabel', None)
        if not self._label:
            raise CoilsException('No message label defined for XPath lookup table')
        return

    def lookup_value(self, *values):
        """
        Perform XPath lookup into referenced document.
        
        :param values: list of values to load into the XPath
        """
        if not values:
            return
        else:
            values = values[0]
            self.log.debug(('XPath lookup requested with values: {0}').format(values))
            if not self._rfile:
                message = self.context.run_command('message::get', process=self._process, scope=self._scope, label=self._label)
                if message:
                    self.log.debug(('Retrieved message labelled "{0}" in scope "{1}"').format(self._label, self._label))
                    rfile = self.context.run_command('message::get-handle', message=message)
                    self.log.debug(('Opened handle for message text"').format(self._label, self._label))
                    self._rfile = rfile
                else:
                    raise CoilsException(('No message labelled "{0}" found in scope "{0}" of OGo#{2} [Process]').format(self._label, self._scope, self._process.object_id))
            if not self._xmldoc:
                doc = etree.parse(self._rfile)
                self.log.debug('Content of message parsed')
                nsm = doc.getroot().nsmap
                for (ab, ns) in HARD_NAMESPACES.items():
                    if ab not in nsm:
                        nsm[ab] = ns

                self._xmldoc = doc
                self._ns_map = nsm
            xp = self._xpath.format(*values)
            self.log.debug(('Performing XPath expression: {0}').format(xp))
            result = self._xmldoc.xpath(xp, namespaces=self._ns_map)
            if result:
                self.log.debug(('XPath evluated to {0} results').format(len(result)))
                result = result[0]
                if isinstance(result, basestring):
                    self.log.debug('XPath result is type string')
                    return result
                self.log.debug('XPath result is not a string')
                return etree.tostring(result)
            else:
                if self._chained_table:
                    if self._debug:
                        self.log.debug(('Passing lookup to chained table {0}').format(self._chained_table.name))
                    return self._chained_table.lookup_value(*values)
                else:
                    if self._default:
                        self.log.debug('Returning default value')
                        return self._default
                    self.log.debug('No result for XPath expression')
                    return
            return

    def shutdown(self):
        """
        Tear down any externally referenced resources
        """
        if self._rfile:
            BLOBManager.Close(self._rfile)
        Table.shutdown(self)