# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/pep517/build.py
# Compiled at: 2019-02-14 00:35:07
"""Build a project using PEP 517 hooks.
"""
import argparse, logging, os, contextlib
from pip._vendor import pytoml
import shutil, errno, tempfile
from .envbuild import BuildEnvironment
from .wrappers import Pep517HookCaller
log = logging.getLogger(__name__)

@contextlib.contextmanager
def tempdir():
    td = tempfile.mkdtemp()
    try:
        yield td
    finally:
        shutil.rmtree(td)


def _do_build(hooks, env, dist, dest):
    get_requires_name = ('get_requires_for_build_{dist}').format(**locals())
    get_requires = getattr(hooks, get_requires_name)
    reqs = get_requires({})
    log.info('Got build requires: %s', reqs)
    env.pip_install(reqs)
    log.info('Installed dynamic build dependencies')
    with tempdir() as (td):
        log.info('Trying to build %s in %s', dist, td)
        build_name = ('build_{dist}').format(**locals())
        build = getattr(hooks, build_name)
        filename = build(td, {})
        source = os.path.join(td, filename)
        shutil.move(source, os.path.join(dest, os.path.basename(filename)))


def mkdir_p(*args, **kwargs):
    """Like `mkdir`, but does not raise an exception if the
    directory already exists.
    """
    try:
        return os.mkdir(*args, **kwargs)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def build(source_dir, dist, dest=None):
    pyproject = os.path.join(source_dir, 'pyproject.toml')
    dest = os.path.join(source_dir, dest or 'dist')
    mkdir_p(dest)
    with open(pyproject) as (f):
        pyproject_data = pytoml.load(f)
    buildsys = pyproject_data['build-system']
    requires = buildsys['requires']
    backend = buildsys['build-backend']
    hooks = Pep517HookCaller(source_dir, backend)
    with BuildEnvironment() as (env):
        env.pip_install(requires)
        _do_build(hooks, env, dist, dest)


parser = argparse.ArgumentParser()
parser.add_argument('source_dir', help='A directory containing pyproject.toml')
parser.add_argument('--binary', '-b', action='store_true', default=False)
parser.add_argument('--source', '-s', action='store_true', default=False)
parser.add_argument('--out-dir', '-o', help='Destination in which to save the builds relative to source dir')

def main(args):
    dists = list(filter(None, (
     'sdist' if args.source or not args.binary else None,
     'wheel' if args.binary or not args.source else None)))
    for dist in dists:
        build(args.source_dir, dist, args.out_dir)

    return


if __name__ == '__main__':
    main(parser.parse_args())