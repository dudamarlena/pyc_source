# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dnsomatic_api.py
# Compiled at: 2009-01-07 08:31:22
import urllib, urllib2, socket

class DnsOMatic:
    """Uses the DNS-o-matic API to update the IP address.
        Documentation about the DNS-O-Matic API is at https://www.dnsomatic.com/wiki/api.
        Be aware that nscd might cache DNS resolutions, rendering this program useless!
        """
    version = '0.3.1'
    _updateUrl = 'https://updates.dnsomatic.com'
    _defaultUrl = '%s/nic/update' % _updateUrl
    _defaultRealm = 'DNSOMATIC'
    _getIpUrl = 'http://myip.dnsomatic.com'
    _updateAllIPsKludge = 'all.dnsomatic.com'
    _defaultUserAgent = 'SukkoSoft - dnsomatic_api.py - %s' % version

    def __init__(self, username=None, password=None, baseUrl=_defaultUrl, realm=_defaultRealm, userAgent=_defaultUserAgent):
        self._username = username
        self._password = password
        self._baseUrl = baseUrl
        self._realm = realm
        self._userAgent = userAgent
        self._setupHttp()

    def _setupHttp(self):
        """Sets up all things needed to use Basic HTTP Authentication."""
        if self._username is not None and self._username != '' and self._password is not None and self._password != '':
            passwdMan = urllib2.HTTPPasswordMgrWithDefaultRealm()
            auth_handler = urllib2.HTTPBasicAuthHandler(passwdMan)
            auth_handler.add_password(None, self._updateUrl, self._username, self._password)
            self._httpOpener = urllib2.build_opener(auth_handler)
        else:
            self._httpOpener = urllib2.build_opener()
        return

    def getCurrentLocalIP(self):
        """Retrieve the current local IP through the DNS-O-Matic service."""
        f = self._httpOpener.open(self._getIpUrl)
        ip = ('').join(f.readlines()).strip()
        return ip

    def getCurrentRemoteIP(self, hostname):
        """Retrieve the IP the hostname we want to update currently points to."""
        try:
            sa = socket.getaddrinfo(hostname, None)
            ip = sa[0][4][0]
        except socket.gaierror:
            ip = None

        return ip

    def shouldUpdate(self, hostname, currentIP=None):
        if hostname is None:
            ret = True
        else:
            if currentIP is None:
                currentIP = self.getCurrentLocalIP()
            desiredIP = self.getCurrentRemoteIP(hostname)
            if desiredIP is not None and currentIP == desiredIP:
                ret = False
            else:
                ret = True
        return ret

    def updateSingle(self, hostname=None, ip=None, force=False):
        """Update a single address at the remote site."""
        if ip is None:
            ip = self.getCurrentLocalIP()
        if force or self.shouldUpdate(hostname, ip):
            params = {'myip': ip}
            if hostname is not None:
                params['hostname'] = hostname
            headers = {'User-Agent': self._userAgent}
            enc_params = urllib.urlencode(params)
            if None:
                req = urllib2.Request(self._baseUrl, enc_params, headers)
            else:
                url = '%s?%s' % (self._baseUrl, enc_params)
                req = urllib2.Request(url, headers=headers)
            try:
                f = self._httpOpener.open(req)
                result = ('').join(f.readlines()).strip()
                if result == 'nohost':
                    status = result
                else:
                    (status, ip) = result.split()
            except urllib2.HTTPError:
                status = 'badauth'
                ip = '0.0.0.0'
            else:
                res = (
                 status, ip)
        else:
            res = (
             'alreadyok', ip)
        return res

    def update(self, ip=None, hostnames=None, force=False):
        """Update several addresses to the same IP at the remote site."""
        if hostnames is None or len(hostnames) == 0:
            res = self.updateSingle(ip=ip, force=force)
            ret = [res]
        ret = []
        for hostname in hostnames:
            res = self.updateSingle(hostname, ip, force)
            ret.append(res)

        return ret