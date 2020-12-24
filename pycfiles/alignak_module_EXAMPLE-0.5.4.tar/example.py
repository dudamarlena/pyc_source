# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: alignak_module_example/example.py
# Compiled at: 2018-05-06 01:54:24
"""
This module is an Alignak Broker module that collects the `monitoring_log` broks to send
them to a Python logger configured in the module configuration file
"""
import time, logging
from queue import Queue
import inspect
from alignak.basemodule import BaseModule
logger = logging.getLogger('alignak.module')
properties = {'daemons': [
             'arbiter', 'broker', 'scheduler', 'poller', 'receiver', 'reactionner'], 
   'type': 'example', 
   'external': True, 
   'phases': [
            'configuration', 'late_configuration', 'running', 'retention']}

def get_instance(mod_conf):
    """
    Return a module instance for the modules manager

    :param mod_conf: the module properties as defined globally in this file
    :return:
    """
    global logger
    logger.info('Give an instance of %s for alias: %s', mod_conf.python_name, mod_conf.module_alias)
    return Example(mod_conf)


class Example(BaseModule):
    """
    Example module main class
    """

    def __init__(self, mod_conf):
        """
        Module initialization

        mod_conf is a dictionary that contains:
        - all the variables declared in the module configuration file
        - a 'properties' value that is the module properties as defined globally in this file

        :param mod_conf: module configuration file as a dictionary
        """
        global logger
        BaseModule.__init__(self, mod_conf)
        logger = logging.getLogger('alignak.module.%s' % self.alias)
        logger.debug('inner properties: %s', self.__dict__)
        logger.debug('received configuration: %s', mod_conf.__dict__)
        self.option_1 = getattr(mod_conf, 'option1', None)
        self.option_2 = getattr(mod_conf, 'option2', None)
        self.option_3 = getattr(mod_conf, 'option3', None)
        logger.info('configuration, %s, %s, %s', self.option_1, self.option_2, self.option_3)
        return

    def init(self):
        """
        This function initializes the module instance. If False is returned, the modules manager
        will periodically retry an to initialize the module.
        If an exception is raised, the module will be definitely considered as dead :/

        This function must be present and return True for Alignak to consider the module as loaded
        and fully functional.

        :return: True if initialization is ok, else False
        """
        logger.info('Test - Example in %s', inspect.stack()[0][3])
        logger.info('Initialization of the example module')
        return True

    def do_loop_turn(self):
        """This function is called/used when you need a module with
        a loop function (and use the parameter 'external': True)
        """
        logger.info('In loop')
        time.sleep(1)

    def hook_tick(self, daemon):
        """This function is called on each daemon 'tick'"""
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_read_configuration(self, daemon):
        """This function is called after conf file reading"""
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def get_alignak_configuration(self):
        """This function must return a list of Alignak configuration parameters
        (variables, MACROS, ...)

        This is useful when your module allows to import configuration
        """
        logger.info('Test - Example in %s', inspect.stack()[0][3])
        configuration = {'process_performance_data': True, 
           'passive_service_checks_enabled': True, 
           'event_handlers_enabled': True, 
           'global_host_event_handler': None, 
           'global_service_event_handler': None, 
           'interval_length': 60, 
           'check_external_commands': True, 
           'passive_host_checks_enabled': True, 
           'check_host_freshness': True, 
           'check_service_freshness': True, 
           'notifications_enabled': True, 
           'flap_detection_enabled': True, 
           'active_service_checks_enabled': True, 
           'active_host_checks_enabled': True}
        logger.info('Returning Alignak configuration to the Arbiter: %s', str(configuration))
        return configuration

    def get_objects(self):
        """This function must return a list of config
        objects (hosts, services, commands, ...)

        This is useful when your module allows to import objects from external database
        """
        logger.info('Test - Example in %s', inspect.stack()[0][3])
        r = {'hosts': []}
        h = {'name': 'dummy host from dummy arbiter module', 
           'register': '0'}
        r['hosts'].append(h)
        r['hosts'].append({'host_name': 'module_host_1', 
           'address': 'localhost'})
        logger.info('Returning hosts objects to the Arbiter: %s', str(r))
        return r

    def hook_early_configuration(self, daemon):
        """This function is called after getting all config objects"""
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_late_configuration(self, daemon):
        """This function is called after configuration compilation
        This the last step of configuration reading
        """
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def update_retention_objects(self, daemon):
        """ Update retention date """
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def load_retention_objects(self, daemon):
        """ Self daemon objects retention - avoid using this! """
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_load_retention(self, daemon):
        """This function is called by the daemon to restore the objects live state """
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_save_retention(self, daemon):
        """This function is called before daemon exit to save the objects live state """
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_get_new_actions(self, daemon):
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_pre_scheduler_mod_start(self, daemon):
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def hook_scheduler_tick(self, daemon):
        logger.info('Test - Example in %s for daemon: %s', inspect.stack()[0][3], daemon)

    def want_brok(self, brok):
        """ This function is called to check if a module wants a specific type of brok
        Default is to return True to get all broks

        Only implement this function if it is necessary!
        """
        logger.info('Test - Example in %s, want brok type: %s', inspect.stack()[0][3], brok.type)
        return True

    def manage_brok(self, brok):
        """ This function is called as soon as a brok is received """
        logger.info('Test - Example in %s, got brok type: %s', inspect.stack()[0][3], brok.type)

    def manage_log_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_monitoring_log_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_clean_all_my_instance_id_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_downtime_raise_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_initial_broks_done_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_notification_raise_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_program_status_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_unknown_host_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_unknown_service_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_initial_host_status_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_initial_service_status_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_host_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_service_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_host_next_schedule_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_service_next_schedule_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_host_snapshot_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_service_snapshot_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_update_host_status_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def manage_update_service_status_brok(self, brok):
        """Deprecated ..."""
        logger.error('Deprecated function (%s) for module example', inspect.stack()[0][3])

    def main(self):
        """
        Main loop of the process

        This module is an "external" module
        :return:
        """
        global logger
        logger = logging.getLogger('alignak.module.%s' % self.alias)
        self.set_proctitle(self.alias)
        self.set_exit_handler()
        logger.info('starting...')
        while not self.interrupted:
            try:
                logger.debug('queue length: %s', self.to_q.qsize())
                start = time.time()
                message = self.to_q.get_nowait()
                for brok in message:
                    brok.prepare()
                    self.manage_brok(brok)

                logger.debug('time to manage %s broks (%d secs)', len(message), time.time() - start)
            except queue.Empty:
                time.sleep(0.1)

        logger.info('stopping...')
        logger.info('stopped')