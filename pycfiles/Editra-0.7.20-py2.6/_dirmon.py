# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/_dirmon.py
# Compiled at: 2012-12-22 13:45:16
"""
Editra Business Model Library: DirectoryMonitor

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__cvsid__ = '$Id: _dirmon.py 73166 2012-12-12 04:31:53Z CJP $'
__revision__ = '$Revision: 73166 $'
__all__ = [
 'DirectoryMonitor']
import wx, os, time, threading, fileutil

class DirectoryMonitor(object):
    """Object to manage monitoring file system changes"""

    def __init__(self, checkFreq=1000.0):
        """@keyword checkFreq: check frequency in milliseconds"""
        super(DirectoryMonitor, self).__init__()
        self._watcher = WatcherThread(self._ThreadNotifier, checkFreq=checkFreq)
        self._callbacks = list()
        self._cbackLock = threading.Lock()
        self._running = False

    def __del__(self):
        if self._running:
            self._watcher.Shutdown()
            self._watcher.join()

    def _ThreadNotifier(self, added, deleted, modified):
        """Notifier callback from background L{WatcherThread}
        to call notifiers on main thread.
        @note: this method is invoked from a background thread and
               is not safe to make direct UI calls from.

        """
        with self._cbackLock:
            for cback in self._callbacks:
                wx.CallAfter(cback, added, deleted, modified)

    Monitoring = property(lambda self: self._running)
    Frequency = property(lambda self: self._watcher.GetFrequency(), lambda self, freq: self._watcher.SetFrequency(freq))

    def AddDirectory(self, dname):
        """Add a directory to the monitor
        @param dname: directory path
        @return: bool - True if added, False if failed to add

        """
        return self._watcher.AddWatchDirectory(dname)

    def SubscribeCallback(self, callback):
        """Subscribe a callback method to be called when changes are
        detected in one of the watched directories.
        @param callback: callable([added,], [deleted,], [modified,])

        """
        with self._cbackLock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)

    def UnsubscribeCallback(self, callback):
        """Remove a callback method from the monitor"""
        with self._cbackLock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def RemoveDirectory(self, dname):
        """Remove a directory from the watch list
        @param dname: directory path

        """
        self._watcher.RemoveWatchDirectory(dname)

    def StartMonitoring(self):
        """Start monitoring the directories in the watch list and
        notifying target of changes.

        """
        self._running = True
        self._watcher.start()

    def Suspend(self, pause=True):
        """Suspend background processing
        @keyword pause: True (suspend) False (resume)

        """
        if pause:
            self._watcher.Suspend()
        else:
            self._watcher.Continue()

    def Refresh(self, paths=None):
        """Force a recheck of the monitored directories. This method
        is useful for doing manual control of the refresh cycle. It is
        ignored and does nothing when WatcherThread is set up for automatic
        refresh cycles.
        @keyword paths: specific paths to refresh or None for all.

        """
        self._watcher.Refresh(paths)


class WatcherThread(threading.Thread):
    """Background thread to monitor a directory"""

    def __init__(self, notifier, checkFreq=1000.0):
        """Create the WatcherThread. Provide a callback notifier method
        that will be called when changes are detected in the directory.
        The notifier will be called in the context of this thread. Notifier
        will be called with three lists of ebmlib.File objects to indicate
        the changes that have occurred.
        @param notifier: callable([added,], [deleted,], [modified,])
        @keyword checkFreq: check frequency in milliseconds. If value is set
                            to zero or less update checks must be manually
                            controlled via the Refresh interface.

        """
        super(WatcherThread, self).__init__()
        assert callable(notifier)
        self._notifier = notifier
        self._dirs = list()
        self._refreshDirs = None
        self._freq = checkFreq
        self._continue = True
        self._changePending = False
        self._lock = threading.Lock()
        self._suspend = False
        self._suspendcond = threading.Condition()
        self._listEmptyCond = threading.Condition()
        self._refreshCond = threading.Condition()
        return

    def run(self):
        """Run the watcher"""
        while self._continue:
            deleted = list()
            added = list()
            modified = list()
            if not self._dirs:
                with self._listEmptyCond:
                    self._listEmptyCond.wait()
            if self._suspend:
                with self._suspendcond:
                    self._suspendcond.wait()
            with self._lock:
                for dobj in self._PendingRefresh:
                    if not self._continue:
                        return
                    if self._changePending:
                        break
                    if not os.path.exists(dobj.Path):
                        deleted.append(dobj)
                        self._dirs.remove(dobj)
                        continue
                    snapshot = fileutil.GetDirectoryObject(dobj.Path, False, True)
                    dobjFiles = dobj.Files
                    dobjIndex = dobjFiles.index
                    snapFiles = snapshot.Files
                    for tobj in dobjFiles:
                        if not self._continue:
                            pass
                        else:
                            return
                            if self._changePending:
                                break
                            if tobj not in snapFiles:
                                deleted.append(tobj)
                                dobjFiles.remove(tobj)

                    for tobj in snapFiles:
                        if not self._continue:
                            pass
                        else:
                            return
                            if self._changePending:
                                break
                            if tobj not in dobjFiles:
                                added.append(tobj)
                                dobjFiles.append(tobj)
                            else:
                                idx = dobjIndex(tobj)
                                existing = dobjFiles[idx]
                                if existing.ModTime < tobj.ModTime:
                                    modified.append(tobj)
                                    existing.ModTime = tobj.ModTime

            if any((added, deleted, modified)):
                self._notifier(added, deleted, modified)
            if self._freq > 0:
                time.sleep(self._freq / 1000.0)
            else:
                with self._refreshCond:
                    self._refreshDirs = None
                    self._refreshCond.wait()

        return

    @property
    def _PendingRefresh(self):
        """Get the list of directories pending refresh"""
        if self._refreshDirs is None:
            return self._dirs
        else:
            return self._refreshDirs
            return

    def AddWatchDirectory(self, dpath):
        """Add a directory to the watch list
        @param dpath: directory path (unicode)
        @return: bool - True means watch was added, False means unable to list directory

        """
        assert os.path.isdir(dpath)
        dobj = fileutil.Directory(dpath)
        self._changePending = True
        with self._lock:
            if dobj not in self._dirs and os.access(dobj.Path, os.R_OK):
                try:
                    dobj = fileutil.GetDirectoryObject(dpath, False, True)
                except OSError:
                    self._changePending = False
                    return False
                else:
                    self._dirs.append(dobj)
                    with self._listEmptyCond:
                        self._listEmptyCond.notify()
        self._changePending = False
        return True

    def RemoveWatchDirectory(self, dpath):
        """Remove a directory from the watch
        @param dpath: directory path to remove (unicode)

        """
        dobj = fileutil.Directory(dpath)
        self._changePending = True
        with self._lock:
            if dobj in self._dirs:
                self._dirs.remove(dobj)
            toremove = list()
            for d in self._dirs:
                if fileutil.IsSubPath(d.Path, dpath):
                    toremove.append(d)

            for todel in toremove:
                self._dirs.remove(todel)

        self._changePending = False

    def GetFrequency(self):
        """Get the update frequency
        @return: int (milliseconds)

        """
        return self._freq

    def SetFrequency(self, milli):
        """Set the update frequency
        @param milli: int (milliseconds)

        """
        self._freq = float(milli)

    def Refresh(self, paths=None):
        """Recheck the monitored directories
        only useful when manually controlling refresh cycle of the monitor.
        @keyword paths: if None refresh all, else list of specific directories

        """
        with self._refreshCond:
            if paths is not None:
                self._refreshDirs = list()
                for dobj in paths:
                    self._refreshDirs.append(dobj)

            self._refreshCond.notify()
        return

    def Shutdown(self):
        """Shut the thread down"""
        self._continue = False

    def Suspend(self):
        """Suspend the thread"""
        self._suspend = True

    def Continue(self):
        """Continue the thread"""
        self._suspend = False
        with self._suspendcond:
            self._suspendcond.notify()