# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/ldaputil/asynch.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 6156 bytes
"""
web2ldap.ldaputil.asynch - handle async LDAP operations

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0, ldap0.ldif
from ldap0.res import SearchResultEntry

class AsyncSearchHandler:
    __doc__ = '\n    Class for stream-processing LDAP search results\n\n    Arguments:\n\n    l\n      LDAPObject instance\n    '

    def __init__(self, l):
        self._l = l
        self._msg_id = None
        self._after_first = True

    def start_search(self, searchRoot, searchScope, filterStr, attrList=None, sizelimit=0, req_ctrls=None):
        """
        searchRoot
            See parameter base of method LDAPObject.search()
        searchScope
            See parameter scope of method LDAPObject.search()
        filterStr
            See parameter filter of method LDAPObject.search()
        attrList=None
            See parameter attrlist of method LDAPObject.search()
        sizelimit
            Maximum number of entries a server should return
            (request client-side limit)
        req_ctrls
            list of server-side LDAP controls
        """
        self._msg_id = self._l.search(searchRoot,
          scope=searchScope,
          filterstr=filterStr,
          attrlist=attrList,
          req_ctrls=req_ctrls,
          sizelimit=sizelimit)
        self._after_first = True

    def pre_processing(self):
        """
        Do anything you want after starting search but
        before receiving and processing results
        """
        pass

    def after_first(self):
        """
        Do anything you want right after successfully receiving but before
        processing first result
        """
        pass

    def post_processing(self):
        """
        Do anything you want after receiving and processing all results
        """
        pass

    def process_results(self, ignoreResultsNumber=0, processResultsCount=0):
        """
        ignoreResultsNumber
            Don't process the first ignoreResultsNumber results.
        processResultsCount
            If non-zero this parameters indicates the number of results
            processed is limited to processResultsCount.
        """
        self.pre_processing()
        result_counter = 0
        end_result_counter = ignoreResultsNumber + processResultsCount
        go_ahead = True
        partial = False
        self.beginResultsDropped = 0
        self.endResultBreak = result_counter
        try:
            for result in self._l.results(self._msg_id):
                if self._after_first:
                    self.after_first()
                    self._after_first = False
                for result_item in result.rdata:
                    if result_counter < ignoreResultsNumber:
                        self.beginResultsDropped += 1
                    else:
                        if processResultsCount == 0 or result_counter < end_result_counter:
                            self._process_result(result_item)
                        else:
                            go_ahead = False
                            partial = True
                            break
                    result_counter = result_counter + 1
                else:
                    self.endResultBreak = result_counter

        finally:
            if partial:
                if self._msg_id is not None:
                    self._l.abandon(self._msg_id)

        self.post_processing()
        return partial

    def _process_result(self, resultItem):
        """
        Process single entry

        resultItem
            Single item of a result list
        """
        pass


class List(AsyncSearchHandler):
    __doc__ = '\n    Class for collecting all search results.\n\n    This does not seem to make sense in the first place but think\n    of retrieving exactly a certain portion of the available search\n    results.\n    '

    def __init__(self, l):
        AsyncSearchHandler.__init__(self, l)
        self.allResults = []

    def _process_result(self, resultItem):
        self.allResults.append(resultItem)


class FileWriter(AsyncSearchHandler):
    __doc__ = '\n    Class for writing a stream of LDAP search results to a file object\n\n    Arguments:\n    l\n      LDAPObject instance\n    f\n      File object instance where the LDIF data is written to\n    '
    encoding = 'utf-8'

    def __init__(self, l, f, header='', footer=''):
        AsyncSearchHandler.__init__(self, l)
        self._f = f
        self.header = header
        self.footer = footer

    def pre_processing(self):
        """
        The header is written to output after starting search but
        before receiving and processing results.
        """
        self._f.write(self.header.encode(self.encoding))

    def post_processing(self):
        """
        The footer is written to output after receiving and
        processing results.
        """
        self._f.write(self.footer.encode(self.encoding))


class LDIFWriter(FileWriter):
    __doc__ = '\n    Class for writing a stream LDAP search results to a LDIF file\n\n    Arguments:\n\n    l\n      LDAPObject instance\n    writer_obj\n      Either a file-like object or a ldif.LDIFWriter instance used for output\n    '

    def __init__(self, l, writer_obj, header='', footer=''):
        if isinstance(writer_obj, ldap0.ldif.LDIFWriter):
            self._ldif_writer = writer_obj
        else:
            self._ldif_writer = ldap0.ldif.LDIFWriter(writer_obj)
        FileWriter.__init__(self, l, self._ldif_writer._output_file, header, footer)

    def _process_result(self, resultItem):
        if isinstance(resultItem, SearchResultEntry):
            self._ldif_writer.unparse(resultItem.dn_b, resultItem.entry_b)