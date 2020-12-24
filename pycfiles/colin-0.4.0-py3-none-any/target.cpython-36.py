# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/target.py
# Compiled at: 2018-09-19 09:35:52
# Size of source mod 2**32: 14762 bytes
import io, json, logging, os, shutil, subprocess
from tempfile import mkdtemp
from dockerfile_parse import DockerfileParser
from .checks.dockerfile import DockerfileAbstractCheck
from .checks.images import ImageAbstractCheck
from ..core.exceptions import ColinException
from ..utils.cont import ImageName
logger = logging.getLogger(__name__)

def is_compatible(target_type, check_instance):
    """
    Check the target compatibility with the check instance.

    :param target_type: Target subclass, if None, returns True
    :param check_instance: instance of some Check class
    :return: True if the target is None or compatible with the check instance
    """
    if not target_type:
        return True
    else:
        return isinstance(check_instance, target_type.get_compatible_check_class())


def inspect_object(obj, refresh=True):
    """
    inspect provided object (container, image) and return raw dict with the metadata

    :param obj: instance of Container or an Image
    :param refresh: bool, refresh the metadata or return cached?
    :return: dict
    """
    if hasattr(obj, 'inspect'):
        return obj.inspect(refresh=refresh)
    else:
        return obj.get_metadata(refresh=refresh)


class Target(object):
    __doc__ = '\n    Target is the thing we are going to check; it can be\n    - an image (specified by name, ostree or dockertar)\n    - dockerfile (specified by path or file-like object)\n    '

    def __init__(self):
        self._labels = None
        self.target_name = None

    @property
    def labels(self):
        """
        Get list of labels from the target instance.

        :return: [str]
        """
        pass

    def clean_up(self):
        """
        Perform clean up on the low level objects: atm atomic and skopeo mountpoints
        and data are being cleaned up.
        """
        pass

    @classmethod
    def get_compatible_check_class(cls):
        """
        Get the compatible abstract check class.
        :return: cls
        """
        pass

    @staticmethod
    def get_instance(target_type, **kwargs):
        """
        :param target_type: string, either image, dockertar, ostree or dockerfile
        """
        if target_type in TARGET_TYPES:
            cls = TARGET_TYPES[target_type]
            try:
                return cls(**kwargs)
            except Exception:
                logger.error('Please make sure that you picked the correct target type: --target-type CLI option.')
                raise

        raise ColinException("Unknown target type '{}'. Please make sure that you picked the correct target type: --target-type CLI option.".format(target_type))


class DockerfileTarget(Target):
    target_type = 'dockerfile'

    def __init__(self, target, **_):
        super().__init__()
        self.target_name = target
        logger.debug('Target is a dockerfile.')
        if isinstance(target, io.IOBase):
            logger.debug('Target is a dockerfile loaded from the file-like object.')
            self.instance = DockerfileParser(fileobj=target)
        else:
            self.instance = DockerfileParser(fileobj=(open(target)))

    @property
    def labels(self):
        """
        Get list of labels from the target instance.

        :return: [str]
        """
        if self._labels is None:
            self._labels = self.instance.labels
        return self._labels

    @classmethod
    def get_compatible_check_class(cls):
        return DockerfileAbstractCheck


class AbstractImageTarget(Target):
    __doc__ = '\n    Abstract predecessor for the image-target classes. (e.g. ostree and podman image)\n    '

    @property
    def config_metadata(self):
        """ metadata from "Config" key """
        raise NotImplementedError('Unsupported right now.')

    @property
    def mount_point(self):
        """ real filesystem """
        raise NotImplementedError('Unsupported right now.')

    def get_output(self, cmd):
        """
        Get output of the command from the container based on this image.
        :param cmd: [str]
        :return: str
        """
        raise NotImplementedError('Unsupported right now.')

    def read_file(self, file_path):
        """
        read file specified via 'file_path' and return its content - raises an ConuException if
        there is an issue accessing the file
        :param file_path: str, path to the file to read
        :return: str (not bytes), content of the file
        """
        try:
            with open(self.cont_path(file_path)) as (fd):
                return fd.read()
        except IOError as ex:
            logger.error('error while accessing file %s: %r', file_path, ex)
            raise ColinException('There was an error while accessing file %s: %r' % (file_path, ex))

    def get_file(self, file_path, mode='r'):
        """
        provide File object specified via 'file_path'
        :param file_path: str, path to the file
        :param mode: str, mode used when opening the file
        :return: File instance
        """
        return open((self.cont_path(file_path)), mode=mode)

    def file_is_present(self, file_path):
        """
        check if file 'file_path' is present, raises IOError if file_path
        is not a file
        :param file_path: str, path to the file
        :return: True if file exists, False if file does not exist
        """
        real_path = self.cont_path(file_path)
        if not os.path.exists(real_path):
            return False
        else:
            if not os.path.isfile(real_path):
                raise IOError('%s is not a file' % file_path)
            return True

    def cont_path(self, path):
        """
        provide absolute path within the container

        :param path: path with container
        :return: str
        """
        if path.startswith('/'):
            path = path[1:]
        real_path = os.path.join(self.mount_point, path)
        logger.debug('path = %s', real_path)
        return real_path

    @classmethod
    def get_compatible_check_class(cls):
        return ImageAbstractCheck


class ImageTarget(AbstractImageTarget):
    __doc__ = '\n    Represents the podman image as a target.\n    '
    target_type = 'image'

    def __init__(self, target, pull, insecure=False, **_):
        super().__init__()
        logger.debug('Target is an image.')
        self.pull = pull
        self.insecure = insecure
        self.image_name_obj = ImageName.parse(target)
        self.target_name = self.image_name_obj.name
        self._config_metadata = None
        self._mount_point = None
        self._mounted_container_id = None
        self.image_id = None
        self._try_image()

    @property
    def config_metadata(self):
        if not self._config_metadata:
            cmd = [
             'podman', 'inspect', self.target_name]
            loaded_config = json.loads(subprocess.check_output(cmd))
            if loaded_config:
                if isinstance(loaded_config, list):
                    self._config_metadata = loaded_config[0]
            else:
                raise ColinException('Cannot load config for the image.')
        return self._config_metadata

    @property
    def labels(self):
        return self.config_metadata['Labels'] or {}

    @property
    def mount_point(self):
        """ podman mount -- real filesystem """
        if self._mount_point is None:
            cmd_create = [
             'podman', 'create', self.target_name, 'some-cmd']
            self._mounted_container_id = subprocess.check_output(cmd_create).decode().rstrip()
            cmd_mount = ['podman', 'mount', self._mounted_container_id]
            self._mount_point = subprocess.check_output(cmd_mount).decode().rstrip()
        return self._mount_point

    def _try_image(self):
        logger.debug('Trying to find an image.')
        cmd = ['podman', 'images', '--quiet', self.target_name]
        result = subprocess.run(cmd, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        if result.returncode == 0:
            self.image_id = result.stdout.decode().rstrip()
            logger.debug("Image found with id: '{}'.".format(self.image_id))
        else:
            if 'unable to find' in result.stderr.decode():
                if self.pull:
                    logger.debug('Pulling an image.')
                    cmd_pull = ['podman', 'pull', '--quiet', self.target_name]
                    result_pull = subprocess.run(cmd_pull, stdout=(subprocess.PIPE),
                      stderr=(subprocess.PIPE))
                    if result_pull.returncode == 0:
                        self.image_id = result_pull.stdout.decode().rstrip()
                        logger.debug("Image pulled with id: '{}'.".format(self.image_id))
                    else:
                        raise ColinException("Cannot pull an image: '{}'.".format(self.target_name))
                else:
                    raise ColinException("Image '{}' not found.".format(self.target_name))
            else:
                raise ColinException('Podman error: {}'.format(result.stderr))

    def clean_up(self):
        if self._mount_point:
            cmd = [
             'podman', 'umount', self._mounted_container_id]
            subprocess.check_call(cmd, stdout=(subprocess.DEVNULL))
            self._mount_point = None
        if self._mounted_container_id:
            cmd = [
             'podman', 'rm', self._mounted_container_id]
            subprocess.check_call(cmd, stdout=(subprocess.DEVNULL))
            self._mounted_container_id = None

    def get_output(self, cmd):
        raise NotImplementedError('Unsupported right now.')


class OstreeTarget(AbstractImageTarget):
    __doc__ = '\n    Represents the ostree repository as an image target.\n    '
    target_type = 'ostree'

    def __init__(self, target, **_):
        super().__init__()
        logger.debug('Target is an ostree repository.')
        self.target_name = target
        if self.target_name.startswith('ostree:'):
            self.target_name = self.target_name[7:]
        try:
            self.ref_image_name, self._ostree_path = self.target_name.split('@', 1)
        except ValueError:
            raise RuntimeError("Invalid ostree target: should be 'image@path'.")

        self._tmpdir = None
        self._mount_point = None
        self._layers_path = None
        self._labels = None

    @property
    def labels(self):
        """
        Provide labels without the need of dockerd. Instead skopeo is being used.

        :return: dict
        """
        if self._labels is None:
            cmd = [
             'skopeo', 'inspect', self.skopeo_target]
            self._labels = json.loads(subprocess.check_output(cmd))['Labels']
        return self._labels

    @property
    def layers_path(self):
        """ Directory with all the layers (docker save). """
        if self._layers_path is None:
            self._layers_path = os.path.join(self.tmpdir, 'layers')
        return self._layers_path

    @property
    def mount_point(self):
        """ ostree checkout -- real filesystem """
        if self._mount_point is None:
            self._mount_point = os.path.join(self.tmpdir, 'checkout')
            os.makedirs(self._mount_point)
            self._checkout()
        return self._mount_point

    @property
    def ostree_path(self):
        """ ostree repository -- content """
        if self._ostree_path is None:
            self._ostree_path = os.path.join(self.tmpdir, 'ostree-repo')
            subprocess.check_call(['ostree', 'init', '--mode', 'bare-user-only',
             '--repo', self._ostree_path])
        return self._ostree_path

    @property
    def skopeo_target(self):
        """ Skopeo format for the ostree repository. """
        return 'ostree:{}@{}'.format(self.ref_image_name, self.ostree_path)

    @property
    def tmpdir(self):
        """ Temporary directory holding all the runtime data. """
        if self._tmpdir is None:
            self._tmpdir = mkdtemp(prefix='colin-', dir='/var/tmp')
        return self._tmpdir

    def clean_up(self):
        cmd = [
         'atomic', 'unmount', self.mount_point]
        self._run_and_log(cmd, self.ostree_path, 'Failed to unmount ostree checkout.')
        shutil.rmtree(self.tmpdir)

    def _checkout(self):
        """ check out the image filesystem on self.mount_point """
        cmd = [
         'atomic', 'mount', '--storage', 'ostree', self.ref_image_name, self.mount_point]
        self._run_and_log(cmd, self.ostree_path, 'Failed to mount selected image as an ostree repo.')

    @staticmethod
    def _run_and_log(cmd, ostree_repo_path, error_msg, wd=None):
        """ run provided command and log all of its output; set path to ostree repo """
        logger.debug('running command %s', cmd)
        kwargs = {'stderr':subprocess.STDOUT, 
         'env':os.environ.copy()}
        if ostree_repo_path:
            kwargs['env']['ATOMIC_OSTREE_REPO'] = ostree_repo_path
        if wd:
            kwargs['cwd'] = wd
        try:
            out = (subprocess.check_output)(cmd, **kwargs)
        except subprocess.CalledProcessError:
            logger.error(error_msg)
            raise

        logger.debug('%s', out)

    @property
    def config_metadata(self):
        """ metadata from "Config" key """
        raise NotImplementedError('Skopeo does not provide metadata yet.')

    def get_output(self, cmd):
        raise NotImplementedError('Unsupported right now.')


TARGET_TYPES = {'image':ImageTarget, 
 'dockerfile':DockerfileTarget, 
 'ostree':OstreeTarget}