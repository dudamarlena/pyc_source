# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/ofxclient/cli.py
# Compiled at: 2017-04-21 11:10:37
from __future__ import absolute_import
from __future__ import unicode_literals
import argparse, getpass, io, logging, os, os.path, sys
from ofxhome import OFXHome
from ofxclient.account import BankAccount, BrokerageAccount, CreditCardAccount
from ofxclient.config import OfxConfig
from ofxclient.institution import Institution
from ofxclient.util import combined_download
from ofxclient.client import DEFAULT_OFX_VERSION
AUTO_OPEN_DOWNLOADS = 1
DOWNLOAD_DAYS = 30
GlobalConfig = None

def run():
    global GlobalConfig
    parser = argparse.ArgumentParser(prog=b'ofxclient')
    parser.add_argument(b'-a', b'--account')
    parser.add_argument(b'-d', b'--download', type=argparse.FileType(b'wb', 0))
    parser.add_argument(b'-o', b'--open', action=b'store_true')
    parser.add_argument(b'-v', b'--verbose', action=b'store_true')
    parser.add_argument(b'-c', b'--config', help=b'config file path')
    parser.add_argument(b'--download-days', default=DOWNLOAD_DAYS, type=int, help=b'number of days to download (default: %s)' % DOWNLOAD_DAYS)
    parser.add_argument(b'--ofx-version', default=DEFAULT_OFX_VERSION, type=int, help=b'ofx version to use for new accounts (default: %s)' % DEFAULT_OFX_VERSION)
    args = parser.parse_args()
    if args.config:
        GlobalConfig = OfxConfig(file_name=args.config)
    else:
        GlobalConfig = OfxConfig()
    accounts = GlobalConfig.accounts()
    account_ids = [ a.local_id() for a in accounts ]
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if args.download:
        if accounts:
            if args.account:
                a = GlobalConfig.account(args.account)
                ofxdata = a.download(days=args.download_days)
            else:
                ofxdata = combined_download(accounts, days=args.download_days)
            args.download.write(ofxdata.read())
            if args.open:
                open_with_ofx_handler(args.download.name)
            sys.exit(0)
        else:
            print b'no accounts configured'
    main_menu(args)


def main_menu(args):
    while 1:
        menu_title(b'Main\nEdit %s to\nchange descriptions or ofx options' % GlobalConfig.file_name)
        accounts = GlobalConfig.accounts()
        for idx, account in enumerate(accounts):
            menu_item(idx, account.long_description())

        menu_item(b'A', b'Add an account')
        if accounts:
            menu_item(b'D', b'Download all combined')
        menu_item(b'Q', b'Quit')
        choice = prompt().lower()
        if choice == b'a':
            add_account_menu(args)
        elif choice == b'd':
            if not accounts:
                print b'no accounts on file'
            else:
                ofxdata = combined_download(accounts, days=args.download_days)
                wrote = write_and_handle_download(ofxdata, b'combined_download.ofx')
                print b'wrote: %s' % wrote
        else:
            if choice in ('q', ''):
                return
            if int(choice) < len(accounts):
                account = accounts[int(choice)]
                view_account_menu(account, args)


def add_account_menu--- This code section failed: ---

 L. 102         0  LOAD_GLOBAL           0  'menu_title'
                3  LOAD_CONST               'Add account'
                6  CALL_FUNCTION_1       1  None
                9  POP_TOP          

 L. 103        10  SETUP_LOOP          279  'to 292'

 L. 104        13  LOAD_CONST               '------'
               16  PRINT_ITEM       
               17  PRINT_NEWLINE_CONT

 L. 105        18  LOAD_CONST               'Notice'
               21  PRINT_ITEM       
               22  PRINT_NEWLINE_CONT

 L. 106        23  LOAD_CONST               '------'
               26  PRINT_ITEM       
               27  PRINT_NEWLINE_CONT

 L. 107        28  LOAD_CONST               'You are about to search for bank connection information'
               31  PRINT_ITEM       
               32  PRINT_NEWLINE_CONT

 L. 108        33  LOAD_CONST               'on a third party website.  This means you are trusting'
               36  PRINT_ITEM       
               37  PRINT_NEWLINE_CONT

 L. 109        38  LOAD_CONST               'http://ofxhome.com and their security policies.'
               41  PRINT_ITEM       
               42  PRINT_NEWLINE_CONT

 L. 110        43  LOAD_CONST               ''
               46  PRINT_ITEM       
               47  PRINT_NEWLINE_CONT

 L. 111        48  LOAD_CONST               'You will be sending your bank name to this website.'
               51  PRINT_ITEM       
               52  PRINT_NEWLINE_CONT

 L. 112        53  LOAD_CONST               '------'
               56  PRINT_ITEM       
               57  PRINT_NEWLINE_CONT

 L. 113        58  LOAD_GLOBAL           1  'prompt'
               61  LOAD_CONST               'bank name eg. "express" (enter to exit)> '
               64  CALL_FUNCTION_1       1  None
               67  STORE_FAST            1  'query'

 L. 114        70  LOAD_FAST             1  'query'
               73  LOAD_ATTR             2  'lower'
               76  CALL_FUNCTION_0       0  None
               79  LOAD_CONST               ('',)
               82  COMPARE_OP            6  in
               85  POP_JUMP_IF_FALSE    92  'to 92'

 L. 115        88  LOAD_CONST               None
               91  RETURN_END_IF    
             92_0  COME_FROM            85  '85'

 L. 117        92  LOAD_GLOBAL           3  'OFXHome'
               95  LOAD_ATTR             4  'search'
               98  LOAD_FAST             1  'query'
              101  CALL_FUNCTION_1       1  None
              104  STORE_FAST            2  'found'

 L. 118       107  LOAD_FAST             2  'found'
              110  POP_JUMP_IF_TRUE    129  'to 129'

 L. 119       113  LOAD_GLOBAL           5  'error'
              116  LOAD_CONST               'No banks found'
              119  CALL_FUNCTION_1       1  None
              122  POP_TOP          

 L. 120       123  CONTINUE             13  'to 13'
              126  JUMP_FORWARD          0  'to 129'
            129_0  COME_FROM           126  '126'

 L. 122       129  SETUP_LOOP          156  'to 288'

 L. 123       132  SETUP_LOOP           43  'to 178'
              135  LOAD_GLOBAL           6  'enumerate'
              138  LOAD_FAST             2  'found'
              141  CALL_FUNCTION_1       1  None
              144  GET_ITER         
              145  FOR_ITER             29  'to 177'
              148  UNPACK_SEQUENCE_2     2 
              151  STORE_FAST            3  'idx'
              154  STORE_FAST            4  'bank'

 L. 124       157  LOAD_GLOBAL           7  'menu_item'
              160  LOAD_FAST             3  'idx'
              163  LOAD_FAST             4  'bank'
              166  LOAD_CONST               'name'
              169  BINARY_SUBSCR    
              170  CALL_FUNCTION_2       2  None
              173  POP_TOP          
              174  JUMP_BACK           145  'to 145'
              177  POP_BLOCK        
            178_0  COME_FROM           132  '132'

 L. 125       178  LOAD_GLOBAL           1  'prompt'
              181  CALL_FUNCTION_0       0  None
              184  LOAD_ATTR             2  'lower'
              187  CALL_FUNCTION_0       0  None
              190  STORE_FAST            5  'choice'

 L. 126       193  LOAD_FAST             5  'choice'
              196  LOAD_CONST               ('q', '')
              199  COMPARE_OP            6  in
              202  POP_JUMP_IF_FALSE   209  'to 209'

 L. 127       205  LOAD_CONST               None
              208  RETURN_END_IF    
            209_0  COME_FROM           202  '202'

 L. 128       209  LOAD_GLOBAL           8  'int'
              212  LOAD_FAST             5  'choice'
              215  CALL_FUNCTION_1       1  None
              218  LOAD_GLOBAL           9  'len'
              221  LOAD_FAST             2  'found'
              224  CALL_FUNCTION_1       1  None
              227  COMPARE_OP            0  <
              230  POP_JUMP_IF_FALSE   132  'to 132'

 L. 129       233  LOAD_GLOBAL           3  'OFXHome'
              236  LOAD_ATTR            10  'lookup'
              239  LOAD_FAST             2  'found'
              242  LOAD_GLOBAL           8  'int'
              245  LOAD_FAST             5  'choice'
              248  CALL_FUNCTION_1       1  None
              251  BINARY_SUBSCR    
              252  LOAD_CONST               'id'
              255  BINARY_SUBSCR    
              256  CALL_FUNCTION_1       1  None
              259  STORE_FAST            4  'bank'

 L. 130       262  LOAD_GLOBAL          11  'login_check_menu'
              265  LOAD_FAST             4  'bank'
              268  LOAD_FAST             0  'args'
              271  CALL_FUNCTION_2       2  None
              274  POP_JUMP_IF_FALSE   284  'to 284'

 L. 131       277  LOAD_CONST               None
              280  RETURN_VALUE     
              281  JUMP_BACK           132  'to 132'
              284  JUMP_BACK           132  'to 132'
              287  POP_BLOCK        
            288_0  COME_FROM           129  '129'
              288  JUMP_BACK            13  'to 13'
              291  POP_BLOCK        
            292_0  COME_FROM            10  '10'

Parse error at or near `POP_BLOCK' instruction at offset 287


def view_account_menu(account, args):
    while 1:
        menu_title(account.long_description())
        institution = account.institution
        client = institution.client()
        print b'Overview:'
        print b'  Name:           %s' % account.description
        print b'  Account Number: %s' % account.number_masked()
        print b'  Institution:    %s' % institution.description
        print b'  Main Type:      %s' % str(type(account))
        if hasattr(account, b'routing_number'):
            print b'  Routing Number: %s' % account.routing_number
            print b'  Sub Type:       %s' % account.account_type
        if hasattr(account, b'broker_id'):
            print b'  Broker ID:      %s' % account.broker_id
        print b'Nerdy Info:'
        print b'  Download Up To:        %s days' % args.download_days
        print b'  Username:              %s' % institution.username
        print b'  Local Account ID:      %s' % account.local_id()
        print b'  Local Institution ID:  %s' % institution.local_id()
        print b'  FI Id:                 %s' % institution.id
        print b'  FI Org:                %s' % institution.org
        print b'  FI Url:                %s' % institution.url
        if institution.broker_id:
            print b'  FI Broker Id:          %s' % institution.broker_id
        print b'  Client Id:             %s' % client.id
        print b'  App Ver:               %s' % client.app_version
        print b'  App Id:                %s' % client.app_id
        print b'  OFX Ver:               %s' % client.ofx_version
        print b'  Config File:           %s' % GlobalConfig.file_name
        menu_item(b'D', b'Download')
        choice = prompt().lower()
        if choice == b'd':
            out = account.download(days=args.download_days)
            wrote = write_and_handle_download(out, b'%s.ofx' % account.local_id())
            print b'wrote: %s' % wrote
        return


def login_check_menu(bank_info, args):
    print b'------'
    print b'Notice'
    print b'------'
    print b'You are about to test to make sure your username and password'
    print b'are correct.  This means you will be sending it to the URL below.'
    print b'If the URL does not appear to belong to your bank then you should'
    print b'exit this program by hitting CTRL-C.'
    print b'  bank name: %s' % bank_info[b'name']
    print b'  bank url:  %s' % bank_info[b'url']
    print b'------'
    while 1:
        username = b''
        while not username:
            username = prompt(b'username> ')

        password = b''
        prompt_text = b'password> '
        if os.name == b'nt' and sys.version_info < (3, 0):
            prompt_text = prompt_text.encode(b'utf8')
        while not password:
            password = getpass.getpass(prompt=prompt_text)

        i = Institution(id=bank_info[b'fid'], org=bank_info[b'org'], url=bank_info[b'url'], broker_id=bank_info[b'brokerid'], description=bank_info[b'name'], username=username, password=password, client_args={b'ofx_version': args.ofx_version})
        try:
            i.authenticate()
        except Exception as e:
            print b'authentication failed: %s' % e
            continue

        accounts = i.accounts()
        for a in accounts:
            GlobalConfig.add_account(a)

        GlobalConfig.save()
        return 1


def write_and_handle_download(ofx_data, name):
    outfile = io.open(name, b'w')
    outfile.write(ofx_data.read())
    outfile.close()
    if AUTO_OPEN_DOWNLOADS:
        open_with_ofx_handler(name)
    return os.path.abspath(name)


def prompt(text=b'choice> '):
    try:
        got = raw_input(text)
    except NameError:
        got = input(text)

    return got


def error(text=b''):
    print b'!! %s' % text


def menu_item(key, description):
    print b'(%s) %s' % (key, description)


def menu_title(name):
    print b'+----------------------------------'
    print b'%s' % name
    print b'+----------------------------------'


def open_with_ofx_handler(filename):
    import platform
    sysname = platform.system()
    if sysname == b'Darwin':
        os.system(b"/usr/bin/open '%s'" % filename)
    elif sysname == b'Windows':
        os.startfile(filename)
    else:
        os.system(b"xdg-open '%s'" % filename)


if __name__ == b'__main__':
    run()