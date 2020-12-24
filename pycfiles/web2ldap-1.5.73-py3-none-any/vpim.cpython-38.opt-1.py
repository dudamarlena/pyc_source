# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/vpim.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1808 bytes
"""
web2ldap plugin classes for attributes defined in VPIM (see RFC 4237)
"""
from web2ldap.app.schema.syntaxes import SelectList, RFC822Address, syntax_registry
syntax_registry.reg_at(RFC822Address.oid, [
 '1.3.6.1.1.11.1.2.2'])

class VPIMExtendedAbsenceStatus(SelectList):
    oid = 'VPIMExtendedAbsenceStatus-oid'
    oid: str
    desc = ''
    desc: str
    attr_value_dict = {'':'', 
     'Off':'Off', 
     'On':'On', 
     'MsgBlocked':'MsgBlocked'}


syntax_registry.reg_at(VPIMExtendedAbsenceStatus.oid, [
 '1.3.6.1.1.11.1.2.7'])

class VPIMSupportedUABehaviors(SelectList):
    oid = 'VPIMSupportedUABehaviors-oid'
    oid: str
    desc = ''
    desc: str
    attr_value_dict = {'':'', 
     'MessageDispositionNotification':'recipient will send a MDN in response to an MDN request', 
     'MessageSensitivity':'recipient supports sensitivity indication', 
     'MessageImportance':'recipient supports importance indication'}


syntax_registry.reg_at(VPIMSupportedUABehaviors.oid, [
 '1.3.6.1.1.11.1.2.8'])

class VPIMSupportedAudioMediaTypes(SelectList):
    oid = 'VPIMSupportedAudioMediaTypes-oid'
    oid: str
    desc = 'Audio Media Types'
    desc: str
    attr_value_dict = {'audio/basic':'audio/basic', 
     'audio/mpeg':'audio/mpeg', 
     'audio/x-aiff':'audio/x-aiff', 
     'audio/x-realaudio':'audio/x-realaudio', 
     'audio/x-wav':'audio/x-wav'}


syntax_registry.reg_at(VPIMSupportedAudioMediaTypes.oid, [
 '1.3.6.1.1.11.1.2.5'])
syntax_registry.reg_syntaxes(__name__)