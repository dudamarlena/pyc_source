# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./gthnk/adaptors/librarian.py
# Compiled at: 2017-11-21 20:58:03
# Size of source mod 2**32: 4413 bytes
import datetime, os, shutil, hashlib, gthnk.adaptors.journal_buffer
from gthnk.models import Day, Page

def overwrite_if_different(filename, new_content):
    if os.path.isfile(filename):
        with open(filename, 'r') as (f):
            existing_checksum = hashlib.md5(f.read()).hexdigest()
        generated_checksum = hashlib.md5(new_content).hexdigest()
        if generated_checksum == existing_checksum:
            return False
    with open(filename, 'w') as (f):
        f.write(new_content)
    return True


class Librarian(object):

    def __init__(self, app):
        self.app = app

    def rotate_buffers(self):
        self.app.logger.info('processing list: {}'.format(self.app.config['INPUT_FILES']))
        file_list = gthnk.adaptors.journal_buffer.split_filename_list(self.app.config['INPUT_FILES'])
        todays_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H%M%S')
        backup_path = os.path.join(self.app.config['BACKUP_PATH'], todays_date)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        for filename in file_list:
            self.app.logger.info('begin: {}'.format(filename))
            shutil.copy2(filename, backup_path)
            journal_buffer = gthnk.adaptors.journal_buffer.TextFileJournalBuffer()
            journal_buffer.process_one(filename)
            journal_buffer.save_entries()
            with open(filename, 'w'):
                pass
            self.app.logger.info('finish: {}'.format(filename))

    def export_journal(self):
        app = self.app
        app.logger.info('start')
        if not os.path.exists(app.config['EXPORT_PATH']):
            os.makedirs(app.config['EXPORT_PATH'])
            os.makedirs(os.path.join(app.config['EXPORT_PATH'], 'day'))
            os.makedirs(os.path.join(app.config['EXPORT_PATH'], 'text'))
            os.makedirs(os.path.join(app.config['EXPORT_PATH'], 'markdown'))
            os.makedirs(os.path.join(app.config['EXPORT_PATH'], 'attachment'))
            os.makedirs(os.path.join(app.config['EXPORT_PATH'], 'thumbnail'))
            os.makedirs(os.path.join(app.config['EXPORT_PATH'], 'preview'))
        for day in Day.query.order_by(Day.date).all():
            app.logger.info(day)
            output_filename = os.path.join(app.config['EXPORT_PATH'], 'text', '{0}.txt'.format(day.date))
            if not overwrite_if_different(output_filename, day.render()):
                app.logger.info('skipping; generated file identical to existing export')
            output_filename = os.path.join(app.config['EXPORT_PATH'], 'markdown', '{0}.md'.format(day.date))
            if not overwrite_if_different(output_filename, day.render_markdown()):
                app.logger.info('skipping; generated file identical to existing export')

        for page in Page.query.order_by(Page.id).all():
            app.logger.info(page)
            output_filename = os.path.join(app.config['EXPORT_PATH'], 'attachment', page.filename())
            if not overwrite_if_different(output_filename, page.binary):
                app.logger.info('skipping; generated file identical to existing export')
            else:
                output_filename = os.path.join(app.config['EXPORT_PATH'], 'thumbnail', page.filename(extension='jpg'))
                overwrite_if_different(output_filename, page.thumbnail)
                output_filename = os.path.join(app.config['EXPORT_PATH'], 'preview', page.filename(extension='jpg'))
                overwrite_if_different(output_filename, page.preview)

        app.logger.info('finish')