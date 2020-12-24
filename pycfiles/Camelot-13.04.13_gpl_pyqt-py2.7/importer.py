# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/importer.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.action import Action
from camelot.core.utils import ugettext_lazy as _
from camelot.view.art import Icon

class ImportCovers(Action):
    verbose_name = _('Import cover images')
    icon = Icon('tango/22x22/mimetypes/image-x-generic.png')

    def model_run(self, model_context):
        from camelot.view.action_steps import SelectFile, UpdateProgress, Refresh, FlushSession
        select_image_files = SelectFile('Image Files (*.png *.jpg);;All Files (*)')
        select_image_files.single = False
        file_names = yield select_image_files
        file_count = len(file_names)
        import os
        from sqlalchemy import orm
        from camelot.core.orm import Session
        from camelot_example.model import Movie
        movie_mapper = orm.class_mapper(Movie)
        cover_property = movie_mapper.get_property('cover')
        storage = cover_property.columns[0].type.storage
        session = Session()
        for i, file_name in enumerate(file_names):
            yield UpdateProgress(i, file_count)
            title = os.path.splitext(os.path.basename(file_name))[0]
            stored_file = storage.checkin(unicode(file_name))
            movie = Movie(title=unicode(title))
            movie.cover = stored_file

        yield FlushSession(session)
        yield Refresh()