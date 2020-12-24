# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/voice_info.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings
from pyogp.lib.client.enums import AssetType
from pyogp.lib.base.datatypes import UUID
from pyogp.lib.base.message.message import Message, Block

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-q', '--quiet', dest='quiet', default=False, action='store_true', help='log warnings and above (default is debug)')
    parser.add_option('-d', '--verbose', dest='verbose', default=False, action='store_true', help='log info and above (default is debug)')
    parser.add_option('-p', '--password', dest='password', default=None, help='specifies password instead of being prompted for one')
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error('Expected 2 arguments')
    (firstname, lastname) = args
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    if options.verbose:
        logging.getLogger('').setLevel(logging.INFO)
    elif options.quiet:
        logging.getLogger('').setLevel(logging.WARNING)
    else:
        logging.getLogger('').setLevel(logging.DEBUG)
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = False
    settings.ENABLE_COMMUNICATIONS_TRACKING = False
    settings.ENABLE_OBJECT_TRACKING = False
    settings.ENABLE_UDP_LOGGING = True
    settings.ENABLE_EQ_LOGGING = True
    settings.ENABLE_CAPS_LOGGING = True
    settings.MULTIPLE_SIM_CONNECTIONS = False
    client = Agent(settings)
    api.spawn(client.login, options.loginuri, firstname, lastname, password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    fetch_voice_info(client, callback=lambda x, y: client.logout())
    while client.running:
        api.sleep(0)

    return


def fetch_voice_info(client, callback=None):
    """Runs asynchronously"""
    try:
        voice_account_cap = client.region.capabilities['ProvisionVoiceAccountRequest']
    except KeyError:
        print >> sys.stderr, 'No capability for ProvisionVoiceAccountRequest'
        return

    try:
        voice_info_cap = client.region.capabilities['ParcelVoiceInfoRequest']
    except KeyError:
        print >> sys.stderr, 'No capability for ParcelVoiceInfoRequest'
        return

    def _request_voice_info():
        try:
            print 'Provisionining voice account...'
            account_info = voice_account_cap.POST({})
            print 'Received voice account: %s' % repr(account_info)
        except Exception, error:
            print >> sys.stderr, 'Exception requesting parcel voice info: %s' % str(error)
            callback(None, None)
            return
        else:
            try:
                print 'Requesting parcel voice info'
                parcel_info = voice_info_cap.POST({})
                print 'Received parcel voice info: %s' % repr(parcel_info)
            except Exception, error:
                print >> sys.stderr, 'Exception requesting parcel voice info: %s' % str(error)
                callback(account_info, None)
                return

            if callback:
                callback(account_info, parcel_info)

        return

    api.spawn(_request_voice_info)


def main():
    return login()


if __name__ == '__main__':
    main()