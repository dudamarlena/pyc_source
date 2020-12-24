# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\CacheDir.py
# Compiled at: 2016-07-07 03:21:31
__revision__ = 'src/engine/SCons/CacheDir.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__doc__ = '\nCacheDir support\n'
import json, os, stat, sys, SCons.Action, SCons.Warnings
cache_enabled = True
cache_debug = False
cache_force = False
cache_show = False
cache_readonly = False

def CacheRetrieveFunc(target, source, env):
    t = target[0]
    fs = t.fs
    cd = env.get_CacheDir()
    cachedir, cachefile = cd.cachepath(t)
    if not fs.exists(cachefile):
        cd.CacheDebug('CacheRetrieve(%s):  %s not in cache\n', t, cachefile)
        return 1
    cd.CacheDebug('CacheRetrieve(%s):  retrieving from %s\n', t, cachefile)
    if SCons.Action.execute_actions:
        if fs.islink(cachefile):
            fs.symlink(fs.readlink(cachefile), t.get_internal_path())
        else:
            env.copy_from_cache(cachefile, t.get_internal_path())
        st = fs.stat(cachefile)
        fs.chmod(t.get_internal_path(), stat.S_IMODE(st[stat.ST_MODE]) | stat.S_IWRITE)
    return 0


def CacheRetrieveString(target, source, env):
    t = target[0]
    fs = t.fs
    cd = env.get_CacheDir()
    cachedir, cachefile = cd.cachepath(t)
    if t.fs.exists(cachefile):
        return "Retrieved `%s' from cache" % t.get_internal_path()
    else:
        return


CacheRetrieve = SCons.Action.Action(CacheRetrieveFunc, CacheRetrieveString)
CacheRetrieveSilent = SCons.Action.Action(CacheRetrieveFunc, None)

def CachePushFunc(target, source, env):
    if cache_readonly:
        return
    t = target[0]
    if t.nocache:
        return
    fs = t.fs
    cd = env.get_CacheDir()
    cachedir, cachefile = cd.cachepath(t)
    if fs.exists(cachefile):
        cd.CacheDebug('CachePush(%s):  %s already exists in cache\n', t, cachefile)
        return
    cd.CacheDebug('CachePush(%s):  pushing to %s\n', t, cachefile)
    tempfile = cachefile + '.tmp' + str(os.getpid())
    errfmt = 'Unable to copy %s to cache. Cache file is %s'
    if not fs.isdir(cachedir):
        try:
            fs.makedirs(cachedir)
        except EnvironmentError:
            if not fs.isdir(cachedir):
                msg = errfmt % (str(target), cachefile)
                raise SCons.Errors.EnvironmentError(msg)

    try:
        if fs.islink(t.get_internal_path()):
            fs.symlink(fs.readlink(t.get_internal_path()), tempfile)
        else:
            fs.copy2(t.get_internal_path(), tempfile)
        fs.rename(tempfile, cachefile)
        st = fs.stat(t.get_internal_path())
        fs.chmod(cachefile, stat.S_IMODE(st[stat.ST_MODE]) | stat.S_IWRITE)
    except EnvironmentError:
        msg = errfmt % (str(target), cachefile)
        SCons.Warnings.warn(SCons.Warnings.CacheWriteErrorWarning, msg)


CachePush = SCons.Action.Action(CachePushFunc, None)
warned = dict()

class CacheDir(object):

    def __init__(self, path):
        global warned
        try:
            import hashlib
        except ImportError:
            msg = 'No hashlib or MD5 module available, CacheDir() not supported'
            SCons.Warnings.warn(SCons.Warnings.NoMD5ModuleWarning, msg)
            path = None

        self.path = path
        self.current_cache_debug = None
        self.debugFP = None
        self.config = dict()
        if path is None:
            return
        else:
            config_file = os.path.join(path, 'config')
            if not os.path.exists(config_file):
                if os.path.isdir(path) and len(os.listdir(path)) != 0:
                    self.config['prefix_len'] = 1
                    if self.path not in warned:
                        msg = 'Please upgrade your cache by running ' + ' scons-configure-cache.py ' + self.path
                        SCons.Warnings.warn(SCons.Warnings.CacheVersionWarning, msg)
                        warned[self.path] = True
                else:
                    if not os.path.isdir(path):
                        try:
                            os.makedirs(path)
                        except OSError:
                            msg = 'Failed to create cache directory ' + path
                            raise SCons.Errors.EnvironmentError(msg)

                    self.config['prefix_len'] = 2
                    if not os.path.exists(config_file):
                        try:
                            with open(config_file, 'w') as (config):
                                json.dump(self.config, config)
                        except:
                            msg = 'Failed to write cache configuration for ' + path
                            raise SCons.Errors.EnvironmentError(msg)

            else:
                try:
                    with open(config_file) as (config):
                        self.config = json.load(config)
                except ValueError:
                    msg = 'Failed to read cache configuration for ' + path
                    raise SCons.Errors.EnvironmentError(msg)

            return

    def CacheDebug(self, fmt, target, cachefile):
        if cache_debug != self.current_cache_debug:
            if cache_debug == '-':
                self.debugFP = sys.stdout
            elif cache_debug:
                self.debugFP = open(cache_debug, 'w')
            else:
                self.debugFP = None
            self.current_cache_debug = cache_debug
        if self.debugFP:
            self.debugFP.write(fmt % (target, os.path.split(cachefile)[1]))
        return

    def is_enabled(self):
        return cache_enabled and self.path is not None

    def is_readonly(self):
        return cache_readonly

    def cachepath(self, node):
        """
        """
        if not self.is_enabled():
            return (None, None)
        else:
            sig = node.get_cachedir_bsig()
            subdir = sig[:self.config['prefix_len']].upper()
            dir = os.path.join(self.path, subdir)
            return (dir, os.path.join(dir, sig))

    def retrieve(self, node):
        """
        This method is called from multiple threads in a parallel build,
        so only do thread safe stuff here. Do thread unsafe stuff in
        built().

        Note that there's a special trick here with the execute flag
        (one that's not normally done for other actions).  Basically
        if the user requested a no_exec (-n) build, then
        SCons.Action.execute_actions is set to 0 and when any action
        is called, it does its showing but then just returns zero
        instead of actually calling the action execution operation.
        The problem for caching is that if the file does NOT exist in
        cache then the CacheRetrieveString won't return anything to
        show for the task, but the Action.__call__ won't call
        CacheRetrieveFunc; instead it just returns zero, which makes
        the code below think that the file *was* successfully
        retrieved from the cache, therefore it doesn't do any
        subsequent building.  However, the CacheRetrieveString didn't
        print anything because it didn't actually exist in the cache,
        and no more build actions will be performed, so the user just
        sees nothing.  The fix is to tell Action.__call__ to always
        execute the CacheRetrieveFunc and then have the latter
        explicitly check SCons.Action.execute_actions itself.
        """
        if not self.is_enabled():
            return False
        env = node.get_build_env()
        if cache_show:
            if CacheRetrieveSilent(node, [], env, execute=1) == 0:
                node.build(presub=0, execute=0)
                return True
        elif CacheRetrieve(node, [], env, execute=1) == 0:
            return True
        return False

    def push(self, node):
        if self.is_readonly() or not self.is_enabled():
            return
        return CachePush(node, [], node.get_build_env())

    def push_if_forced(self, node):
        if cache_force:
            return self.push(node)