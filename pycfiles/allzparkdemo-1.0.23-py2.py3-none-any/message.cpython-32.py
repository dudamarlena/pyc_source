# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/internationalization/meta/message.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Mar 5, 2012\n\n@package: internationalization\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the SQL alchemy meta for message API.\n'
from ..api.message import Message
from .metadata_internationalization import meta
from .source import Source
from ally.support.sqlalchemy.mapper import mapperModel, addLoadListener, addInsertListener, addUpdateListener
from sqlalchemy.dialects.mysql.base import INTEGER, VARCHAR
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.types import String
from ally.exception import InputError, Ref
table = Table('inter_message', meta, Column('id', INTEGER(unsigned=True), primary_key=True, key='Id'), Column('fk_source_id', ForeignKey(Source.Id, ondelete='RESTRICT'), key='Source'), Column('singular', VARCHAR(255, charset='utf8'), nullable=False, key='Singular'), Column('plural_1', VARCHAR(255, charset='utf8'), key='plural1'), Column('plural_2', VARCHAR(255, charset='utf8'), key='plural2'), Column('plural_3', VARCHAR(255, charset='utf8'), key='plural3'), Column('plural_4', VARCHAR(255, charset='utf8'), key='plural4'), Column('context', VARCHAR(255, charset='utf8'), key='Context'), Column('line_number', INTEGER(unsigned=True), key='LineNumber'), Column('comments', String(255), key='Comments'), mysql_engine='InnoDB')
Message = mapperModel(Message, table)

def _onLoadMessage(message):
    """
    Called when a message is loaded.
    """
    assert isinstance(message, Message), 'Invalid message %s' % message
    plurals = [plural for plural in (getattr(message, 'plural%s' % k) for k in range(1, 5)) if plural is not None]
    if plurals:
        message.Plural = plurals


def _onPersistMessage(message):
    """
    Called when a message is persisted.
    """
    assert isinstance(message, Message), 'Invalid message %s' % message
    if message.Plural:
        if len(message.Plural) > 4:
            raise InputError(Ref(_('Only a maximum of four plural forms is accepted, got %(nplurals)i') % dict(nplurals=len(message.Plural))))
        for k, plural in enumerate(message.Plural, 1):
            setattr(message, 'plural%s' % k, plural)


addLoadListener(Message, _onLoadMessage)
addInsertListener(Message, _onPersistMessage)
addUpdateListener(Message, _onPersistMessage)