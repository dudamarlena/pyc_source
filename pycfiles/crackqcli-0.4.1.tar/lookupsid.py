# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/enum/lookupsid.py
# Compiled at: 2016-12-29 01:49:52
import sys, logging, codecs, traceback
from impacket import version
from impacket.dcerpc.v5 import transport, lsat, lsad
from impacket.dcerpc.v5.samr import SID_NAME_USE
from impacket.dcerpc.v5.dtypes import MAXIMUM_ALLOWED
from impacket.dcerpc.v5.rpcrt import DCERPCException

class LSALookupSid:
    KNOWN_PROTOCOLS = {'139/SMB': ('ncacn_np:%s[\\pipe\\lsarpc]', 139), 
       '445/SMB': ('ncacn_np:%s[\\pipe\\lsarpc]', 445)}

    def __init__(self, connection):
        self.__logger = connection.logger
        self.__addr = connection.host
        self.__username = connection.username
        self.__password = connection.password
        self.__protocol = connection.args.smb_port
        self.__hash = connection.hash
        self.__maxRid = int(connection.args.rid_brute)
        self.__domain = connection.domain
        self.__lmhash = ''
        self.__nthash = ''
        if self.__hash is not None:
            self.__lmhash, self.__nthash = self.__hash.split(':')
        if self.__password is None:
            self.__password = ''
        return

    def brute_force(self):
        logging.info('Brute forcing SIDs at %s' % self.__addr)
        protodef = LSALookupSid.KNOWN_PROTOCOLS[('{}/SMB').format(self.__protocol)]
        port = protodef[1]
        logging.info('Trying protocol %s...' % self.__protocol)
        stringbinding = protodef[0] % self.__addr
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        rpctransport.set_dport(port)
        if hasattr(rpctransport, 'set_credentials'):
            rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
        try:
            self.__logger.success('Brute forcing SIDs (rid:domain:user)')
            self.__bruteForce(rpctransport, self.__maxRid)
        except Exception as e:
            traceback.print_exc()

    def __bruteForce(self, rpctransport, maxRid):
        dce = rpctransport.get_dce_rpc()
        dce.connect()
        dce.bind(lsat.MSRPC_UUID_LSAT)
        resp = lsat.hLsarOpenPolicy2(dce, MAXIMUM_ALLOWED | lsat.POLICY_LOOKUP_NAMES)
        policyHandle = resp['PolicyHandle']
        resp = lsad.hLsarQueryInformationPolicy2(dce, policyHandle, lsad.POLICY_INFORMATION_CLASS.PolicyAccountDomainInformation)
        domainSid = resp['PolicyInformation']['PolicyAccountDomainInfo']['DomainSid'].formatCanonical()
        soFar = 0
        SIMULTANEOUS = 1000
        for j in range(maxRid / SIMULTANEOUS + 1):
            if (maxRid - soFar) / SIMULTANEOUS == 0:
                sidsToCheck = (maxRid - soFar) % SIMULTANEOUS
            else:
                sidsToCheck = SIMULTANEOUS
            if sidsToCheck == 0:
                break
            sids = list()
            for i in xrange(soFar, soFar + sidsToCheck):
                sids.append(domainSid + '-%d' % i)

            try:
                lsat.hLsarLookupSids(dce, policyHandle, sids, lsat.LSAP_LOOKUP_LEVEL.LsapLookupWksta)
            except DCERPCException as e:
                if str(e).find('STATUS_NONE_MAPPED') >= 0:
                    soFar += SIMULTANEOUS
                    continue
                elif str(e).find('STATUS_SOME_NOT_MAPPED') >= 0:
                    resp = e.get_packet()
                else:
                    raise

            for n, item in enumerate(resp['TranslatedNames']['Names']):
                if item['Use'] != SID_NAME_USE.SidTypeUnknown:
                    self.__logger.highlight('%d: %s\\%s (%s)' % (soFar + n, resp['ReferencedDomains']['Domains'][item['DomainIndex']]['Name'], item['Name'], SID_NAME_USE.enumItems(item['Use']).name))

            soFar += SIMULTANEOUS

        dce.disconnect()