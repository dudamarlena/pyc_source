# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/namanbharadwaj/en/lib/python2.6/site-packages/bobb/api.py
# Compiled at: 2013-08-06 13:35:04
import subprocess, os, os.path, time
from contextlib import contextmanager
from functools import wraps
import bobb.internal, bobb.exceptions

def run(command):
    """ Run the given command in the shell. """
    subprocess.call(command, shell=True)


@contextmanager
def cd(directory):
    """ Change directory within a context manager. """
    if directory is None:
        prev = os.getcwd()
        yield
        os.chdir(prev)
    else:
        prev = os.getcwd()
        os.chdir(directory)
        yield
        os.chdir(prev)
    return


def builder(tgts=[], deps=[], always_build=False, dir=None):
    """ Register the given function as a builder.

  Bobb expects builders to create certain target paths. Bobb will also ensure
  that any paths required to build the targets (dependencies) exist, and if
  they don't, Bobb will attempt to build them.

  The builder can expect that none of the target paths exist prior to execution
  and that all of the dependencies do exist and have been appropriately built
  (by some other registered builder if it exists).

  Keyword arguments:
  tgts -- a list of paths which Bobb expects the builder to generate.
  deps -- a list of paths on which the builder depends.
  always_build -- if True, always rebuild the targets; otherwise, be smart.
  dir  -- the working directory within which Bobb will execute the builder.

  Note: If relative paths are used, they are assumed to be relative to the dir
  argument.

  Note 2: The builder should be able to build its targets without any passed
  arguments (default arguments are ok). When resolving dependencies, Bobb
  passes no arguments to the builder function.

  """

    def decorate(fn):
        if len(tgts) == 0:
            raise bobb.exceptions.TargetConfigError(fn.__name__)

        @wraps(fn)
        def wrapper():
            with cd(dir):

                def has_builder(tgt):
                    return bobb.internal.has_builder(os.path.abspath(tgt))

                def is_file(path):
                    return os.path.exists(path)

                def check_valid(dep):
                    if not has_builder(dep) or is_file(dep):
                        raise bobb.exceptions.BuilderNotFoundError(dep)

                map(check_valid, deps)

                def call_builder(dep):
                    if has_builder(dep):
                        bobb.internal.get_builder(os.path.abspath(dep))()

                map(call_builder, deps)

                def check_not_deleted(dep):
                    if not is_file(dep):
                        raise bobb.exceptions.TargetDeletionError(dep)

                map(check_not_deleted, deps)

                def build():
                    run('rm -Rf %s' % (' ').join(tgts))
                    fn()

                if always_build:
                    build()
                elif not all(map(is_file, tgts)):
                    build()
                elif len(deps) > 0:
                    newest_dep_time = max(map(os.getmtime, deps))
                    oldest_tgt_time = min(map(os.getmtime, tgts))
                    if oldest_tgt_time < newest_dep_time:
                        build()
                    else:
                        return False
                else:
                    return False

                def check_built(tgt):
                    if not is_file(tgt):
                        raise BuilderError(tgt, fn.__name__)

                map(check_built, deps)
                return True

        with cd(dir):
            for tgt in tgts:
                bobb.internal.register_builder(os.path.abspath(tgt), wrapper)

        return wrapper

    return decorate


def action(deps=[], dir=None):
    """ Register the given function as an action.

  Bobb will ensure that any paths required to execute the action (dependencies)
  exist, and if they don't, Bobb will attempt to build them.

  The action can expect that all of the dependencies do exist and have been
  appropriately built (by some other registered builder if it exists) prior to
  execution.

  Keyword arguments:
  deps -- a list of paths on which the builder depends.
  dir  -- the working directory within which Bobb will execute the builder.

  Note: If relative paths are used, they are assumed to be relative to the dir
  argument.

  """

    def decorate(fn):

        @wraps(fn)
        def wrapper():
            with cd(dir):

                def has_builder(tgt):
                    return bobb.internal.has_builder(os.path.abspath(tgt))

                def is_file(path):
                    return os.path.exists(path)

                def check_valid(dep):
                    if not has_builder(dep) or is_file(dep):
                        raise bobb.exceptions.BuilderNotFoundError(dep)

                map(check_valid, deps)

                def call_builder(dep):
                    if has_builder(dep):
                        bobb.internal.get_builder(os.path.abspath(dep))()

                map(call_builder, deps)

                def check_not_deleted(dep):
                    if not is_file(dep):
                        raise bobb.exceptions.TargetDeletionError(dep)

                map(check_not_deleted, deps)
                fn()

        with cd(dir):
            bobb.internal.register_action(wrapper)
        return wrapper

    return decorate