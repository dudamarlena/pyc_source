# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/bundle_wrapper/../external/bundle/src/bundle/impl/bundle_manager.py
# Compiled at: 2014-02-24 20:40:00
import sys, getopt, logging, Queue, threading, argparse, pickle
try:
    import bundle_agent
except ImportError:
    logging.critical("Can't find module: bundle_agent")
    sys.exit(1)

cluster_list = {}
default_credential_file = 'bundle_credentials.txt'
cluster_credentials = []

class BundleManager(object):

    def __init__(self):
        pass

    def add_cluster(self, cluster_credential, finished_job_trace):
        cluster = bundle_agent.get(cluster_credential, finished_job_trace)
        if cluster:
            cluster_list[cluster_credential['hostname']] = cluster
            cluster_credentials.append(dict(cluster_credential))
            return cluster_credential['hostname']
        else:
            return

    def remove_cluster(self, cluster_id):
        if cluster_id in cluster_list:
            cluster_list[cluster_id].close()
            cluster_list.pop(cluster_id, None)
        else:
            print ('ERROR - cluster {} not in cluster list {}').format(cluster_id, cluster_list.keys())
        return

    def get_cluster_list(self):
        return cluster_list.keys()

    def get_cluster_configuration(self, cluster_id):
        if cluster_id in cluster_list:
            return cluster_list[cluster_id].get_attributes()
        print ('ERROR - cluster {} not in cluster list {}').format(cluster_id, cluster_list.keys())

    def get_cluster_workload(self, cluster_id):
        if cluster_id in cluster_list:
            return cluster_list[cluster_id].workload()
        print ('ERROR - cluster {} not in cluster list {}').format(cluster_id, cluster_list.keys())

    def resource_predict(self, cluster_id, resource):
        """
        fields in resource:
            p_procs, how many processors does the caller request
            est_runtime, how long does the caller estimate the application could run, or walltime

        valid combination of fields:
            (1) INPUT - <p_procs> + <est_runtime>
                OUTPUT - qtime, estimated queue wait time based on input

        """
        if cluster_id in cluster_list:
            cluster = cluster_list[cluster_id]
            if 'p_procs' in resource and 'est_runtime' in resource:
                try:
                    return cluster.estimate_qwait(resource.get('p_procs'), resource['est_runtime'])
                except Exception as e:
                    logging.error('Caught exception: ' + str(e.__class__) + ': ' + str(e))
                    return -1

            else:
                print "ERROR - need both 'p_procs' and 'est_runtime' in resource"
        else:
            print ('ERROR - cluster {} not in cluster list {}').format(cluster_id, cluster_list.keys())

    def show_supported_cluster_types():
        print bundle_agent.supported_cluster_types.keys()

    def load_cluster_credentials(self, file_name=default_credential_file):
        try:
            c_file = open(file_name, 'r')
            for line in c_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('finished_job_trace'):
                        _, finished_job_trace = line.split('=')
                        finished_job_trace = finished_job_trace.strip()
                    else:
                        cc = {}
                        for param in line.split():
                            k, v = param.split('=')
                            cc[k.strip()] = v.strip()

                        self.add_cluster(cc, finished_job_trace)

        except Exception as e:
            logging.error('Caught exception: ' + str(e.__class__) + ': ' + str(e))

    def unit_test(self, case):
        pass

    def __del__(self):
        for cluster_id in cluster_list:
            cluster_list[cluster_id].close()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Turn on debug information printing')
    parser.add_argument('-D', '--daemon', action='store_true', default=False, help='Launch as a service daemon')
    parser.add_argument('-t', '--test', dest='n', default=False, help='Run test case #N')
    parser.add_argument('-c', '--config_file', dest='bundle_config_file', default=False, help='Location of the bundle configuration file')
    return parser.parse_args()


def main(argv=None):
    arguments = parse_arguments()
    if arguments.debug:
        print 'debug mode'
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(filename)s:%(lineno)s:%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(filename)s:%(lineno)s:%(message)s', level=logging.WARNING)
    if arguments.daemon:
        print 'daemon mode'
        try:
            import Pyro4
        except ImportError:
            logging.critical('Bundle Manager depends on Pyro4 package installation')
            sys.exit(1)

        bm = BundleManager()
        bm.load_cluster_credentials(arguments.bundle_config_file)
        Pyro4.Daemon.serveSimple({bm: 'BundleManager'}, ns=True)


if __name__ == '__main__':
    sys.exit(main())