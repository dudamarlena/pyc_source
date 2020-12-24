# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/notification.py
# Compiled at: 2016-06-22 17:23:26
"""
linux和OSX下的系统通知
"""
import platform, subprocess, tempfile, os, logging, urllib
logger = logging.getLogger('doubanfm.notification')
PLATFORM = platform.system()

def send_notification(title='Douban.fm', content='', cover_file=None):
    u"""发送桌面通知"""
    if PLATFORM == 'Linux':
        send_Linux_notify(title, content, cover_file)
    elif PLATFORM == 'Darwin':
        send_OS_X_notify(title, content, cover_file)


def send_Linux_notify(title, content, img_path):
    u"""发送Linux桌面通知"""
    command = [
     'notify-send',
     '-a', 'Douban.fm',
     '-t', '5000',
     '--hint=int:transient:1']
    if img_path is not None:
        command.extend(['-i', img_path])
    subprocess.call(command + [title, content])
    return


def send_OS_X_notify(title, content, img_path):
    u"""发送Mac桌面通知"""
    try:
        from Foundation import NSDate, NSUserNotification, NSUserNotificationCenter
        from AppKit import NSImage
        import objc
    except ImportError:
        logger.info('failed to init OSX notify!')
        return

    def swizzle(cls, SEL, func):
        old_IMP = getattr(cls, SEL, None)
        if old_IMP is None:
            old_IMP = cls.instanceMethodForSelector_(SEL)

        def wrapper(self, *args, **kwargs):
            return func(self, old_IMP, *args, **kwargs)

        new_IMP = objc.selector(wrapper, selector=old_IMP.selector, signature=old_IMP.signature)
        objc.classAddMethod(cls, SEL.encode(), new_IMP)
        return

    def swizzled_bundleIdentifier(self, original):
        return 'com.apple.itunes'

    swizzle(objc.lookUpClass('NSBundle'), 'bundleIdentifier', swizzled_bundleIdentifier)
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(content)
    notification.setInformativeText_('')
    notification.setUserInfo_({})
    if img_path is not None:
        image = NSImage.alloc().initWithContentsOfFile_(img_path)
        notification.set_identityImage_(image)
    notification.setDeliveryDate_(NSDate.dateWithTimeInterval_sinceDate_(0, NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    logger.info('send notify success!')
    return


class Notify(object):

    def __init__(self):
        self._tempdir = tempfile.mkdtemp()
        self.cover_file = None
        self.has_cover = False
        self.title = None
        return

    def get_pic(self, playingsong, tempfile_path):
        u"""获取专辑封面"""
        url = playingsong['picture'].replace('\\', '')
        for _ in range(3):
            try:
                urllib.urlretrieve(url, tempfile_path)
                logger.debug('Get cover art success!')
                return True
            except (IOError, urllib.ContentTooShortError):
                pass

        logger.error('Get cover art failed!')
        return False

    def init_notification(self, playingsong):
        u"""第一次桌面通知时加入图片"""
        logger.debug('init_notification')
        old_title = playingsong['title']
        self.cover_file = tempfile.NamedTemporaryFile(suffix='.jpg', dir=self._tempdir)
        if not self.get_pic(playingsong, self.cover_file.name):
            return
        title = playingsong['title']
        if old_title != title:
            return
        self.has_cover = True
        content = playingsong['artist'] + ' - ' + playingsong['albumtitle']
        send_notification(title.decode('utf-8'), content.decode('utf-8'), self.cover_file.name)

    def send_notify(self, playingsong, content=''):
        u"""需要解码一下,通知需要unicode编码"""
        title = playingsong['title'].decode('utf-8')
        content = content.decode('utf-8')
        if title == self.title:
            if self.has_cover:
                send_notification(self.title, content, self.cover_file.name)
            else:
                send_notification(self.title, content)
        else:
            self.init_notification(playingsong)
            self.title = title

    def __del__(self):
        try:
            if self.cover_file is not None:
                self.cover_file.close()
            os.rmdir(self._tempdir)
            logger.info('Temporary files removed.')
        except OSError:
            pass

        return


def main():
    send_notification(title='Test title', content='test content')


if __name__ == '__main__':
    main()