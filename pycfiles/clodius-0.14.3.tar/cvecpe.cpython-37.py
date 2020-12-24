# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/detector/cvecpe.py
# Compiled at: 2020-02-24 23:28:40
# Size of source mod 2**32: 3988 bytes


def cpe_parse(cpe23_uri):
    """

    :param cpe23_uri:
    :return:
    """
    result = {'vendor':'', 
     'product':'', 
     'version':'', 
     'update':'', 
     'edition':'', 
     'language':'', 
     'sw_edition':'', 
     'target_sw':'', 
     'target_hw':'', 
     'other':''}
    try:
        if cpe23_uri:
            part = cpe23_uri.split(':')
            result['vendor'] = part[3]
            result['product'] = part[4]
            result['version'] = part[5]
            result['update'] = part[6]
            result['edition'] = part[7]
            result['language'] = part[8]
            result['sw_edition'] = part[9]
            result['target_sw'] = part[10]
            result['target_hw'] = part[11]
            result['other'] = part[12]
        return result
    except Exception as ex:
        try:
            import traceback
            traceback.print_exc()
        finally:
            ex = None
            del ex


def cpe_compare_version(rule_version, rule_update, conf_version):
    """
    :param rule_version:
    :param rule_update:
    :param conf_version:
    :return:
    """
    rule_version = rule_version.lower()
    rule_update = rule_update.lower()
    conf_version = conf_version.lower()
    result = False
    try:
        if rule_version in conf_version:
            if '*' not in rule_update:
                conf_version_sub = conf_version[len(rule_version):]
                if conf_version_sub[0] in ('.', ):
                    conf_version_sub = conf_version_sub[1:]
                for i in range(0, len(rule_update)):
                    if conf_version_sub[i] != rule_update[i]:
                        conf_version_sub_suffix = conf_version_sub[i:]
                        if rule_update.endswith(conf_version_sub_suffix):
                            result = True
                            break

    except IndexError as ex:
        try:
            pass
        finally:
            ex = None
            del ex

    return result


class Cpe23Info(object):

    def __init__(self, **kwargs):
        """

        :param uri:
        """
        self._uri = kwargs.get('uri')
        self._cve_info = kwargs.get('cve')
        self._cpe_version = '2.3'
        self._vendor = kwargs.get('vendor')
        self._product = kwargs.get('product')
        self._version = kwargs.get('version')
        self._update = kwargs.get('update')
        if self._cve_info:
            self._cve = self._cve_info.cve
        else:
            self._cve = ''

    def __str__(self):
        return {'cve':self._cve, 
         'vendor':self._vendor, 
         'product':self._product, 
         'version':self._version, 
         'update':self._update}

    @property
    def uri(self):
        return self._uri

    @property
    def cve_info(self):
        return self._cve_info

    @property
    def cve(self):
        return self._cve

    @property
    def cpe_version(self):
        return self._cpe_version

    @property
    def vendor(self):
        return self._vendor

    @property
    def product(self):
        return self._product.lower()

    @property
    def version(self):
        return self._version

    @property
    def update(self):
        return self._update

    def compare(self, vendor, product, version):
        """

        :param vendor:
        :param product:
        :param version:
        :return:
        """
        result = False
        if self.version:
            if product:
                if product.lower() == self.product.lower():
                    if vendor:
                        if self._vendor.lower() not in vendor.lower():
                            return False
                    else:
                        if self.version == version.lower():
                            result = True
                        result = result or cpe_compare_version(rule_version=(self.version),
                          rule_update=(self.update),
                          conf_version=version)
        return result