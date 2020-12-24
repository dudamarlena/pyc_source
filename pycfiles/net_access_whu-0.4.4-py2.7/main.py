# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/net_access/main.py
# Compiled at: 2016-10-31 06:37:52
from re import compile, DOTALL
import json, tempfile, os
from urllib2 import urlopen, HTTPCookieProcessor, build_opener
from cookielib import CookieJar
from urllib import urlencode
import sys
reload(sys)
sys.setdefaultencoding('utf8')
cookie = CookieJar()
opener = build_opener(HTTPCookieProcessor(cookie))

def std_write(thing):
    sys.stdout.write(('{}\r\n').format(thing))


try_url = 'http://www.baidu.com'
ip_port = ''

def downloader(url):
    try:
        handle = urlopen(url, timeout=5)
        return (str(handle.read()), handle.url)
    except Exception as e:
        std_write(('Failed to retrieve the DATA with the error \x1b[01;31m{}\x1b[00m!!').format(e))
        exit(1)


def logout(uname):
    if not uname:
        std_write('Username is necessary no matter who you are!!')
        return False
    else:
        temp_file = tempfile.gettempdir() + ('/{}-whu.logout').format(uname)
        iis_temp = tempfile.gettempdir() + '/IIS-WEB.logout'
        if not os.path.exists(temp_file) and not os.path.exists(iis_temp):
            std_write("You've NOT Login Yet!!!")
            exit(1)
        if os.path.exists(temp_file):
            with open(temp_file) as (handle):
                content = handle.read()
                mode = 'WHU'
        else:
            with open(iis_temp) as (handle):
                content = handle.read()
                mode = 'IIS'
        if not content:
            std_write("You've Logout already ~~")
            exit(0)
        feed, url = downloader(content)
        if mode == 'WHU':
            regs = compile('window.location.replace\\("(.+?)"\\)', DOTALL)
            match = regs.findall(feed)
            if match and 'goToLogout' in match[0]:
                std_write('Logout Succeeded!')
                os.unlink(temp_file)
                return True
            std_write('Logout Failed!')
            return False
        data_str = content.split('?')[(-1)]
        req = opener.open(url, data=data_str)
        result = req.read()
        error_code = compile('<errcode>(.+?)</errcode>').findall(result)
        msg = compile('<message>(.+?)</message>').findall(result)
        if int(error_code[0]) == 0:
            std_write('Logout Succeeded!')
            os.unlink(iis_temp)
            return True
        std_write('Logout Failed......')
        std_write(msg[0].strip())
        return False


def get_auth_link():
    data, url = downloader(try_url)
    if url == try_url and not data.startswith('<script>') or url != try_url:
        std_write("You've already able to access the Network")
        exit(0)
    if 'Portal登陆页面' in data:
        return (url, 'IIS')
    regs = compile("'(.+?)'")
    result = regs.findall(data)
    if result and result[0].startswith('http'):
        return (result[0], 'COMMON')
    std_write('Failed the Retrieve Auth Page !!')
    exit(1)


def do_login(auth_link, username, password, qr_code=''):
    global ip_port
    post_data = {'username': username, 
       'uuidQrCode': qr_code, 
       'pwd': password}
    post_link = auth_link.replace('index.jsp?', 'userV2.do?method=login&')
    post_link += ('&username={}&pwd={}').format(username, password)
    req = opener.open(post_link, urlencode(post_data))
    content = req.read()
    ip_reg = compile('http://(.+?)/')
    ip_port = ip_reg.findall(auth_link)[0]
    return content


def iis_do_login(auth_link, username, password):
    global ip_port
    post_data = auth_link.split('?')[(-1)]
    post_data += ('&username={}&password={}').format(username, password)
    post_link = auth_link.replace('login.html', 'do.portallogin')
    try:
        req = opener.open(post_link, post_data, timeout=5)
        content = req.read()
        ip_port = post_link
        return content
    except Exception as e:
        std_write(e)
        exit(1)


def iis_check_success(content):
    message = compile('<message>(.+?)</message>').findall(content)
    error_code = compile('<errcode>(.+?)</errcode>').findall(content)
    platform = sys.platform
    if error_code and int(error_code[0]) != 0:
        if 'linux' in platform or 'darwin' in platform:
            std_write(('\x1b[01;31m{}\x1b[00m').format(message[0].strip()))
        else:
            std_write(('{}').format(message[0].strip()))
        return False
    with open(tempfile.gettempdir() + '/IIS-WEB.logout', 'w') as (handle):
        handle.write(ip_port.replace('do.portallogin', 'do.portallogoff'))
    ip = compile('wlanuserip=(.+?)&').findall(ip_port)
    if 'linux' in platform or 'darwin' in platform:
        std_write('IIS-WEB Login \x1b[01;31mSucceeded\x1b[00m!!')
        std_write(('IP: \x1b[01;37m{}\x1b[00m').format(ip[0]))
    else:
        std_write('IIS-WEB Login Succeeded!!')
        std_write(('IP: {}').format(ip[0]))
    return True


def check_success(content):
    uname = compile("d.userName.innerText='(.+?)'").findall(content)
    userip = compile("d.contentDive.userip='(.+?)'").findall(content)
    time_left = compile("d.maxLeaving.innerText='(.+?)'").findall(content)
    account_left = compile("d.accountInfo.innerText='(.+?)'").findall(content)
    logout_url = compile("d.toLogOut.href='(.+?)'").findall(content)
    platform = sys.platform
    if not uname or not userip:
        error_msg = compile('<div id="errorInfo_center" val="(.+?)">').findall(content)
        if error_msg:
            if 'linux' in platform or 'darwin' in platform:
                std_write(('\x1b[01;31m{}\x1b[00m').format(error_msg[0].decode('gbk')))
            else:
                std_write(('{}').format(error_msg[0]))
        else:
            std_write('Logging Failed......')
        return False
    temp_dir = tempfile.gettempdir()
    temp_file = temp_dir + ('/{}-whu.logout').format(uname[0])
    with open(temp_file, 'w') as (handle):
        handle.write(('http://{}').format(ip_port) + logout_url[0])
    if 'linux' in platform or 'darwin' in platform:
        std_write('Logging \x1b[01;31mSucceeded\x1b[00m!!\n')
        std_write(('Username: \x1b[01;34m{}\x1b[00m').format(uname[0]))
        std_write(('IP: \x1b[01;37m{}\x1b[00m').format(userip[0]))
        std_write(('Time Left: \x1b[01;32m{}\x1b[00m').format(time_left[0].decode('gbk')))
        std_write(('Account Remain: \x1b[01;31m{}\x1b[00m\n').format(account_left[0].decode('gbk')))
    else:
        std_write('Logging Succeeded')
        std_write(('Username: {}').format(uname[0]))
        std_write(('IP: {}').format(userip[0]))
        std_write(('Time Left: {}').format(time_left[0]))
        std_write(('Account Remain: {}').format(account_left[0]))
    return True


def help_menu():
    """
    ===* net-access-whu help menu *===

     -u     :username
     -p     :password
     -c     :config file

     -d  logout   :method for logout

     deploy like this:
        method 1. net-access-whu -u your_account -p your_password
        method 2. net-access-whu -c config.json

        config.json has the format like below(older edition, works always fine with only one type of network):
            {
                "username": "your_account",
                "password": "your_password"
            }
        or something like these
            {
                "COMMON": {
                    "username": "your_xiaoyuanwang_account",
                    "password": "your_xiaoyuanwang_password"
                },
                "IIS": {
                    "username": "your_guoraun_account",
                    "password": "your_guoruan_password"
                }
            }

        Logout(username is necessary for WHU network user, IIS user is not):

        method 1. net-access-whu -u your_account -d logout
        method 2. net-access-whu -c config.json -d logout
    """
    std_write(help_menu.__doc__)


def main():
    argv = sys.argv
    if not len(argv) == 3 and not len(argv) == 5:
        return help_menu()
    config = {'COMMON': {'username': '', 
                  'password': ''}, 
       'IIS': {'username': '', 
               'password': ''}}
    username = ''
    password = ''
    for i in argv[1:]:
        if i == '-c':
            with open(argv[(argv.index(i) + 1)]) as (handle):
                reader = handle.read()
            try:
                reader = json.loads(reader)
                config = reader
            except Exception as e:
                std_write(e)
                return help_menu()

            username = reader.get('username', '')
            password = reader.get('password', '')
            if not username and not password:
                common = reader.get('COMMON', '')
                iis = reader.get('IIS', '')
                if common:
                    username = common.get('username', '')
                    password = common.get('password', '')
                elif iis:
                    username = iis.get('username', '')
                    password = iis.get('password', '')
            break
        if i == '-u':
            username = argv[(argv.index(i) + 1)]
        if i == '-p':
            password = argv[(argv.index(i) + 1)]

    if 'logout' in argv[1:]:
        return logout(uname=username)
    auth_link, web_type = get_auth_link()
    if web_type == 'COMMON':
        check_success(do_login(auth_link, username, password))
    else:
        from_config = config.get('IIS', {})
        if from_config:
            username = from_config.get('username', '')
            password = from_config.get('password', '')
        iis_check_success(iis_do_login(auth_link, username, password))


if __name__ == '__main__':
    main()