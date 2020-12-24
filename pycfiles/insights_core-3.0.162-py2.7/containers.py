# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/containers.py
# Compiled at: 2019-05-16 13:41:33
from __future__ import absolute_import
import os, logging, shlex, subprocess, sys
from .constants import InsightsConstants as constants
APP_NAME = constants.app_name
logger = logging.getLogger(__name__)

def run_command_very_quietly(cmdline):
    with open(os.devnull, 'w') as (devnull):
        cmd = shlex.split(cmdline.encode('utf8'))
        proc = subprocess.Popen(cmd, stdout=devnull, stderr=subprocess.STDOUT)
        returncode = proc.wait()
        return returncode


UseAtomic = True
UseDocker = False
HaveDocker = False
HaveDockerException = None
try:
    if run_command_very_quietly('which docker') == 0:
        HaveDocker = True
except Exception as e:
    HaveDockerException = e

HaveAtomic = False
HaveAtomicException = None
try:
    if run_command_very_quietly('which atomic') == 0:
        HaveAtomic = True
    else:
        HaveAtomic = False
except Exception as e:
    HaveAtomic = False
    HaveAtomicException = e

HaveAtomicMount = HaveAtomic
if not HaveAtomic and HaveDocker:
    UseDocker = True
    UseAtomic = False
if not HaveDocker and HaveAtomic:
    UseAtomic = True
    UseDocker = False
DockerIsRunning = False
try:
    if run_command_very_quietly('docker info') == 0:
        DockerIsRunning = True
except Exception as e:
    HaveDockerException = e

if DockerIsRunning and UseDocker and HaveDocker or DockerIsRunning and UseAtomic and HaveAtomic:
    import tempfile, shutil, json

    def runcommand(cmd):
        logger.debug('Running Command: %s' % cmd)
        proc = subprocess.Popen(cmd)
        returncode = proc.wait()
        return returncode


    def run_command_capture_output(cmdline):
        cmd = shlex.split(cmdline.encode('utf8'))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        return out


    def use_atomic_run():
        return UseAtomic and HaveAtomic


    def use_atomic_mount():
        return UseAtomic and HaveAtomicMount


    def pull_image(image):
        return runcommand(shlex.split('docker pull') + [image])


    def get_targets(config):
        targets = []
        logger.debug('Getting targets to scan...')
        for d in _docker_all_image_ids():
            logger.debug('Checking if %s equals %s.' % (d, config.analyze_image_id))
            if config.analyze_image_id == d or d.split('sha256:')[(-1)].startswith(config.analyze_image_id):
                logger.debug('%s equals %s' % (d, config.analyze_image_id))
                targets.append({'type': 'docker_image', 'name': d})
                return targets

        logger.debug('Done collecting targets')
        logger.debug(targets)
        if len(targets) == 0:
            logger.error('There was an error collecting targets. No image was found matching this ID.')
            sys.exit(constants.sig_kill_bad)
        return targets


    class AtomicTemporaryMountPoint:

        def __init__(self, image_id, mount_point):
            self.image_id = image_id
            self.mount_point = mount_point

        def get_fs(self):
            return self.mount_point

        def close(self):
            try:
                logger.debug('Closing Id %s On %s' % (self.image_id, self.mount_point))
                runcommand(shlex.split('atomic unmount') + [self.mount_point])
            except Exception as e:
                logger.debug('exception while unmounting image or container: %s' % e)

            shutil.rmtree(self.mount_point, ignore_errors=True)


    from .mount import DockerMount, Mount

    class DockerTemporaryMountPoint:

        def __init__(self, driver, image_id, mount_point, cid):
            self.driver = driver
            self.image_id = image_id
            self.mount_point = mount_point
            self.cid = cid

        def get_fs(self):
            return self.mount_point

        def close(self):
            try:
                logger.debug('Closing Id %s On %s' % (self.image_id, self.mount_point))
                if self.driver == 'devicemapper':
                    Mount.unmount_path(self.mount_point)
                DockerMount(self.mount_point).unmount(self.cid)
            except Exception as e:
                logger.debug('exception while unmounting image or container: %s' % e)

            shutil.rmtree(self.mount_point, ignore_errors=True)


    def open_image(image_id):
        global HaveAtomicException
        if HaveAtomicException and UseAtomic:
            logger.debug('atomic is either not installed or not accessable %s' % HaveAtomicException)
            HaveAtomicException = None
        if use_atomic_mount():
            mount_point = tempfile.mkdtemp()
            logger.debug('Opening Image Id %s On %s using atomic' % (image_id, mount_point))
            if runcommand(shlex.split('atomic mount') + [image_id, mount_point]) == 0:
                return AtomicTemporaryMountPoint(image_id, mount_point)
            logger.error('Could not mount Image Id %s On %s' % (image_id, mount_point))
            shutil.rmtree(mount_point, ignore_errors=True)
            return
        else:
            driver = _docker_driver()
            if driver is None:
                return
            mount_point = tempfile.mkdtemp()
            logger.debug('Opening Image Id %s On %s using docker client' % (image_id, mount_point))
            mount_point, cid = DockerMount(mount_point).mount(image_id)
            if driver == 'devicemapper':
                DockerMount.mount_path(os.path.join(mount_point, 'rootfs'), mount_point, bind=True)
            if cid:
                return DockerTemporaryMountPoint(driver, image_id, mount_point, cid)
            logger.error('Could not mount Image Id %s On %s' % (image_id, mount_point))
            shutil.rmtree(mount_point, ignore_errors=True)
            return
        return


    def open_container(container_id):
        global HaveAtomicException
        if HaveAtomicException and UseAtomic:
            logger.debug('atomic is either not installed or not accessable %s' % HaveAtomicException)
            HaveAtomicException = None
        if use_atomic_mount():
            mount_point = tempfile.mkdtemp()
            logger.debug('Opening Container Id %s On %s using atomic' % (
             container_id, mount_point))
            if runcommand(shlex.split('atomic mount') + [container_id, mount_point]) == 0:
                return AtomicTemporaryMountPoint(container_id, mount_point)
            logger.error('Could not mount Container Id %s On %s' % (container_id, mount_point))
            shutil.rmtree(mount_point, ignore_errors=True)
            return
        else:
            driver = _docker_driver()
            if driver is None:
                return
            mount_point = tempfile.mkdtemp()
            logger.debug('Opening Container Id %s On %s using docker client' % (
             container_id, mount_point))
            mount_point, cid = DockerMount(mount_point).mount(container_id)
            if driver == 'devicemapper':
                DockerMount.mount_path(os.path.join(mount_point, 'rootfs'), mount_point, bind=True)
            if cid:
                return DockerTemporaryMountPoint(driver, container_id, mount_point, cid)
            logger.error('Could not mount Container Id %s On %s' % (container_id, mount_point))
            shutil.rmtree(mount_point, ignore_errors=True)
            return
        return


    def _docker_inspect_image(docker_name, docker_type):
        a = json.loads(run_command_capture_output('docker inspect --type %s %s' % (docker_type, docker_name)))
        if len(a) == 0:
            return
        else:
            return a[0]
            return


    def _docker_driver():
        x = 'Storage Driver:'
        if UseAtomic:
            atomic_docker = 'atomic'
        else:
            atomic_docker = 'docker'
        for each in run_command_capture_output(atomic_docker + ' info').splitlines():
            if each.startswith(x):
                return each[len(x):].strip()

        return ''


    def _docker_all_image_ids():
        l = []
        if UseAtomic:
            atomic_docker = 'atomic images list'
        else:
            atomic_docker = 'docker images'
        for each in run_command_capture_output(atomic_docker + ' --quiet --no-trunc').splitlines():
            if each not in l:
                l.append(each)

        return l


    def _docker_all_container_ids():
        l = []
        if UseAtomic:
            atomic_docker = 'atomic'
        else:
            atomic_docker = 'docker'
        for each in run_command_capture_output(atomic_docker + ' ps --all --quiet --no-trunc').splitlines():
            if each not in l:
                l.append(each)

        return l


else:
    if UseAtomic:
        the_verbiage = 'Atomic'
        the_exception = HaveAtomicException
    else:
        the_verbiage = 'Docker'
        the_exception = HaveDockerException

    def get_targets(config):
        logger.error('Could not connect to ' + the_verbiage + ' to collect from images and containers')
        logger.error(the_verbiage + ' is either not installed or not accessable: %s' % (the_exception if the_exception else ''))
        return []


    def open_image(image_id):
        logger.error('Could not connect to ' + the_verbiage + ' to examine image %s' % image_id)
        logger.error(the_verbiage + ' is either not installed or not accessable: %s' % (the_exception if the_exception else ''))
        return


    def open_container(container_id):
        logger.error('Could not connect to ' + the_verbiage + ' to examine container %s' % container_id)
        logger.error(the_verbiage + ' is either not installed or not accessable: %s' % (the_exception if the_exception else ''))
        return