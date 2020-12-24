# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/provisioners/abstractProvisioner.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 15113 bytes
from future.utils import with_metaclass
from abc import ABCMeta, abstractmethod
from builtins import object
from functools import total_ordering
import logging, os.path, subprocess
from toil import applianceSelf, customDockerInitCmd
from toil.lib.retry import never
a_short_time = 5
log = logging.getLogger(__name__)

@total_ordering
class Shape(object):
    __doc__ = '\n    Represents a job or a node\'s "shape", in terms of the dimensions of memory, cores, disk and\n    wall-time allocation.\n\n    The wallTime attribute stores the number of seconds of a node allocation, e.g. 3600 for AWS.\n    FIXME: and for jobs?\n\n    The memory and disk attributes store the number of bytes required by a job (or provided by a\n    node) in RAM or on disk (SSD or HDD), respectively.\n    '

    def __init__(self, wallTime, memory, cores, disk, preemptable):
        self.wallTime = wallTime
        self.memory = memory
        self.cores = cores
        self.disk = disk
        self.preemptable = preemptable

    def __eq__(self, other):
        return self.wallTime == other.wallTime and self.memory == other.memory and self.cores == other.cores and self.disk == other.disk and self.preemptable == other.preemptable

    def greater_than(self, other):
        if self.preemptable < other.preemptable:
            return True
        else:
            if self.preemptable > other.preemptable:
                return False
            else:
                if self.memory > other.memory:
                    return True
                else:
                    if self.memory < other.memory:
                        return False
                    else:
                        if self.cores > other.cores:
                            return True
                        else:
                            if self.cores < other.cores:
                                return False
                            if self.disk > other.disk:
                                return True
                        if self.disk < other.disk:
                            return False
                    if self.wallTime > other.wallTime:
                        return True
                if self.wallTime < other.wallTime:
                    return False
            return False

    def __gt__(self, other):
        return self.greater_than(other)

    def __repr__(self):
        return 'Shape(wallTime=%s, memory=%s, cores=%s, disk=%s, preemptable=%s)' % (
         self.wallTime,
         self.memory,
         self.cores,
         self.disk,
         self.preemptable)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((
         self.wallTime,
         self.memory,
         self.cores,
         self.disk,
         self.preemptable))


class AbstractProvisioner(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    An abstract base class to represent the interface for provisioning worker nodes to use in a\n    Toil cluster.\n    '
    LEADER_HOME_DIR = '/root/'

    def __init__(self, clusterName=None, zone=None, nodeStorage=50):
        """
        Initialize provisioner.

        :param clusterName: The cluster identifier.
        :param zone: The zone the cluster runs in.
        :param nodeStorage: The amount of storage on the worker instances, in gigabytes.
        """
        self.clusterName = clusterName
        self._zone = zone
        self._nodeStorage = nodeStorage
        self._leaderPrivateIP = None

    def readClusterSettings(self):
        """
        Initialize class from an existing cluster. This method assumes that
        the instance we are running on is the leader.
        """
        raise NotImplementedError

    def setAutoscaledNodeTypes(self, nodeTypes):
        """
        Set node types, shapes and spot bids. Preemptable nodes will have the form "type:spotBid".
        :param nodeTypes: A list of node types
        """
        self._spotBidsMap = {}
        self.nodeShapes = []
        self.nodeTypes = []
        for nodeTypeStr in nodeTypes:
            nodeBidTuple = nodeTypeStr.split(':')
            if len(nodeBidTuple) == 2:
                nodeType, bid = nodeBidTuple
                self.nodeTypes.append(nodeType)
                self.nodeShapes.append(self.getNodeShape(nodeType, preemptable=True))
                self._spotBidsMap[nodeType] = bid
            else:
                self.nodeTypes.append(nodeTypeStr)
                self.nodeShapes.append(self.getNodeShape(nodeTypeStr, preemptable=False))

    @staticmethod
    def retryPredicate(e):
        """
        Return true if the exception e should be retried by the cluster scaler.
        For example, should return true if the exception was due to exceeding an API rate limit.
        The error will be retried with exponential backoff.

        :param e: exception raised during execution of setNodeCount
        :return: boolean indicating whether the exception e should be retried
        """
        return never(e)

    @abstractmethod
    def launchCluster(self, leaderNodeType, leaderStorage, owner, **kwargs):
        """
        Initialize a cluster and create a leader node.

        :param leaderNodeType: The leader instance.
        :param leaderStorage: The amount of disk to allocate to the leader in gigabytes.
        :param owner: Tag identifying the owner of the instances.

        """
        raise NotImplementedError

    @abstractmethod
    def addNodes(self, nodeType, numNodes, preemptable, spotBid=None):
        """
        Used to add worker nodes to the cluster

        :param numNodes: The number of nodes to add
        :param preemptable: whether or not the nodes will be preemptable
        :param spotBid: The bid for preemptable nodes if applicable (this can be set in config, also).
        :return: number of nodes successfully added
        """
        raise NotImplementedError

    @abstractmethod
    def terminateNodes(self, nodes):
        """
        Terminate the nodes represented by given Node objects

        :param nodes: list of Node objects
        """
        raise NotImplementedError

    @abstractmethod
    def getLeader(self):
        """
        :return: The leader node.
        """
        raise NotImplementedError

    @abstractmethod
    def getProvisionedWorkers(self, nodeType, preemptable):
        """
        Gets all nodes of the given preemptability from the provisioner.
        Includes both static and autoscaled nodes.

        :param preemptable: Boolean value indicating whether to return preemptable nodes or
           non-preemptable nodes
        :return: list of Node objects
        """
        raise NotImplementedError

    @abstractmethod
    def getNodeShape(self, nodeType=None, preemptable=False):
        """
        The shape of a preemptable or non-preemptable node managed by this provisioner. The node
        shape defines key properties of a machine, such as its number of cores or the time
        between billing intervals.

        :param str nodeType: Node type name to return the shape of.

        :rtype: Shape
        """
        raise NotImplementedError

    @abstractmethod
    def destroyCluster(self):
        """
        Terminates all nodes in the specified cluster and cleans up all resources associated with the
        cluser.
        :param clusterName: identifier of the cluster to terminate.
        """
        raise NotImplementedError

    def _setSSH(self):
        """
        Generate a key pair, save it in /root/.ssh/id_rsa.pub, and return the public key.
        The file /root/.sshSuccess is used to prevent this operation from running twice.
        :return Public key.
        """
        if not os.path.exists('/root/.sshSuccess'):
            subprocess.check_call(['ssh-keygen', '-f', '/root/.ssh/id_rsa', '-t', 'rsa', '-N', ''])
            with open('/root/.sshSuccess', 'w') as (f):
                f.write('written here because of restrictive permissions on .ssh dir')
        else:
            os.chmod('/root/.ssh', 448)
            subprocess.check_call(['bash', '-c', 'eval $(ssh-agent) && ssh-add -k'])
            with open('/root/.ssh/id_rsa.pub') as (f):
                masterPublicKey = f.read()
            masterPublicKey = masterPublicKey.split(' ')[1]
            assert masterPublicKey.startswith('AAAAB3NzaC1yc2E'), masterPublicKey
        return masterPublicKey

    cloudConfigTemplate = '#cloud-config\n\nwrite_files:\n    - path: "/home/core/volumes.sh"\n      permissions: "0777"\n      owner: "root"\n      content: |\n        #!/bin/bash\n        set -x\n        ephemeral_count=0\n        drives=""\n        directories="toil mesos docker cwl"\n        for drive in /dev/xvd{{a..z}} /dev/nvme{{0..26}}n1; do\n            echo checking for $drive\n            if [ -b $drive ]; then\n                echo found it\n                if mount | grep $drive; then\n                    echo "already mounted, likely a root device"\n                else\n                    ephemeral_count=$((ephemeral_count + 1 ))\n                    drives="$drives $drive"\n                    echo increased ephemeral count by one\n                fi\n            fi\n        done\n        if (("$ephemeral_count" == "0" )); then\n            echo no ephemeral drive\n            for directory in $directories; do\n                sudo mkdir -p /var/lib/$directory\n            done\n            exit 0\n        fi\n        sudo mkdir /mnt/ephemeral\n        if (("$ephemeral_count" == "1" )); then\n            echo one ephemeral drive to mount\n            sudo mkfs.ext4 -F $drives\n            sudo mount $drives /mnt/ephemeral\n        fi\n        if (("$ephemeral_count" > "1" )); then\n            echo multiple drives\n            for drive in $drives; do\n                dd if=/dev/zero of=$drive bs=4096 count=1024\n            done\n            sudo mdadm --create -f --verbose /dev/md0 --level=0 --raid-devices=$ephemeral_count $drives # determine force flag\n            sudo mkfs.ext4 -F /dev/md0\n            sudo mount /dev/md0 /mnt/ephemeral\n        fi\n        for directory in $directories; do\n            sudo mkdir -p /mnt/ephemeral/var/lib/$directory\n            sudo mkdir -p /var/lib/$directory\n            sudo mount --bind /mnt/ephemeral/var/lib/$directory /var/lib/$directory\n        done\n\ncoreos:\n    update:\n      reboot-strategy: off\n    units:\n    - name: "volume-mounting.service"\n      command: "start"\n      content: |\n        [Unit]\n        Description=mounts ephemeral volumes & bind mounts toil directories\n        Before=docker.service\n\n        [Service]\n        Type=oneshot\n        Restart=no\n        ExecStart=/usr/bin/bash /home/core/volumes.sh\n\n    - name: "toil-{role}.service"\n      command: "start"\n      content: |\n        [Unit]\n        Description=toil-{role} container\n        After=docker.service\n\n        [Service]\n        Restart=on-failure\n        RestartSec=2\n        ExecStartPre=-/usr/bin/docker rm toil_{role}\n        ExecStart=/usr/bin/docker run             --entrypoint={entrypoint}             --net=host             -v /var/run/docker.sock:/var/run/docker.sock             -v /var/lib/mesos:/var/lib/mesos             -v /var/lib/docker:/var/lib/docker             -v /var/lib/toil:/var/lib/toil             -v /var/lib/cwl:/var/lib/cwl             -v /tmp:/tmp             --name=toil_{role}             {dockerImage}             {mesosArgs}\n    - name: "node-exporter.service"\n      command: "start"\n      content: |\n        [Unit]\n        Description=node-exporter container\n        After=docker.service\n\n        [Service]\n        Restart=on-failure\n        RestartSec=2\n        ExecStartPre=-/usr/bin/docker rm node_exporter\n        ExecStart=/usr/bin/docker run             -p 9100:9100             -v /proc:/host/proc             -v /sys:/host/sys             -v /:/rootfs             --name node-exporter             --restart always             prom/node-exporter:v0.15.2             --path.procfs /host/proc             --path.sysfs /host/sys             --collector.filesystem.ignored-mount-points ^/(sys|proc|dev|host|etc)($|/)\n'
    sshTemplate = 'ssh_authorized_keys:\n    - "ssh-rsa {sshKey}"\n'
    MESOS_LOG_DIR = '--log_dir=/var/lib/mesos '
    LEADER_DOCKER_ARGS = '--registry=in_memory --cluster={name}'
    WORKER_DOCKER_ARGS = '--work_dir=/var/lib/mesos --master={ip}:5050 --attributes=preemptable:{preemptable} --no-hostname_lookup --no-systemd_enable_support'

    def _getCloudConfigUserData(self, role, masterPublicKey=None, keyPath=None, preemptable=False):
        """
        Return the text (not bytes) user data to pass to a provisioned node.
        """
        if role == 'leader':
            entryPoint = 'mesos-master'
            mesosArgs = self.MESOS_LOG_DIR + self.LEADER_DOCKER_ARGS.format(name=(self.clusterName))
        else:
            if role == 'worker':
                entryPoint = 'mesos-slave'
                mesosArgs = self.MESOS_LOG_DIR + self.WORKER_DOCKER_ARGS.format(ip=(self._leaderPrivateIP), preemptable=preemptable)
            else:
                raise RuntimeError('Unknown role %s' % role)
            template = self.cloudConfigTemplate
            if masterPublicKey:
                template += self.sshTemplate
            if keyPath:
                mesosArgs = keyPath + ' ' + mesosArgs
                entryPoint = 'waitForKey.sh'
            customDockerInitCommand = customDockerInitCmd()
            if customDockerInitCommand:
                mesosArgs = ' '.join(["'" + customDockerInitCommand + "'", entryPoint, mesosArgs])
                entryPoint = 'customDockerInit.sh'
        templateArgs = dict(role=role, dockerImage=(applianceSelf()),
          entrypoint=entryPoint,
          sshKey=masterPublicKey,
          mesosArgs=mesosArgs)
        userData = (template.format)(**templateArgs)
        return userData