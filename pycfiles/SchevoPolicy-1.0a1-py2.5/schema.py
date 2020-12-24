# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/schema.py
# Compiled at: 2008-01-19 12:32:25
"""Policy schema support.

Everything in here is imported by all policy schemata.

For copyright, license, and warranty, see bottom of file.
"""
__all__ = [
 'ALLOW',
 'DENY',
 'schevopolicy']
from textwrap import dedent
import threading
from dispatch import generic, strategy
from schevo.lib.module import from_string, forget, remember
import schevo.schema, schevopolicy
from schevopolicy.constant import ALLOW, DENY
from schevopolicy.policy import Policy
import_lock = threading.Lock()

def start(policy):
    """Lock policy schema importing."""
    import_lock.acquire()


def prep(namespace):
    """Add syntax support magic to the policy schema namespace.

    At the top of each policy schema, the following two lines perform
    the magic::

      from schevopolicy.schema import *
      schevopolicy.schema.prep(locals())
    """

    @generic()
    def allow(db, context):
        """Return True if any operation should be allowed."""
        pass

    @generic()
    def allow_t(db, context, extent, entity, t_name):
        """Return True if the transaction should be allowed."""
        pass

    @generic()
    def allow_v(db, context, entity, v_name):
        """Return True if the transaction should be allowed."""
        pass

    namespace['allow'] = allow
    namespace['allow_t'] = allow_t
    namespace['allow_v'] = allow_v


def finish(policy, schema_module=None):
    """Unlock the policy schema import mutex and return the policy
    schema."""
    if schema_module is None:
        import_lock.release()
        return
    try:
        db = policy.db
        allow = schema_module.allow
        allow_t = schema_module.allow_t
        allow_v = schema_module.allow_v

        def policy_allow(context):
            return allow(db, context)

        def policy_allow_t(context, extent, entity, t_name):
            return allow_t(db, context, extent, entity, t_name)

        def policy_allow_v(context, entity, v_name):
            return allow_v(db, context, entity, v_name)

        policy.allow = policy_allow
        policy.allow_t = policy_allow_t
        policy.allow_v = policy_allow_v
        default = schema_module.default

        @allow.when(strategy.default)
        def allow(db, context):
            return default

        @allow_t.when(strategy.default)
        def allow_t(db, context, extent, entity, t_name):
            return default

        @allow_v.when(strategy.default)
        def allow_v(db, context, entity, v_name):
            return default

    finally:
        import_lock.release()

    return


PREAMBLE = 'from schevopolicy.schema import *\nschevopolicy.schema.prep(locals())\n'
counter = 0

def next_name():
    """Return the next policy module name for an imported policy schema."""
    global counter
    cur = counter
    counter += 1
    return 'schevopolicy-module-%i' % cur


def policy_from_location(db, location):
    source = schevo.schema.read(location, db.version)
    return policy_from_source(db, source)


def policy_from_source(db, source):
    policy = Policy(db)
    start(policy)
    module = from_string(source, next_name())
    remember(module)
    finish(policy, module)
    return policy


def policy_from_string(db, body):
    source = PREAMBLE + dedent(body)
    return policy_from_source(db, source)