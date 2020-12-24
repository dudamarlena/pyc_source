# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/distami/cli.py
# Compiled at: 2013-11-11 02:09:50
import argparse, logging, sys
from distami.core import Distami, Logging
from distami import __version__, utils
from distami.exceptions import DistamiException
from boto.utils import get_instance_metadata
from multiprocessing import Pool
__all__ = ('run', )
log = logging.getLogger(__name__)

def _fail(message='Unknown failure', code=1):
    log.error(message)
    sys.exit(code)


def copy(param_array):
    """ Copies distami to the given region """
    distami = param_array[0]
    to_region = param_array[1]
    args = param_array[2]
    copied_ami_id = distami.copy_to_region(to_region)
    ami_cp = Distami(copied_ami_id, to_region)
    if args.non_public:
        distami.make_ami_non_public()
        distami.make_snapshot_non_public()
    else:
        ami_cp.make_ami_public()
        ami_cp.make_snapshot_public()
    if args.accounts:
        distami.share_ami_with_accounts(args.accounts)


def run():
    parser = argparse.ArgumentParser(description='Distributes an AMI by copying it to one, many, or all AWS regions, and by optionally making the AMIs and Snapshots public or shared with specific AWS Accounts.')
    parser.add_argument('ami_id', metavar='AMI_ID', help='the source AMI ID to distribute. E.g. ami-1234abcd')
    parser.add_argument('--region', metavar='REGION', help='the region the AMI is in (default is current region of EC2 instance this is running on). E.g. us-east-1')
    parser.add_argument('--to', metavar='REGIONS', help='comma-separated list of regions to copy the AMI to. The default is all regions. Specify "none" to prevent copying to other regions. E.g. us-east-1,us-west-1,us-west-2')
    parser.add_argument('--non-public', action='store_true', default=False, help='Copies the AMIs to other regions, but does not make the AMIs or snapshots public. Bad karma, but good for AMIs that need to be private/internal only')
    parser.add_argument('--accounts', metavar='AWS_ACCOUNT_IDs', help='comma-separated list of AWS Account IDs to share an AMI with. Assumes --non-public. Specify --to=none to share without copying.')
    parser.add_argument('-p', '--parallel', action='store_true', default=False, help='Perform each copy to another region in parallel. The default is in serial which can take a long time')
    parser.add_argument('-v', '--verbose', action='count', help='enable verbose output (-vvv for more)')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__, help='display version number and exit')
    args = parser.parse_args()
    if args.accounts:
        args.non_public = True
    Logging().configure(args.verbose)
    log.debug('CLI parse args: %s', args)
    if args.region:
        ami_region = args.region
    else:
        log.debug('Figure out which region I am running in...')
        instance_metadata = get_instance_metadata(timeout=5)
        log.debug('Instance meta-data: %s', instance_metadata)
        if not instance_metadata:
            _fail('Could not determine region. This script is either not running on an EC2 instance, or the meta-data service is down')
        ami_region = instance_metadata['placement']['availability-zone'][:-1]
        log.debug('Running in region: %s', ami_region)
    try:
        distami = Distami(args.ami_id, ami_region)
        if not args.non_public:
            distami.make_ami_public()
            distami.make_snapshot_public()
        if args.accounts:
            account_ids = args.accounts.split(',')
            distami.share_ami_with_accounts(account_ids)
            distami.share_snapshot_with_accounts(account_ids)
        if args.to and args.to == 'none':
            to_regions = []
        else:
            if args.to and args.to != 'all':
                to_regions = args.to.split(',')
            else:
                to_regions = utils.get_regions_to_copy_to(ami_region)
            if args.parallel:
                f = lambda x, y, z: [x, y, z]
                param_array = map(f, [distami] * len(to_regions), to_regions, [args] * len(to_regions))
                log.debug(param_array)
                log.info('Copying in parallel. Hold on to your hat...')
                pool = Pool(processes=8)
                pool.map(copy, param_array)
                pool.close()
                pool.join()
            else:
                for region in to_regions:
                    copy([distami, region, args])

    except DistamiException as e:
        _fail(e.message)

    log.info('AMI successfully distributed!')
    sys.exit(0)