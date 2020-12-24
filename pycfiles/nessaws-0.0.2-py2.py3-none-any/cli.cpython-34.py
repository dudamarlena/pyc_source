# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adamstauffer/Desktop/TerbiumCode/Github/nessaws/src/nessaws/cli.py
# Compiled at: 2017-06-23 14:11:34
# Size of source mod 2**32: 8068 bytes
"""Provides the nessaws command line interface."""
from builtins import input
import datetime, logging, sys, click, yaml
from nessaws.aws import get_ec2_instances, get_rds_instances
from nessaws.config import load_state, parse_config
from nessaws.excel import write_excel_output
from nessaws.mailer import send_pentest_request
from nessaws.nessus import NessusConnection
logger = logging.getLogger('nessaws')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename='nessaws.log', mode='w')
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

@click.group()
@click.option('-c', '--config', default='config.yml', help='Provide the path to the configuration file.', type=click.Path(exists=True))
@click.pass_context
def main(ctx, config):
    """Automate Nessus scans against AWS EC2 endpoints."""
    global_config = parse_config(config)
    ctx.obj = {'config': global_config}


@main.command('pentest-request')
@click.option('-t', '--tags', help='Tag values to determine applicable EC2/RDS instances. Multiple tag values supported.', multiple=True, required=True)
@click.option('--dry-run', is_flag=True, help='Generates state file without sending a pentest request.')
@click.pass_obj
@click.pass_context
def pen_test_request(ctx, options, tags, dry_run):
    """Create/send the penetration test request for the tagged instances."""
    logger.info('Performing pentest-request with following tag values "{}"'.format(', '.join(tags)))
    ec2_scans = get_ec2_instances(tag_values=tags, aws_accounts=options['config']['aws_accounts'])
    rds_scans = get_rds_instances(tag_values=tags, aws_accounts=options['config']['aws_accounts'])
    config_values = options['config']
    scans = rds_scans
    for scan in ec2_scans:
        if scans.get(scan):
            scans[scan]['targets'] += ec2_scans[scan]['targets']
        else:
            scans[scan] = ec2_scans[scan]

    if scans == {}:
        logger.critical('No EC2/RDS instances with the tag values "{}" were found.'.format(', '.join(tags)))
        sys.exit(-1)
    aws_account_names = []
    for account in options['config']['aws_accounts']:
        aws_account_names.append(account['account_name'])

    state = {'start_date': config_values['start_date'], 
     'end_date': config_values['end_date'], 
     'tag_values': tags, 
     'account_names': aws_account_names, 
     'scans': []}
    for scan_name in scans:
        state['scans'].append({'scan_name': scan_name, 
         'targets': scans[scan_name]['targets']})

    with open('.nessaws_state', 'w') as (state_file):
        yaml.safe_dump(state, state_file, default_flow_style=False)
    send_pentest_request(config=options['config'], state=state, dry_run=dry_run)


@main.command('perform-scan')
@click.pass_obj
@click.pass_context
def perform_scan(ctx, options):
    """Perform the Nessus scan against the tagged instances."""
    state_object = load_state()
    start_datetime = datetime.datetime.strptime(state_object['start_date'], '%a, %d %b %Y %H:%M:%S GMT')
    end_datetime = datetime.datetime.strptime(state_object['end_date'], '%a, %d %b %Y %H:%M:%S GMT')
    now = datetime.datetime.utcnow()
    if now > end_datetime or now < start_datetime:
        while True:
            print('The current system time is not within the submitted start time and end time. Are you sure you want to continue?\n\nType "yes" or "no":')
            choice = input().lower()
            if choice == 'yes':
                break
            elif choice == 'no':
                sys.exit(1)
            else:
                print('Please respond with "yes" or "no"')

    logger.info('Performing Nessus scans with authorization between {} - {}'.format(state_object['start_date'], state_object['end_date']))
    nessus_conn = NessusConnection(options['config']['nessus_url'], options['config']['nessus_username'], options['config']['nessus_password'], options['config']['nessus_secure'])
    successful_scan = False
    for scan in state_object['scans']:
        scan_name = scan['scan_name']
        scan['status'] = None
        instance_ips = []
        for target in scan['targets']:
            if target['type'] == 'ec2':
                if options['config']['always_use_private_ip']:
                    instance_ips.append(str(target['private_ip']))
                else:
                    instance_ips.append(str(target['public_ip']) if target.get('public_ip') else str(target['private_ip']))
            if target['type'] == 'rds':
                instance_ips.append(target['endpoint'])
                continue

        logger.info('Launching scan {}'.format(scan_name))
        scan_uuid = nessus_conn.launch_scan(scan_name, instance_ips)
        if scan_uuid:
            logger.info('\nWaiting for scan "{}" to be completed...'.format(scan_name))
            if nessus_conn.wait_for_scan_completion(scan_uuid) == 'completed':
                scan.update(nessus_conn.get_credentialed_hosts(scan_name, scan_uuid))
                logger.info('Exporting scan csv {}-{}'.format(scan_name, scan_uuid))
                result_filename = nessus_conn.export_scan_csv(scan_name, scan_uuid)
                scan['result_file'] = result_filename
                scan['status'] = 'completed'
                successful_scan = True
                logger.info('Scan "{}" completed successfully'.format(scan_name))
            else:
                logger.warning('\nNessus scan "{}" was not completed successfully, the following instances may not have been scanned:\n\n {}'.format(scan_name, ', '.join(instance_ips)))
                scan['status'] = 'failed'
        else:
            logger.warning('\nUnable to find a Nessus scan with name "{}", the following instances will not be scanned:\n\n {}'.format(scan_name, ', '.join(instance_ips)))
            scan['status'] = 'not_found'

    if not successful_scan:
        logger.critical('None of the Nessus scans completed successfully. Please check your Nessus scans configurations and try again.')
        sys.exit(-1)
    logger.info('\nScans completed, determining output...')
    if options['config']['output'] == 'excel':
        logger.info('\nExcel was selected for output, writing xlsx...')
        output_filename = write_excel_output(state_object)
        logger.info('\nExported result file is named: "{}"'.format(output_filename))
    else:
        logger.info('\nNo output configured, Nessus report CSVs are located in the current directory.')