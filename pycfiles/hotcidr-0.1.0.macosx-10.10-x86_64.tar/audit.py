# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/audit.py
# Compiled at: 2014-09-11 23:30:12
from __future__ import print_function
import datetime, math, boto.ec2, hotcidr.state
from hotcidr.modifydatabase import printSinceSpecifiedTime
from hotcidr.util import *

def get_icmp_control_msg(code):
    controlmsg_dict = {'-1': 'All', 
       '0': 'Echo Reply', 
       '3': 'Destination Unreachable', 
       '4': 'Source Quench', 
       '5': 'Redirect Message', 
       '8': 'Echo Request', 
       '9': 'Router Advertisement', 
       '10': 'Router Solicitation', 
       '11': 'Time Exceeded', 
       '12': 'Parameter Problem: Bad IP header', 
       '13': 'Timestamp', 
       '14': 'Timestamp Reply', 
       '15': 'Information Request', 
       '16': 'Information Reply', 
       '17': 'Address Mask Request', 
       '18': 'Address Mask Reply', 
       '30': 'Traceroute'}
    if isinstance(code, int):
        if code in controlmsg_dict:
            return controlmsg_dict[code]
        else:
            return 'reserved'

    else:
        return 'n/a'


def format_rule(rule, repo, yamlfile, createdby, createdon, approvedby, approvedon, action):
    corrupted = False
    corrupted_str = 'n/a'
    rule['date_timestamp'] = createdon
    rule['approved_date_timestamp'] = approvedon
    if 'direction' in rule:
        if rule['direction'] == 'inbound':
            from_or_to = 'from'
        else:
            from_or_to = 'to'
    else:
        corrupted = True
        from_or_to = 'from/to'
        rule['direction'] = corrupted_str
    if 'location' in rule:
        if is_cidr(rule['location']):
            type_str = 'CIDR'
        else:
            type_str = 'group'
    else:
        corrupted = True
        type_str = 'group'
        rule['location'] = corrupted_str
    if 'ports' in rule:
        if hasattr(rule['ports'], 'toport') and rule['ports'].toport:
            rule['toport'] = str(rule['ports'].toport)
        if hasattr(rule['ports'], 'fromport') and rule['ports'].fromport:
            rule['fromport'] = str(rule['ports'].fromport)
    if 'protocol' not in rule:
        corrupted = True
    if 'protocol' not in rule:
        rule['protocol'] = corrupted_str
    if 'description' not in rule:
        rule['description'] = corrupted_str
    if 'hexsha' in rule:
        commit_message = get_git_commit(rule['hexsha'], repo, yamlfile)
    else:
        commit_message = None
    if 'justification' not in rule and not commit_message:
        rule['justification'] = corrupted_str
    else:
        if 'justification' not in rule and commit_message:
            rule['justification'] = commit_message
        else:
            if 'justification' in rule and commit_message:
                rule['justification'] += " (commit message: '" + commit_message + "')"
            if rule['protocol'] == 'icmp':
                if 'fromport' in rule:
                    ports_str = get_icmp_control_msg(rule['fromport'])
                    rule['toport'] = 'n/a'
                    rule['fromport'] = ports_str
                else:
                    ports_str = corrupted_str
            else:
                if 'fromport' not in rule or not rule['fromport']:
                    rule['fromport'] = corrupted_str
                if 'toport' not in rule or not rule['toport']:
                    rule['toport'] = corrupted_str
                if rule['fromport'] == rule['toport']:
                    ports_str = rule['fromport']
                else:
                    ports_str = str(rule['fromport']) + '-' + str(rule['toport'])
            try:
                createdon_str = datetime.datetime.fromtimestamp(float(createdon)).strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
            except ValueError:
                createdon_str = 'n/a'

        try:
            approvedon_str = datetime.datetime.fromtimestamp(float(approvedon)).strftime('%Y-%m-%d %H:%M:%S') + ' UTC'
        except ValueError:
            approvedon_str = 'n/a'

    action_str = action
    if corrupted:
        action_str = 'corruptly ' + action_str
    rule['action'] = action_str
    rule['approved_author'] = approvedby
    rule['approved_date'] = approvedon_str
    rule['author'] = createdby
    rule['date'] = createdon_str
    rule['ports'] = ports_str
    rule['from_or_to'] = from_or_to
    rule['type'] = type_str
    rule['protocol'] = str(rule['protocol'])
    rule['fromport'] = str(rule['fromport'])
    rule['toport'] = str(rule['toport'])
    return rule


def print_rule(rule, from_time, to_time, output_webserver):
    output = ''
    if int(rule['date_timestamp']) >= from_time and int(rule['date_timestamp']) <= to_time:
        if output_webserver:
            output += ('"{action}","{protocol}","{ports}","{direction}","{type_str}","{location}","{createdby}","{createdon}","{approvedby}","{approvedon}","{justification}","{description}"\n').format(action=rule['action'], protocol=rule['protocol'], ports=rule['ports'], direction=rule['direction'], fromto=rule['from_or_to'], type_str=rule['type'], location=rule['location'], createdby=rule['author'], createdon=rule['date'], approvedby=rule['approved_author'], approvedon=rule['approved_date'], justification=rule['justification'], description=rule['description'])
        else:
            output += ('\t {protocol} {fromport} to {toport} {direction} {fromto} {type_str} {location} {action} by {createdby} on {createdon} approved by {approvedby} on {approvedon} because {justification} {description} \n').format(protocol=rule['protocol'].ljust(5), fromport=rule['fromport'].ljust(9), toport=rule['toport'].ljust(7), direction=rule['direction'].ljust(10), fromto=rule['from_or_to'].ljust(7), type_str=rule['type'].ljust(6), location=rule['location'].ljust(20), action=rule['action'].ljust(26), createdby=rule['author'].ljust(16), createdon=rule['date'].ljust(26), approvedby=rule['approved_author'].ljust(16), approvedon=rule['approved_date'].ljust(26), justification=rule['justification'].ljust(20), description=rule['description'])
    return output


def main(repo, from_time, to_time, region_code, vpc_id, aws_id, aws_key, output, output_webserver, selectedgroup, sort_chronologically, silence):
    repo, is_clone_url = get_valid_repo(repo)
    if not repo:
        print('Error: invalid repo specified', file=sys.stderr)
        return 1
    else:
        if not from_time:
            from_time = 0
        else:
            if isint(from_time):
                from_time = int(from_time)
            else:
                print('Warning: from-time argument is not an integer. It should be a timestamp in UTC. It will be set to 0.', file=sys.stderr)
                from_time = 0
            if not to_time:
                to_time = int(math.floor(time.time()))
            else:
                if isint(to_time):
                    to_time = int(to_time)
                else:
                    print('Warning: from-time argument is not an integer. It should be a timestamp in UTC. It will be set to the current time.', file=sys.stderr)
                    to_time = int(math.floor(time.time()))
                output_str = ''
                if output_webserver:
                    output_str += '---\n'
                boxgroups = {}
                try:
                    boxesyaml = file(os.path.join(repo, 'boxes.yaml'), 'r')
                    boxes = hotcidr.state.load(boxesyaml)
                except IOError:
                    print('Warning: ' + os.path.join(repo, 'boxes.yaml') + ' is missing. Audit output will have no instances listed.', file=sys.stderr)
                    boxes = []
                except yaml.scanner.ScannerError as e:
                    print('Warning: boxes.yaml is not properly formatted:\n' + str(e), file=sys.stderr)
                    print('Audit output will have no instances listed', file=sys.stderr)
                    boxes = []

            if hasattr(boxes, 'keys'):
                for box in boxes.keys():
                    for boxgroup in boxes[box]['groups']:
                        if boxgroup not in boxgroups:
                            boxgroups[boxgroup] = []
                        if 'domain' in boxes[box] and boxes[box]['domain']:
                            boxgroups[boxgroup].append(boxes[box]['domain'])
                        elif 'ip' in boxes[box] and boxes[box]['ip']:
                            boxgroups[boxgroup].append(boxes[box]['ip'])
                        elif 'tags' in boxes[box] and 'Name' in boxes[box]['tags'] and boxes[box]['tags']['Name']:
                            boxgroups[boxgroup].append(boxes[box]['tags']['Name'])

            connection = None
            if region_code:
                try:
                    if not aws_id or not aws_key:
                        connection = boto.ec2.connect_to_region(region_code)
                    else:
                        connection = boto.ec2.connect_to_region(region_code, aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
                except boto.exception.NoAuthHandlerFound:
                    print('Warning: boto credentials and/or region-code are invalid or missing. The audit will not include security group ids.')
                    return 1

            else:
                print('Warning: region-code argument required for printing security group ids in audit. The audit will not include security group ids.')
            groups = None
            if connection:
                if vpc_id:
                    groups = connection.get_all_security_groups(filters={'vpc-id': vpc_id})
                else:
                    groups = connection.get_all_security_groups()
            nameid_lookup = dict()
            if groups:
                for group in groups:
                    if selectedgroup and not group.name == selectedgroup:
                        continue
                    if group.name in nameid_lookup:
                        print('Warning: vpc-id has not been specified, and there are two vpcs with the group ' + group.name + '. The audit will not include security group ids.')
                        break
                    nameid_lookup[group.name.encode('ascii')] = group.id.encode('ascii')

            if selectedgroup:
                if not selectedgroup.endswith('.yaml'):
                    selectedgroup += '.yaml'
                groups = {selectedgroup: os.path.join('groups', selectedgroup)}
            else:
                groups = get_groups_dict(repo)
            groups_num = len(groups)
            i = 0
            for group in groups:
                if groups_num == 0:
                    print('ERROR: No groups loaded.', file=sys.stderr)
                    return 1
                i += 1
                if not silence:
                    print('%s%% Processing %s' % (str(int(100 * i / groups_num)), group), file=sys.stderr)
                sys.stderr.flush()
                if i > 1:
                    if output_webserver:
                        output_str += '---\n'
                    else:
                        output_str += '\n'
                try:
                    yamlfile = open(os.path.join(repo, groups[group]), 'r')
                    rulesyaml = yamlfile.read()
                    yamlfile.close()
                    rules = hotcidr.state.load(rulesyaml)
                except IOError:
                    print('Warning: ' + os.path.join(repo, groups[group]) + ' is missing.', file=sys.stderr)
                    print('Skipping group; it will not be included in the audit output', file=sys.stderr)
                    continue
                except yaml.scanner.ScannerError as e:
                    print('Warning: ' + os.path.join(repo, groups[group]) + ' is not properly formatted:\n' + str(e), file=sys.stderr)
                    print('Skipping group; it will not be included in the audit output', file=sys.stderr)
                    continue

                group_name = groups[group].split('/')[1].split('.')[0]
                if group_name in nameid_lookup:
                    output_str += nameid_lookup[group_name] + ',' + group_name + '\n'
                else:
                    output_str += group_name + '\n'
                output_str += 'Machines:\n'
                if group in boxgroups:
                    if output_webserver:
                        for boxg in boxgroups[group]:
                            output_str += boxg
                            if not boxg == boxgroups[group][(-1)]:
                                output_str += ','

                    else:
                        for boxg in boxgroups[group]:
                            output_str += '\t' + boxg + '\n'

                if output_webserver:
                    output_str += '\n'
                added_deleted_rules = get_added_deleted_rules(repo, groups[group])
                formatted_rules = []
                if output_webserver:
                    output_str += 'Action,Protocol,Ports,Direction,Type,Location,Changed by,Changed on,Approved by,Approved on,Justification,Description\n'
                else:
                    if not sort_chronologically:
                        output_str += 'Rules added:\n'
                    else:
                        output_str += 'Rules:\n'
                    for rule in added_deleted_rules['added']:
                        if len(rule.keys()) == 3 and 'hexsha' in rule and 'date' in rule and 'author' in rule:
                            continue
                        approved_authdate = get_commit_approved_authdate(rule['hexsha'], repo, groups[group])
                        formatted_rule = format_rule(rule, repo, groups[group], rule['author'], rule['date'], approved_authdate['author'], approved_authdate['date'], 'added')
                        if not sort_chronologically:
                            output_str += print_rule(formatted_rule, from_time, to_time, output_webserver)
                        else:
                            formatted_rules.append(formatted_rule)
                        approved_authdate = {}

                    if not output_webserver and not sort_chronologically:
                        output_str += 'Rules previously added:\n'
                    for rule in added_deleted_rules['added_previously']:
                        approved_authdate = get_commit_approved_authdate(rule['hexsha'], repo, groups[group])
                        formatted_rule = format_rule(rule, repo, groups[group], rule['author'], rule['date'], approved_authdate['author'], approved_authdate['date'], 'added previously')
                        if not sort_chronologically:
                            output_str += print_rule(formatted_rule, from_time, to_time, output_webserver)
                        else:
                            formatted_rules.append(formatted_rule)
                        approved_authdate = {}

                    if not output_webserver and not sort_chronologically:
                        output_str += 'Rules deleted:\n'
                    for rule in added_deleted_rules['deleted']:
                        approved_authdate = get_commit_approved_authdate(rule['hexsha'], repo, groups[group])
                        formatted_rule = format_rule(rule, repo, groups[group], rule['author'], rule['date'], approved_authdate['author'], approved_authdate['date'], 'deleted')
                        if not sort_chronologically:
                            output_str += print_rule(formatted_rule, from_time, to_time, output_webserver)
                        else:
                            formatted_rules.append(formatted_rule)
                        approved_authdate = {}

                if sort_chronologically:
                    sort_by_key = 'approved_date'
                    formatted_dict = {}
                    for formatted_rule in formatted_rules:
                        if formatted_rule[sort_by_key] not in formatted_dict:
                            formatted_dict[formatted_rule[sort_by_key]] = []
                        formatted_dict[formatted_rule[sort_by_key]].append(formatted_rule)

                    for timestamp in sorted(formatted_dict, reverse=True):
                        for formatted_rule in formatted_dict[timestamp]:
                            output_str += print_rule(formatted_rule, from_time, to_time, output_webserver)

        if output:
            f = open(output, 'w')
            f.write(output_str)
            f.close()
        else:
            print(output_str)
        if is_clone_url:
            rmtree(repo)
        if not silence:
            print('Audit successfully completed for %d groups.' % i, file=sys.stderr)
        sys.stderr.flush()
        return output_str