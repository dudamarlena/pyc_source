# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywurfl/__init__.py
# Compiled at: 2011-01-06 14:57:38
"""
pywurfl - Python tools for processing and querying the Wireless Universal Resource File (WURFL)
"""
import re, hashlib, warnings
from copy import copy
from pywurfl.exceptions import WURFLException, ActualDeviceRootNotFound, DeviceNotFound, ExistsException
from pywurfl.algorithms.wurfl import normalizers
__author__ = 'Armand Lynch <lyncha@users.sourceforge.net>'
__contributors__ = 'Pau Aliagas <pau@newtral.org>'
__copyright__ = 'Copyright 2006-2011, Armand Lynch'
__license__ = 'LGPL'
__url__ = 'http://celljam.net/'
__version__ = '7.2.1'
__all__ = ['devclass', 'Devices']

class RootDevice(object):
    """
    pywurfl Root Device base class.

    All classes created by pywurfl are at root a subclass of this class.
    """
    pass


def devclass(parent, devid, devua, actual_device_root, new_caps=None):
    """
    Return a pywurfl.Device class.

    @param parent: A Device class or None.
    @type parent: Device
    @param devid: The device id for the returned class.
    @type devid: unicode
    @param devua: The user agent for the returned class.
    @type devua: unicode
    @param actual_device_root: Whether or not the returned class is an actual
                               device.
    @type actual_device_root: boolean
    @param new_caps: The new capabilities for the returned class.
    @type new_caps: dict
    """
    if parent is None:

        class Device(RootDevice):
            """pywurfl Generic Device"""

            def __iter__(self):
                for group in sorted(self.groups.keys()):
                    for capability in sorted(self.groups[group]):
                        yield (
                         group, capability, getattr(self, capability))

            def __str__(self):
                s = []
                s.append('User Agent: %s\n' % self.devua)
                s.append('WURFL ID: %s\n' % self.devid)
                s.append('Fallbacks: ')
                fbs = []
                base_class = self.__class__.__bases__[0]
                while base_class is not RootDevice:
                    fbs.append(base_class.devid)
                    base_class = base_class.__bases__[0]

                s.append('%s\n' % fbs)
                s.append('Actual Device Root: %s\n\n' % self.actual_device_root)
                for group in sorted(self.groups.keys()):
                    s.append('%s\n' % group.upper())
                    for cap in sorted(self.groups[group]):
                        attr = getattr(self, cap)
                        if isinstance(attr, basestring):
                            attr = attr.encode('ascii', 'xmlcharrefreplace')
                        s.append('%s: %s\n' % (cap, attr))

                    s.append('\n')

                return ('').join(s)

        Device.fall_back = 'root'
        Device.groups = {}
    else:

        class Device(parent):
            """pywurfl Device"""
            pass

        parent.children.add(Device)
        Device.fall_back = parent.devid
    if new_caps is not None:
        for (name, value) in new_caps.iteritems():
            setattr(Device, name, value)

    Device.devid = devid
    Device.devua = devua
    Device.children = set()
    Device.actual_device_root = actual_device_root
    return Device


class Devices(object):
    """
    Main pywurfl API class.
    """

    def __init__(self):
        self.devids = {}
        self.devuas = {}
        self._name_test_re = re.compile('^(_|[a-z])(_|[a-z]|[0-9])+$')

    def find_actual_root(self, device=RootDevice):
        """
        Find an actual device root.

        @param device: A Device class.
        @type device: Device class
        @raise ActualDeviceNotFound:
        """
        while device is not RootDevice:
            if device.actual_device_root:
                return device
            device = device.__bases__[0]

        raise ActualDeviceRootNotFound

    def select_ua(self, devua, actual_device_root=False, normalize=None, search=None, instance=True):
        """
        Return a Device object based on the user agent.

        @param devua: The device user agent to search for.
        @type devua: unicode
        @param actual_device_root: Return a device that is an actual device
                                   root
        @type actual_device_root: boolean
        @param normalize: Deprecated
        @type normalize: None
        @param search: The algorithm to use for searching. If 'search' is None,
                       a search will not be performed.
        @type search: pywurfl.Algorithm
        @param instance: Used to select that you want an instance instead of a
                         class object.
        @type instance: boolean
        @raise DeviceNotFound:
        """
        _unicode_check('devua', devua)
        if normalize is not None:
            warnings.warn('use of the `normalize` argument in select_ua is deprecated', DeprecationWarning)
        if search is not None and not hasattr(search, 'use_normalized_ua'):
            warnings.warn('search algorithm object should have a `use_normalized_ua` boolean attribute.', FutureWarning)
            search.use_normalized_ua = True
        devua = devua.strip()
        device = self.devuas.get(devua)
        if device is None:
            norm_devua = normalizers.generic(devua)
            device = self.devuas.get(norm_devua)
            if device is None and search is not None:
                if search.use_normalized_ua:
                    device = search(norm_devua, self)
                else:
                    device = search(devua, self)
        if device is not None:
            if actual_device_root:
                device = self.find_actual_root(device)
            if instance:
                return device()
            return device
        else:
            raise DeviceNotFound(devua)
        return

    def select_id(self, devid, actual_device_root=False, instance=True):
        """
        Return a Device object based on the WURFL ID.

        @param devid: The WURFL id to search for.
        @type devid: unicode
        @param actual_device_root: Return a device that is an actual device
                                   root.
        @param instance: Used to select that you want an instance instead of a
                         class.
        @type instance: boolean
        @raise DeviceNotFound:
        """
        _unicode_check('devid', devid)
        if devid in self.devids:
            device = self.devids.get(devid)
            if actual_device_root:
                device = self.find_actual_root(device)
            if instance:
                return device()
            return device
        else:
            raise DeviceNotFound(devid)

    def add_group(self, group):
        """
        Add a group to the WURFL class hierarchy
        @param group: The group's name. The group name should match this regexp
                      ^(_|[a-z])(_|[a-z]|[0-9])+$
        @type group: unicode
        """
        _unicode_check('group', group)
        self._name_test('group', group)
        if group not in self.devids['generic'].groups:
            self.devids['generic'].groups[group] = []
        else:
            raise ExistsException("'%s' group exists" % group)

    def remove_group(self, group):
        """
        Remove a group and all its capabilities from the WURFL class hierarchy
        @param group: The group name. The group name should match this
                      regex '^[a-z]+(_|[a-z])+$' and be unique.
        @type group: unicode
        """
        _unicode_check('group', group)
        if group not in self.devids['generic'].groups:
            raise WURFLException("'%s' group not found" % group)
        caps = self.devids['generic'].groups[group]
        generic = self.devids['generic']
        for cap in caps:
            self._remove_capability(generic, cap)

        del self.devids['generic'].groups[group]

    def _remove_capability(self, device, capability):
        if capability in device.__dict__:
            delattr(device, capability)
        for child in device.children:
            self._remove_capability(child, capability)

    def _remove_tree(self, devid):
        device = self.devids[devid]
        for child in copy(device.children):
            self._remove_tree(child.devid)

        del self.devids[device.devid]
        del self.devuas[device.devua]

    def add_capability(self, group, capability, default):
        """
        Add a capability to the WURFL class hierarchy
        @param group: The group name. The group name should match this
                      regex ^(_|[a-z])(_|[a-z]|[0-9])+$
        @type group: unicode
        @param capability: The capability name. The capability name should match
                           this regex ^(_|[a-z])(_|[a-z]|[0-9])+$' and be
                           unique amongst all capabilities.
        @type capability: unicode
        """
        _unicode_check('group', group)
        _unicode_check('capability', capability)
        _unicode_check('default', default)
        try:
            self.add_group(group)
        except ExistsException:
            pass

        self._name_test('capability', capability)
        for (grp, caps) in self.devids['generic'].groups.iteritems():
            if capability in caps:
                raise ExistsException("'%s' capability exists in group '%s'" % (
                 capability, grp))
        else:
            self.devids['generic'].groups[group].append(capability)
            setattr(self.devids['generic'], capability, default)

    def remove_capability(self, capability):
        """
        Remove a capability from the WURFL class hierarchy
        @param capability: The capability name.
        @type capability: unicode
        """
        _unicode_check('capability', capability)
        for group in self.devids['generic'].groups:
            if capability in self.devids['generic'].groups[group]:
                break
        else:
            raise WURFLException("'%s' capability not found" % capability)

        generic = self.devids['generic']
        self._remove_capability(generic, capability)
        self.devids['generic'].groups[group].remove(capability)

    def add(self, parent, devid, devua, actual_device_root=False, capabilities=None):
        """
        Add a device to the WURFL class hierarchy

        @param parent: A WURFL ID.
        @type parent: unicode
        @param devid: The device id for the new device.
        @type devid: unicode
        @param devua: The user agent for the new device.
        @type devua: unicode
        @param actual_device_root: Whether or not the new device is an
                                   actual device.
        @type actual_device_root: boolean
        @param capabilities: The new capabilities for the new device class.
        @type capabilities: dict
        """
        _unicode_check('parent', parent)
        _unicode_check('devid', devid)
        _unicode_check('devua', devua)
        if parent not in self.devids:
            raise DeviceNotFound(parent)
        if devid in self.devids:
            raise ExistsException("'%s' device already exists" % devid)
        elif devua in self.devuas:
            dup_devid = self.devuas[devua].devid
            raise ExistsException("'%s' duplicate user agent with '%s'" % (
             devua, dup_devid))
        self.devids[devid] = devclass(self.devids[parent], devid, devua, actual_device_root, capabilities)
        self.devuas[devua] = self.devids[devid]

    def insert_before(self, child, devid, devua, actual_device_root=False, capabilities=None):
        """
        Create and insert a device before another. The parent of the inserted
        device becomes the parent of the child device. The child device's
        parent is changed to the inserted device.

        @param child: A WURFL ID. The child device cannot be the generic
                      device.
        @type child: unicode
        @param devid: The device id for the new device.
        @type devid: unicode
        @param devua: The user agent for the new device.
        @type devua: unicode
        @param actual_device_root: Whether or not the new device is an
                                   actual device.
        @type actual_device_root: boolean
        @param capabilities: The new capabilities for the new device class.
        @type capabilities: dict
        """
        _unicode_check('child', child)
        _unicode_check('devid', devid)
        _unicode_check('devua', devua)
        if child == 'generic':
            raise WURFLException('cannot insert device before generic device')
        if child not in self.devids:
            raise DeviceNotFound(child)
        if devid in self.devids:
            raise ExistsException("'%s' device already exists" % devid)
        elif devua in self.devuas:
            dup_devid = self.devuas[devua].devid
            raise ExistsException("'%s' duplicate user agent with '%s'" % (
             devua, dup_devid))
        child_device = self.devids[child]
        parent_device = child_device.__bases__[0]
        new_device = devclass(parent_device, devid, devua, actual_device_root, capabilities)
        parent_device.children.remove(child_device)
        new_device.children.add(child_device)
        child_device.__bases__ = (new_device,)
        child_device.fall_back = devid
        self.devids[devid] = new_device
        self.devuas[devua] = self.devids[devid]

    def insert_after(self, parent, devid, devua, actual_device_root=False, capabilities=None):
        """
        Create and insert a device after another. The parent of the inserted
        device becomes the parent argument. The children of the parent device
        become the children of the inserted device then the parent device's
        children attribute is to the inserted device.

        @param parent: A WURFL ID.
        @type parent: unicode
        @param devid: The device id for the new device.
        @type devid: unicode
        @param devua: The user agent for the new device.
        @type devua: unicode
        @param actual_device_root: Whether or not the new device is an
                                   actual device.
        @type actual_device_root: boolean
        @param capabilities: The new capabilities for the new device class.
        @type capabilities: dict
        """
        _unicode_check('parent', parent)
        _unicode_check('devid', devid)
        _unicode_check('devua', devua)
        if parent not in self.devids:
            raise DeviceNotFound(parent)
        if devid in self.devids:
            raise ExistsException("'%s' device already exists" % devid)
        elif devua in self.devuas:
            dup_devid = self.devuas[devua].devid
            raise ExistsException("'%s' duplicate user agent with '%s'" % (
             devua, dup_devid))
        parent_device = self.devids[parent]
        new_device = devclass(parent_device, devid, devua, actual_device_root, capabilities)
        new_device.children = parent_device.children
        new_device.children.remove(new_device)
        parent_device.children = set([new_device])
        for child_device in new_device.children:
            child_device.__bases__ = (new_device,)
            child_device.fall_back = devid

        self.devids[devid] = new_device
        self.devuas[devua] = self.devids[devid]

    def remove(self, devid):
        """
        Remove a device from the WURFL class hierarchy

        @param devid: A WURFL ID. The generic device cannot be removed.
        @type devid: unicode
        """
        _unicode_check('devid', devid)
        if devid not in self.devids:
            raise DeviceNotFound(devid)
        if devid == 'generic':
            raise WURFLException('cannot remove generic device')
        device = self.devids[devid]
        parent_device = device.__bases__[0]
        for cls in device.children:
            cls.__bases__ = device.__bases__
            parent_device.children.add(cls)
            cls.fall_back = parent_device.devid

        parent_device.children.remove(device)
        del self.devids[device.devid]
        del self.devuas[device.devua]

    def remove_tree(self, devid):
        """
        Remove a device and all of its children from the WURFL class hierarchy

        @param devid: A WURFL ID. The generic device cannot be removed.
        @type devid: unicode
        """
        _unicode_check('devid', devid)
        if devid not in self.devids:
            raise DeviceNotFound(devid)
        if devid == 'generic':
            raise WURFLException('cannot remove generic device')
        device = self.devids[devid]
        self._remove_tree(devid)
        parent_device = device.__bases__[0]
        parent_device.children.remove(device)

    @property
    def groups(self):
        """
        Yields all group names
        """
        return self.devids['generic'].groups.iterkeys()

    def _capability_generator(self, return_groups=False):
        for group in self.devids['generic'].groups:
            for capability in self.devids['generic'].groups[group]:
                if return_groups:
                    yield (
                     group, capability)
                else:
                    yield capability

    @property
    def capabilities(self):
        """
        Yields all capability names
        """
        for capability in self._capability_generator():
            yield capability

    @property
    def grouped_capabilities(self):
        """
        Yields the tuple (group, capability) for all capabilities
        """
        for grp_cap in self._capability_generator(return_groups=True):
            yield grp_cap

    @property
    def ids(self):
        """
        Return an iterator of all WURFL device ids
        """
        return self.devids.iterkeys()

    @property
    def uas(self):
        """
        Return an iterator of all device user agents
        """
        return self.devuas.iterkeys()

    @property
    def md5_hexdigest(self):
        """
        Return MD5 hex digest for all WURFL data
        """
        data = (str(self.devids[x]()) for x in sorted(self.devids))
        return hashlib.md5(('').join(data)).hexdigest()

    def __iter__(self):
        return self.devids.__iter__()

    def __len__(self):
        return len(self.devids)

    def _normalize_types(self):
        type_set = set()
        common_caps = ['actual_device_root', 'children', 'devid', 'devua',
         'groups', 'fall_back']
        for device in self.devids.itervalues():
            for cap in (c for c in device.__dict__ if c not in common_caps if not c.startswith('_')):
                if isinstance(getattr(device, cap), unicode):
                    type_set.add((cap, unicode))
                    try:
                        type_set.remove((cap, float))
                    except KeyError:
                        pass
                    else:
                        try:
                            type_set.remove((cap, int))
                        except KeyError:
                            pass
                        else:
                            try:
                                type_set.remove((cap, bool))
                            except KeyError:
                                pass

                elif isinstance(getattr(device, cap), float):
                    if (
                     cap, unicode) not in type_set:
                        type_set.add((cap, float))
                        try:
                            type_set.remove((cap, int))
                        except KeyError:
                            pass
                        else:
                            try:
                                type_set.remove((cap, bool))
                            except KeyError:
                                pass

                elif isinstance(getattr(device, cap), int):
                    if (
                     cap, unicode) not in type_set and (
                     cap, float) not in type_set:
                        if isinstance(getattr(device, cap), bool):
                            if (
                             cap, int) not in type_set:
                                type_set.add((cap, bool))
                        else:
                            type_set.add((cap, int))
                            try:
                                type_set.remove((cap, bool))
                            except KeyError:
                                pass

        conv_dict = {}
        for (cap, cap_type) in type_set:
            conv_dict[cap] = cap_type

        for device in self.devids.itervalues():
            for cap in conv_dict:
                if cap in device.__dict__:
                    setattr(device, cap, conv_dict[cap](device.__dict__[cap]))

    def _name_test(self, name, value):
        if not self._name_test_re.match(value):
            msg = "%s '%s' does not conform to regexp "
            msg += "r'^(_|[a-z])(_|[a-z]|[0-9])+$'"
            raise WURFLException(msg % (name, value))


def _unicode_check(name, val):
    if isinstance(val, basestring):
        if isinstance(val, str):
            raise UnicodeError("argument '%s' must be a unicode string" % name)