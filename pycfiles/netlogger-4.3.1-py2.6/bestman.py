# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/bestman.py
# Compiled at: 2010-04-29 00:14:31
"""
Parse output file from SRM "Bestman" implementation

Sample input: see netlogger/tests/data/srm-transfer.log
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: bestman.py 24753 2010-04-29 04:14:31Z dang $'
try:
    from hashlib import md5
    md5_ctor = md5
except ImportError:
    import md5
    md5_ctor = md5.new

import re
from netlogger import util
from netlogger.nllog import TRACE
from netlogger.parsers.base import BaseParser
_NS = 'gov.lbl.srm.'
_NS_LEN = len(_NS)
_NS_OUT = 'srm.server.'

class Parser(BaseParser):
    """Parse logs from Berkeley Storage Manager (BeStMan).
    See also http://datagrid.lbl.gov/bestman/

    Parameters:
        - version {1,2,2*}: Version 1 is anything before bestman-2.2.1.r3, Version 2 is that
                         version and later ones.
        - transfer_only {yes,no,no*}: For Version2, report only those events
                                        needed for transfer performance.

    """
    REQUEST_EVENT = 'gov.lbl.srm.server.TSRMRequestCopy'
    STATUS_EVENT = 'gov.lbl.srm.server.TSRMRequestCopyToRemote.setStatus'
    READY_EVENT = _NS + 'server.ContainerThread.ServerReady'
    E1 = re.compile('\\s*([a-zA-Z][a-zA-Z0-9._\\-]*)=([^"]\\S*|"[^"]*")\\s*')
    _HASH = md5_ctor
    TX_EVENT = re.compile('(tx|put|get)\\.')
    REQID_ATTR = 'req.id'
    EVENT_MAP = {'server.ContainerThread': {'ServerReady': 'ready'}, 
       'server.TSRMServer': {'incoming.srmPing': 'ping.in', 
                             'incoming.srmGetTransferProtocols': 'getTransferProtocols.in', 
                             'incoming.srmGetSpaceTokens': 'getSpaceTokens.in', 
                             'incoming.srmCopy': 'copy.in', 
                             'outcoming.srmPing': 'ping.out', 
                             'outcoming.srmGetTransferProtocols': 'getTransferProtocols.out', 
                             'outcoming.srmGetSpaceTokens': 'getSpaceTokens.out', 
                             'list': 'list'}, 
       'impl.TSRMService': {'outcoming.SrmCopy': 'copy.out', 
                            'outcoming.SrmPrepareToPut': 'put.start', 
                            'outcoming.SrmPutDone': 'put.end', 
                            'outcoming.SrmPrepareToGet': 'get.start', 
                            'outcoming.SrmGetDone': 'get.end'}, 
       'server.TSRMSourceFile': {'download': 'download'}, 
       'server.TSRMDownloadCommon': {'txfSetup': 'tx.pull.size', 
                                     'TxfStartsPull': 'tx.pull.start', 
                                     'TxfEndsPull': 'tx.pull.end'}, 
       'server.TSRMUploadCommon': {'txfSetup': 'tx.push.size', 
                                   'TxfStartsPush': 'tx.push.start', 
                                   'TxfEndsPush': 'tx.push.end'}}
    STATUS_MAP = {'SRM_SUCCESS': 0, 
       'SRM_RELEASED': 1, 
       'SRM_FILE_PINNED': 2, 
       'SRM_REQUEST_INPROGRESS': 11, 
       'SRM_FILE_IN_CACHE': 12, 
       'SRM_SPACE_AVAILABLE': 13, 
       'SRM_FAILURE': -1, 
       'SRM_AUTHORIZATION_FAILURE': -2, 
       'SRM_DUPLICATION_ERROR': -3, 
       'SRM_FILE_BUSY': -4, 
       'SRM_FILE_LIFETIME_EXPIRED': -5, 
       'SRM_INVALID_PATH': -6, 
       'SRM_INVALID_REQUEST': -7, 
       'SRM_ABORTED': -8}
    STATUS_UNKNOWN = -100
    END_EVENT_STATUS_MAX = 10
    ATTR_MAP = {'reqSize': 'req.size', 
       'trustedSize': 'file.size', 
       'GivenBytes': 'file.size', 
       'JVMfreebytes': 'bytes', 
       'JVMtotalbytes': 'bytes'}

    def __init__(self, f, version='2', transfer_only='no', **kw):
        BaseParser.__init__(self, f, fullname=__name__, **kw)
        self._trace = self.log.isEnabledFor(TRACE)
        self.log.info('version', value=version)
        if version == '1':
            self.proc_func = self._process_v1
        elif version == '2':
            self.proc_func = self._process_v2
            self._xonly = self.boolParam(transfer_only)
            self._tid = {}
            self._ends = util.FIFODict(1000)
        else:
            raise ValueError('Unknown version: %s' % version)

    def process(self, line):
        return self.proc_func(line)

    def getParameters(self):
        """For v2, save the threadid-to-requestid mapping.
        """
        result = {}
        if self.proc_func == self._process_v2:
            result = self._tid
        return result

    def setParameters(self, param):
        """For v2, restore the threadid-to-requestid mapping.
        """
        if self.proc_func == self._process_v2:
            if param:
                self._tid.update(param)

    def _process_v2(self, line):
        """This is the newer, version 2, bestman parser
        """
        s = line.strip()
        d = {}
        if len(s) == 0 or s.startswith('#'):
            return ()
        else:
            if s.find('level=Debug') >= 0:
                if s.find('JVMfreebytes=') >= 0:
                    if self._trace:
                        self.log.trace('jvm.free')
                    d['event'] = 'jvm.free'
                elif s.find('JVMtotalbytes=') >= 0:
                    if self._trace:
                        self.log.trace('jvm.total')
                    d['event'] = 'jvm.total'
                else:
                    return ()
            if self._trace:
                self.log.trace('not.debug', value=s)
            (th_id, req_id, status) = (None, None, None)
            is_request = False
            fields = self.E1.findall(s)
            for (n, v) in fields:
                if v == 'null':
                    continue
                v = v.strip('"')
                if self.ATTR_MAP.has_key(n):
                    d[self.ATTR_MAP[n]] = v
                elif n == 'tid':
                    if v.startswith('Thread-'):
                        th_id = v[len('Thread-'):]
                    else:
                        th_id = v
                    d['th.id'] = th_id
                elif n == 'rid':
                    d[self.REQID_ATTR] = req_id = v
                elif n == 'statusCode':
                    d['status'] = status = self.STATUS_MAP.get(v, self.STATUS_UNKNOWN)
                elif n == 'class':
                    bm_class = v[_NS_LEN:]
                else:
                    d[n] = v

            try:
                event = d['event']
            except KeyError:
                if self.log.isEnabledFor(TRACE):
                    self.log.trace('event.unknown', value=s)
                return ()
            else:
                if event.startswith('jvm.'):
                    mapped_event = event
                elif bm_class.startswith('server.TSRMRequest'):
                    is_request = True
                    req_type = bm_class[18:].lower()
                    req_event = event.lower()
                    mapped_event = 'req.' + req_type + '.' + req_event
                elif bm_class.startswith('server.TUserRequest'):
                    is_request = True
                    req_type = bm_class[19:].lower()
                    req_event = event.lower()
                    mapped_event = 'ureq.' + req_type + '.' + req_event
                else:
                    mapped_event = self.EVENT_MAP.get(bm_class, {}).get(event, None)
                    if mapped_event is None:
                        if self._xonly:
                            return ()
                        mapped_event = bm_class + '.' + event
                        if mapped_event.startswith('server.'):
                            mapped_event = mapped_event[7:]
                    elif self._xonly and not self.TX_EVENT.match(mapped_event):
                        return ()
                if th_id:
                    if req_id is None:
                        d[self.REQID_ATTR] = self._tid.get(th_id, 'unknown')
                    if mapped_event.endswith('.end'):
                        if self._tid.has_key(th_id):
                            del self._tid[th_id]
                    elif req_id:
                        self._tid[th_id] = req_id

            if not bm_class.startswith('server.TSRMRequest') and status is not None and status <= self.END_EVENT_STATUS_MAX and mapped_event.endswith('.reqstatus') and req_id is not None and self._ends.add(req_id):
                mapped_event = mapped_event[:-9] + 'end'
            d['event'] = _NS_OUT + mapped_event
            return (
             d,)

    def _processRequestId(self, event_name, attrs, thread_id):
        """Set request id or modify mapping
           between the thread id and request id.
        """
        pass

    def _process_v1(self, line):
        """ This is the Dan's older version 1 """
        fields = line.split()
        result = ()
        if len(fields) > 4:
            event = fields[3]
            if event.startswith(self.STATUS_EVENT):
                status = fields[4]
                if status == 'SRM_SUCCESS':
                    result = self._processSuccess(fields)
            elif event.startswith(self.REQUEST_EVENT):
                result = self._processRequest(fields)
        return result

    def _gmt(self, fields):
        (date, time) = fields[1][:-3].split('-')
        date = date.replace('.', '-')
        return date + 'T' + time + 'Z'

    _URL_RE = '(?P<url>[^:]*://.*)'
    _FROM_RE = re.compile('.*\\[from\\]=' + _URL_RE)
    _TO_RE = re.compile('\\[to\\]=' + _URL_RE)

    def _processRequest(self, fields):
        m = self._FROM_RE.match(fields[3])
        if not m:
            return ()
        from_url = m.groupdict()['url']
        m = self._TO_RE.match(fields[4])
        to_url = m.groupdict()['url']
        guid = self._getGuid(from_url, to_url)
        event = {'ts': self._gmt(fields), 'event': _NS + 'server.TSRMRequestCopy.start', 
           'guid': guid, 
           'src': from_url, 
           'dst': to_url}
        return (
         event,)

    def _processSuccess(self, fields):
        p = fields[9].find(':')
        if p < 0:
            return ()
        from_url = fields[9][p + 1:]
        to_url = fields[11][4:]
        guid = self._getGuid(from_url, to_url)
        event_name = _NS + 'server.TSRMRequestCopy.end'
        event = {'ts': self._gmt(fields), 'event': event_name, 
           'guid': guid, 
           'src': from_url, 
           'dst': to_url, 
           'status': 0}
        return (
         event,)

    def _getGuid(self, *args):
        h = self._HASH()
        for arg in args:
            h.update(arg)

        guid = h.hexdigest()
        return guid