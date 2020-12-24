# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/PickleSaver.py
# Compiled at: 2018-01-06 14:43:43
"""
An object that makes some of the attributes of your class persistent, pickling
them and lazily writing them to a file.
"""
import os, cPickle as pickle, warnings, fileutil, nummedobj, twistedutil
from twisted.python import log

class PickleSaver(nummedobj.NummedObj):
    """ 
    This makes some of the attributes of your class persistent, saving
    them in a pickle and saving them lazily.

    The general idea:  You are going to tell PickleSaver which of your
    attributes ought to be persistently saved, and the name of a file to
    save them in.  Those attributes will get saved to disk, and when
    your object is instantiated those attributes will get set to the
    values loaded from the file.

    Usage: inherit from PickleSaver and call PickleSaver.__init__() in your
    constructor.  You will pass arguments to PickleSaver.__init__()
    telling it which attributes to save, which file to save them in, and
    what values they should have if there is no value stored for them in
    the file.

    Note: do *not* assign values to your persistent attributes in your
    constructor, because you might thus overwrite their persistent
    values.

    Then whenever you change one of the persistent attributes, call
    self.lazy_save() (it won't *really* save -- it'll just schedule a
    save for DELAY minutes later.)  If you update an attribute and
    forget to call self.lazy_save() then the change will not be saved,
    unless you later call self.lazy_save() before you shut down.

    Data could be lost if the Python interpreter were to die
    unexpectedly (for example, due to a segfault in a compiled machine
    code module or due to the Python process being killed without
    warning via SIGKILL) before the delay passes.  However if the Python
    interpreter shuts down cleanly (i.e., if it garbage collects and
    invokes the __del__ methods of the collected objects), then the data
    will be saved at that time (unless your class has the "not-collectable"
    problem: http://python.org/doc/current/lib/module-gc.html -- search
    in text for "uncollectable").

    Note: you can pass DELAY=0 to make PickleSaver a not-so-lazy saver.
    The advantage of laziness is that you don't touch the disk as
    often -- touching disk is a performance cost.

    To cleanly shutdown, invoke shutdown().  Further operations after that
    will result in exceptions.
    """

    class ExtRes:
        """
        This is for holding things (external resources) that PickleSaver needs
        to finalize after PickleSaver is killed.  (post-mortem finalization)

        In particular, this holds the names and values of all attributes
        that have been changed, so that after the PickleSaver is
        garbage-collected those values will be saved to the persistent file.
        """

        def __init__(self, fname, objname):
            self.fname = fname
            self.objname = objname
            self.dirty = False
            self.savertask = None
            self.valstr = None
            return

        def _save_to_disk(self):
            if self.valstr is not None:
                log.msg('%s._save_to_disk(): fname: %s' % (self.objname, self.fname))
                of = open(self.fname + '.tmp', 'wb')
                of.write(self.valstr)
                of.flush()
                of.close()
                of = None
                fileutil.remove_if_possible(self.fname)
                fileutil.rename(self.fname + '.tmp', self.fname)
                log.msg('%s._save_to_disk(): now, having finished write(), os.path.isfile(%s): %s' % (self, self.fname, os.path.isfile(self.fname)))
                self.valstr = None
                self.dirty = False
                try:
                    self.savertask.callId.cancel()
                except:
                    pass

                self.savertask = None
            return

        def shutdown(self):
            if self.dirty:
                self._save_to_disk()
            if self.savertask:
                try:
                    self.savertask.callId.cancel()
                except:
                    pass

                self.savertask = None
            return

        def __del__(self):
            self.shutdown()

    def __init__(self, fname, attrs, DELAY=3600, savecb=None):
        """
        @param attrs: a dict whose keys are the names of all the attributes to be persistently stored and whose values are the initial default value that the attribute gets set to the first time it is ever used;  After this first initialization, the value will be persistent so the initial default value will never be used again.
        @param savecb: if not None, then it is a callable that will be called after each save completes (useful for unit tests) (savecb doesn't get called after a shutdown-save, only after a scheduled save)
        """
        warnings.warn('deprecated', DeprecationWarning)
        nummedobj.NummedObj.__init__(self)
        self._DELAY = DELAY
        self._attrnames = attrs.keys()
        self._extres = PickleSaver.ExtRes(fname=fname, objname=self.__repr__())
        self._savecb = savecb
        for attrname, defaultval in attrs.items():
            setattr(self, attrname, defaultval)

        try:
            attrdict = pickle.loads(open(self._extres.fname, 'rb').read())
            for attrname, attrval in attrdict.items():
                if not hasattr(self, attrname):
                    log.msg('WARNING: %s has no attribute named %s on load from disk, value: %s.' % (self, attrname, attrval))
                setattr(self, attrname, attrval)

        except (pickle.UnpicklingError, IOError, EOFError) as le:
            try:
                attrdict = pickle.loads(open(self._extres.fname + '.tmp', 'rb').read())
                for attrname, attrval in attrdict.items():
                    if not hasattr(self, attrname):
                        log.msg('WARNING: %s has no attribute named %s on load from disk, value: %s.' % (self, attrname, attrval))
                    setattr(self, attrname, attrval)

            except (pickle.UnpicklingError, IOError, EOFError) as le2:
                log.msg("Got exception attempting to load attrs.  (This is normal if this is the first time you've used this persistent %s object.)  fname: %s, le: %s, le2: %s" % (self.__class__, self._extres.fname, le, le2))

        self.lazy_save()

    def _store_attrs_in_extres(self):
        d = {}
        for attrname in self._attrnames:
            d[attrname] = getattr(self, attrname)

        self._extres.valstr = pickle.dumps(d, True)
        self._extres.dirty = True

    def _save_to_disk(self):
        log.msg('%s._save_to_disk()' % (self,))
        self._extres._save_to_disk()
        if self._savecb:
            self._savecb()

    def _lazy_save(self, delay=None):
        """ @deprecated: use lazy_save() instead """
        return self.lazy_save(delay)

    def lazy_save(self, delay=None):
        """
        @param delay: how long from now before the data gets saved to disk, or `None' in order to use the default value provided in the constructor
        """
        if delay is None:
            delay = self._DELAY
        self._store_attrs_in_extres()
        newsavetask = twistedutil.callLater_weakly(delay, self._save_to_disk)
        if self._extres.savertask:
            if self._extres.savertask.callId.getTime() < newsavetask.callId.getTime():
                try:
                    newsavetask.callId.cancel()
                except:
                    pass

            else:
                try:
                    self._extres.savertask.callId.cancel()
                except:
                    pass

                self._extres.savertask = newsavetask
        else:
            self._extres.savertask = newsavetask
        return

    def shutdown(self):
        self.extres.shutdown()
        self.extres = None
        return