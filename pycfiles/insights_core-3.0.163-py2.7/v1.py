# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/phase/v1.py
# Compiled at: 2020-04-16 14:56:28
from __future__ import print_function
import functools, json, logging, os, sys, atexit
from insights.client import InsightsClient
from insights.client.config import InsightsConfig
from insights.client.constants import InsightsConstants as constants
from insights.client.support import InsightsSupport
from insights.client.utilities import validate_remove_file, print_egg_versions, write_to_disk
from insights.client.schedule import get_scheduler
from insights.client.apps.compliance import ComplianceClient
from insights.client.apps.aws import aws_main
logger = logging.getLogger(__name__)

def phase(func):

    @functools.wraps(func)
    def _f():
        try:
            config = InsightsConfig().load_all()
        except ValueError as e:
            sys.stderr.write('ERROR: ' + str(e) + '\n')
            sys.exit(constants.sig_kill_bad)

        client = InsightsClient(config)
        if config.debug:
            logger.info('Core path: %s', os.path.dirname(__file__))
        try:
            func(client, config)
        except Exception:
            logger.exception('Fatal error')
            sys.exit(1)
        else:
            sys.exit(0)

    return _f


def get_phases():
    return [
     {'name': 'pre_update', 
        'run_as_root': True},
     {'name': 'update', 
        'run_as_root': True},
     {'name': 'post_update', 
        'run_as_root': True},
     {'name': 'collect_and_output', 
        'run_as_root': True}]


@phase
def pre_update(client, config):
    if config.version:
        logger.info(constants.version)
        sys.exit(constants.sig_kill_ok)
    if config.validate:
        try:
            validate_remove_file(config)
            sys.exit(constants.sig_kill_ok)
        except RuntimeError as e:
            logger.error(e)
            sys.exit(constants.sig_kill_bad)

    if config.enable_schedule:
        logger.debug('Updating config...')
        updated = get_scheduler(config).set_daily()
        if updated:
            logger.info('Automatic scheduling for Insights has been enabled.')
        sys.exit(constants.sig_kill_ok)
    if config.disable_schedule:
        updated = get_scheduler(config).remove_scheduling()
        if updated:
            logger.info('Automatic scheduling for Insights has been disabled.')
        if not config.register:
            sys.exit(constants.sig_kill_ok)
    if config.test_connection:
        logger.info('Running Connection Tests...')
        rc = client.test_connection()
        if rc == 0:
            sys.exit(constants.sig_kill_ok)
        else:
            sys.exit(constants.sig_kill_bad)
    if config.support:
        support = InsightsSupport(config)
        support.collect_support_info()
        sys.exit(constants.sig_kill_ok)
    if config.diagnosis:
        remediation_id = None
        if config.diagnosis is not True:
            remediation_id = config.diagnosis
        resp = client.get_diagnosis(remediation_id)
        if not resp:
            sys.exit(constants.sig_kill_bad)
        print(json.dumps(resp))
        sys.exit(constants.sig_kill_ok)
    return


@phase
def update(client, config):
    client.update()
    if config.payload:
        logger.debug('Uploading a payload. Bypassing rules update.')
        return
    client.update_rules()


@phase
def post_update(client, config):
    logger.debug('Machine ID: %s', client.get_machine_id())
    logger.debug('CONFIG: %s', config)
    print_egg_versions()
    if config.portal_access or config.portal_access_no_insights:
        logger.debug('Entitling an AWS host. Bypassing registration check.')
        return
    else:
        if config.show_results:
            try:
                client.show_results()
                sys.exit(constants.sig_kill_ok)
            except Exception as e:
                print(e)
                sys.exit(constants.sig_kill_bad)

        if config.check_results:
            try:
                client.check_results()
                sys.exit(constants.sig_kill_ok)
            except Exception as e:
                print(e)
                sys.exit(constants.sig_kill_bad)

        if config.legacy_upload:
            if config.status:
                reg_check = client.get_registration_status()
                for msg in reg_check['messages']:
                    logger.info(msg)

                if reg_check['status']:
                    sys.exit(constants.sig_kill_ok)
                else:
                    sys.exit(constants.sig_kill_bad)
            if config.unregister:
                if client.unregister():
                    sys.exit(constants.sig_kill_ok)
                else:
                    sys.exit(constants.sig_kill_bad)
            if config.offline:
                logger.debug('Running client in offline mode. Bypassing registration.')
                return
            if config.display_name and not config.register:
                if client.set_display_name(config.display_name):
                    if 'display_name' in config._cli_opts:
                        sys.exit(constants.sig_kill_ok)
                else:
                    sys.exit(constants.sig_kill_bad)
            reg = client.register()
            if reg is None:
                logger.info('Could not connect to the Insights API. Run insights-client --test-connection for more information.')
                sys.exit(constants.sig_kill_bad)
            elif reg is False:
                sys.exit(constants.sig_kill_bad)
            if config.register and not config.disable_schedule:
                if get_scheduler(config).set_daily():
                    logger.info('Automatic scheduling for Insights has been enabled.')
            return
        if config.offline:
            logger.debug('Running client in offline mode. Bypassing registration.')
            return
        if config.payload:
            logger.debug('Uploading a specified archive. Bypassing registration.')
            return
        reg_check = client.get_registration_status()
        if reg_check is None:
            sys.exit(constants.sig_kill_bad)
        if config.status:
            if reg_check:
                logger.info('This host is registered.')
                sys.exit(constants.sig_kill_ok)
            else:
                logger.info('This host is unregistered.')
                sys.exit(constants.sig_kill_bad)
        if config.unregister:
            if reg_check:
                logger.info('Unregistering this host from Insights.')
                if client.unregister():
                    get_scheduler(config).remove_scheduling()
                    sys.exit(constants.sig_kill_ok)
                else:
                    sys.exit(constants.sig_kill_bad)
            else:
                logger.info('This host is not registered, unregistration is not applicable.')
                sys.exit(constants.sig_kill_bad)
        if not reg_check and not config.register:
            logger.info('This host has not been registered. Use --register to register this host.')
            sys.exit(constants.sig_kill_bad)
        if config.reregister:
            reg_check = False
            client.clear_local_registration()
        if config.register:
            if reg_check:
                logger.info('This host has already been registered.')
            if not config.disable_schedule and get_scheduler(config).set_daily():
                logger.info('Automatic scheduling for Insights has been enabled.')
        if 'display_name' in config._cli_opts and not config.register:
            if client.set_display_name(config.display_name):
                sys.exit(constants.sig_kill_ok)
            else:
                sys.exit(constants.sig_kill_bad)
        return


@phase
def collect_and_output(client, config):
    atexit.register(write_to_disk, constants.pidfile, delete=True)
    if config.portal_access or config.portal_access_no_insights:
        if aws_main(config):
            sys.exit(constants.sig_kill_ok)
        else:
            sys.exit(constants.sig_kill_bad)
    if config.compliance:
        config.payload, config.content_type = ComplianceClient(config).oscap_scan()
    if config.payload:
        insights_archive = config.payload
    else:
        try:
            insights_archive = client.collect()
        except RuntimeError as e:
            logger.error(e)
            sys.exit(constants.sig_kill_bad)

        config.content_type = 'application/vnd.redhat.advisor.collection+tgz'
    if config.no_upload:
        if config.output_dir:
            client.copy_to_output_dir(insights_archive)
        elif config.output_file:
            client.copy_to_output_file(insights_archive)
    else:
        if not insights_archive:
            sys.exit(constants.sig_kill_bad)
        resp = None
        try:
            resp = client.upload(payload=insights_archive, content_type=config.content_type)
        except (IOError, ValueError, RuntimeError) as e:
            logger.error(str(e))
            sys.exit(constants.sig_kill_bad)

        if resp:
            if config.to_json:
                print(json.dumps(resp))
        client.delete_cached_branch_info()
        try:
            client.rotate_eggs()
        except IOError:
            message = 'Failed to rotate %s to %s' % (
             constants.insights_core_newest,
             constants.insights_core_last_stable)
            logger.debug(message)
            raise IOError(message)

    return