# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.dennis/development/ship_it/ship_it/manifest.py
# Compiled at: 2018-07-05 17:18:06
from __future__ import unicode_literals
from os import path
import pipes, six, time, yaml

def get_manifest_from_path(manifest_path):
    return Manifest(manifest_path)


class Manifest(object):
    """
    Utility class for getting command line arguments and flags out of
    configuration
    """

    def __init__(self, manifest_path=None, manifest_contents=None, pkg_type=b'rpm', pkg_location=b'/opt'):
        if not pkg_type in ('rpm', ):
            raise AssertionError
            assert path.isabs(pkg_location)
            self.path = self.normalize_path(manifest_path)
            self.pkg_type = pkg_type
            self.pkg_location = pkg_location
            self.contents = manifest_contents or self.get_manifest_content_from_path(self.path)
        else:
            self.contents = manifest_contents

    @staticmethod
    def normalize_path(original_path):
        return path.normpath(path.abspath(path.expanduser(original_path)))

    @staticmethod
    def get_manifest_fobj(manifest_path):
        return open(manifest_path, b'rb')

    @staticmethod
    def get_manifest_content_from_path(manifest_path):
        fobj = Manifest.get_manifest_fobj(manifest_path)
        return yaml.load(fobj, Loader=yaml.BaseLoader)

    def get_args_and_flags(self):
        args = [
         pipes.quote((b'{}={}').format(self.local_virtualenv_path, self.pkg_location))]
        flags = self.get_single_flags()
        flags.extend([ ((b'{}-{}').format(self.pkg_type, name_type), self.contents.get(name_type, self.virtualenv_name)) for name_type in ('user',
                                                                                                                                           'group')
                     ])
        flags.append((b'directories', self.remote_virtualenv_path))
        cfg_args, cfg_flags = self.get_config_args_and_flags()
        args.extend(cfg_args)
        flags.extend(cfg_flags)
        flags.extend(self.get_dependency_flags())
        flags.extend(self.get_exclude_flags())
        return (
         args, flags)

    def get_config_args_and_flags(self):
        args = []
        flags = []
        if not self.contents.get(b'config_files'):
            return (args, flags)
        for remote_path, local_path in self.contents[b'config_files'].items():
            remote_cfg = path.normpath(path.join(self.remote_virtualenv_path, remote_path))
            assert path.isabs(remote_cfg)
            local_cfg = path.normpath(path.join(self.manifest_dir, local_path))
            assert path.isabs(local_cfg)
            flags.append((b'config-files', remote_cfg[1:]))
            args.append((b'{}={}/').format(pipes.quote(local_cfg), pipes.quote(path.dirname(remote_cfg))))

        return (args, flags)

    def get_single_flags(self):
        flags = {flag.replace(b'_', b'-'):value for flag, value in self.contents.items() if flag in ('name',
                                                                                                     'version',
                                                                                                     'iteration',
                                                                                                     'epoch',
                                                                                                     'before_install',
                                                                                                     'after_install',
                                                                                                     'description') if flag in ('name',
                                                                                                                                'version',
                                                                                                                                'iteration',
                                                                                                                                'epoch',
                                                                                                                                'before_install',
                                                                                                                                'after_install',
                                                                                                                                'description')}
        for script_type in ('before-install', 'after-install'):
            script_path = flags.get(script_type)
            if script_path and not path.isabs(script_path):
                flags[script_type] = path.normpath(path.join(self.manifest_dir, script_path))

        if isinstance(flags.get(b'epoch'), six.string_types) and flags.get(b'epoch').lower() == b'timestamp':
            flags[b'epoch'] = str(int(time.time()))
        return list(flags.items())

    def get_bool_value(self, name):
        """
        Get manifest value `name` as a boolean
        """
        return bool(self.contents.get(name, b'').lower() in ('true', 'yes', 'on', 'y'))

    def get_dependency_flags(self):
        """
        get all the flags related to dependencies
        """
        return [ (b'depends', dep) for dep in self.contents.get(b'depends', []) ]

    def get_exclude_flags(self):
        """
        Get all the excludes defined in manifest. Optionally add '*.py[co]' and
        '__pycache__' if exclude_compiled is set.
        """
        excludes = set([ (b'exclude', excl) for excl in self.contents.get(b'exclude', []) ])
        if self.get_bool_value(b'exclude_compiled'):
            excludes |= set([ (b'exclude', excl) for excl in [b'*.py[co]', b'__pycache__'] ])
        return excludes

    @property
    def manifest_dir(self):
        return path.dirname(self.path)

    @property
    def name(self):
        return self.contents[b'name']

    @property
    def upgrade_pip(self):
        return self.get_bool_value(b'upgrade_pip')

    @property
    def upgrade_wheel(self):
        return self.get_bool_value(b'upgrade_wheel')

    @property
    def virtualenv_name(self):
        return self.contents.setdefault(b'virtualenv_name', self.contents[b'name'])

    @property
    def local_package_path(self):
        self.contents.setdefault(b'local_package_path', self.virtualenv_name)
        if not path.isabs(self.contents[b'local_package_path']):
            return path.abspath(path.join(self.manifest_dir, self.contents[b'local_package_path']))
        else:
            return self.contents[b'local_package_path']

    @property
    def local_virtualenv_path(self):
        return path.join(self.manifest_dir, b'build', self.virtualenv_name)

    @property
    def remote_virtualenv_path(self):
        return path.join(self.pkg_location, self.virtualenv_name)