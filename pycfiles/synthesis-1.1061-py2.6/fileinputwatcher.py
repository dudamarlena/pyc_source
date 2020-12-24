# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/fileinputwatcher.py
# Compiled at: 2011-01-03 14:39:55
"""
This module watches multiple directories for new files and notifies when a new file encountered.  It has POSIX and win32 versions.  The POSIX version uses a queue to run the watch as a thread and make a non-polling notification.
"""
import os, time, exceptions
from time import sleep
from conf import settings
if os.name == 'nt':
    osiswin32 = True
    try:
        import win32file, win32event, win32con
    except ImportError:
        print 'Could not import win32 modules.'

else:
    osiswin32 = False
    try:
        import pyinotify
        from pyinotify import WatchManager, ThreadedNotifier, ProcessEvent, EventsCodes
    except ImportError:
        print 'Could not import POSIX pyinotify modules.'

    class FileInputWatcher:
        """controlling class for file monitoring"""

        def __init__(self, dir_to_watch, queue):
            print 'FileInputWatcher Initialized'
            if settings.DEBUG:
                print '*************Debugging On*************'
            self.queue = queue
            self.dir_to_watch = dir_to_watch
            self.notifier1 = None
            self.notifier2 = None
            return

        def monitor(self):
            """The command to start monitoring a directory or set of them."""
            global osiswin32
            print 'Monitoring Directories: %s' % self.dir_to_watch
            print 'Watching started at %s' % time.asctime()
            if osiswin32:
                print 'Watching win32 OS'
                return self.watch_win32(self.dir_to_watch)
            print 'Watching POSIX OS'
            self.watch_posix_start()
            return True

        def stop_monitoring(self):
            """os independent method to stop monitoring, but only posix uses it."""
            if isinstance(self.notifier1, ThreadedNotifier):
                if isinstance(self.notifier2, ThreadedNotifier):
                    self.watch_posix_stop()
            elif settings.DEBUG:
                print 'notifiers were not instantiated, so not calling self.watch_posix_stop() again'
            print 'Done Monitoring'

        def watch_win32(self, dir_to_watch):
            """os-specific watch command"""
            files_added = []
            old_path_contents = []
            new_path_contents = []
            cnt = 0
            try:
                while 1:
                    cnt += 1
                    for item in dir_to_watch:
                        change_handle = win32file.FindFirstChangeNotification(item, 0, win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
                        old_path_contents.append(os.listdir(item))

                    result = win32event.WaitForSingleObject(change_handle, 500)
                    if result == win32con.WAIT_OBJECT_0:
                        for item in dir_to_watch:
                            new_path_contents.append(os.listdir(item))

                        files_added = [ f for f in new_path_contents if f not in old_path_contents ]
                        if files_added:
                            print
                            print time.asctime()
                            print 'Added:', files_added or 'Nothing'
                            return files_added
                    win32file.FindNextChangeNotification(change_handle)

            except KeyboardInterrupt:
                return []

        def watch_posix_start(self):
            """os-specific command to watch"""
            if self.notifier1 == None and self.notifier2 == None:
                try:
                    pyinotify.compatibility_mode()
                    print 'pyinotify running in compatibility mode'
                except:
                    print 'pyinotify running in standard mode'
                else:
                    try:
                        mask = pyinotify.ALL_EVENTS
                        watch_manager1 = WatchManager()
                        self.notifier1 = ThreadedNotifier(watch_manager1, EventHandler(self.queue))
                        self.notifier1.start()
                        print 'Starting the threaded notifier on ', self.dir_to_watch
                        watch_manager1.add_watch(self.dir_to_watch, mask)
                        watch_manager2 = WatchManager()
                        self.notifier2 = ThreadedNotifier(watch_manager2, EventHandlerDummy(self.queue))
                        self.notifier2.start()
                        watch_manager2.add_watch(settings.BASE_PATH, mask)
                        if settings.DEBUG:
                            print 'both notifiers started'
                    except KeyboardInterrupt:
                        print 'Keyboard Interrupt in notifier'
                        self.notifier1.stop()
                        self.notifier2.stop()
                        return
                    except NameError:
                        self.notifier1.stop()
                        self.notifier2.stop()
                        return ['POSIX Watch Error']
                    except:
                        print 'General exception caught within notifier while loop, stopping both notifiers now'
                        self.notifier1.stop()
                        self.notifier2.stop()
                        self.notifier1.VERBOSE = settings.DEBUG
                        print 'returning to calling function'
                        return True

            return

        def watch_posix_stop(self):
            """os specific call to stop monitoring"""
            print 'Stopping the threaded notifiers.'
            self.notifier1.stop()
            print 'stopped self.notifier1.stop()'
            self.notifier2.stop()
            print 'stopped self.notifier2.stop()'


    class EventHandler(ProcessEvent):
        """Event handler processing create events passed in to the     watch manager by the notifier."""

        def __init__(self, queue):
            self.queue = queue

        def process_IN_CREATE(self, event):
            """What happens when a file is added"""
            if event.name[0] == '.':
                print 'ignoring ', event.name
            else:
                print 'Create: %s' % os.path.join(event.path, event.name)
                self.queue.put(os.path.join(event.path, event.name))

        def process_IN_MOVED_TO(self, event):
            """What happens when a file is added"""
            if event.name[0] == '.':
                print 'ignoring ', event.name
            else:
                print 'In_Moved_To: %s' % os.path.join(event.path, event.name)
                self.queue.put(os.path.join(event.path, event.name))
                print 'queue is now', self.queue


    class EventHandlerDummy(ProcessEvent):
        """Event handler processing create events passed in to the     watch manager by the notifier."""

        def __init__(self, queue):
            self.queue = queue

        def process_IN_CREATE(self, event):
            """What happens when a file is added"""
            print 'Create: %s' % os.path.join(event.path, event.name)