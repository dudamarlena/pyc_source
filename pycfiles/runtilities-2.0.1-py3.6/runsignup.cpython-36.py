# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\runsignup.py
# Compiled at: 2020-02-26 14:40:05
# Size of source mod 2**32: 18402 bytes
"""
runsignup - access methods for runsignup.com
===================================================
"""
import logging
from threading import RLock
from csv import DictReader, DictWriter
from datetime import datetime, timedelta
from os.path import dirname, abspath
from os import stat, chmod, rename, remove
from tempfile import NamedTemporaryFile
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from loutilities.configparser import getitems
from loutilities.timeu import asctime
from loutilities.transform import Transform
from loutilities.csvwt import record2csv
login_url = 'https://runsignup.com/rest/login'
logout_url = 'https://runsignup.com/rest/logout'
members_url = 'https://runsignup.com/rest/club/{club_id}/members'
KMPERMILE = 1.609344

class accessError(Exception):
    pass


class notImplemented(Exception):
    pass


class parameterError(Exception):
    pass


thislogger = logging.getLogger('running.runsignup')

class RunSignUp:
    __doc__ = '\n    access methods for RunSignUp.com\n\n    either key and secret OR email and password should be supplied\n    key and secret take precedence\n\n    :param key: key from runsignup (direct key, no OAuth)\n    :param secret: secret from runsignup (direct secret, no OAuth)\n    :param email: email for use by Login API (deprecated)\n    :param password: password for use by Login API (deprecated)\n    :param debug: set to True for debug logging of http requests, default False\n    '

    def __init__(self, key=None, secret=None, email=None, password=None, debug=False):
        """
        initialize
        """
        logging.basicConfig()
        if debug:
            thislogger.setLevel(logging.DEBUG)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
        else:
            thislogger.setLevel(logging.NOTSET)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.NOTSET)
            requests_log.propagate = False
        if not key:
            if not email:
                raise parameterError('either key/secret or email/password must be supplied')
        if key and not secret or secret and not key:
            raise parameterError('key and secret must be supplied together')
        else:
            if email and not password or password and not email:
                raise parameterError('email and password must be supplied together')
            self.key = key
            self.secret = secret
            self.email = email
            self.password = password
            self.debug = debug
            self.client_credentials = {}
            if key:
                self.credentials_type = 'key'
            else:
                self.credentials_type = 'login'

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        self.session = requests.Session()
        if self.credentials_type == 'key':
            self.client_credentials = {'api_key':self.key, 
             'api_secret':self.secret}
        else:
            r = requests.post(login_url, params={'format': 'json'}, data={'email':self.email,  'password':self.password})
            resp = r.json()
            self.credentials_type = 'login'
            self.client_credentials = {'tmp_key':resp['tmp_key'],  'tmp_secret':resp['tmp_secret']}

    def close(self):
        """
        close down
        """
        self.client_credentials = {}
        self.session.close()

    def members(self, club_id):
        """
        return members accessible to this application
        """
        BITESIZE = 100
        page = 1
        members = []
        while 1:
            data = self._rsuget(members_url.format(club_id=club_id), page=page,
              results_per_page=BITESIZE,
              include_questions='T')
            if len(data['club_members']) == 0:
                break
            theseusers = data['club_members']
            members += theseusers
            page += 1
            if len(data['club_members']) < BITESIZE:
                break

        return members

    def _rsuget(self, methodurl, **payload):
        """
        get method for runsignup access
        
        :param methodurl: runsignup method url to call
        :param contentfield: content field to retrieve from response
        :param **payload: parameters for the method
        """
        thispayload = self.client_credentials.copy()
        thispayload.update(payload)
        thispayload.update({'format': 'json'})
        resp = self.session.get(methodurl, params=thispayload)
        if resp.status_code != 200:
            raise accessError('HTTP response code={}, url={}'.format(resp.status_code, resp.url))
        data = resp.json()
        if 'error' in data:
            raise accessError('RSU response code={}-{}, url={}'.format(data['error']['error_code'], data['error']['error_msg'], resp.url))
        return data


def updatemembercache(club_id, membercachefilename, key=None, secret=None, email=None, password=None, debug=False):
    if debug:
        thislogger.setLevel(logging.DEBUG)
        thislogger.propagate = True
    else:
        thislogger.setLevel(logging.ERROR)
        thislogger.propagate = True
    rsu = RunSignUp(key=key, secret=secret, email=email, password=password, debug=debug)
    rsu.open()
    xform = Transform({'MemberID':lambda mem: mem['user']['user_id'], 
     'MembershipID':'membership_id', 
     'MembershipType':'club_membership_level_name', 
     'FamilyName':lambda mem: mem['user']['last_name'], 
     'GivenName':lambda mem: mem['user']['first_name'], 
     'MiddleName':lambda mem: mem['user']['middle_name'], 
     'Gender':lambda mem: 'Female' if mem['user']['gender'] == 'F' else 'Male', 
     'DOB':lambda mem: mem['user']['dob'], 
     'Email':lambda mem: mem['user']['email'] if 'email' in mem['user'] else '', 
     'PrimaryMember':'primary_member', 
     'JoinDate':'membership_start', 
     'ExpirationDate':'membership_end', 
     'LastModified':'last_modified'},
      sourceattr=False,
      targetattr=False)
    members = {}
    currmemberrecs = {}
    dt = asctime('%Y-%m-%d')
    today = dt.dt2asc(datetime.now())

    def getmemberkey(memberrec):
        lastname = memberrec['FamilyName']
        firstname = memberrec['GivenName']
        dob = memberrec['DOB']
        memberkey = '{},{},{}'.format(lastname, firstname, dob)
        return memberkey

    def add2cache(memberrec):
        memberkey = getmemberkey(memberrec)
        members.setdefault(memberkey, [])
        recordlist = [mr for mr in members[memberkey] if mr['ExpirationDate'] != memberrec['ExpirationDate']] + [memberrec]
        members[memberkey] = recordlist
        sortby = 'ExpirationDate'
        members[memberkey].sort(key=(lambda item: item[sortby]))
        for i in range(1, len(members[memberkey])):
            lastrec = members[memberkey][(i - 1)]
            thisrec = members[memberkey][i]
            if thisrec['JoinDate'] <= lastrec['ExpirationDate']:
                exp = thisrec['ExpirationDate']
                oldstart = thisrec['JoinDate']
                newstart = dt.dt2asc(dt.asc2dt(lastrec['ExpirationDate']) + timedelta(1))
                thislogger.error('overlap detected: {} end={} was start={} now start={}'.format(memberkey, exp, oldstart, newstart))
                thisrec['JoinDate'] = newstart

        return memberkey

    def incache(memberrec):
        memberkey = getmemberkey(memberrec)
        if memberkey not in members:
            cachedmember = False
        else:
            if memberrec['ExpirationDate'] in [m['ExpirationDate'] for m in members[memberkey]]:
                cachedmember = True
            else:
                cachedmember = False
        return cachedmember

    rlock = RLock()
    with rlock:
        starttime = datetime.now()
        with open(membercachefilename, newline='') as (memfile):
            cachedmembers = DictReader(memfile)
            for memberrec in cachedmembers:
                memberkey = add2cache(memberrec)
                if memberrec['JoinDate'] <= today:
                    if memberrec['ExpirationDate'] >= today:
                        if memberkey in currmemberrecs:
                            thislogger.error('member duplicated in cache: {}'.format(memberkey))
                    currmemberrecs[memberkey] = memberrec

        rsumembers = rsu.members(club_id)
        rsucurrmembers = []
        for rsumember in rsumembers:
            memberrec = {}
            xform.transform(rsumember, memberrec)
            rsucurrmembers.append(memberrec)

        for memberrec in rsucurrmembers:
            currmember = incache(memberrec)
            memberkey = add2cache(memberrec)
            if currmember:
                try:
                    del currmemberrecs[memberkey]
                except KeyError:
                    pass

        for memberkey in currmemberrecs:
            removedrec = currmemberrecs[memberkey]
            memberkey = getmemberkey(removedrec)
            members[memberkey] = [mr for mr in members[memberkey] if mr != removedrec]
            thislogger.debug('membership removed from cache: {}'.format(removedrec))

        cachedir = dirname(abspath(membercachefilename))
        sortedmembers = sorted(members.keys())
        with NamedTemporaryFile(mode='w', suffix='.rsucache', delete=False, dir=cachedir, newline='') as (tempcache):
            tempmembercachefilename = tempcache.name
            cachehdr = 'MemberID,MembershipID,MembershipType,FamilyName,GivenName,MiddleName,Gender,DOB,Email,PrimaryMember,JoinDate,ExpirationDate,LastModified'.split(',')
            cache = DictWriter(tempcache, cachehdr)
            cache.writeheader()
            for memberkey in sortedmembers:
                for memberrec in members[memberkey]:
                    cache.writerow(memberrec)

        cachemode = stat(membercachefilename).st_mode & 511
        chmod(tempmembercachefilename, cachemode)
        try:
            rename(tempmembercachefilename, membercachefilename)
        except OSError:
            remove(membercachefilename)
            rename(tempmembercachefilename, membercachefilename)

        finishtime = datetime.now()
        thislogger.debug('updatemembercache() duration={}'.format(finishtime - starttime))
    rsu.close()
    return rsumembers


def members2csv(club_id, key, secret, mapping, filepath=None):
    """
    Access club_id through RunSignUp API to retrieve members. Return
    list of members as if csv file. Optionally save csv file.

    :param club_id: club_id from RunSignUp
    :param key: api key for RunSignUp
    :param secret: api secret for RunSignUp
    :param mapping: OrderedDict {'outfield1':'infield1', 'outfield2':outfunction(inrec), ...} or ['inoutfield1', 'inoutfield2', ...]
    :param normfile: (optional) pathname to save csv file
    :rtype: csv file records, as list
    """
    with RunSignUp(key=key, secret=secret) as (rsu):
        members = rsu.members(club_id)
    filerows = record2csv(members, mapping, filepath)
    return filerows