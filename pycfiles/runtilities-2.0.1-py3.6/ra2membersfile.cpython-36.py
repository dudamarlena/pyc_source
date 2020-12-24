# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\ra2membersfile.py
# Compiled at: 2020-02-27 16:30:16
# Size of source mod 2**32: 8193 bytes
"""
ra2membersfile - retrieve RunningAHEAD member file to be put into file similar to RA export file
=========================================================================================================
"""
import unicodecsv, argparse, logging
from running.running import runningahead
filehdr = [
 'MemberID', 'MembershipType', 'FamilyName', 'GivenName', 'MiddleName', 'Gender', 'DOB', 'Email', 'EmailOptIn', 'PrimaryMember', 'RenewalDate', 'JoinDate', 'ExpirationDate', 'Street1', 'Street2', 'City', 'State', 'PostalCode', 'Country', 'Telephone', 'EntryType']
from loutilities import csvwt
logging.basicConfig()
logger = logging.getLogger('ra2membersfile')
logger.setLevel(logging.DEBUG)
logger.propagate = True

def adddetails(details, memberrecord, debug=False):
    """
    add details of membership to member record

    :param id: member implied
    :param memberrecord: dict to be updated with detailed information
    """
    memberrecord['FamilyName'] = details['person'].get('familyName', None)
    memberrecord['GivenName'] = details['person'].get('givenName', None)
    memberrecord['MiddleName'] = details['person'].get('middleName', None)
    gender = details['person'].get('gender', None)
    memberrecord['Gender'] = 'Male' if gender == 'm' else 'Female' if gender == 'f' else None
    memberrecord['DOB'] = details['person'].get('birthDate', None)
    memberrecord['Email'] = details['person'].get('email', None)
    memberrecord['Telephone'] = details['person'].get('phone', None)
    if 'ExpirationDate' not in memberrecord or not memberrecord['ExpirationDate']:
        memberrecord['ExpirationDate'] = details.get('expiration', None)
    memberrecord['JoinDate'] = details.get('join', None)
    memberrecord['Street1'] = details['address'].get('street1', None)
    memberrecord['Street2'] = details['address'].get('street2', None)
    memberrecord['City'] = details['address'].get('city', None)
    memberrecord['State'] = details['address'].get('state', None)
    memberrecord['PostalCode'] = details['address'].get('postalCode', None)
    memberrecord['Country'] = details['address'].get('country', None)
    if debug:
        last = memberrecord['FamilyName']
        first = memberrecord['GivenName']
        try:
            logger.debug('processing {}, {}'.format(last, first))
        except UnicodeEncodeError:
            pass


def ra2members(club, accesstoken, membercachefilename=None, update=False, filename=None, debug=False, key=None, secret=None, **filters):
    """
    retrieve RunningAHEAD members and create a file or list containing
    the member data, similar to export format from RunningAHEAD

    :param club: RunningAHEAD slug for club name
    :param accesstoken: access token for a priviledged viewer for this club
    :param membercachefilename: name of optional file to cache detailed member data
    :param update: update member cache based on latest information from RA
    :param filename: name of file for output. If None, list is returned and file is not created
    :param debug: True turns on requests debug
    :param key: ra key for oauth, if omitted retrieved from apikey
    :param secret: ra secret for oauth, if omitted retrieved from apikey
    :param filters: see http://api.runningahead.com/docs/club/list_members for valid filters
    """
    ra = runningahead.RunningAhead(membercachefilename=membercachefilename, debug=debug, key=key, secret=secret)
    memberlist = csvwt.wlist()
    members = unicodecsv.DictWriter(memberlist, filehdr)
    members.writeheader()
    membershiptypes = ra.listmembershiptypes(club, accesstoken)
    mshipxlate = {}
    for membershiptype in membershiptypes:
        mshipxlate[membershiptype['id']] = membershiptype['name']

    memberships = (ra.listmemberships)(club, accesstoken, **filters)
    for membership in memberships:
        member = {'PrimaryMember': 'Yes'}
        member['MemberID'] = '@{}'.format(membership['id'])
        member['MembershipType'] = mshipxlate[membership['membershipId']]
        member['ExpirationDate'] = membership.get('expiration', None)
        adddetails(ra.getmember(club, (membership['id']), accesstoken, update=update), member, debug)
        members.writerow(member)
        member['PrimaryMember'] = None
        if 'members' in membership:
            for thismember in membership['members']:
                adddetails(ra.getmember(club, (thismember['id']), accesstoken, update=update), member, debug)
                members.writerow(member)

    ra.close()
    if filename:
        with open(filename, 'w', newline='') as (outfile):
            outfile.writelines(memberlist)
    return memberlist


def file2members(fname):
    """
    debug function to read file created by ra2members and return memberlist

    :param fname: name of file
    :rtype: list of strings read from file, suitable for input to csv.DictReader
    """
    with open(fname, 'r', newline='') as (infile):
        memberlist = infile.readlines()
    return memberlist


def main():
    descr = '\n    retrieve members from RunningAHEAD and create a file similar to RA export file\n    '
    parser = argparse.ArgumentParser(description=descr, formatter_class=(argparse.RawDescriptionHelpFormatter), version=('{0} {1}'.format('running', version.__version__)))
    args = parser.parse_args()


if __name__ == '__main__':
    main()