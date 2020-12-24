# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/processbot.py
# Compiled at: 2018-09-24 09:11:31
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import subprocess, thread, re, datetime, os, introspection, thread, logging, traceback, base64, sys, busIndipendentMessages, computation_job_inputs, computational_job_input_actions, configInstance, output_parameters, action, resource_cleaner
from time import sleep
from collections import OrderedDict
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

class ProcessBot(object):
    """
    This script starts when the user call a new WPS execution.
    His task is to call the proper external executable/scripts according to the service.config file (provided in the cmd line with -s option) and send back to the WPS logging/progress
    information and error information if something unexpected happens.
    All the output including the log file is generated in a sand box directory created with joint information from service.config and external process start-up information.
    """

    def __init__(self, remote_config_filepath, service_config_filepath, execute_message):
        self._uniqueExeId = execute_message.UniqueId()
        self._remote_wps_endpoint = execute_message.originator()
        self._remote_wps_baseurl = execute_message.BaseURL()
        self._input_values = execute_message.variables()
        remote_config = configInstance.create(remote_config_filepath)
        bus_class_name = remote_config.get('DEFAULT', 'bus_class_name')
        uploader_class_name = None
        try:
            uploader_class_name = remote_config.get('UPLOADER', 'uploader_class_name')
        except:
            pass

        self._resource_file_dir = remote_config.get_path('DEFAULT', 'resource_file_dir')
        if remote_config.has_option('DEFAULT', 'wps_execution_shared_dir'):
            self._wps_execution_shared_dir = remote_config.get_path('DEFAULT', 'wps_execution_shared_dir')
            if not self._wps_execution_shared_dir.exists():
                self._wps_execution_shared_dir.mkdir()
        else:
            self._wps_execution_shared_dir = None
        serviceConfig = configInstance.create(service_config_filepath, case_sensitive=True, variables={'unique_exe_id': self._uniqueExeId, 'wps_execution_shared_dir': self._wps_execution_shared_dir}, raw=False)
        self.service = serviceConfig.get('DEFAULT', 'service')
        self.namespace = serviceConfig.get('DEFAULT', 'namespace')
        self.description = serviceConfig.get('DEFAULT', 'description')
        self._active = serviceConfig.get('DEFAULT', 'active').lower() == 'true'
        self._executable_path = serviceConfig.get('DEFAULT', 'executable_path')
        self._executable_cmd = serviceConfig.get('DEFAULT', 'executable_cmd')
        if not os.path.isabs(self._executable_path):
            full_executable_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self._executable_path)
            self._executable_cmd = self._executable_cmd.replace(self._executable_path, full_executable_path)
            self._executable_path = full_executable_path
        self._stdout_parser = serviceConfig.get_list('Logging', 'stdout_parser')
        self._stdout_action = serviceConfig.get_list('Logging', 'stdout_action')
        self._output_dir = serviceConfig.get_path('DEFAULT', 'output_dir')
        if not os.path.isabs(self._output_dir):
            self._output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self._output_dir)
        self._max_running_time = datetime.timedelta(seconds=serviceConfig.getint('DEFAULT', 'max_running_time_seconds'))
        if uploader_class_name:
            uploader_host = remote_config.get('UPLOADER', 'uploader_host')
            uploader_username = remote_config.get('UPLOADER', 'uploader_username')
            uploader_password = remote_config.get('UPLOADER', 'uploader_password')
            if remote_config.has_option('UPLOADER', 'uploader_private_rsa_key') and remote_config.has_option('UPLOADER', 'uploader_passphrase'):
                uploader_private_rsa_key = remote_config.get('UPLOADER', 'uploader_private_rsa_key')
                uploader_passphrase = remote_config.get('UPLOADER', 'uploader_passphrase')
                privatekey = open(uploader_private_rsa_key, 'r')
                rsa_key = RSA.importKey(privatekey, passphrase=uploader_passphrase)
                uploader_password = rsa_key.decrypt(base64.b64decode(uploader_password))
            self._uploader = introspection.get_class_four_arg(uploader_class_name, uploader_host, uploader_username, uploader_password, self._uniqueExeId)
        else:
            self._uploader = None
        input_sections = OrderedDict()
        for input_section in [ s for s in serviceConfig.sections() if 'input' in s.lower() or 'const' in s.lower() ]:
            input_sections[input_section] = serviceConfig.items_without_defaults(input_section, raw=False)

        self._input_parameters_defs = computation_job_inputs.ComputationJobInputs.create_from_config(input_sections)
        output_sections = OrderedDict()
        for output_section in [ s for s in serviceConfig.sections() if 'output' in s.lower() ]:
            output_sections[output_section] = serviceConfig.items_without_defaults(output_section, raw=False)

        self._output_parameters_defs = output_parameters.OutputParameters.create_from_config(output_sections, self._wps_execution_shared_dir, self._uploader)
        action_sections = OrderedDict()
        for action_section in [ s for s in serviceConfig.sections() if 'action' in s.lower() ]:
            action_sections[action_section] = serviceConfig.items_without_defaults(action_section, raw=False)

        self._input_params_actions = computational_job_input_actions.ComputationalJobInputActions.create_from_config(action_sections)
        self._lock_bus = thread.allocate_lock()
        self.bus = introspection.get_class_four_arg(bus_class_name, remote_config, self.service, self.namespace, self._uniqueExeId)
        self._finished = False
        self.bus.RegisterMessageCallback(busIndipendentMessages.FinishMessage, self.handle_finish)
        self.bus.RegisterMessageCallback(busIndipendentMessages.AbortMessage, self.handle_abort)
        return

    def get_resource_file_dir(self):
        return self._resource_file_dir

    def get_wps_execution_shared_dir(self):
        return self._wps_execution_shared_dir

    def max_execution_time(self):
        return self._max_running_time

    def ensure_output_dir_exists(self):
        directory = self._output_dir / self._uniqueExeId
        if not directory.exists():
            directory.mkdir()
        return directory

    def workdir(self):
        return self._output_dir / self._uniqueExeId

    def run(self):
        thread.start_new_thread(self.SpawnProcess, ())
        self.bus.Listen()

    def SpawnProcess(self):
        try:
            logger = logging.getLogger('ProcessBot.SpawnProcess')
            self.ensure_output_dir_exists()
            self._input_parameters_defs.set_values(self._input_values)
            self._input_params_actions.execute(self._input_parameters_defs)
            cmd = self._executable_cmd + ' ' + self._input_params_actions.get_cmd_line()
            invoked_process = subprocess.Popen(args=cmd.split(), cwd=self._executable_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            logger.info('process ' + self.service + ' created with PId ' + str(invoked_process.pid) + ' and command line: ' + cmd)
            rc = resource_cleaner.Resource.create_from_file(self._uniqueExeId, os.getpid())
            rc.set_from_processbot(os.getpid(), [invoked_process.pid])
            rc.write()
        except Exception as ex:
            logging.exception('Process ' + str(self._uniqueExeId) + ' Exception: ' + str(traceback.format_exc(sys.exc_info())))
            error_message = 'process failure\n' + str(ex)
            self.send_error_message(error_message)
            logger.info('after send job-error message to WPS')
            thread.interrupt_main()
            os._exit(return_code)

        self.process_output_parser(invoked_process)

    def process_output_parser(self, invoked_process):
        logger = logging.getLogger('ProcessBot.process_output_parser')
        logger.info('start parsing stdout of created process ' + self.service)
        with self._lock_bus:
            if self.bus.state() == 'connected':
                self.bus.SendMessage(busIndipendentMessages.LogMessage(self._remote_wps_endpoint, 'INFO', 'start parsing stdout of created process ' + self.service))
            else:
                try:
                    self.bus.xmpp.reconnect()
                    self.bus.xmpp.send_presence()
                    if self.bus.state() == 'connected':
                        self.bus.SendMessage(busIndipendentMessages.LogMessage(self._remote_wps_endpoint, 'INFO', 'start parsing stdout of created process ' + self.service))
                    else:
                        logger.info('[XMPP Disconnected]: Process ' + str(self._uniqueExeId) + ' Could not send info message to GeoServer Endpoint ' + str(self._remote_wps_endpoint))
                except:
                    logger.info('[XMPP Disconnected]: Process ' + str(self._uniqueExeId) + ' Could not send info message to GeoServer Endpoint ' + str(self._remote_wps_endpoint))

        stdout_parser_compiled = [ re.compile(r) for r in self._stdout_parser ]
        stack_trace = []
        while True:
            line = invoked_process.stdout.readline()
            if line != '':
                line = line.strip()
                logger.debug('Received line: ' + line)
                stack_trace.append(line)
                match = False
                for rgx, action in zip(stdout_parser_compiled, self._stdout_action):
                    res = rgx.match(line)
                    if res:
                        if action == 'progress':
                            with self._lock_bus:
                                if self.bus.state() != 'connected':
                                    try:
                                        self.bus.xmpp.reconnect()
                                        self.bus.xmpp.send_presence()
                                    except:
                                        logger.info('[XMPP Disconnected]: Process ' + str(self._uniqueExeId) + ' Could not send info message to GeoServer Endpoint ' + str(self._remote_wps_endpoint))

                                self.bus.SendMessage(busIndipendentMessages.ProgressMessage(self._remote_wps_endpoint, float(res.group(1).strip())))
                            match = True
                            break
                        elif action == 'log':
                            with self._lock_bus:
                                if self.bus.state() != 'connected':
                                    try:
                                        self.bus.xmpp.reconnect()
                                        self.bus.xmpp.send_presence()
                                    except:
                                        logger.info('[XMPP Disconnected]: Process ' + str(self._uniqueExeId) + ' Could not send info message to GeoServer Endpoint ' + str(self._remote_wps_endpoint))

                                self.bus.SendMessage(busIndipendentMessages.LogMessage(self._remote_wps_endpoint, res.group(1).strip(), res.group(2).strip()))
                            match = True
                            break
                        elif action == 'abort':
                            with self._lock_bus:
                                if self.bus.state() != 'connected':
                                    try:
                                        self.bus.xmpp.reconnect()
                                        self.bus.xmpp.send_presence()
                                    except:
                                        logger.info('[XMPP Disconnected]: Process ' + str(self._uniqueExeId) + ' Could not send info message to GeoServer Endpoint ' + str(self._remote_wps_endpoint))

                                self.bus.SendMessage(busIndipendentMessages.ErrorMessage(self._remote_wps_endpoint, res.group(2).strip()))
                            match = True
                            break
                        elif action == 'ignore':
                            match = True
                            break
                        else:
                            continue

            else:
                break

        logger.debug('process ' + self.service + 'stdout is over')
        return_code = invoked_process.wait()
        logger.info('process exit code is ' + str(return_code))
        if return_code == 0:
            logger.info('process exit code is ' + str(return_code) + ': success')
            logger.info('send job-completed message to WPS with output parameter')
            outputs = dict()
            try:
                for p in self._output_parameters_defs.parameters():
                    outputs[p.get_name()] = [
                     p.get_value(), p.get_description(), p.get_title(), p.get_type(), p.is_publish_as_layer(), p.get_publish_layer_name(), p.get_publish_default_style(), p.get_publish_target_workspace(), p.get_metadata()]

            except:
                logging.exception('Process ' + str(self._uniqueExeId) + ' Exception: ' + str(traceback.format_exc(sys.exc_info())))
                error_message = 'process exit code is ' + str(return_code) + ': failure\n' + ('\n').join(str(e) for e in stack_trace)
                self.send_error_message(error_message)
                logger.info('after send job-error message to WPS')
                thread.interrupt_main()
                os._exit(return_code)

            logger.info('trying to acquire bus lock...')
            with self._lock_bus:
                logger.info('bus lock acquired...')
                if self.bus.state() != 'connected':
                    try:
                        self.bus.xmpp.reconnect()
                        self.bus.xmpp.send_presence()
                    except:
                        logger.info('[XMPP Disconnected]: Process ' + str(self._uniqueExeId) + ' Could not send info message to GeoServer Endpoint ' + str(self._remote_wps_endpoint))

                counter = 1
                while not self._finished:
                    logger.info("sending 'completed' message tentative #" + str(counter))
                    self.bus.SendMessage(busIndipendentMessages.CompletedMessage(self._remote_wps_endpoint, self._remote_wps_baseurl, outputs))
                    counter = counter + 1
                    if counter < 100:
                        sleep(10)
                    else:
                        logger.error('Could not contact Remote WPS with. Forcibly shutdown the process...')
                        thread.interrupt_main()
                        os._exit(-1)

            logger.info('after send job-completed message to WPS')
        else:
            error_message = 'process exit code is ' + str(return_code) + ': failure\n' + ('\n').join(str(e) for e in stack_trace)
            logger.critical('process exit code is ' + str(return_code) + ': failure')
            self.send_error_message(error_message)
            logger.info('after send job-error message to WPS')
            thread.interrupt_main()
            os._exit(return_code)

    def handle_finish(self, finished_message):
        logger = logging.getLogger('ProcessBot.handle_finish')
        logger.info('received finish mesasge from WPS')
        self._finished = True
        with self._lock_bus:
            self.bus.disconnect()
        logger.info('disconnected from communication bus')
        sys.exit(0)

    def handle_abort(self, aborted_message):
        logger = logging.getLogger('ProcessBot.handle_abort')
        logger.info('received abort mesasge from WPS')
        self._finished = True
        with self._lock_bus:
            self.bus.disconnect()
        logger.info('disconnected from communication bus')
        sys.exit(-1)

    def send_error_message(self, msg):
        logger = logging.getLogger('ProcessBot.send_error_message to ' + str(self._remote_wps_endpoint))
        logger.error(msg)
        with self._lock_bus:
            if self.bus.state() == 'connected':
                self.bus.SendMessage(busIndipendentMessages.ErrorMessage(self._remote_wps_endpoint, msg))
            else:
                try:
                    self.bus.xmpp.reconnect()
                    self.bus.xmpp.send_presence()
                    if self.bus.state() == 'connected':
                        self.bus.SendMessage(busIndipendentMessages.ErrorMessage(self._remote_wps_endpoint, msg))
                    else:
                        sys.stdout.write('[XMPP Disconnected]: Process <UID>' + str(self._uniqueExeId) + '</UID> Could not send error message to GeoServer Endpoint <JID>' + str(self._remote_wps_endpoint) + '</JID> <MSG>' + msg.replace('\n', ' ').replace('\r', '') + '</MSG>')
                except:
                    sys.stdout.write('[XMPP Disconnected]: Process <UID>' + str(self._uniqueExeId) + '</UID> Could not send error message to GeoServer Endpoint <JID>' + str(self._remote_wps_endpoint) + '</JID> <MSG>' + msg.replace('\n', ' ').replace('\r', '') + '</MSG>')

        logger.debug('send error msg complete')
        thread.interrupt_main()
        os._exit(-1)

    def disconnect(self):
        with self._lock_bus:
            self.bus.disconnect()