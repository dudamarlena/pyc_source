# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/useragents.py
# Compiled at: 2012-10-12 07:02:39
import copy
DEFAULT_USER_AGENT = '148c9d0d669648ed8b8ed0292df478fd'
USER_AGENTS = {'148c9d0d669648ed8b8ed0292df478fd': {'name': 'default', 'patterns': [], 'webdav': {'filenameAsDisplayName': False, 'showProjectContactsFolder': True, 
                                                   'showProjectEnterprisesFolder': True, 
                                                   'showProjectTasksFolder': True, 
                                                   'showProjectProjectsFolder': True, 
                                                   'showProjectDocumentsFolder': True, 
                                                   'showProjectNotesFolder': True, 
                                                   'showProjectVersionsFolder': False, 
                                                   'folderContentType': 'unix/httpd-directory', 
                                                   'escapeGETs': False, 
                                                   'supports301': True, 
                                                   'supportsLocation': True, 
                                                   'supportsMEMOs': False, 
                                                   'absoluteHrefs': False, 
                                                   'portInAbsoluteHref': False, 
                                                   'hideLockRoot': False, 
                                                   'defaultPropeties': [
                                                                      ('name', 'DAV:', 'webdav', 'D:name'),
                                                                      ('href', 'DAV:', 'webdav', 'D:href'),
                                                                      ('getcontenttype', 'DAV:', 'webdav', 'D:getcontenttype'),
                                                                      ('contentclass', 'DAV:', 'webdav', 'D:contentclass'),
                                                                      ('getlastmodified', 'DAV:', 'webdav', 'D:getlastmodified'),
                                                                      ('getcontentlength', 'DAV:', 'webdav', 'D:getcontentlength'),
                                                                      ('iscollection', 'DAV:', 'webdav', 'D:iscollection'),
                                                                      ('displayname', 'DAV:', 'webdav', 'D:displayname'),
                                                                      ('getctag', 'urn:ietf:params:xml:ns:caldav', 'caldav', 'C:getctag'),
                                                                      ('resourcetype', 'DAV:', 'webdav', 'D:resourcetype')], 
                                                   'defaultNamespaces': {'C': 'urn:ietf:params:xml:ns:caldav', 'D': 'DAV:', 
                                                                         'G': 'http://groupdav.org/'}}, 
                                        'jsonrpc': {}, 'xmlrpc': {'allowNone': False}, 'vcard': {'setVoiceAttrInTel': True, 'setCoilsTypeInTel': True, 
                                                  'telTypeMap': {'10_fax': {'types': ['fax', 'work'], 'voice': False}, '01_tel': {'types': ['work', 'pref'], 'voice': True}, '03_tel_funk': {'types': ['cell'], 'voice': True}, '05_tel_private': {'types': ['home'], 'voice': True}, '30_pager': {'types': ['pager'], 'voice': False}}, 'setCoilsTypeInAdr': True, 
                                                  'adrTypeMap': {'private': {'types': ['home']}, 'mailing': {'types': ['work', 'pref']}, 'bill': {'types': ['work', 'pref']}, 'shipto': {'types': ['work']}}, 'includeObjectPropertes': False, 
                                                  'includeCoilsXAttributes': False, 
                                                  'includeCompanyValues': False}, 
                                        'icalendar': {}, 'omphalos': {'associativeLists': False}}, 
   '2f398cabd700444ca54e132b20b50aa0': {'name': 'GNOME Evolution', 'patterns': [
                                                   'evolution'], 
                                        'webdav': {'escapeGETs': False, 'supports301': True, 
                                                   'supportsLocation': True, 
                                                   'supportsMEMOs': True, 
                                                   'absoluteHrefs': False}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {'setVoiceAttrInTel': True, 'setCoilsTypeInTel': True, 
                                                 'setCoilsTypeInAdr': True}, 
                                        'icalendar': {}}, 
   'ecd0eda8f8b244109c7672ac4a630187': {'name': 'JGroupDAV', 'patterns': [
                                                   'bionicmessage.net jgroupdav'], 
                                        'webdav': {'escapeGETs': True, 'supports301': False, 
                                                   'supportsLocation': False, 
                                                   'supportsMEMOs': True, 
                                                   'absoluteHrefs': False}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {}, 'icalendar': {}}, 
   'ecd0eda8f8b244109c7672ac4a630187': {'name': 'Mozilla', 'patterns': [
                                                   'mozilla'], 
                                        'webdav': {'supports301': False, 'supportsLocation': False}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {}, 'icalendar': {}}, 
   'b6fb2c8a632148728d364b3d49dfe2dd': {'name': 'Microsoft WebDAV MiniRedirector', 'patterns': [
                                                   'microsoft-webdav-miniredir'], 
                                        'webdav': {'folderContentType': 'text/html', 'escapeGETs': False, 
                                                   'supports301': False, 
                                                   'supportsLocation': False, 
                                                   'supportsMEMOs': False, 
                                                   'absoluteHrefs': True, 
                                                   'portInAbsoluteHref': False, 
                                                   'hideLockRoot': True, 
                                                   'defaultPropeties': [
                                                                      ('href', 'DAV:', 'webdav', 'D:href'),
                                                                      ('getcontenttype', 'DAV:', 'webdav', 'D:getcontenttype'),
                                                                      ('getlastmodified', 'DAV:', 'webdav', 'D:getlastmodified'),
                                                                      ('creationdate', 'DAV:', 'webdav', 'D:creationdate'),
                                                                      ('displayname', 'DAV:', 'webdav', 'D:displayname'),
                                                                      ('getcontentlength', 'DAV:', 'webdav', 'D:getcontentlength'),
                                                                      ('executable', 'http://apache.org/dav/props/', 'apache', 'A:executable'),
                                                                      ('resourcetype', 'DAV:', 'webdav', 'D:resourcetype')], 
                                                   'defaultNamespaces': {'A': 'http://apache.org/dav/props/', 'D': 'DAV:'}}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {}, 'icalendar': {}}, 
   'e9556b2aad474923a52315d9bffbf124': {'name': 'Microsoft Data Access', 'patterns': [
                                                   'microsoft data access internet publishing'], 
                                        'webdav': {'folderContentType': 'text/html', 'escapeGETs': True, 
                                                   'supports301': False, 
                                                   'supportsLocation': False, 
                                                   'supportsMEMOs': False, 
                                                   'absoluteHrefs': True, 
                                                   'portInAbsoluteHref': False, 
                                                   'hideLockRoot': True, 
                                                   'defaultPropeties': [
                                                                      ('href', 'DAV:', 'webdav', 'D:href'),
                                                                      ('getcontenttype', 'DAV:', 'webdav', 'D:getcontenttype'),
                                                                      ('getlastmodified', 'DAV:', 'webdav', 'D:getlastmodified'),
                                                                      ('creationdate', 'DAV:', 'webdav', 'D:creationdate'),
                                                                      ('displayname', 'DAV:', 'webdav', 'D:displayname'),
                                                                      ('getcontentlength', 'DAV:', 'webdav', 'D:getcontentlength'),
                                                                      ('executable', 'http://apache.org/dav/props/', 'webdav', 'A:executable'),
                                                                      ('resourcetype', 'DAV:', 'webdav', 'D:resourcetype')], 
                                                   'defaultNamespaces': {'A': 'http://apache.org/dav/props/', 'D': 'DAV:'}}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {}, 'icalendar': {}}, 
   '4879e0253828479aaff784e4c52b23ad': {'name': 'Curl', 'patterns': [
                                                   'curl'], 
                                        'webdav': {'escapeGETs': True, 
                                                   'supports301': False, 
                                                   'supportsLocation': False, 
                                                   'supportsMEMOs': True, 
                                                   'absoluteHrefs': False}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {}, 'icalendar': {}}, 
   '1ce39e9fc8c2416986f56667ee6320d5': {'name': 'GNOME Virtual File-System', 'patterns': [
                                                   'gvfs'], 
                                        'webdav': {'escapeGETs': True, 
                                                   'supports301': False, 
                                                   'supportsLocation': False, 
                                                   'supportsMEMOs': False, 
                                                   'absoluteHrefs': False}, 
                                        'jsonrpc': {}, 'xmlrpc': {}, 'vard': {}, 'icalendar': {}}, 
   '9d2eb441-921b-4436-b0b9-771348f8ce44': {'name': 'Test User Agent', 'patterns': [
                                                       'testtesttest'], 
                                            'webdav': {'escapeGETs': True, 
                                                       'supports301': False, 
                                                       'supportsLocation': False, 
                                                       'supportsMEMOs': True, 
                                                       'absoluteHrefs': False}, 
                                            'jsonrpc': {}, 'xmlrpc': {}, 'vcard': {'setVoiceAttrInTel': False, 'setCoilsTypeInTel': False, 
                                                      'telTypeMap': {'10_fax': {'types': ['fax', 'work'], 'voice': False}, '01_tel': {'types': ['work', 'pref'], 'voice': True}, '03_tel_funk': {'types': ['cell'], 'voice': True}, '05_tel_private': {'types': ['home'], 'voice': True}, '30_pager': {'types': ['pager'], 'voice': False}}, 'setCoilsTypeInAdr': False, 
                                                      'adrTypeMap': {'private': {'types': ['home']}, 'mailing': {'types': ['work', 'pref']}, 'bill': {'types': ['work', 'pref']}, 'shipto': {'types': ['work']}}, 'includeObjectPropertes': False, 
                                                      'includeCoilsXAttributes': False, 
                                                      'includeCompanyValues': False}, 
                                            'icalendar': {}}, 
   '11e687c2-4cea-4464-a31c-5d9f97f8c6f4': {'name': 'CardDAV-Sync for Android', 'patterns': [
                                                       'carddav-sync for android'], 
                                            'webdav': {'escapeGETs': True, 
                                                       'supports301': False, 
                                                       'supportsLocation': False, 
                                                       'supportsMEMOs': False, 
                                                       'absoluteHrefs': False}, 
                                            'jsonrpc': {}, 'xmlrpc': {}, 'vcard': {'setVoiceAttrInTel': False, 'setCoilsTypeInTel': False, 
                                                      'setCoilsTypeInAdr': False, 
                                                      'includeObjectPropertes': False, 
                                                      'includeCoilsXAttributes': False, 
                                                      'includeCompanyValues': False}, 
                                            'icalendar': {}}, 
   '1dcddeea-c5c6-4076-a0e5-4bf933114b86': {'name': 'PHP Web Client (Use Associative Lists)', 'patterns': [
                                                       'simple-rpcclient', 'pear xml_rpc'], 
                                            'omphalos': {'associativeLists': True}, 'xmlrpc': {'allowNone': False}}, 
   'b9020396-85ae-4e47-9bc7-b67d62e88fb7': {'name': 'Android WebDAV File Manager', 'patterns': [
                                                       'apache-httpclient'], 
                                            'webdav': {'showProjectContactsFolder': False, 'showProjectEnterprisesFolder': False, 
                                                       'showProjectTasksFolder': False}}}

def lookup_user_agent(agent_string):

    def recursive_update(source, target, domain=None):
        for (key, value) in source.items():
            if key in target:
                if isinstance(value, dict):
                    if domain == 'webdav' and key in 'defaultNamespaces':
                        target[key] = source[key]
                    else:
                        recursive_update(value, target[key], domain=key)
                else:
                    target[key] = value
            else:
                target[key] = value

    if agent_string is None:
        return (DEFAULT_USER_AGENT, USER_AGENTS[DEFAULT_USER_AGENT])
    parts = agent_string.split('/')
    if len(parts) > 1:
        agent_name = parts[0].lower()
        agent_version = parts[1].lower()
    else:
        agent_name = parts[0].lower()
        agent_version = 'Unknown'
    agent = None
    if agent_name in USER_AGENTS:
        agent = agent_name
    else:
        for (agent_id, agent_data) in USER_AGENTS.items():
            for pattern in agent_data['patterns']:
                if agent_name == pattern or pattern.startswith(agent_name):
                    agent = agent_id
                    break

            if agent:
                break
        else:
            return (
             DEFAULT_USER_AGENT, USER_AGENTS[DEFAULT_USER_AGENT])

        agent_id = agent
        agent_data = copy.deepcopy(USER_AGENTS[DEFAULT_USER_AGENT])
        recursive_update(USER_AGENTS[agent_id], agent_data)
        return (agent_id, agent_data)