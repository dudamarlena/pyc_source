# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangjiangfeng/Documents/IdeaProjects/baidu/bainuo-feed/FinBull/finbull/conf.py
# Compiled at: 2019-08-01 05:55:18
# Size of source mod 2**32: 5317 bytes
import os, io, finbull.error, validate
from configobj import ConfigObj

def _validator_is_dict(value):
    """
    extents for ConfigObj Vaildator
    """
    if not isinstance(value, dict):
        raise validate.VdtTypeError(value)
    return value


VALIDATOR = validate.Validator()
VALIDATOR.functions['dict'] = _validator_is_dict

class Conf(object):
    __doc__ = '\n    Huskar Conf Class\n    adapter for baidu idc\n    '
    _IDC_PREFIX = '.IDC_'
    _VALID_SUFFIX = '.valid'
    _ENCODEING = 'UTF-8'
    _INDENT_TYPE = None
    _conf = None

    def __init__(self, **kwargs):
        """
        super __init__
        """
        infile = kwargs['infile'] or None
        self._idc = kwargs['_idc'] if '_idc' in kwargs else None
        if self._idc is not None:
            del kwargs['_idc']
        else:
            kwargs['encoding'] = self._ENCODEING
            kwargs['default_encoding'] = self._ENCODEING
            kwargs['indent_type'] = self._INDENT_TYPE
            kwargs['write_empty_values'] = True
            if infile is not None:
                if isinstance(infile, str) and os.path.isfile(infile):
                    infile_valid = infile + self._VALID_SUFFIX
                    if os.path.isfile(infile_valid):
                        kwargs['infile'] = infile
                        kwargs['configspec'] = infile_valid
                        self._conf = ConfigObj(**kwargs)
                        test = self._conf.validate(VALIDATOR)
                        if test is not True:
                            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                              errmsg=('conf vaild failed.[%s]' % str(test)))
            else:
                raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                  errmsg=('can not find valid file for [%s] needed valid file [%s]' % (
                 infile, infile_valid)))
        if isinstance(infile, io.StringIO):
            if getattr(infile, 'read') is not None:
                self._conf = ConfigObj(**kwargs)
        if self._conf is None:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg=('conf is not found. [%s]' % infile))
        self._conf.walk((self._parse_idc), call_on_sections=True)

    def _parse_idc(self, section, key):
        """
        get the configuration by the current idc
        """
        value = section[key]
        if isinstance(value, dict):
            if len(value) > 0:
                keys = list(value.keys())
                cur_idc = self._IDC_PREFIX + self._idc
                idc_mode_keys = [x for x in keys if x.startswith(self._IDC_PREFIX)]
                if len(idc_mode_keys) > 0:
                    matches_idc = [x for x in idc_mode_keys if x == cur_idc]
                    if len(matches_idc) == 1:
                        section[key] = self._merge_dicts(section[key], value[cur_idc])
                        del section[key][cur_idc]
                    else:
                        raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                          errmsg=('useing idc mode, can not find matched idc[%s] in file[%s]' % (
                         cur_idc, self._conf.filename)))
                for k in keys:
                    if k.startswith(self._IDC_PREFIX) and k != cur_idc:
                        del section[key][k]

    def _merge_dicts(self, *dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)

        return result

    def __getitem__(self, key):
        """
        hack for __getitem__
        adapter for baidu idc
        """
        return self._conf.__getitem__(key)

    def __setitem__(self, key, value):
        """
        hack for __setitem__
        you CAN NOT set value to the configuration
        """
        pass

    def __repr__(self):
        """
        __repr__
        """
        return repr(self._conf)

    def __str__(self):
        """
        __str__
        """
        return str(self._conf)


if __name__ == '__main__':
    input_config = '\n    [s1]\n    author = dongliqiang\n    description = Test config\n\n    [s2]\n    [[.IDC_nj]]\n    key1 = aaa\n    [[.IDC_sh]]\n    key1 = bbb\n\n    [s3]\n    key3 = abc\n    [[s4]]\n    [[[.IDC_nj]]]\n    key2 = ccc\n    [[[.IDC_sh]]]\n    key2 = ddd\n    '
    conf = Conf(infile=(io.StringIO(input_config)), _idc='nj')
    print(conf, conf['s2'])