# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabrizio/Dropbox/free_range_factory/boot/boot_pkg/opencores.py
# Compiled at: 2012-08-26 08:59:39
import os, mechanize, cookielib

class open_cores_website:
    """ Class to login and download stuff from: "www.opencores.org"
        Cookies are automatically turned on.
    """

    def __init__(self):
        self.br = mechanize.Browser()
        self.cookies = mechanize.MozillaCookieJar()
        self.cookies_file = os.path.join(os.environ['HOME'], '.boot_cookies.txt')
        if os.path.isfile(self.cookies_file):
            self.cookies.load(self.cookies_file)
        print 'cookies loaded:', len(self.cookies)
        self.br.set_cookiejar(self.cookies)
        USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; tr-TR; rv:1.8.1.9) ' + 'Gecko/20071102 Pardus/2007 Firefox/2.0.0.9'
        self.br.addheaders = [('User-agent', USER_AGENT)]

    def login(self, login_data):
        """ Method to login on "www.opencores.org/login".
        """
        self.user = login_data[0]
        self.pwd = login_data[1]
        self.br.open('http://www.opencores.org/login')
        self.br.select_form(nr=0)
        self.br['user'] = self.user
        self.br['pass'] = self.pwd
        res = self.br.submit()
        answer = res.read()
        if 'Username/Password missmatch' in answer:
            print 'Problems in authenticating.'
            return 1
        if 'Account not found' in answer:
            print 'This account does not exist.'
            return 1
        print 'Successfully authenticated in OpenCores website.'
        self.cookies.save(self.cookies_file)
        return 0

    def login_needed(self):
        """ Method to check if you need to login or if you are already
            logged in. 
        """
        _web = self.br.open('http://opencores.org/acc')
        _answer = self.br.response().read()
        if '403 - Forbidden' in _answer:
            print 'Login needed.'
            return 'yes'
        else:
            print 'You seem already logged in.'
            return 'no'

    def download(self, dl_url, dl_dir, dl_fl):
        """ Method to download a file or a page given a specific location.
            the page will be saved in a file.
        """
        self.br.open(dl_url)
        dl_fl = os.path.join(dl_dir, dl_fl)
        with open(dl_fl, 'w') as (file):
            file.write(self.br.response().read())
        print dl_fl, 'has been downloaded.\n'
        return 0


def get_login_data():
    return [
     'mark', 'strange']


if __name__ == '__main__':
    dl_dir = '/tmp'
    login_data = ['', '']
    if not login_data[1]:
        login_data = get_login_data()
    website = open_cores_website()
    if 'yes' in website.login_needed():
        website.login(login_data)
    dl_url = 'http://opencores.org/download,othellogame'
    if 'http://opencores.org/download,' in dl_url:
        dl_fl = dl_url.split('http://opencores.org/download,')[(-1)] + '.tar.gz'
    elif dl_url.endswith('.html') or dl_url.endswith('.htm'):
        dl_fl = dl_url.split('/')[(-1)]
    else:
        dl_fl = dl_url.split('/')[(-1)] + '.html'
    website.download(dl_url, dl_dir, dl_fl)
    print 'bye bye'