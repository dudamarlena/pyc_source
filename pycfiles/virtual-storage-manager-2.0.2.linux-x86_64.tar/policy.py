# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/policy.py
# Compiled at: 2016-06-13 14:11:03
"""Policy Engine For Vsm"""
from oslo.config import cfg
from vsm import exception
from vsm import flags
from vsm.openstack.common import policy
from vsm import utils
policy_opts = [
 cfg.StrOpt('policy_file', default='policy.json', help=_('JSON file representing policy')),
 cfg.StrOpt('policy_default_rule', default='default', help=_('Rule checked when requested rule is not found'))]
FLAGS = flags.FLAGS
FLAGS.register_opts(policy_opts)
_POLICY_PATH = None
_POLICY_CACHE = {}

def reset():
    global _POLICY_CACHE
    global _POLICY_PATH
    _POLICY_PATH = None
    _POLICY_CACHE = {}
    policy.reset()
    return


def init():
    global _POLICY_PATH
    if not _POLICY_PATH:
        _POLICY_PATH = utils.find_config(FLAGS.policy_file)
    utils.read_cached_file(_POLICY_PATH, _POLICY_CACHE, reload_func=_set_brain)


def _set_brain(data):
    default_rule = FLAGS.policy_default_rule
    policy.set_brain(policy.HttpBrain.load_json(data, default_rule))


def enforce(context, action, target):
    """Verifies that the action is valid on the target in this context.

       :param context: vsm context
       :param action: string representing the action to be checked
           this should be colon separated for clarity.
           i.e. ``compute:create_instance``,
           ``compute:attach_storage``,
           ``storage:attach_storage``

       :param object: dictionary representing the object of the action
           for object creation this should be a dictionary representing the
           location of the object e.g. ``{'project_id': context.project_id}``

       :raises vsm.exception.PolicyNotAuthorized: if verification fails.

    """
    init()
    match_list = (
     'rule:%s' % action,)
    credentials = context.to_dict()
    policy.enforce(match_list, target, credentials, exception.PolicyNotAuthorized, action=action)


def check_is_admin(roles):
    """Whether or not roles contains 'admin' role according to policy setting.

    """
    init()
    action = 'context_is_admin'
    match_list = ('rule:%s' % action,)
    target = {'project_id': ''}
    credentials = {'roles': roles}
    return policy.enforce(match_list, target, credentials)