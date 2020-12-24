# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chris/Development/pymacadmin-env/lib/python2.5/site-packages/PyMacAdmin/Security/Keychain.py
# Compiled at: 2009-06-07 22:49:10
__doc__ = "\nWrapper for the core Keychain API\n\nMost of the internals are directly based on the native Keychain API. Apple's developer documentation is highly relevant:\n\nhttp://developer.apple.com/documentation/Security/Reference/keychainservices/Reference/reference.html#//apple_ref/doc/uid/TP30000898-CH1-SW1\n"
import os, ctypes
from PyMacAdmin import Security

class Keychain(object):
    """A friendlier wrapper for the Keychain API"""

    def __init__(self, keychain_name=None):
        self.keychain_handle = self.open_keychain(keychain_name)

    def open_keychain(self, path=None):
        """Open a keychain file - if no path is provided, the user's default keychain will be used"""
        if not path:
            return
        if path and not os.path.exists(path):
            raise IOError('Keychain %s does not exist' % path)
        keychain = ctypes.c_void_p()
        keychain_ptr = ctypes.pointer(keychain)
        rc = Security.lib.SecKeychainOpen(path, keychain_ptr)
        if rc != 0:
            raise RuntimeError("Couldn't open system keychain: rc=%d" % rc)
        return keychain

    def find_generic_password(self, service_name='', account_name=''):
        """Pythonic wrapper for SecKeychainFindGenericPassword"""
        item_p = ctypes.c_uint32()
        password_length = ctypes.c_uint32(0)
        password_data = ctypes.c_char_p(256)
        if not service_name:
            service_name = ''
        if not account_name:
            account_name = ''
        rc = Security.lib.SecKeychainFindGenericPassword(self.keychain_handle, len(service_name), service_name, len(account_name), account_name, ctypes.byref(password_length), ctypes.pointer(password_data), ctypes.byref(item_p))
        if rc == -25300:
            raise KeyError('No keychain entry for generic password: service=%s, account=%s' % (service_name, account_name))
        elif rc != 0:
            raise RuntimeError('Unable to retrieve generic password (service=%s, account=%s): rc=%d' % (service_name, account_name, rc))
        password = password_data.value[0:password_length.value]
        info = SecKeychainAttributeInfo()
        attrs_p = SecKeychainAttributeList_p()
        info.count = 1
        info.tag.contents = Security.kSecLabelItemAttr
        Security.lib.SecKeychainItemCopyAttributesAndData(item_p, ctypes.pointer(info), None, ctypes.byref(attrs_p), None, None)
        attrs = attrs_p.contents
        assert attrs.count == 1
        label = attrs.attr[0].data[:attrs.attr[0].length]
        Security.lib.SecKeychainFreeAttributeInfo(attrs_p)
        return GenericPassword(service_name=service_name, account_name=account_name, password=password, keychain_item=item_p, label=label)

    def find_internet_password(self, account_name='', password='', server_name='', security_domain='', path='', port=0, protocol_type=None, authentication_type=None):
        """Pythonic wrapper for SecKeychainFindInternetPassword"""
        item = ctypes.c_void_p()
        password_length = ctypes.c_uint32(0)
        password_data = ctypes.c_char_p(256)
        if protocol_type and len(protocol_type) != 4:
            raise TypeError('protocol_type must be a valid FourCharCode - see http://developer.apple.com/documentation/Security/Reference/keychainservices/Reference/reference.html#//apple_ref/doc/c_ref/SecProtocolType')
        if authentication_type and len(authentication_type) != 4:
            raise TypeError('authentication_type must be a valid FourCharCode - see http://developer.apple.com/documentation/Security/Reference/keychainservices/Reference/reference.html#//apple_ref/doc/c_ref/SecAuthenticationType')
        if not isinstance(port, int):
            port = int(port)
        rc = Security.lib.SecKeychainFindInternetPassword(self.keychain_handle, len(server_name), server_name, len(security_domain) if security_domain else 0, security_domain, len(account_name), account_name, len(path), path, port, protocol_type, authentication_type, ctypes.byref(password_length), ctypes.pointer(password_data), ctypes.pointer(item))
        if rc == -25300:
            raise KeyError('No keychain entry for internet password: server=%s, account=%s' % (server_name, account_name))
        elif rc != 0:
            raise RuntimeError('Unable to retrieve internet password (server=%s, account=%s): rc=%d' % (server_name, account_name, rc))
        password = password_data.value[0:password_length.value]
        Security.lib.SecKeychainItemFreeContent(None, password_data)
        return InternetPassword(server_name=server_name, account_name=account_name, password=password, keychain_item=item, security_domain=security_domain, path=path, port=port, protocol_type=protocol_type, authentication_type=authentication_type)

    def add(self, item):
        """Add the provided GenericPassword or InternetPassword object to this Keychain"""
        assert isinstance(item, GenericPassword)
        item_ref = ctypes.c_void_p()
        if isinstance(item, InternetPassword):
            rc = Security.lib.SecKeychainAddInternetPassword(self.keychain_handle, len(item.server_name), item.server_name, len(item.security_domain), item.security_domain, len(item.account_name), item.account_name, len(item.path), item.path, item.port, item.protocol_type, item.authentication_type, len(item.password), item.password, ctypes.pointer(item_ref))
        else:
            rc = Security.lib.SecKeychainAddGenericPassword(self.keychain_handle, len(item.service_name), item.service_name, len(item.account_name), item.account_name, len(item.password), item.password, ctypes.pointer(item_ref))
        if rc != 0:
            raise RuntimeError('Error adding %s: rc=%d' % (item, rc))
        item.keychain_item = item_ref

    def remove(self, item):
        """Remove the provided keychain item as the reverse of Keychain.add()"""
        assert isinstance(item, GenericPassword)
        item.delete()


class GenericPassword(object):
    """Generic keychain password used with SecKeychainAddGenericPassword and SecKeychainFindGenericPassword"""
    account_name = None
    service_name = None
    label = None
    password = None
    keychain_item = None

    def __init__(self, **kwargs):
        super(GenericPassword, self).__init__()
        for (k, v) in kwargs.items():
            if not hasattr(self, k):
                raise AttributeError('Unknown property %s' % k)
            setattr(self, k, v)

    def update_password(self, new_password):
        """Change the stored password"""
        rc = Security.lib.SecKeychainItemModifyAttributesAndData(self.keychain_item, None, len(new_password), new_password)
        if rc == -61:
            raise RuntimeError('Permission denied updating %s' % self)
        elif rc != 0:
            raise RuntimeError('Unable to update password for %s: rc = %d' % rc)
        return

    def delete(self):
        """Removes this item from the keychain"""
        rc = Security.lib.SecKeychainItemDelete(self.keychain_item)
        if rc != 0:
            raise RuntimeError('Unable to delete %s: rc=%d' % (self, rc))
        from CoreFoundation import CFRelease
        CFRelease(self.keychain_item)
        self.keychain_item = None
        self.service_name = None
        self.account_name = None
        self.password = None
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        props = []
        for k in ['service_name', 'account_name', 'label']:
            props.append('%s=%s' % (k, repr(getattr(self, k))))

        return '%s(%s)' % (self.__class__.__name__, (', ').join(props))


class InternetPassword(GenericPassword):
    """Specialized keychain item for internet passwords used with SecKeychainAddInternetPassword and SecKeychainFindInternetPassword"""
    account_name = ''
    password = None
    keychain_item = None
    server_name = ''
    security_domain = ''
    path = ''
    port = 0
    protocol_type = None
    authentication_type = None

    def __init__(self, **kwargs):
        super(InternetPassword, self).__init__(**kwargs)

    def __repr__(self):
        props = []
        for k in ['account_name', 'server_name', 'security_domain', 'path', 'port', 'protocol_type', 'authentication_type']:
            if getattr(self, k):
                props.append('%s=%s' % (k, repr(getattr(self, k))))

        return '%s(%s)' % (self.__class__.__name__, (', ').join(props))


class SecKeychainAttribute(ctypes.Structure):
    """Contains keychain attributes

    tag:    A 4-byte attribute tag.
    length: The length of the buffer pointed to by data.
    data:   A pointer to the attribute data.
    """
    _fields_ = [
     (
      'tag', ctypes.c_uint32),
     (
      'length', ctypes.c_uint32),
     (
      'data', ctypes.c_char_p)]


class SecKeychainAttributeList(ctypes.Structure):
    """Represents a list of keychain attributes

    count:  An unsigned 32-bit integer that represents the number of keychain attributes in the array.
    attr:   A pointer to the first keychain attribute in the array.
    """
    _fields_ = [
     (
      'count', ctypes.c_uint),
     (
      'attr', ctypes.POINTER(SecKeychainAttribute))]


class SecKeychainAttributeInfo(ctypes.Structure):
    """Represents a keychain attribute as a pair of tag and format values.

    count:  The number of tag-format pairs in the respective arrays
    tag:    A pointer to the first attribute tag in the array
    format: A pointer to the first CSSM_DB_ATTRIBUTE_FORMAT in the array
    """
    _fields_ = [
     (
      'count', ctypes.c_uint),
     (
      'tag', ctypes.POINTER(ctypes.c_uint)),
     (
      'format', ctypes.POINTER(ctypes.c_uint))]


SecKeychainAttributeInfo_p = ctypes.POINTER(SecKeychainAttributeInfo)
SecKeychainAttributeList_p = ctypes.POINTER(SecKeychainAttributeList)