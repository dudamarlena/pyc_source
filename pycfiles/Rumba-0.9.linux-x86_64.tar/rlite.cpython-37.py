# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/prototypes/rlite.py
# Compiled at: 2018-07-25 06:08:30
# Size of source mod 2**32: 7206 bytes
import rumba.ssh_support as ssh
import rumba.model as mod
import rumba.log as log
import rumba.multiprocess as m_processing
import time
logger = log.get_logger(__name__)

class Experiment(mod.Experiment):
    __doc__ = '\n    Represents an rlite experiment.\n    '

    def __init__(self, testbed, nodes=None, git_repo='https://gitlab.com/arcfire/rlite', git_branch='master', enrollment_strategy='minimal'):
        """
        Initializes the experiment class.

        :param testbed: The testbed to run the experiment on.
        :param nodes: The list of nodes.
        :param git_repo: The git repository to use for installation.
        :param git_branch: The branch of the git repository to use.
        :param enrollment_strategy: Can be 'full-mesh', 'minimal' or 'manual'.
        """
        mod.Experiment.__init__(self, testbed, nodes, git_repo, git_branch, prototype_logs=[
         '/tmp/uipcp.log'],
          enrollment_strategy=enrollment_strategy)

    @staticmethod
    def make_executor(node, packages, testbed):

        def executor(commands):
            ssh.aptitude_install(testbed, node, packages)
            node.execute_commands(commands, time_out=None, use_proxy=True)

        return executor

    def prototype_name(self):
        return 'rlite'

    def execute_commands(self, node, cmds):
        ssh.execute_commands((self.testbed), (node.ssh_config), cmds,
          time_out=None)

    def may_sudo(self, cmds):
        if self.testbed.username != 'root':
            for i in range(len(cmds)):
                cmds[i] = 'sudo %s' % cmds[i]

    def init_nodes(self):
        cmds = ['modprobe rlite',
         'modprobe rlite-normal',
         'modprobe rlite-shim-eth',
         'modprobe rlite-shim-udp4',
         'modprobe rlite-shim-loopback',
         'rlite-uipcps -v DBG > /tmp/uipcp.log 2>&1 &']
        self.may_sudo(cmds)
        for node in self.nodes:
            self.execute_commands(node, cmds)

    def create_ipcps(self):
        for node in self.nodes:
            cmds = []
            for ipcp in node.ipcps:
                if isinstance(ipcp.dif, mod.NormalDIF):
                    ipcp_type = 'normal'
                else:
                    if isinstance(ipcp.dif, mod.ShimEthDIF):
                        ipcp_type = 'shim-eth'
                    else:
                        if isinstance(ipcp.dif, mod.ShimUDPDIF):
                            ipcp_type = 'shim-udp4'
                        else:
                            logger.warning('unknown type for DIF %s, default to loopback', ipcp.dif.name)
                            ipcp_type = 'shim-loopback'
                cmds.append('rlite-ctl ipcp-create %s %s %s' % (
                 ipcp.name, ipcp_type, ipcp.dif.name))
                if isinstance(ipcp.dif, mod.ShimEthDIF):
                    cmds.append('rlite-ctl ipcp-config %s netdev %s' % (
                     ipcp.name, ipcp.ifname))
                if isinstance(ipcp.dif, mod.NormalDIF) and ipcp.dif_bootstrapper:
                    cmds.append('rlite-ctl ipcp-enroller-enable %s' % ipcp.name)

            self.may_sudo(cmds)
            self.execute_commands(node, cmds)

    def register_ipcps(self):
        for node in self.nodes:
            cmds = []
            for ipcp in node.ipcps:
                for lower in ipcp.registrations:
                    cmds.append('rlite-ctl ipcp-register %s %s' % (
                     ipcp.name, lower.name))

            self.may_sudo(cmds)
            self.execute_commands(node, cmds)

    def enroll_ipcps(self):
        for el in self.enrollments:
            for e in el:
                d = {'enrollee':e['enrollee'].name, 
                 'dif':e['dif'].name, 
                 'lower_dif':e['lower_dif'].name, 
                 'enroller':e['enroller'].name}
                cmd = 'rlite-ctl ipcp-enroll-retry %(enrollee)s %(dif)s %(lower_dif)s %(enroller)s' % d
                cmds = [cmd]
                self.may_sudo(cmds)
                self.execute_commands(e['enrollee'].node, cmds)
                time.sleep(1)

    def _install_prototype(self):
        logger.info('installing rlite on all nodes')
        packages = [
         'g++', 'gcc', 'cmake', 'linux-headers-$(uname -r)',
         'protobuf-compiler', 'libprotobuf-dev', 'git']
        cmds = [
         'rm -rf ~/rlite',
         'cd ~; git clone -b ' + self.git_branch + ' ' + self.git_repo,
         'cd ~/rlite && ./configure && make && sudo make install',
         'cd ~/rlite && sudo make depmod']
        names = []
        executors = []
        args = []
        for node in self.nodes:
            executor = self.make_executor(node, packages, self.testbed)
            names.append(node.name)
            executors.append(executor)
            args.append(cmds)

        m_processing.call_in_parallel(names, args, executors)
        logger.info('installation complete')

    def _bootstrap_prototype(self):
        for dif in self.dif_ordering:
            if isinstance(dif, mod.NormalDIF) and len(dif.qos_cubes) != 0:
                logger.warn('QoS cubes not (yet) supported by the rlite plugin. Will ignore.')

        logger.info('setting up')
        self.init_nodes()
        logger.info('software initialized on all nodes')
        self.create_ipcps()
        logger.info('IPCPs created on all nodes')
        self.register_ipcps()
        logger.info('IPCPs registered to their lower DIFs on all nodes')
        self.enroll_ipcps()
        logger.info('enrollment completed in all DIFs')

    def _terminate_prototype(self):
        pass