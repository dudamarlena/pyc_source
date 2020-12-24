# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/imgtags/interfaces.py
# Compiled at: 2016-07-13 11:13:38
from zope.interface import Interface, Attribute
from ztfy.imgtags import _

class IBaseTagInfo(Interface):
    """Base pyexiv2 tag interface"""
    key = Attribute(_('Tag key code'))
    name = Attribute(_('Tag name'))
    description = Attribute(_('Tag description'))
    type = Attribute(_('Tag type'))


class IBaseTagWriter(Interface):
    """Base pyexiv2 tag writer interface"""
    value = Attribute(_('Tag value'))
    raw_value = Attribute(_('Tag raw value'))


class IExifTagInfo(IBaseTagInfo):
    """Base pyexiv2 EXIF tag interface"""
    label = Attribute(_('Tag label'))
    section_name = Attribute(_('Section name'))
    section_description = Attribute(_('Section description'))
    human_value = Attribute(_('Tag human value'))

    def contents_changed(self):
        """Check if tag contents changed"""
        pass


class IExifTagWriter(IBaseTagWriter):
    """Base pyexiv2 EXIF tag writer interface"""
    pass


class IExifTag(IExifTagInfo, IExifTagWriter):
    """Pyexiv2 EXIF tag interface"""
    pass


class IIptcTagInfo(IBaseTagInfo):
    """Base pyexiv2 IPTC tag interface"""
    title = Attribute(_('Tag title'))
    photoshop_name = Attribute(_('Photoshop name'))
    record_name = Attribute(_('Tag record name'))
    record_description = Attribute(_('Tag record description'))
    repeatable = Attribute(_('Repeatable tag ?'))

    def contents_changed(self):
        """Check if tag contents changed"""
        pass


class IIptcTagWriter(IBaseTagWriter):
    """Base pyexiv2 IPTC tag writer interface"""
    values = Attribute(_('Tag values'))
    raw_values = Attribute(_('Tag raw values'))


class IIptcTag(IIptcTagInfo, IIptcTagWriter):
    """Pyexiv2 IPTC tag interface"""
    pass


class IXmpTagInfo(IBaseTagInfo):
    """Base pyexiv2 XMP tag interface"""
    title = Attribute(_('Tag title'))


class IXmpTagWriter(IBaseTagWriter):
    """Base pyexiv2 XMP tag writer interface"""
    pass


class IXmpTag(IXmpTagInfo, IXmpTagWriter):
    """Pyexiv2 XMP tag interface"""
    pass


class IImageTags(Interface):
    """Image tags interface"""
    metadata = Attribute(_('Raw metadata'))

    def getExifKeys(self):
        """Get keys of used EXIF tags"""
        pass

    def getExifTags(self):
        """Get key/tag dict of used EXIF tags"""
        pass

    def getIptcKeys(self):
        """Get keys of used IPTC tags"""
        pass

    def getIptcTags(self):
        """Get key/tag dict of used IPTC tags"""
        pass

    def getXmpKeys(self):
        """Get keys of used XMP tags"""
        pass

    def getXmpTags(self):
        """Get key/tag dict of used XMP tags"""
        pass

    def getKeys(self):
        """Get keys of all used tags"""
        pass

    def getTags(self):
        """Get key/tag dict of all used tags"""
        pass

    def getTag(self, key):
        """Get tag for given key
        
        Key can also be a list or tuple, in which case given tags are
        checked until one of them is not null
        """
        pass

    def setTag(self, key, value, raw=False):
        """Set value of given tag"""
        pass

    def getGPSLocation(self, precision=None):
        """Get GPS coordinates in WGS84 projection system"""
        pass

    def flush(self):
        """Write modified tags to image"""
        pass


class IImageTagString(Interface):
    """Image tag string representation interface"""

    def toString(self, encoding='utf-8'):
        """Render tag as string
        
        Returns a tuple containing tag name and tag value
        """
        pass


class IImageTagIndexValue(Interface):
    """Get index value for a given tag"""

    def __getattr__(self, attr):
        """Get indexed value for given tag"""
        pass