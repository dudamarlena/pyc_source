# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/fetch.py
# Compiled at: 2015-05-14 23:06:54
from __future__ import print_function
from hotcidr import util
from hotcidr import ports
from hotcidr import state
import boto.ec2, contextlib, os.path, shutil, sys, tempfile, yaml

def dump(x):
    return state.dump(x, default_flow_style=False)


def append_to_rules(connection, rules, group, rule, grant, inout_str, nameid_lookup):
    srcip_str = None
    if hasattr(grant, 'cidr_ip'):
        if grant.cidr_ip:
            srcip_str = str(grant.cidr_ip)
    if not srcip_str:
        srcip_str = nameid_lookup[grant.group_id]
    none_string = 'None'
    if rule.ip_protocol == '-1':
        ip_protocol_str = 'all'
    else:
        ip_protocol_str = none_string if rule.ip_protocol == None else rule.ip_protocol.encode('utf-8')
    if not rule.from_port or not rule.to_port:
        rules.append(dict([
         (
          'description', none_string if group.description == None else group.description.encode('utf-8')),
         (
          'direction', inout_str),
         (
          'protocol', ip_protocol_str),
         (
          'location', srcip_str)]))
    else:
        rules.append(dict([
         (
          'description', none_string if group.description == None else group.description.encode('utf-8')),
         (
          'direction', inout_str),
         (
          'protocol', ip_protocol_str),
         (
          'location', srcip_str),
         (
          'ports', ports.Port(int(rule.from_port), int(rule.to_port)))]))
    return


def main(region_code, vpc_id, output='', access_id=None, access_key=None, silence=None):
    if not util.is_valid_vpc(region_code):
        print('Error: invalid vpc-region-code.', file=sys.stderr)
        return 1
    yaml.add_representer(dict, yaml.representer.SafeRepresenter.represent_dict)
    outdir = output
    relgroupsdir = 'groups'
    groupsdir = os.path.join(outdir, relgroupsdir)
    try:
        os.mkdir(outdir)
    except:
        shutil.rmtree(outdir)
        os.mkdir(outdir)

    try:
        os.mkdir(groupsdir)
    except Exception:
        print('Please remove the directory ' + groupsdir + ' before continuing')
        return 1

    try:
        if not access_id or not access_key:
            connection = boto.ec2.connect_to_region(region_code)
        else:
            connection = boto.ec2.connect_to_region(region_code, aws_access_key_id=access_id, aws_secret_access_key=access_key)
    except boto.exception.NoAuthHandlerFound:
        print('Error: boto credentials are invalid. Check your configuration.')
        return 1

    if vpc_id:
        groups = connection.get_all_security_groups(filters={'vpc-id': vpc_id})
    else:
        groups = connection.get_all_security_groups()
    nameid_lookup = dict()
    for group in groups:
        nameid_lookup[group.id] = group.name

    for group in groups:
        fn = os.path.join(outdir, relgroupsdir, '%s.yaml' % str(group.name))
        if os.path.exists(fn):
            if not silence:
                duplicated_str = ' and merging duplicated'
            rules = state.load(open(fn))['rules']
        else:
            rules = []
            duplicated_str = ''
        if not silence:
            print('Forming%s group %s' % (duplicated_str, str(group.name)))
        data = {'description': group.description.encode('utf-8'), 
           'rules': rules}
        for rule in group.rules:
            for grant in rule.grants:
                append_to_rules(connection, rules, group, rule, grant, 'inbound', nameid_lookup)

        for rule in group.rules_egress:
            for grant in rule.grants:
                append_to_rules(connection, rules, group, rule, grant, 'outbound', nameid_lookup)

        with open(fn, 'w') as (out):
            out.write(dump(data))

    instances = connection.get_only_instances()
    instancesDict = dict()
    for instance in instances:
        if not silence:
            print('Found instance %s' % instance)
        k = instance.id.encode('utf-8')
        try:
            ip = instance.ip_address or ''
            domain = instance.public_dns_name or ''
            v = {'ip': ip.encode('utf-8'), 
               'domain': domain.encode('utf-8'), 
               'tags': {k.encode('utf-8'):v.encode('utf-8') for k, v in instance.tags.items()}, 'groups': [ str(group.name) for group in instance.groups ]}
            instancesDict[k] = v
        except Exception:
            print('ERROR: Could not process instance %s' % instance)

    with open(os.path.join(outdir, 'boxes.yaml'), 'w') as (out):
        out.write(dump(instancesDict))
    open(os.path.join(outdir, 'expirations.yaml'), 'w')


@contextlib.contextmanager
def vpc(region, vpc, key, secret):
    tmpdir = tempfile.mkdtemp()
    main(region, vpc, tmpdir, key, secret, True)
    yield tmpdir
    shutil.rmtree(tmpdir)