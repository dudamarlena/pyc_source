# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/editor/management/commands/bookexport.py
# Compiled at: 2012-02-14 23:34:00
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from booki.editor import common, models
import shutil

class Command(BaseCommand):
    help = 'Export book content as ZIP file. For now, only content of one book version will be exported and you will not get your history data.'
    args = '<book name>'
    option_list = BaseCommand.option_list + (
     make_option('--book-version', action='store', dest='book_version', default=None, help='Book version, e.g.'),
     make_option('--output', action='store', dest='output_name', default=None, help='Output filename or -- for STDOUT, e.g. my_book.zip.'))
    requires_model_validation = False

    def handle(self, *args, **options):
        from booki.editor.views import getVersion
        if len(args) == 0:
            raise CommandError('You must specify book name!')
        try:
            book = models.Book.objects.get(url_title__iexact=args[0])
        except models.Book.DoesNotExist:
            raise CommandError('Book "%s" does not exist.' % args[0])

        try:
            book_version = getVersion(book, options['book_version'])
        except models.BookVersion.DoesNotExist:
            raise CommandError('Book version %s does not exist.' % options['book_version'])

        fileName = common.exportBook(book_version)
        exportFileName = None
        if options['output_name']:
            if options['output_name'] == '--':
                print open(fileName, 'rb').read(),
                import os
                os.unlink(fileName)
                return
            exportFileName = options['output_name']
        else:
            exportFileName = 'export-%s.zip' % book.url_title
        shutil.move(fileName, exportFileName)
        if options['verbosity'] in ('1', '2'):
            print 'Book successfully exported into "%s" file.' % exportFileName
        return