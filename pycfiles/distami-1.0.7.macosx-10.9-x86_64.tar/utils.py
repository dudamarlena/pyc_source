# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/distami/utils.py
# Compiled at: 2014-10-24 18:40:42
import logging, time, boto
from boto import ec2
from distami.exceptions import *
log = logging.getLogger(__name__)

def get_ami(conn, ami_id):
    """ Gets a single AMI as a boto.ec2.image.Image object """
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            attempts += 1
            images = conn.get_all_images(ami_id)
        except boto.exception.EC2ResponseError:
            msg = "Could not find AMI '%s' in region '%s'" % (ami_id, conn.region.name)
            if attempts < max_attempts:
                log.debug(msg + ' so waiting 5 seconds and retrying')
                time.sleep(5)
            else:
                raise DistamiException(msg)

    log.debug('Found AMIs: %s', images)
    if len(images) != 1:
        msg = 'Somehow more than 1 AMI was detected - this is a weird error'
        raise DistamiException(msg)
    return images[0]


def get_snapshot(conn, snapshot_id):
    """ Gets a single snapshot as a boto.ec2.snapshot.Snapshot object """
    try:
        snapshots = conn.get_all_snapshots(snapshot_id)
    except boto.exception.EC2ResponseError:
        msg = "Could not snapshot '%s' in region '%s'" % (snapshot_id, conn.region.name)
        raise DistamiException(msg)

    log.debug('Found snapshots: %s', snapshots)
    if len(snapshots) != 1:
        msg = 'Somehow more than 1 snapshot was detected - this is a weird error'
        raise DistamiException(msg)
    return snapshots[0]


def get_regions_to_copy_to(source_region):
    """ Gets the list of regions to copy an AMI to """
    regions = []
    for region in ec2.regions():
        if region.name == source_region:
            continue
        if region.name == 'us-gov-west-1':
            continue
        if region.name == 'cn-north-1':
            continue
        regions.append(region.name)

    return regions


def wait_for_ami_to_be_available(conn, ami_id):
    """ Blocking wait until the AMI is available """
    ami = get_ami(conn, ami_id)
    log.debug('AMI details: %s', vars(ami))
    while ami.state != 'available':
        log.info('%s in %s not available, waiting...', ami_id, conn.region.name)
        time.sleep(30)
        ami = get_ami(conn, ami_id)
        if ami.state == 'failed':
            msg = "AMI '%s' is in a failed state and will never be available" % ami_id
            raise DistamiException(msg)

    return ami