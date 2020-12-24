# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/compositeindex/wrapper.py
# Compiled at: 2009-04-09 11:12:35
import logging
from config import PROJECTNAME
logger = logging.getLogger(PROJECTNAME)

def log(msg):
    logger.info(msg)


wrapper_key = PROJECTNAME
PATTERN = '__%s_patch_%s__' % (wrapper_key, '%s')

def call(self, __name__, *args, **kw):
    return getattr(self, PATTERN % __name__)(*args, **kw)


WRAPPER = '__%s_patch_is_wrapper_method__' % wrapper_key
ORIG_NAME = '__%s_patch_original_method_name__' % wrapper_key

def isWrapperMethod(meth):
    return getattr(meth, WRAPPER, False)


def wrap_method(klass, name, method, pattern=PATTERN):
    old_method = getattr(klass, name)
    if isWrapperMethod(old_method):
        log('Already wrapped method %s.%s, skipping.' % (klass.__name__, name))
        return
    log('Wrapping method %s.%s' % (klass.__name__, name))
    new_name = pattern % name
    setattr(klass, new_name, old_method)
    setattr(method, ORIG_NAME, new_name)
    setattr(method, WRAPPER, True)
    setattr(klass, name, method)


def unwrap_method(klass, name):
    old_method = getattr(klass, name)
    if not isWrapperMethod(old_method):
        raise ValueError, 'Trying to unwrap non-wrapped method %s.%s' % (klass.__name__, name)
    orig_name = getattr(old_method, ORIG_NAME)
    new_method = getattr(klass, orig_name)
    delattr(klass, orig_name)
    setattr(klass, name, new_method)