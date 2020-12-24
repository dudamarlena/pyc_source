# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\dbghelp.py
# Compiled at: 2011-02-21 01:24:11
"""dbghelp module.

Debugging aid
"""
import gc, inspect, logging, sys, traceback, types, weakref, stackless
gc.disable()
DEBUG_LEVEL_DISABLE = 0
DEBUG_LEVEL_NORMAL = 1
DEBUG_LEVEL_HIGH = 2
DEBUG_LEVEL_ABSURD = 3
DEFAULT_DEBUG_LEVEL = DEBUG_LEVEL_HIGH

class DbgHelp(object):

    def __init__(self):
        self.garbage = []
        self.logFileCounter = 0
        self.discardCollect = True
        self.debug = DEFAULT_DEBUG_LEVEL
        self.log = logging.getLogger('CORE.Debug')
        self.orphanedTasklets = weakref.WeakKeyDictionary()

    def TaskletExiting(self, tasklet):
        """Keep track of dead tasklets to make sure they don't stay in memory"""
        if self.debug:
            self.orphanedTasklets[tasklet] = 1

    def ReportShutdown(self):
        if self.debug and self.orphanedTasklets:
            if len(self.orphanedTasklets) == 1 and self.orphanedTasklets.keys()[0] == stackless.getcurrent():
                pass
            else:
                self.log.error('Orphaned tasklets:')
                for t in self.orphanedTasklets.keys():
                    if t == stackless.getcurrent():
                        continue
                    self.log.error('\t%s', `t`)
                    if t.frame:
                        self.log.error('\tframe=%s', t.frame)
                        traceback.print_stack(t.frame)

        self.ReportGarbage()

    def ReportGarbage(self):
        """Collects gc.garbage and reports it.
        'level' is 1 for summary, 2 for verbose
        """
        if self.discardCollect:
            gc.collect()
            del gc.garbage[:]
            self.discardCollect = False
            return
        if self.debug == DEBUG_LEVEL_ABSURD:
            gc.set_debug(gc.DEBUG_SAVEALL)
            if gc.collect():
                f = open('c:/logs/leaks/leaks.%07d.txt' % self.logFileCounter, 'w')
                self.log.error('Garbage count: %s. Please fix this!', len(gc.garbage))
                self.logFileCounter += 1
                for i, v in enumerate(gc.garbage):
                    f.write('[%s]\r\n%s\r\n' % (i, Repr(v)))
                    r = gc.get_referrers(v)
                    f.write('Referrers (count=%s):\r\n' % len(r))
                    for j in r:
                        f.write('\t%s\r\n' % Repr(j))

                    f.write('\r\n')
                    self.log.error('\t%s', v)

                f.close()
        elif self.debug == DEBUG_LEVEL_HIGH:
            gc.set_debug(gc.DEBUG_SAVEALL)
            if gc.collect(1):
                self.TraceGarbage(gc.garbage)
                del gc.garbage[:]
                gc.set_debug(0)
                gc.collect(1)
                return
            del gc.garbage[:]
        elif self.debug == DEBUG_LEVEL_NORMAL:
            leaks = gc.collect(1)
            if leaks:
                self.log.warning('Object leaks, count = %s', leaks)

    def TraceGarbage(self, garbage):
        self.log.error('Garbage count: %s. Please fix this!', len(garbage))
        for obj in garbage:
            try:
                s = Repr(obj)
                if not s:
                    continue
                self.log.error('\tLEAK: %s', s)
                r = gc.get_referrers(obj)
                self.log.error('\tReferrers (count=%s):', len(r))
                for ref in r:
                    if ref == stackless.getcurrent().frame:
                        continue
                    s = Repr(ref)
                    if s:
                        self.log.error('\t\t%s', s)

                del r[:]
                r = gc.get_referents(obj)
                self.log.error('\tReferents (count=%s):', len(r))
                for ref in r:
                    s = Repr(ref)
                    if s:
                        self.log.error('\t\t%s', s)

                self.log.error('')
                del r[:]
            except ReferenceError:
                pass

    def ReportReferrers(self, title, objects):
        """Reports referrers of 'objects'. 'objects' is a list of objects that have leaked"""
        self.log.error('%s: %s', title, objects)
        for o in objects:
            self.log.error('\t%s\t%s', o, gc.get_referrers(o))
            for line in traceback.format_stack(o.frame):
                self.log.error(line.rstrip())

            self.log.error('----------------------')


def Repr(o, maxlen=500):

    def Id(obj):
        return '<%s object at %s>' % (type(obj).__name__, hex(id(obj)))

    s = Id(o)
    if isinstance(o, (basestring, types.IntType, types.FloatType)):
        return None
    else:
        if isinstance(o, types.IntType):
            if o in (-1, 0, 1):
                return None
            s += str(o)
        elif isinstance(o, types.FloatType):
            if o in (-1.0, 0.0, 1.0):
                return None
            s += str(o)
        elif isinstance(o, (types.ListType, types.TupleType)):
            s += ' size %s: %s' % (len(o), repr(o))
        elif isinstance(o, types.DictType):
            s += ' size %s: %s' % (len(o), repr(o.keys()))
        elif isinstance(o, types.FrameType):
            filename = o.f_code.co_filename
            lineno = o.f_lineno
            s += ' %s(%s)' % (filename, lineno)
        elif hasattr(o, '__class__'):
            s += repr(o)
        elif hasattr(o, 'im_func'):
            s += ' %s %s(%s)' % (o.im_func.func_name, o.im_func.func_code.co_filename, o.im_func.func_code.co_firstlineno)
        elif hasattr(o, 'func_code'):
            s += ' %s %s(%s)' % (o.func_name, o.func_code.co_filename, o.func_code.co_firstlineno)
        elif type(o) == types.TypeType:
            s += repr(o)
        elif type(o) == types.InstanceType:
            s = '%s %s' % (repr(o), inspect.getfile(o.__class__))
        return s[:maxlen]