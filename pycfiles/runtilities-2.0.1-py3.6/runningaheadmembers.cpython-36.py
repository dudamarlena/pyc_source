# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\runningaheadmembers.py
# Compiled at: 2020-02-26 14:50:54
# Size of source mod 2**32: 14089 bytes
import csv
from datetime import datetime
import difflib
from loutilities import timeu
ymd = timeu.asctime('%Y-%m-%d')
from loutilities.csvwt import wlist

class unsupportedFileType:
    pass


class RunningAheadMember:
    __doc__ = '\n    Represents single RunningAHEAD member\n\n    :param membership: membership record from RunningAHEAD export file\n    '
    filehdr = 'MembershipType,FamilyName,GivenName,MiddleName,Gender,DOB,Email,EmailOptIn,PrimaryMember,RenewalDate,JoinDate,ExpirationDate,Street1,Street2,City,State,PostalCode,Country,Telephone,EntryType'.split(',')
    memberattr = 'membershiptype,lname,fname,mname,gender,dob,email,emailoptin,primarymember,renew,join,expiration,street1,street2,city,state,zip,country,telephone,entrytype'.split(',')
    memberxlate = dict(list(zip(filehdr, memberattr)))
    reprattr = 'fname,lname,dob,join,renew,expiration'.split(',')

    def __init__(self, membership):
        for key in self.filehdr:
            if key in self.memberxlate:
                setattr(self, self.memberxlate[key], membership[key])

    def __repr__(self):
        reprval = '{}('.format(self.__class__)
        for attr in self.reprattr:
            if not attr[0:2] == '__':
                if attr == 'fields':
                    pass
                else:
                    reprval += '{}={},'.format(attr, getattr(self, attr))

        reprval = reprval[:-1]
        reprval += ')'
        return reprval


class RunningAheadMembers:
    __doc__ = "\n    Collect member data from RunningAHEAD individual membership export\n    file, containing records from the beginning of the club's member\n    registration until present.\n\n    Provide access functions to gain access to these membership records.\n\n    :param memberfile: member filename, filehandle or string of file records\n    :param overlapfile: debug file to test for overlaps between records\n    "

    def __init__(self, memberfile, overlapfile=None):
        self.closematches = None
        self.names = {}
        self.dobnames = {}
        openedhere = False
        if isinstance(memberfile, str):
            memberfileh = open(memberfile, 'r', newline='')
            openedhere = True
        else:
            if isinstance(memberfile, file):
                memberfileh = memberfile
            else:
                if type(memberfile) in [list, wlist]:
                    memberfileh = memberfile
                else:
                    raise unsupportedFileType
        INCSV = csv.DictReader(memberfileh)
        for membership in INCSV:
            asc_joindate = membership['JoinDate']
            asc_expdate = membership['ExpirationDate']
            fname = membership['GivenName']
            lname = membership['FamilyName']
            dob = membership['DOB']
            memberid = membership['MemberID']
            fullname = '{}, {}'.format(lname, fname)
            thisrec = {'MemberID':memberid, 
             'name':fullname,  'join':asc_joindate,  'expiration':asc_expdate,  'dob':dob,  'fullrec':membership,  'RunningAheadMember':RunningAheadMember(membership)}
            thisname = (
             lname, fname, dob)
            if thisname not in self.names:
                self.names[thisname] = []
            self.names[thisname].append(thisrec)

        if overlapfile:
            _OVRLP = open(overlapfile, 'w', newline='')
            OVRLP = csv.DictWriter(_OVRLP, ['MemberID', 'name', 'dob', 'renewal', 'join', 'expiration', 'tossed'], extrasaction='ignore')
            OVRLP.writeheader()
        for thisname in self.names:
            lname, fname, dob = thisname
            if dob not in self.dobnames:
                self.dobnames[dob] = []
            if (
             lname, fname) not in self.dobnames[dob]:
                self.dobnames[dob].append({'lname':lname,  'fname':fname})
            self.names[thisname] = sorted((self.names[thisname]), key=(lambda k: (k['expiration'], k['join'])))
            toss = []
            for i in range(1, len(self.names[thisname])):
                if self.names[thisname][i]['join'] <= self.names[thisname][(i - 1)]['expiration']:
                    lastexp_dt = ymd.asc2dt(self.names[thisname][(i - 1)]['expiration'])
                    thisexp_dt = ymd.asc2dt(self.names[thisname][i]['expiration'])
                    jan1_dt = datetime(lastexp_dt.year + 1, 1, 1)
                    jan1_asc = ymd.dt2asc(jan1_dt)
                    if jan1_dt > thisexp_dt:
                        toss.append(i)
                        self.names[thisname][i]['tossed'] = 'Y'
                    if overlapfile:
                        OVRLP.writerow(self.names[thisname][(i - 1)])
                        OVRLP.writerow(self.names[thisname][i])
                    self.names[thisname][i]['join'] = jan1_asc
                    self.names[thisname][i]['fullrec']['JoinDate'] = jan1_asc
                    self.names[thisname][i]['RunningAheadMember'].join = jan1_asc

            toss.reverse()
            for i in toss:
                self.names[thisname].pop(i)

        if overlapfile:
            _OVRLP.close()
        if openedhere:
            memberfileh.close()

    def membership_iter(self, raw=False):
        """
        generator function that yields full record for each of memberships

        :param raw: True to yield dict, False to yield RunningAheadMember object, default False
        """
        for thisname in self.names:
            for thismembership in self.names[thisname]:
                if not raw:
                    yield thismembership['RunningAheadMember']
                else:
                    yield thismembership['fullrec']

    def member_iter(self, raw=False):
        """
        generator function that yields latest membership record for each of names with
        JoinDate updated to earliest JoinDate

        :param raw: True to yield dict, False to yield RunningAheadMember object, default False
        """
        for thisname in self.names:
            if not raw:
                thismembership = self.names[thisname][(-1)]['RunningAheadMember']
                thismembership.join = self.names[thisname][0]['join']
                yield thismembership
            else:
                thismembership = self.names[thisname][(-1)]['fullrec']
                thismembership['JoinDate'] = self.names[thisname][0]['join']
                yield thismembership

    def getmember(self, memberkey):
        """
        retrieve latest membership record for memberkey with 
        JoinDate updated to earliest JoinDate

        :param memberkey: (lname,fname,dob)
        :rtype: RunningAheadMember object
        """
        thismembership = self.names[memberkey][(-1)]['RunningAheadMember']
        thismembership.join = self.names[memberkey][0]['join']
        return thismembership

    def getmemberships(self, memberkey):
        """
        retrieve list of membership records for memberkey

        :param memberkey: (lname,fname,dob)
        :rtype: [RunningAheadMember object, ...]
        """
        thesememberships = []
        for thismembership in self.names[memberkey]:
            thesememberships.append(thismembership['RunningAheadMember'])

        return thesememberships

    def getmemberkey(self, lname, fname, dob, cutoff=0.6, n=10):
        """
        retrieve member key based on name, dob

        if name wasn't found, None is returned
        if None is returned, check close matches using getclosematches()
        
        :param lname: last name
        :param fname: first name
        :param dob: date of birth yyyy-mm-dd
        :param cutoff: float in range (0,1] ratio of closeness to match name
        :param n: number of names checked for closeness (most similar)
        :rtype: (lname,fname,dob) or None if not found
        """
        self.closematches = []
        if dob not in self.dobnames:
            return
        nameskeys = [('{} {}'.format(n['fname'], n['lname']).lower(), n) for n in self.dobnames[dob]]
        possiblenames = [nk[0] for nk in nameskeys]
        possiblekeys = [(nk[1]['lname'], nk[1]['fname'], dob) for nk in nameskeys]
        searchname = '{} {}'.format(fname, lname).lower()
        closematches = difflib.get_close_matches(searchname, possiblenames, n=10, cutoff=cutoff)
        for match in closematches:
            if match == searchname:
                return possiblekeys[possiblenames.index(match)]
            self.closematches.append(possiblekeys[possiblenames.index(match)])

    def getclosematchkeys(self):
        """
        can be called after findmembers() to return list of members found, but did not match exactly
        
        :rtype: [(lname,fname,dob), ...]
        """
        return self.closematches