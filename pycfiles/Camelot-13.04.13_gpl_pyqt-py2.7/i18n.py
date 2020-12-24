# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/model/i18n.py
# Compiled at: 2013-04-11 17:47:52
"""Set of classes to store internationalization data in the database.  Camelot
applications can be translated by the developer using regular PO files, or by
the user.  In case the user makes a translation, this translation is stored into
the `Translation` table.  This table can be exported to PO files for inclusion
in the development cycle.
"""
from camelot.core.orm import Entity, Session
from camelot.core.utils import ugettext_lazy as _
from camelot.admin.action import Action
from camelot.admin.entity_admin import EntityAdmin
from camelot.view.art import Icon
from camelot.view.utils import default_language
import camelot.types
from sqlalchemy import sql
from sqlalchemy.schema import Column
from sqlalchemy.types import Unicode, INT
import logging
logger = logging.getLogger('camelot.model.i18n')

class ExportAsPO(Action):
    verbose_name = _('PO Export')
    icon = Icon('tango/16x16/actions/document-save.png')

    def model_run(self, model_context):
        from camelot.view.action_steps import SelectFile
        select_file = SelectFile()
        select_file.existing = False
        filenames = yield select_file
        for filename in filenames:
            file = open(filename, 'w')
            for translation in model_context.get_collection():
                file.write(('msgid  "%s"\n' % translation.source).encode('utf-8'))
                file.write(('msgstr "%s"\n\n' % translation.value).encode('utf-8'))


class Translation(Entity):
    """Table to store user generated translations or customization.
    """
    __tablename__ = 'translation'
    language = Column(camelot.types.Language, index=True, nullable=False)
    source = Column(Unicode(500), index=True, nullable=False)
    value = Column(Unicode(500), index=True)
    cid = Column(INT(), default=0, index=True)
    uid = Column(INT(), default=0, index=True)
    _cache = dict()

    class Admin(EntityAdmin):
        verbose_name_plural = _('Translations')
        form_size = (700, 150)
        list_display = ['source', 'language', 'value', 'uid']
        list_filter = ['language']
        list_actions = [ExportAsPO()]
        field_attributes = {'language': {'default': default_language}}

    @classmethod
    def translate(cls, source, language):
        """Translate source to language, return None if no translation is found"""
        if source:
            key = (
             source, language)
            if key in cls._cache:
                return cls._cache[key]
            query = Session().query(cls)
            query = query.filter(sql.and_(cls.source == unicode(source), cls.language == language, cls.uid != 0))
            translation = query.first()
            if translation:
                cls._cache[key] = translation.value
                return translation.value
            return None
        return ''

    @classmethod
    def translate_or_register(cls, source, language):
        """Translate source to language, if no translation is found, register the
        source as to be translated and return the source"""
        if source:
            source = unicode(source)
            translation = cls.translate(source, language)
            if not translation:
                session = Session()
                query = session.query(cls)
                translation = query.filter_by(source=source, language=language).first()
                if not translation:
                    if (
                     source, language) not in cls._cache:
                        registered_translation = Translation(source=source, language=language)
                        cls._cache[(source, language)] = source
                        session.flush([registered_translation])
                        logger.debug('registed %s with id %s' % (source, registered_translation.id))
                return source
            return translation
        return ''