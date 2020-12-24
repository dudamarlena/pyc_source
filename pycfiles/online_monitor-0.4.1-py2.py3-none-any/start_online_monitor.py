# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/start_online_monitor.py
# Compiled at: 2018-07-05 04:39:41
import sys, os, psutil, subprocess, logging
from PyQt5 import Qt
import online_monitor
from online_monitor.utils import settings
from online_monitor.OnlineMonitor import OnlineMonitorApplication
from online_monitor.utils import utils

def kill(proc):
    process = psutil.Process(proc.pid)
    for child_proc in process.children(recursive=True):
        child_proc.kill()

    process.kill()


def run_script_in_shell(script, arguments, command=None):
    return subprocess.Popen('%s %s %s' % ('python' if not command else command, script, arguments), shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0)


def main():
    if sys.argv[1:]:
        args = utils.parse_arguments()
    else:
        package_path = os.path.dirname(online_monitor.__file__)
        settings.add_producer_sim_path(os.path.abspath(os.path.join(package_path, 'examples', 'producer_sim')))
        settings.add_converter_path(os.path.abspath(os.path.join(package_path, 'examples', 'converter')))
        settings.add_receiver_path(os.path.abspath(os.path.join(package_path, 'examples', 'receiver')))

        class Dummy(object):

            def __init__(self):
                self.config_file = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)) + '/configuration.yaml'))
                self.log = 'INFO'

        args = Dummy()
        logging.warning('No configuration file provided! Show a demo of the online monitor!')
    utils.setup_logging(args.log)
    producer_sim_process = run_script_in_shell('', args.config_file, 'start_producer_sim')
    converter_manager_process = run_script_in_shell('', args.config_file, 'start_converter')

    def appExec():
        app.exec_()
        try:
            kill(producer_sim_process)
        except psutil.NoSuchProcess:
            pass

        try:
            kill(converter_manager_process)
        except psutil.NoSuchProcess:
            pass

    app = Qt.QApplication(sys.argv)
    win = OnlineMonitorApplication(args.config_file)
    win.show()
    sys.exit(appExec())


if __name__ == '__main__':
    main()