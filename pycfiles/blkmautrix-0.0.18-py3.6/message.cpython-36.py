# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/event/message.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 13499 bytes
from typing import Optional, Union, Pattern
from html import escape
import re
from attr import dataclass
import attr
from .....api import JSON
from ..util import SerializableEnum, SerializableAttrs, Serializable, Obj, deserializer
from ..primitive import ContentURI, EventID
from .base import BaseRoomEvent, BaseUnsigned

class Format(SerializableEnum):
    __doc__ = 'A message format. Currently only ``org.matrix.custom.html`` is available.\n    This will probably be deprecated when extensible events are implemented.'
    HTML = 'org.matrix.custom.html'


TEXT_MESSAGE_TYPES = ('m.text', 'm.emote', 'm.notice')
MEDIA_MESSAGE_TYPES = ('m.image', 'm.sticker', 'm.video', 'm.audio', 'm.file')

class MessageType(SerializableEnum):
    __doc__ = 'A message type.'
    TEXT = 'm.text'
    EMOTE = 'm.emote'
    NOTICE = 'm.notice'
    IMAGE = 'm.image'
    STICKER = 'm.sticker'
    VIDEO = 'm.video'
    AUDIO = 'm.audio'
    FILE = 'm.file'
    LOCATION = 'm.location'

    @property
    def is_text(self) -> bool:
        return self.value in TEXT_MESSAGE_TYPES

    @property
    def is_media(self) -> bool:
        return self.value in MEDIA_MESSAGE_TYPES


class InReplyTo:

    def __init__(self, event_id: Optional[EventID]=None, proxy_target: Optional['RelatesTo']=None) -> None:
        self._event_id = event_id
        self._proxy_target = proxy_target

    @property
    def event_id(self) -> EventID:
        if self._proxy_target:
            return self._proxy_target.event_id
        else:
            return self._event_id

    @event_id.setter
    def event_id(self, event_id: EventID) -> None:
        if self._proxy_target:
            self._proxy_target.rel_type = RelationType.REFERENCE
            self._proxy_target.event_id = event_id
        else:
            self._event_id = event_id


class RelationType(SerializableEnum):
    ANNOTATION = 'm.annotation'
    REFERENCE = 'm.reference'
    REPLACE = 'm.replace'


@dataclass
class RelatesTo(Serializable):
    __doc__ = 'Message relations. Used for reactions, edits and replies.'
    rel_type: RelationType = None
    event_id = None
    event_id: Optional[EventID]
    key = None
    key: Optional[str]

    @classmethod
    def deserialize(cls, data: JSON) -> Optional['RelatesTo']:
        if not data:
            return
        try:
            return cls(rel_type=(RelationType.deserialize(data['rel_type'])), event_id=(data.get('event_id', None)),
              key=(data.get('key', None)))
        except KeyError:
            pass

        try:
            return cls(rel_type=(RelationType.REFERENCE), event_id=(data['m.in_reply_to']['event_id']))
        except KeyError:
            pass

    def serialize(self) -> JSON:
        data = {'rel_type': self.rel_type.serialize()}
        if self.rel_type == RelationType.REFERENCE:
            data['m.in_reply_to'] = {'event_id': self.event_id}
        if self.event_id:
            data['event_id'] = self.event_id
        if self.key:
            data['key'] = self.key
        return data


class BaseMessageEventContentFuncs:
    __doc__ = 'Base class for the contents of all message-type events (currently m.room.message and\n    m.sticker). Contains relation helpers.'
    body: str
    _relates_to: Optional[RelatesTo]

    def set_reply(self, reply_to: Union[(EventID, 'MessageEvent')], **kwargs) -> None:
        self.relates_to.rel_type = RelationType.REFERENCE
        self.relates_to.event_id = reply_to if isinstance(reply_to, str) else reply_to.event_id

    def set_edit(self, edits: Union[(EventID, 'MessageEvent')]) -> None:
        self.relates_to.rel_type = RelationType.REPLACE
        self.relates_to.event_id = edits if isinstance(edits, str) else edits.event_id

    def serialize(self) -> JSON:
        data = SerializableAttrs.serialize(self)
        evt = self.get_edit()
        if evt:
            new_content = {**data}
            del new_content['m.relates_to']
            data['m.new_content'] = new_content
            if 'body' in data:
                data['body'] = f"* {data['body']}"
            if 'formatted_body' in data:
                data['formatted_body'] = f"* {data['formatted_body']}"
        return data

    @property
    def relates_to(self) -> RelatesTo:
        if self._relates_to is None:
            self._relates_to = RelatesTo()
        return self._relates_to

    @relates_to.setter
    def relates_to(self, relates_to: RelatesTo) -> None:
        self._relates_to = relates_to

    def get_reply_to(self) -> Optional[EventID]:
        if self._relates_to:
            if self._relates_to.rel_type == RelationType.REFERENCE:
                return self._relates_to.event_id

    def get_edit(self) -> Optional[EventID]:
        if self._relates_to:
            if self._relates_to.rel_type == RelationType.REPLACE:
                return self._relates_to.event_id

    def trim_reply_fallback(self) -> None:
        pass


@dataclass
class BaseMessageEventContent(BaseMessageEventContentFuncs):
    __doc__ = 'Base event content for all m.room.message-type events.'
    msgtype: MessageType = None
    body: str = ''
    external_url: str = None
    _relates_to = attr.ib(default=None, metadata={'json': 'm.relates_to'})
    _relates_to: Optional[RelatesTo]


@dataclass
class BaseFileInfo(SerializableAttrs['BaseFileInfo']):
    mimetype: str = None
    size: int = None


@dataclass
class ThumbnailInfo(BaseFileInfo, SerializableAttrs['ThumbnailInfo']):
    __doc__ = 'Information about the thumbnail for a document, video, image or location.'
    height: int = attr.ib(default=None, metadata={'json': 'h'})
    width: int = attr.ib(default=None, metadata={'json': 'w'})
    orientation: int = None


@dataclass
class FileInfo(BaseFileInfo, SerializableAttrs['FileInfo']):
    __doc__ = 'Information about a document message.'
    thumbnail_info: ThumbnailInfo = None
    thumbnail_url: ContentURI = None


@dataclass
class ImageInfo(FileInfo, SerializableAttrs['ImageInfo']):
    __doc__ = 'Information about an image message.'
    height: int = attr.ib(default=None, metadata={'json': 'h'})
    width: int = attr.ib(default=None, metadata={'json': 'w'})
    orientation: int = None


@dataclass
class VideoInfo(ImageInfo, SerializableAttrs['VideoInfo']):
    __doc__ = 'Information about a video message.'
    duration: int = None
    orientation: int = None


@dataclass
class AudioInfo(BaseFileInfo, SerializableAttrs['AudioInfo']):
    __doc__ = 'Information about an audio message.'
    duration: int = None


MediaInfo = Union[(ImageInfo, VideoInfo, AudioInfo, FileInfo, Obj)]

@dataclass
class LocationInfo(SerializableAttrs['LocationInfo']):
    __doc__ = 'Information about a location message.'
    thumbnail_url: ContentURI = None
    thumbnail_info: ThumbnailInfo = None


@dataclass
class MediaMessageEventContent(BaseMessageEventContent, SerializableAttrs['MediaMessageEventContent']):
    __doc__ = 'The content of a media message event (m.image, m.audio, m.video, m.file)'
    url: ContentURI = None
    info = None
    info: Optional[MediaInfo]

    @staticmethod
    @deserializer(MediaInfo)
    def deserialize_info(data: JSON) -> MediaInfo:
        if not isinstance(data, dict):
            return Obj()
        else:
            msgtype = data.pop('__mautrix_msgtype', None)
            if msgtype == 'm.image' or msgtype == 'm.sticker':
                return ImageInfo.deserialize(data)
            if msgtype == 'm.video':
                return VideoInfo.deserialize(data)
            if msgtype == 'm.audio':
                return AudioInfo.deserialize(data)
            if msgtype == 'm.file':
                return FileInfo.deserialize(data)
            return Obj(**data)


@dataclass
class LocationMessageEventContent(BaseMessageEventContent, SerializableAttrs['LocationMessageEventContent']):
    geo_uri: str = None
    info: LocationInfo = None


html_reply_fallback_regex: Pattern = re.compile('^<mx-reply>[\\s\\S]+?</mx-reply>')

@dataclass
class TextMessageEventContent(BaseMessageEventContent, SerializableAttrs['TextMessageEventContent']):
    __doc__ = 'The content of a text message event (m.text, m.notice, m.emote)'
    format: Format = None
    formatted_body: str = None

    def set_reply(self, reply_to, *, displayname=None):
        super().set_reply(reply_to)
        if isinstance(reply_to, str):
            return
        if not self.formatted_body or len(self.formatted_body) == 0 or self.format != Format.HTML:
            self.format = Format.HTML
            self.formatted_body = escape(self.body)
        self.formatted_body = reply_to.make_reply_fallback_html(displayname) + self.formatted_body
        self.body = reply_to.make_reply_fallback_text(displayname) + self.body

    def trim_reply_fallback(self) -> None:
        if self.get_reply_to():
            self._trim_reply_fallback_text()
            self._trim_reply_fallback_html()

    def _trim_reply_fallback_text(self) -> None:
        if not self.body.startswith('> ') or '\n' not in self.body:
            return
        lines = self.body.split('\n')
        while len(lines) > 0 and lines[0].startswith('> '):
            lines.pop(0)

        lines.pop(0)
        self.body = '\n'.join(lines)

    def _trim_reply_fallback_html(self) -> None:
        if self.formatted_body:
            if self.format == Format.HTML:
                self.formatted_body = html_reply_fallback_regex.sub('', self.formatted_body)


MessageEventContent = Union[(TextMessageEventContent, MediaMessageEventContent,
 LocationMessageEventContent, Obj)]

@dataclass
class MessageUnsigned(BaseUnsigned, SerializableAttrs['MessageUnsigned']):
    __doc__ = 'Unsigned information sent with message events.'
    transaction_id: str = None


html_reply_fallback_format = "<mx-reply><blockquote><a href='https://matrix.to/#/{room_id}/{event_id}'>In reply to</a> <a href='https://matrix.to/#/{sender}'>{displayname}</a><br/>{content}</blockquote></mx-reply>"
media_reply_fallback_body_map = {MessageType.IMAGE: 'an image', 
 MessageType.STICKER: 'a sticker', 
 MessageType.AUDIO: 'audio', 
 MessageType.VIDEO: 'a video', 
 MessageType.FILE: 'a file', 
 MessageType.LOCATION: 'a location'}

@dataclass
class MessageEvent(BaseRoomEvent, SerializableAttrs['MessageEvent']):
    __doc__ = 'An m.room.message event'
    content: MessageEventContent
    unsigned = None
    unsigned: Optional[MessageUnsigned]

    @staticmethod
    @deserializer(MessageEventContent)
    def deserialize_content(data: JSON) -> MessageEventContent:
        if not isinstance(data, dict):
            return Obj()
        else:
            rel = data.get('m.relates_to', None) or {}
            if rel.get('rel_type', None) == RelationType.REPLACE.value:
                data = data.get('m.new_content', data)
                data['m.relates_to'] = rel
            msgtype = data.get('msgtype', None)
            if msgtype in TEXT_MESSAGE_TYPES:
                return TextMessageEventContent.deserialize(data)
            if msgtype in MEDIA_MESSAGE_TYPES:
                data.get('info', {})['__mautrix_msgtype'] = msgtype
                return MediaMessageEventContent.deserialize(data)
            if msgtype == 'm.location':
                return LocationMessageEventContent.deserialize(data)
            return Obj(**data)

    def make_reply_fallback_html(self, displayname: Optional[str]=None) -> str:
        """Generate the HTML fallback for messages replying to this event."""
        if self.content.msgtype.is_text:
            body = self.content.formatted_body or escape(self.content.body)
        else:
            sent_type = media_reply_fallback_body_map[self.content.msgtype] or 'a message'
            body = f"sent {sent_type}"
        displayname = escape(displayname) if displayname else self.sender
        return html_reply_fallback_format.format(room_id=(self.room_id), event_id=(self.event_id), sender=(self.sender),
          displayname=displayname,
          content=body)

    def make_reply_fallback_text(self, displayname: Optional[str]=None) -> str:
        """Generate the plaintext fallback for messages replying to this event."""
        if self.content.msgtype.is_text:
            body = self.content.body
        else:
            try:
                body = media_reply_fallback_body_map[self.content.msgtype]
            except KeyError:
                body = 'an unknown message type'

        lines = body.strip().split('\n')
        first_line, lines = lines[0], lines[1:]
        fallback_text = f"> <{displayname or self.sender}> {first_line}"
        for line in lines:
            fallback_text += f"\n> {line}"

        fallback_text += '\n\n'
        return fallback_text