# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/detector/cvecpe.py
# Compiled at: 2019-12-10 04:52:13
import re

def cpe_parse(cpe23_uri):
    """

    :param cpe23_uri:
    :return:
    """
    vendor = ''
    product = ''
    version = ''
    update = ''
    try:
        if cpe23_uri:
            part = cpe23_uri.split(':')
            vendor = part[3]
            product = part[4]
            version = part[5]
            update = part[6]
        return (vendor.lower(), product.lower(), version.lower(), update.lower())
    except Exception as ex:
        print cpe23_uri
        import traceback
        traceback.print_exc()


def cpe_compare(**kwargs):
    """
    testcase: commons-httpclient, fastjson, jackson, httpclient
    :param kwargs:
    :return:
    """
    cpe_component_version = kwargs.get('cpe_component_version')
    cpe_component_update = kwargs.get('cpe_component_update')
    version_start_including = kwargs.get('version_start_including')
    version_end_including = kwargs.get('version_end_including')
    version_start_excluding = kwargs.get('version_start_excluding')
    version_end_excluding = kwargs.get('version_end_excluding')
    component_version = kwargs.get('component_version')
    result = False
    if not all((cpe_component_version, component_version)):
        component_version_bit = component_version.split('.')
        cpe_component_version_bit = cpe_component_version.split('.')
        version_start_including_bit = version_start_including.split('.')
        version_end_including_bit = version_end_including.split('.')
        version_start_excluding_bit = version_start_excluding.split('.')
        version_end_excluding_bit = version_end_excluding.split('.')
        if all((version_start_including, version_end_including, version_start_excluding, version_end_excluding)):
            if cpe_component_update == '*' and component_version_bit[0] == cpe_component_version_bit[0]:
                result = True
            elif cpe_component_update == '-':
                pass
    return result


class Cep23Info(object):

    def __init__(self, cve, note=None, risk=None):
        """

        :param cve:
        :param note:
        """
        self._cve = cve
        self._note = note
        self._risk = risk
        self._cpe_version = '2.3'
        self._vendor = ''
        self._product = ''
        self._version = []

    def __str__(self):
        return {'cve': self._cve, 
           'note': self._note, 
           'vendor': self._vendor, 
           'product': self._product, 
           'version_list': self._version}

    def load_cpe(self, cpe23_uri):
        """
        cpe:2.3:a:apache:http_server:2.0.32:beta:win32:*:*:*:*:*
        cpe:cpe_version:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other

        :param cpe23_uri:
        :return:
        """
        result = ''
        if cpe23_uri:
            part = cpe23_uri.split(':')
            version = part[5]
            update = part[6]
            if update not in ('*', '-') and version != '*':
                if not self._cpe_version:
                    self._cpe_version = part[1]
                if not self._vendor:
                    self._vendor = part[3]
                if not self._product:
                    self._product = part[4]
                self._version.append((
                 re.compile(('{0}[\\-\\.]+{1}').format(version.replace('-', '\\-'), update.replace('-', '\\-')), re.I),
                 ('{0}:{1}').format(version.lower(), update.lower())))
                result = ('{0}:{1}').format(version.lower(), update.lower())
            elif version and version != '*':
                self._version.append((version.lower(), version.lower()))
                result = version.lower()
        return result

    @property
    def cve(self):
        return self._cve

    @property
    def note(self):
        return self._note

    @property
    def cpe_version(self):
        return self._cpe_version

    @property
    def vendor(self):
        return self._vendor

    @property
    def risk(self):
        return self._risk

    @property
    def product(self):
        return self._product.lower()

    @property
    def version(self):
        return self._version

    def compare(self, product, version):
        """

        :param product:
        :param version:
        :return:
        """
        result = False
        if self.version:
            if product and product.strip().lower() == self.product:
                for item in self.version:
                    if isinstance(item[0], str) and item[0] == version.lower():
                        result = True
                        break
                    elif item[0].search(version):
                        result = True
                        break

                if not result:
                    for item in self.version:
                        _version, _update = item[1].split(':')
                        if _version in version and len(_version) < len(version):
                            sub = version[len(_version) + 1:]
                            for i in range(0, len(_update)):
                                if _update[i] != sub[i].lower():
                                    _ = sub[i:]
                                    if _update.endswith(_.lower()):
                                        result = True
                                        break

                            if result:
                                break

        return result