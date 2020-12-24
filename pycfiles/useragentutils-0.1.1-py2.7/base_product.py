# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/base_product.py
# Compiled at: 2013-01-04 21:01:37
from utilities import Enum, EnumValue, setProperties
from version import Version
import re

def rgxFindAnyCaseInsensitive(arr):
    arr = arr or []
    return re.compile(('|').join(map(re.escape, arr)), re.I)


class BaseProduct(Enum):
    required = [
     'manufacturer', 'parent', 'versionId', 'name', 'aliases', 'exclude', 'versionRegexString']

    def __init__(self, **kwargs):
        required = self.required
        required.extend(BaseProduct.required)
        for arg in required:
            if arg not in kwargs:
                raise Exception('Missing required arg: ' + arg)

        setProperties(self, **kwargs)
        self.id = (self.manufacturer.id << 8) + self.versionId
        self.children = []
        if self.parent:
            self.parent.children.append(self)
        self._versionRegEx = re.compile(self.versionRegexString) if self.versionRegexString else None
        self.aliasRgx = rgxFindAnyCaseInsensitive(self.aliases)
        if self.exclude:
            self.excludeRgx = rgxFindAnyCaseInsensitive(self.exclude)
        return

    @property
    def group(self):
        if self.parent:
            return self.parent.group
        return self

    @property
    def versionRegEx(self):
        if self._versionRegEx:
            return self._versionRegEx
        else:
            if self.group is not self:
                return self.group.versionRegEx
            return

    def version(self, userAgentString):
        pattern = self.versionRegEx
        if userAgentString and pattern:
            match = pattern.search(userAgentString)
            if match:
                full, major = match.group(1, 2)
                minor = match.group(3) if len(match.groups()) > 2 else '0'
                return Version(full, major, minor)

    def isInUserAgentString(self, userAgentString):
        return self.aliasRgx.search(userAgentString)

    def containsExcludeToken(self, userAgentString):
        if hasattr(self, 'excludeRgx'):
            return self.excludeRgx.search(userAgentString)

    def checkUserAgent(self, userAgentString):
        if self.isInUserAgentString(userAgentString):
            for child in self.children:
                value = child.checkUserAgent(userAgentString)
                if value:
                    return value

            if not self.containsExcludeToken(userAgentString):
                return self

    @classmethod
    def parseUserAgentString(self, userAgentString):
        for value in self.values:
            if not value.parent:
                value = value.checkUserAgent(userAgentString)
                if value:
                    return value

        return self.UNKNOWN