# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scripts/cnp_chargeback_sdk_setup.py
# Compiled at: 2018-06-03 18:49:03
from __future__ import absolute_import, division, print_function
import os, sys, tempfile, six
package_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, package_root)
from cnpsdk import utils

def ask_user():
    attrs = [
     'username',
     'password',
     'merchant_id',
     'url',
     'proxy',
     'print_xml',
     'neuter_xml']
    attr_dict = {'username': '', 
       'password': '', 
       'merchant_id': '', 
       'url': '', 
       'proxy': '', 
       'print_xml': 'n', 
       'neuter_xml': 'n'}
    attr_valid_dict = {'neuter_xml': {'y': True, 
                      'n': False}, 
       'print_xml': {'y': True, 
                     'n': False}}
    attr_des_dict = {'username': 'Presenter Username for online request', 
       'password': 'Presenter Password for online request', 
       'merchant_id': 'Your merchant_id:', 
       'url': 'URL for you online request', 
       'proxy': 'If you want to using https proxy, please input your proxy server address. Must start with "https://"', 
       'print_xml': 'Do you want to print xml in console? y for Yes, n for No.', 
       'neuter_xml': 'Do you want to hide sensitive data in printed xml? y for Yes, n for No.'}
    print(CC.bpurple('Vantiv eCommerce Chargeback SDK configuration!'))
    print('\nPlease enter values for the following settings (just press Enter to\naccept a default value, if one is given in brackets).')
    for attr in attrs:
        while True:
            print(gene_prompt(attr, attr_dict, attr_valid_dict, attr_des_dict))
            if six.PY3:
                x = input('')
            else:
                x = raw_input('')
            if not x:
                x = attr_dict[attr]
            if attr in attr_valid_dict:
                if x.lower() in attr_valid_dict[attr]:
                    x = attr_valid_dict[attr][x.lower()]
                else:
                    print('Invalid input for "%s" = "%s"' % (attr, x))
                    continue
            attr_dict[attr] = x
            break

    conf = utils.Configuration()
    for k in attr_dict:
        setattr(conf, k, attr_dict[k])

    print(CC.bgreen('Configurations have saved at: %s ' % conf.save()))
    print(CC.bpurple('Successful!'))


def gene_prompt(attr, attr_dict, attr_valid_dict, attr_des_dict):
    if attr_dict[attr]:
        if attr in attr_valid_dict:
            option_str = CC.bcyan('Please select from following options:\n')
            for k in attr_valid_dict[attr]:
                _opt = attr_valid_dict[attr][k]
                if isinstance(_opt, bool):
                    _opt = 'True' if _opt else 'False'
                option_str += '%s - %s\n' % (CC.bgreen(k), CC.byellow(_opt))

            prompt = '\n%s\n%s%s [%s]: ' % (
             CC.bcyan(attr_des_dict[attr]), option_str, CC.bred(attr), CC.bgreen(attr_dict[attr]))
        else:
            prompt = '\n%s\n%s [%s]: ' % (CC.bcyan(attr_des_dict[attr]), CC.bred(attr), attr_dict[attr])
    else:
        prompt = '\n%s\n%s: ' % (CC.bcyan(attr_des_dict[attr]), CC.bred(attr))
    return prompt


class CC:
    COLOR_OFF = '\x1b[0m'
    BLACK = '\x1b[0;30m'
    RED = '\x1b[0;31m'
    GREEN = '\x1b[0;32m'
    YELLOW = '\x1b[0;33m'
    BLUE = '\x1b[0;34m'
    PURPLE = '\x1b[0;35m'
    CYAN = '\x1b[0;36m'
    WHITE = '\x1b[0;37m'
    BBLACK = '\x1b[1;30m'
    BRED = '\x1b[1;31m'
    BGREEN = '\x1b[1;32m'
    BYELLOW = '\x1b[1;33m'
    BBLUE = '\x1b[1;34m'
    BPURPLE = '\x1b[1;35m'
    BCYAN = '\x1b[1;36m'
    BWHITE = '\x1b[1;37m'
    UBLACK = '\x1b[4;30m'
    URED = '\x1b[4;31m'
    UGREEN = '\x1b[4;32m'
    UYELLOW = '\x1b[4;33m'
    UBLUE = '\x1b[4;34m'
    UPURPLE = '\x1b[4;35m'
    UCYAN = '\x1b[4;36m'
    UWHITE = '\x1b[4;37m'

    @classmethod
    def black(cls, _str):
        return cls.BLACK + _str + cls.COLOR_OFF

    @classmethod
    def red(cls, _str):
        return cls.RED + _str + cls.COLOR_OFF

    @classmethod
    def green(cls, _str):
        return cls.GREEN + _str + cls.COLOR_OFF

    @classmethod
    def yellow(cls, _str):
        return cls.YELLOW + _str + cls.COLOR_OFF

    @classmethod
    def blue(cls, _str):
        return cls.BLUE + _str + cls.COLOR_OFF

    @classmethod
    def purple(cls, _str):
        return cls.PURPLE + _str + cls.COLOR_OFF

    @classmethod
    def cyan(cls, _str):
        return cls.CYAN + _str + cls.COLOR_OFF

    @classmethod
    def white(cls, _str):
        return cls.WHITE + _str + cls.COLOR_OFF

    @classmethod
    def ublack(cls, _str):
        return cls.UBLACK + _str + cls.COLOR_OFF

    @classmethod
    def ured(cls, _str):
        return cls.URED + _str + cls.COLOR_OFF

    @classmethod
    def ugreen(cls, _str):
        return cls.UGREEN + _str + cls.COLOR_OFF

    @classmethod
    def uyellow(cls, _str):
        return cls.UYELLOW + _str + cls.COLOR_OFF

    @classmethod
    def ublue(cls, _str):
        return cls.UBLUE + _str + cls.COLOR_OFF

    @classmethod
    def upurple(cls, _str):
        return cls.UPURPLE + _str + cls.COLOR_OFF

    @classmethod
    def ucyan(cls, _str):
        return cls.UCYAN + _str + cls.COLOR_OFF

    @classmethod
    def uwhite(cls, _str):
        return cls.UWHITE + _str + cls.COLOR_OFF

    @classmethod
    def bblack(cls, _str):
        return cls.BBLACK + _str + cls.COLOR_OFF

    @classmethod
    def bred(cls, _str):
        return cls.BRED + _str + cls.COLOR_OFF

    @classmethod
    def bgreen(cls, _str):
        return cls.BGREEN + _str + cls.COLOR_OFF

    @classmethod
    def byellow(cls, _str):
        return cls.BYELLOW + _str + cls.COLOR_OFF

    @classmethod
    def bblue(cls, _str):
        return cls.BBLUE + _str + cls.COLOR_OFF

    @classmethod
    def bpurple(cls, _str):
        return cls.BPURPLE + _str + cls.COLOR_OFF

    @classmethod
    def bcyan(cls, _str):
        return cls.BCYAN + _str + cls.COLOR_OFF

    @classmethod
    def bwhite(cls, _str):
        return cls.BWHITE + _str + cls.COLOR_OFF


def main(argv=sys.argv):
    ask_user()


if __name__ == '__main__':
    sys.exit(main(sys.argv))