# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/wpsagent.py
# Compiled at: 2018-09-13 11:06:18
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import logging.config, logging, argparse, sys, thread, path, traceback, servicebot, processbot, configInstance, busIndipendentMessages, resource_cleaner

class WPSAgent(object):

    def __init__(self, args):
        self.verbose = False
        self.args = args

    def find_logger_property_file(self, find_logger_property_file_path):
        if self.args.logconf == None:
            logger_properties_file = find_logger_property_file_path / 'logger.properties'
        else:
            logger_properties_file = self.args.logconf
        return logger_properties_file

    @staticmethod
    def log_bootstrap_error(msg, stack_trace):
        sys.stderr.write(msg + '\n')
        sys.stderr.write(stack_trace + '\n')

    @staticmethod
    def set_resource_cleaner_parameters(pid_files_dir, process_time_threshold, workdir_time_threshold, sleep_time_seconds):
        resource_cleaner.Resource.pid_files_dir = pid_files_dir
        resource_cleaner.Resource.process_time_threshold = process_time_threshold
        resource_cleaner.Resource.workdir_time_threshold = workdir_time_threshold
        resource_cleaner.Resource.sleep_time_seconds = sleep_time_seconds

    @staticmethod
    def create_logger(logger_config_file, workdir, verbose):
        defaults = {}
        if workdir != None:
            defaults['workdir'] = workdir
            if '\\' in defaults['workdir']:
                defaults['workdir'] = defaults['workdir'].replace('\\', '/')
        logging.config.fileConfig(str(logger_config_file), defaults=defaults)
        logger = logging.getLogger('main.create_logger')
        if not verbose:
            for h in logger.root.handlers:
                h.addFilter(SleekXMPPLoggerFilter())

        logger.debug('Logger initialized with file ' + str(logger_config_file))
        return

    def create_bot(self):
        pass

    def run(self):
        logger = logging.getLogger('WPSAgent.run')
        try:
            bot = self.create_bot()
            logger.info('Start bot execution')
            bot.run()
        except Exception as e:
            msg = 'Bot failure due to: ' + str(e)
            logger.fatal(msg)
            logger.fatal(traceback.format_exc())
            bot.send_error_message(msg)
            bot.disconnect()
            logger.fatal('Exit Bot process with code ' + str(101))
            sys.exit(101)


class WPSAgentProcess(WPSAgent):
    """This script starts when the user call a new WPS execution. 
        His task is to call the proper external executable/scripts according to the service.config file (option -s in command line) and send back to the WPS logging and progress 
        information and error information if something unexpected happens.
        All the output including the log file is generated in a sand box directory created with joint information from service.config and external process start-up information.
        """

    def __init__(self, args):
        super(WPSAgentProcess, self).__init__(args)
        try:
            config_dir_service = path.path(args.serviceconfig).dirname()
            self.exe_msg = busIndipendentMessages.ExecuteMessage.deserialize(args.params)
            serviceConfig = configInstance.create(args.serviceconfig, case_sensitive=True, variables={'unique_exe_id': self.exe_msg.UniqueId()}, raw=False)
            work_dir = serviceConfig.get_path('DEFAULT', 'workdir')
            if not work_dir.exists():
                work_dir.mkdir()
            WPSAgent.create_logger(self.find_logger_property_file(config_dir_service), work_dir, self.verbose)
        except Exception as e:
            msg = 'Failure during bot bootstrap due to : ' + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)

        self.run()

    def create_bot(self):
        try:
            logger = logging.getLogger('WPSAgentProcess.create_bot')
            logger.info('Create process bot')
            bot = processbot.ProcessBot(self.args.remoteconfig, self.args.serviceconfig, self.exe_msg)
            self.set_resource_cleaner_parameters(bot.get_resource_file_dir(), bot.max_execution_time(), bot.max_execution_time(), bot.max_execution_time())
            return bot
        except Exception as e:
            msg = 'Failure during bot bootstrap due to : ' + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)


class WPSAgentService(WPSAgent):

    def __init__(self, args):
        try:
            super(WPSAgentService, self).__init__(args)
            remote_config_dir = path.path(args.remoteconfig).dirname()
            self.create_logger(self.find_logger_property_file(remote_config_dir), None, self.verbose)
        except Exception as e:
            msg = 'Failure during bot bootstrap due to : ' + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)

        self.run()
        return

    def create_bot(self):
        try:
            logger = logging.getLogger('WPSAgentService.create_bot')
            logger.info('Create process bot')
            bot = servicebot.ServiceBot(self.args.remoteconfig, self.args.serviceconfig)
            logger.info('Create resource cleaner')
            WPSAgent.set_resource_cleaner_parameters(bot.get_resource_file_dir(), bot.max_execution_time(), bot.max_execution_time(), bot.max_execution_time())
            thread.start_new_thread(resource_cleaner.Resource.clean_up_all, ())
            return bot
        except Exception as e:
            msg = 'Failure during bot bootstrap due to : ' + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)


class SleekXMPPLoggerFilter(logging.Filter):

    def filter(self, record):
        return 'sleekxmpp' not in record.name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--remoteconfig', nargs='?', default='remote.config', help='Config file containing connection information on the calling agent (e.g. XMPP server)')
    parser.add_argument('-s', '--serviceconfig', nargs='?', default='service.config', help='Config file containing information concerning the local process to be invoked by WPS')
    parser.add_argument('-l', '--logconf', nargs='?', default=None, help='Logger config file if not provided logger.conf in remoteconfig directory (runtype=service) or logger.conf in serviceconfig directory (runtype=process) will be used')
    parser.add_argument('-p', '--params', nargs='?', help='JSON file containing input parameters')
    parser.add_argument('-e', '--executionid', nargs='?', help='Unique execution id')
    parser.add_argument('runtype', help='Run type [service|process])')
    cmdargs = parser.parse_args()
    if cmdargs.runtype == 'service':
        WPSAgentService(cmdargs)
    else:
        WPSAgentProcess(cmdargs)