# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/pep517/build.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 3335 bytes
"""Build a project using PEP 517 hooks.
"""
import argparse, logging, os
from pip._vendor import toml
import shutil
from .envbuild import BuildEnvironment
from .wrappers import Pep517HookCaller
from .dirtools import tempdir, mkdir_p
from .compat import FileNotFoundError
log = logging.getLogger(__name__)

def validate_system(system):
    """
    Ensure build system has the requisite fields.
    """
    required = {
     'requires', 'build-backend'}
    if not required <= set(system):
        message = 'Missing required fields: {missing}'.format(missing=(required - set(system)))
        raise ValueError(message)


def load_system(source_dir):
    """
    Load the build system from a source dir (pyproject.toml).
    """
    pyproject = os.path.join(source_dir, 'pyproject.toml')
    with open(pyproject) as (f):
        pyproject_data = toml.load(f)
    return pyproject_data['build-system']


def compat_system(source_dir):
    """
    Given a source dir, attempt to get a build system backend
    and requirements from pyproject.toml. Fallback to
    setuptools but only if the file was not found or a build
    system was not indicated.
    """
    try:
        system = load_system(source_dir)
    except (FileNotFoundError, KeyError):
        system = {}

    system.setdefault('build-backend', 'setuptools.build_meta:__legacy__')
    system.setdefault('requires', ['setuptools', 'wheel'])
    return system


def _do_build(hooks, env, dist, dest):
    get_requires_name = ('get_requires_for_build_{dist}'.format)(**locals())
    get_requires = getattr(hooks, get_requires_name)
    reqs = get_requires({})
    log.info('Got build requires: %s', reqs)
    env.pip_install(reqs)
    log.info('Installed dynamic build dependencies')
    with tempdir() as (td):
        log.info('Trying to build %s in %s', dist, td)
        build_name = ('build_{dist}'.format)(**locals())
        build = getattr(hooks, build_name)
        filename = build(td, {})
        source = os.path.join(td, filename)
        shutil.move(source, os.path.join(dest, os.path.basename(filename)))


def build(source_dir, dist, dest=None, system=None):
    system = system or load_system(source_dir)
    dest = os.path.join(source_dir, dest or 'dist')
    mkdir_p(dest)
    validate_system(system)
    hooks = Pep517HookCaller(source_dir, system['build-backend'], system.get('backend-path'))
    with BuildEnvironment() as (env):
        env.pip_install(system['requires'])
        _do_build(hooks, env, dist, dest)


parser = argparse.ArgumentParser()
parser.add_argument('source_dir',
  help='A directory containing pyproject.toml')
parser.add_argument('--binary',
  '-b', action='store_true',
  default=False)
parser.add_argument('--source',
  '-s', action='store_true',
  default=False)
parser.add_argument('--out-dir',
  '-o', help='Destination in which to save the builds relative to source dir')

def main(args):
    dists = list(filter(None, (
     args.binary or 'sdist' if not args.source else None,
     args.source or 'wheel' if not args.binary else None)))
    for dist in dists:
        build(args.source_dir, dist, args.out_dir)


if __name__ == '__main__':
    main(parser.parse_args())