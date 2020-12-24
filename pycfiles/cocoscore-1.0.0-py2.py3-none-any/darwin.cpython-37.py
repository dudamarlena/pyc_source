# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\cocos\audio\SDL\darwin.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 5265 bytes
__doc__ = 'Darwin (OS X) support.\n\nAppropriated from pygame.macosx\n'
from __future__ import division, print_function, unicode_literals
import six
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
import os, sys
from Foundation import *
from AppKit import *
import objc, MacOS, cocos.audio.SDL.dll, cocos.audio.SDL.events
SDL = cocos.audio.SDL
__all__ = [
 'init']

def setupAppleMenu(app):
    appleMenuController = NSAppleMenuController.alloc().init()
    appleMenuController.retain()
    appleMenu = NSMenu.alloc().initWithTitle_('')
    appleMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('', None, '')
    appleMenuItem.setSubmenu_(appleMenu)
    app.mainMenu().addItem_(appleMenuItem)
    appleMenuController.controlMenu_(appleMenu)
    app.mainMenu().removeItem_(appleMenuItem)


def setupWindowMenu(app):
    windowMenu = NSMenu.alloc().initWithTitle_('Window')
    windowMenu.retain()
    menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Minimize', 'performMiniaturize:', 'm')
    windowMenu.addItem_(menuItem)
    windowMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Window', None, '')
    windowMenuItem.setSubmenu_(windowMenu)
    app.mainMenu().addItem_(windowMenuItem)
    app.setWindowsMenu_(windowMenu)


class SDLAppDelegate(NSObject):

    def applicationShouldTerminate_(self, app):
        event = SDL.events.SDL_Event()
        event.type = SDL_QUIT
        SDL.events.SDL_PushEvent(event)
        return NSTerminateLater

    def windowUpdateNotification_(self, notification):
        win = notification.object()
        if not SDL.dll.version_compatible((1, 2, 8)):
            if isinstance(win, objc.lookUpClass('SDL_QuartzWindow')):
                win.retain()
        NSNotificationCenter.defaultCenter().removeObserver_name_object_(self, NSWindowDidUpdateNotification, None)
        self.release()


def setIcon(app, icon_data):
    data = NSData.dataWithBytes_length_(icon_data, len(icon_data))
    if data is None:
        return
    img = NSImage.alloc().initWithData_(data)
    if img is None:
        return
    app.setApplicationIconImage_(img)


def install():
    app = NSApplication.sharedApplication()
    appDelegate = SDLAppDelegate.alloc().init()
    app.setDelegate_(appDelegate)
    appDelegate.retain()
    NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(appDelegate, 'windowUpdateNotification:', NSWindowDidUpdateNotification, None)
    if not app.mainMenu():
        mainMenu = NSMenu.alloc().init()
        app.setMainMenu_(mainMenu)
        setupAppleMenu(app)
        setupWindowMenu(app)
    app.finishLaunching()
    app.updateWindows()
    app.activateIgnoringOtherApps_(True)


def S(*args):
    return ''.join(args)


OSErr = objc._C_SHT
OUTPSN = 'o^{ProcessSerialNumber=LL}'
INPSN = 'n^{ProcessSerialNumber=LL}'
FUNCTIONS = [
 (
  'GetCurrentProcess', S(OSErr, OUTPSN)),
 (
  'SetFrontProcess', S(OSErr, INPSN)),
 (
  'CPSSetProcessName', S(OSErr, INPSN, objc._C_CHARPTR)),
 (
  'CPSEnableForegroundOperation', S(OSErr, INPSN))]

def WMEnable(name=None):
    if name is None:
        name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    else:
        if isinstance(name, six.unicode):
            name = name.encode('utf-8')
        return hasattr(objc, 'loadBundleFunctions') or False
    bndl = NSBundle.bundleWithPath_(objc.pathForFramework('/System/Library/Frameworks/ApplicationServices.framework'))
    if bndl is None:
        print('ApplicationServices missing', file=(sys.stderr))
        return False
    d = {}
    app = NSApplication.sharedApplication()
    objc.loadBundleFunctions(bndl, d, FUNCTIONS)
    for fn, sig in FUNCTIONS:
        if fn not in d:
            print('Missing', fn, file=(sys.stderr))
            return False

    err, psn = d['GetCurrentProcess']()
    if err:
        print('GetCurrentProcess', (err, psn), file=(sys.stderr))
        return False
    err = d['CPSSetProcessName'](psn, name)
    if err:
        print('CPSSetProcessName', (err, psn), file=(sys.stderr))
        return False
    err = d['CPSEnableForegroundOperation'](psn)
    if err:
        print('CPSEnableForegroundOperation', (err, psn))
        return False
    err = d['SetFrontProcess'](psn)
    if err:
        print('SetFrontProcess', (err, psn))
        return False
    return True


def init():
    if not MacOS.WMAvailable():
        if not WMEnable():
            raise ImportError('Can not access the window manager.  Use py2app or execute with the pythonw script.')
    else:
        if not NSApp():
            install()
        if os.getcwd() == '/' and len(sys.argv) > 1:
            os.chdir(os.path.dirname(sys.argv[0]))
    return True