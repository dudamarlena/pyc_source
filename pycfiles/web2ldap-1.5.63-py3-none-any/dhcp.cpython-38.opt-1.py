# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/dhcp.py
# Compiled at: 2020-03-14 12:28:02
# Size of source mod 2**32: 11827 bytes
"""
web2ldap plugin classes for attributes defined for DHCP service

See http://tools.ietf.org/draft/draft-ietf-dhc-ldap-schema/
"""
import re, ipaddress, web2ldapcnf, web2ldap.app.searchform
from web2ldap.app.schema.syntaxes import MultilineText, IA5String, SelectList, Integer, BitArrayInteger, MacAddress, DynamicDNSelectList, DNSDomain, syntax_registry

class DHCPConfigStatement(MultilineText):
    oid = 'DHCPConfigStatement-oid'
    oid: str
    desc = 'DHCP configuration statement'
    desc: str
    lineSep = b''

    def display(self, valueindex=0, commandbutton=False) -> str:
        r = [
         '<code>%s</code>' % MultilineText.display(self, valueindex, commandbutton)]
        if commandbutton:
            try:
                dhcp_type, dhcp_value = self.av_u.split(' ', 1)
            except ValueError:
                dhcp_type, dhcp_value = self.av_u, ''
            else:
                dhcp_type = dhcp_type.lower().strip()
                dhcp_value = dhcp_value.replace('"', '').strip()
                if dhcp_type == 'host-name':
                    host_name = dhcp_value.lower()
                    r.append(self._app.anchor('search',
                      'DNS RR', (
                     (
                      'dn', str(self._app.naming_context)),
                     ('searchform_mode', 'adv'),
                     ('search_mode', '(|%s)'),
                     ('search_attr', 'dc'),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                     (
                      'search_string', host_name),
                     ('search_attr', 'pTRRecord'),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_BEGINS_WITH),
                     (
                      'search_string', host_name + '.'),
                     ('search_attr', 'associatedDomain'),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_BEGINS_WITH),
                     (
                      'search_string', host_name + '.')),
                      title='Search related DNS RR entry'))
        else:
            if dhcp_type == 'fixed-address':
                search_params = [('dn', str(self._app.naming_context)),
                 ('searchform_mode', 'adv'),
                 ('search_mode', '(|%s)'),
                 ('search_attr', 'aRecord'),
                 (
                  'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                 (
                  'search_string', dhcp_value),
                 ('search_attr', 'aAAARecord'),
                 (
                  'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                 (
                  'search_string', dhcp_value)]
                try:
                    reverse_dns = ipaddress.ip_address(dhcp_value).reverse_pointer
                except ipaddress.AddressValueError:
                    pass
                else:
                    search_params.extend((
                     ('search_attr', 'associatedDomain'),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                     (
                      'search_string', reverse_dns)))
                r.append(self._app.anchor('search',
                  'DNS RRs', search_params,
                  title='Search related DNS RR entries'))
            return web2ldapcnf.command_link_separator.join(r)


syntax_registry.reg_at(DHCPConfigStatement.oid, [
 '2.16.840.1.113719.1.203.4.3',
 '2.16.840.1.113719.1.203.6.9',
 '2.16.840.1.113719.1.203.4.7'])

class DHCPServerDN(DynamicDNSelectList):
    oid = 'DHCPServerDN-oid'
    oid: str
    desc = 'DN of DHCP server entry'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpServer)'


syntax_registry.reg_at(DHCPServerDN.oid, [
 '2.16.840.1.113719.1.203.4.1',
 '2.16.840.1.113719.1.203.4.2',
 '2.16.840.1.113719.1.203.4.54'])

class DHCPOptionsDN(DynamicDNSelectList):
    oid = 'DHCPOptionsDN-oid'
    oid: str
    desc = 'DN of DHCP option object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpOptions)'


syntax_registry.reg_at(DHCPOptionsDN.oid, [
 '2.16.840.1.113719.1.203.4.9'])

class DHCPHostDN(DynamicDNSelectList):
    oid = 'DHCPHostDN-oid'
    oid: str
    desc = 'DN of DHCP host object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpHost)'


syntax_registry.reg_at(DHCPHostDN.oid, [
 '2.16.840.1.113719.1.203.4.10',
 '2.16.840.1.113719.1.203.4.31',
 '2.16.840.1.113719.1.203.4.32'])

class DHCPPoolDN(DynamicDNSelectList):
    oid = 'DHCPPoolDN-oid'
    oid: str
    desc = 'DN of DHCP pool object'
    desc: str
    ldap_url = 'ldap:///_??sub?(objectClass=dhcpPool)'


syntax_registry.reg_at(DHCPPoolDN.oid, [
 '2.16.840.1.113719.1.203.4.11'])

class DHCPGroupDN(DynamicDNSelectList):
    oid = 'DHCPGroupDN-oid'
    oid: str
    desc = 'DN of DHCP group object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpGroup)'


syntax_registry.reg_at(DHCPGroupDN.oid, [
 '2.16.840.1.113719.1.203.4.12'])

class DHCPSubnetDN(DynamicDNSelectList):
    oid = 'DHCPSubnetDN-oid'
    oid: str
    desc = 'DN of DHCP subnet object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpSubnet)'


syntax_registry.reg_at(DHCPSubnetDN.oid, [
 '2.16.840.1.113719.1.203.4.13'])

class DHCPLeasesDN(DynamicDNSelectList):
    oid = 'DHCPLeasesDN-oid'
    oid: str
    desc = 'DN of DHCP leases object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpLeases)'


syntax_registry.reg_at(DHCPLeasesDN.oid, [
 '2.16.840.1.113719.1.203.4.14',
 '2.16.840.1.113719.1.203.4.15'])

class DHCPClassesDN(DynamicDNSelectList):
    oid = 'DHCPClassesDN-oid'
    oid: str
    desc = 'DN of DHCP classes object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpClass)'


syntax_registry.reg_at(DHCPClassesDN.oid, [
 '2.16.840.1.113719.1.203.4.16'])

class DHCPSubclassesDN(DynamicDNSelectList):
    oid = 'DHCPSubclassesDN-oid'
    oid: str
    desc = 'DN of DHCP Subclasses object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpSubclass)'


syntax_registry.reg_at(DHCPSubclassesDN.oid, [
 '2.16.840.1.113719.1.203.4.17'])

class DHCPSharedNetworkDN(DynamicDNSelectList):
    oid = 'DHCPSharedNetworkDN-oid'
    oid: str
    desc = 'DN of DHCP shared network object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpSharedNetwork)'


syntax_registry.reg_at(DHCPSharedNetworkDN.oid, [
 '2.16.840.1.113719.1.203.4.18'])

class DHCPServiceDN(DynamicDNSelectList):
    oid = 'DHCPServiceDN-oid'
    oid: str
    desc = 'DN of DHCP service object'
    desc: str
    ldap_url = 'ldap:///_?cn?sub?(objectClass=dhcpService)'


syntax_registry.reg_at(DHCPServiceDN.oid, [
 '2.16.840.1.113719.1.203.4.19'])

class DHCPHWAddress(MacAddress):
    oid = 'DHCPHWAddress-oid'
    oid: str
    desc = 'Network classifier and MAC address'
    desc: str
    maxLen = 26
    maxLen: str
    reObj = re.compile('^(ethernet|token-ring|fddi) ([0-9a-fA-F]{2}\\:){5}[0-9a-fA-F]{2}$')

    def sanitize(self, attrValue: bytes) -> bytes:
        attrValue = attrValue.strip()
        if len(attrValue) == 17:
            return b'ethernet %s' % attrValue
        return attrValue


syntax_registry.reg_at(DHCPHWAddress.oid, [
 '2.16.840.1.113719.1.203.4.34'])

class DHCPNetMask(Integer):
    oid = 'DHCPNetMask-oid'
    oid: str
    desc = 'Network address mask bits'
    desc: str
    maxValue = 0
    maxValue = 32
    inputSize = 15

    def _maxlen(self, form_value):
        return self.inputSize


syntax_registry.reg_at(DHCPNetMask.oid, [
 '2.16.840.1.113719.1.203.4.6'])

class DHCPRange(IA5String):
    oid = 'DHCPRange-oid'
    oid: str
    desc = 'Network address range'
    desc: str

    def _get_ipnetwork(self):
        cn = self._entry['cn'][0].strip()
        net_mask = self._entry['dhcpNetMask'][0].strip()
        return ipaddress.ip_network((('%s/%s' % (cn, net_mask)).decode('ascii')), strict=False)

    def formValue(self) -> str:
        form_value = IA5String.formValue(self)
        if not form_value:
            try:
                ipv4_network = self._get_ipnetwork().hosts()
                form_value = ' '.join((str(ipv4_network[0]), str(ipv4_network[(-1)])))
            except ipaddress.AddressValueError:
                pass

        return form_value

    def sanitize(self, attrValue: bytes) -> bytes:
        return attrValue.strip().replace(b'  ', b' ').replace(b'-', b' ').replace(b'..', b' ')

    def _validate(self, attrValue: bytes) -> bool:
        try:
            l, h = attrValue.split(b' ', 1)
        except (IndexError, ValueError):
            return False
        else:
            try:
                l_a = ipaddress.ip_address(l.decode(self._app.ls.charset))
                h_a = ipaddress.ip_address(h.decode(self._app.ls.charset))
            except Exception:
                return False
            else:
                if l_a > h_a:
                    return False
                try:
                    ipv4_network = self._get_ipnetwork()
                except Exception:
                    return True
                else:
                    return l_a in ipv4_network and h_a in ipv4_network


syntax_registry.reg_at(DHCPRange.oid, [
 '2.16.840.1.113719.1.203.4.4'])

class DHCPAddressState(SelectList):
    oid = 'DHCPAddressState-oid'
    oid: str
    desc = 'DHCP address state'
    desc: str
    attr_value_dict = {'':'', 
     'FREE':'FREE', 
     'ACTIVE':'ACTIVE', 
     'EXPIRED':'EXPIRED', 
     'RELEASED':'RELEASED', 
     'RESET':'RESET', 
     'ABANDONED':'ABANDONED', 
     'BACKUP':'BACKUP', 
     'UNKNOWN':'UNKNOWN', 
     'RESERVED':'RESERVED (an address that is managed by DHCP that is reserved for a specific client)', 
     'RESERVED-ACTIVE':'RESERVED-ACTIVE (same as reserved, but address is currently in use)', 
     'ASSIGNED':'ASSIGNED (assigned manually or by some other mechanism)', 
     'UNASSIGNED':'UNASSIGNED', 
     'NOTASSIGNABLE':'NOTASSIGNABLE'}


class DHCPDnsStatus(BitArrayInteger):
    __doc__ = '\n    0 (C): name to address (such as A RR) update successfully completed\n    1 (A): Server is controlling A RR on behalf of the client\n    2 (D): address to name (such as PTR RR) update successfully completed (Done)\n    3 (P): Server is controlling PTR RR on behalf of the client\n    4-15 : Must be zero\n    '
    oid = 'DHCPDnsStatus-oid'
    oid: str
    flag_desc_table = (('(C): name to address (such as A RR) update successfully completed', 1),
                       ('(A): Server is controlling A RR on behalf of the client', 2),
                       ('(D): address to name (such as PTR RR) update successfully completed (Done)', 4),
                       ('(P): Server is controlling PTR RR on behalf of the client', 8))


syntax_registry.reg_at(DHCPDnsStatus.oid, [
 '2.16.840.1.113719.1.203.4.28'])
syntax_registry.reg_at(DNSDomain.oid, [
 '2.16.840.1.113719.1.203.4.27'])
syntax_registry.reg_at(DHCPAddressState.oid, [
 '2.16.840.1.113719.1.203.4.22'])
syntax_registry.reg_syntaxes(__name__)