# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ssiyad/PyProjects/automagic-file-mover/venv/lib/python3.8/site-packages/moover/__main__.py
# Compiled at: 2020-01-04 07:42:29
# Size of source mod 2**32: 3984 bytes
import json, os, shutil, time
from pynotifier import Notification
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from moover import SOURCE, DESTINATION, LOGGER, EXISTING
with open(os.path.join(os.path.dirname(__file__), 'extensions.py'), 'r') as (f):
    ext = json.load(f)

def moover_notif(desc):
    Notification(title='Moover',
      description=desc,
      duration=10).send()


def move_file(file_path):
    extension = os.path.splitext(file_path)[(-1)]
    dir_name = extension.upper()[1:]
    if dir_name in ext:
        full_path = os.path.join(DESTINATION, ext[dir_name])
        if not _DirFunctions(full_path).check_dir():
            _DirFunctions(full_path).make_dir()
        dir_name = os.path.join(full_path, dir_name)
    ext_sub_dir = os.path.join(DESTINATION, dir_name)
    if not _DirFunctions(ext_sub_dir).check_dir():
        _DirFunctions(ext_sub_dir).make_dir()
        msg_notify = 'Created new category: {}'.format(dir_name)
        LOGGER.info(msg_notify)
        moover_notif(msg_notify)
    try:
        shutil.move(file_path, ext_sub_dir)
        msg_notify = 'Moved~ {} to {}'.format(file_path, ext_sub_dir)
        LOGGER.info(msg_notify)
        moover_notif(msg_notify)
    except shutil.Error:
        LOGGER.warning('File {} already exists!'.format(file_path))


def move_dir(file_path):
    try:
        shutil.move(file_path, DESTINATION)
        msg_notify = 'Moved Dir~ {} to {}'.format(file_path, DESTINATION)
        LOGGER.info(msg_notify)
        moover_notif(msg_notify)
    except shutil.Error:
        LOGGER.warning('Dir {} already exists!'.format(file_path))


class _FileCreatedPrint(FileSystemEventHandler):

    def on_created(self, event):
        file_path = event.src_path
        if os.path.isdir(file_path):
            LOGGER.info('Directory created: {}'.format(file_path))
            move_dir(file_path)
        else:
            if os.path.dirname(file_path) == SOURCE:
                LOGGER.info('File created: {}'.format(file_path))
                move_file(file_path)


class _DirFunctions(object):

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def check_dir(self):
        if os.path.exists(self.dir_path):
            return True
        return False

    def make_dir(self):
        try:
            os.mkdir(self.dir_path)
        except Exception:
            raise Exception


def main():
    if not _DirFunctions(SOURCE).check_dir():
        _DirFunctions(SOURCE).make_dir()
        LOGGER.info('CREATED SOURCE DIRECTORY: {}'.format(SOURCE))
    else:
        if not _DirFunctions(DESTINATION).check_dir():
            _DirFunctions(DESTINATION).make_dir()
            LOGGER.info('CREATED DESTINATION DIRECTORY: {}'.format(DESTINATION))
        LOGGER.info('Moover started in {} -> {}'.format(SOURCE, DESTINATION))
        if EXISTING:
            existing_files = [os.path.join(SOURCE, name) for name in os.listdir(SOURCE) if not os.path.isdir(os.path.join(SOURCE, name))]
            if len(existing_files) > 0:
                LOGGER.info('Moving existing files~')
                for file in existing_files:
                    move_file(file)
                else:
                    LOGGER.info('Finished moving existing files')

        list_dir = [name for name in os.listdir(DESTINATION) if os.path.isdir(os.path.join(DESTINATION, name))]
        if len(list_dir) < 1:
            sub_dirs = 'No Sub-Directories are present in {}'.format(DESTINATION)
        else:
            sub_dirs = 'Sub-Directories present in {}: {}'.format(DESTINATION, ' | '.join([name for name in list_dir]))
    LOGGER.info(sub_dirs)
    event_handler = _FileCreatedPrint()
    observer = Observer()
    observer.schedule(event_handler, SOURCE, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    else:
        observer.join()


if __name__ == '__main__':
    main()