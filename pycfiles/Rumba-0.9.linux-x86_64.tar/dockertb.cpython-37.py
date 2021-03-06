# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/testbeds/dockertb.py
# Compiled at: 2018-08-31 05:12:48
# Size of source mod 2**32: 8648 bytes
import os
from time import sleep
import docker, subprocess
import rumba.model as mod
import rumba.log as log
from rumba.executors.docker import DockerExecutor
logger = log.get_logger(__name__)

class Testbed(mod.Testbed):
    __doc__ = '\n    Represents a docker testbed.\n    '

    def __init__(self, base_image=None, exp_name='foo', pull_image=True, use_ovs=False):
        """
        Initializes the testbed class.

        :param exp_name: The experiment name.
        :param base_image: The docker base image.
        :param pull_image: Retrieve the docker image from the Docker hub?
        :param use_ovs: Use the OVS switch instead of the Linux bridge?

        .. note:: In case no base image is provided, Rumba will automatically
                  download the latest version available from docker hub.
        """
        mod.Testbed.__init__(self, exp_name, '', '', 'rumba')
        self.base_image = base_image
        self.pull_image = pull_image
        self.use_ovs = use_ovs
        self.running_containers = {}
        self.active_bridges = set()
        self.active_ipcps = set()
        self.docker_client = docker.from_env()
        self.executor = DockerExecutor(self)

    def _swap_in(self, experiment):
        docker_client = self.docker_client
        if not self.base_image:
            if experiment.prototype_name() == 'ouroboros':
                self.base_image = 'arcfirerumba/ouroboros'
            else:
                raise Exception('Only Ouroboros supported for now.')
        img = self.base_image.rsplit(':', 1)
        self.base_image_repo = img[0]
        self.base_image_tag = 'latest' if len(img) == 1 else img[1]
        self.base_image = '%s:%s' % (self.base_image_repo, self.base_image_tag)
        if self.pull_image:
            logger.info('Fetching image...')
            docker_client.images.pull(self.base_image_repo, self.base_image_tag)
        docker_client.images.get('%s:%s' % (self.base_image_repo,
         self.base_image_tag))
        logger.info('Starting nodes...')
        for node in experiment.nodes:
            logger.debug('Starting node %s', node.name)
            self.running_containers[node.name] = docker_client.containers.run((self.base_image),
              command=(node.startup_command), name=('node-' + node.name),
              detach=True,
              network='none',
              privileged=True,
              devices=['/dev/fuse'])

        cmd = 'sudo mkdir /var/run/netns'
        logger.debug('executing >> %s', cmd)
        if not os.path.exists('/var/run/netns'):
            subprocess.check_call(cmd.split())
        for shim in experiment.dif_ordering:
            if not isinstance(shim, mod.ShimEthDIF):
                continue
            else:
                cmd = ''
                if self.use_ovs:
                    cmd += 'sudo ovs-vsctl add-br %(shim)s'
                else:
                    cmd += 'sudo ip link add %(shim)s type bridge'
            cmd = cmd % {'shim': shim.name}
            self.active_bridges.add(shim.name)
            logger.debug('executing >> %s', cmd)
            subprocess.check_call(cmd.split())
            if not self.use_ovs:
                logger.debug('executing >> %s', cmd)
                cmd = 'sudo ip link set dev %(shim)s up' % {'shim': shim.name}
                subprocess.check_call(cmd.split())

        for node in experiment.nodes:
            container = self.running_containers[node.name]
            container.reload()
            state = container.attrs['State']
            while not state['Running']:
                sleep(0.2)
                container.reload()
                state = container.attrs['State']

            pid = state['Pid']
            cmd = 'sudo ln -s /proc/%(pid)i/ns/net /var/run/netns/%(pid)i' % {'pid': pid}
            logger.debug('executing >> %s', cmd)
            subprocess.check_call(cmd.split())
            for ipcp in node.ipcps:
                if isinstance(ipcp, mod.ShimEthIPCP):
                    if ipcp.ifname is None:
                        ipcp.ifname = 'e%i' % node.ipcps.index(ipcp)
                    else:
                        node_name = node.name[0:11]
                        cmd = 'sudo ip link add %(node)s.%(ifname)s type veth peer name _%(node)s.%(ifname)s' % {'node':node_name, 
                         'ifname':ipcp.ifname}
                        logger.debug('executing >> %s', cmd)
                        subprocess.check_call(cmd.split())
                        cmd = ''
                        if self.use_ovs:
                            cmd += 'sudo ovs-vsctl add-port %(dif)s %(node)s.%(ifname)s'
                        else:
                            cmd += 'sudo ip link set %(node)s.%(ifname)s master %(dif)s'
                    cmd = cmd % {'node':node_name,  'ifname':ipcp.ifname, 
                     'dif':ipcp.dif.name}
                    logger.debug('executing >> %s', cmd)
                    subprocess.check_call(cmd.split())
                    cmd = 'sudo ip link set _%(node)s.%(ifname)s netns %(pid)i name %(ifname)s' % {'node':node_name, 
                     'pid':pid, 
                     'ifname':ipcp.ifname}
                    logger.debug('executing >> %s', cmd)
                    subprocess.check_call(cmd.split())
                    cmd = 'sudo ip link set dev %(node)s.%(ifname)s up' % {'node':node_name, 
                     'ifname':ipcp.ifname}
                    logger.debug('executing >> %s', cmd)
                    subprocess.check_call(cmd.split())
                    cmd = 'sudo ip netns exec %(pid)i ip link set dev %(ifname)s up' % {'pid':pid, 
                     'ifname':ipcp.ifname}
                    logger.debug('executing >> %s', cmd)
                    subprocess.check_call(cmd.split())
                    self.active_ipcps.add(ipcp)

        logger.info('Experiment swapped in')

    def _swap_out(self, experiment):
        for name, container in self.running_containers.items():
            logger.debug('Stopping node %s' % name)
            container.remove(force=True)

        for shim in experiment.dif_ordering:
            if isinstance(shim, mod.ShimEthDIF):
                if shim.name in self.active_bridges:
                    cmd = ''
                    if self.use_ovs:
                        cmd += 'sudo ovs-vsctl del-br %(shim)s'
                    else:
                        cmd += 'sudo ip link del %(shim)s'
                cmd = cmd % {'shim': shim.name}
                logger.debug('executing >> %s', cmd)
                subprocess.check_call(cmd.split())
                self.active_bridges.remove(shim.name)

        for name, container in self.running_containers.items():
            pid = container.attrs['State']['Pid']
            if pid == 0:
                continue
            path = '/var/run/netns/%d' % pid
            if os.path.islink(path):
                cmd = 'sudo rm ' + path
                logger.debug('executing >> %s', cmd)
                subprocess.check_call(cmd.split())

        self.running_containers = {}
        logger.info('Experiment swapped out')