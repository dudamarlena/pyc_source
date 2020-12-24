# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jake/CRAPtion/craption/cli.py
# Compiled at: 2018-05-18 03:14:50
from craption import settings, upload, utils
import opster, os, shutil

@opster.command()
def main(clear_conf=(
 'c', False, 'Rewrite example config'), dropbox_login=(
 'd', False, 'Login to dropbox')):
    if dropbox_login:
        settings.dropbox_login()
        return
    if clear_conf:
        utils.install()
        return
    local_image = utils.screenshot()
    if not os.path.exists(local_image):
        raise AssertionError
        filename = utils.get_filename()
        url = upload.upload(local_image, filename)
        print url
        utils.set_clipboard(url)
        conf = settings.get_conf()
        if conf.get('file').as_bool('keep'):
            dest_dir = os.path.expanduser(conf['file']['dir'])
            os.path.exists(dest_dir) or os.mkdir(dest_dir)
        dest = os.path.join(dest_dir, filename)
        shutil.move(local_image, dest)
    else:
        os.unlink(local_image)


def dispatch():
    main.command()


if __name__ == '__main__':
    dispatch()