# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/formatter/entity_string.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 5211 bytes
from abc import ABC, abstractmethod
from itertools import chain
from typing import List, Sequence, Union, Optional, Dict, Any, TypeVar, Type, Generic, Iterable
from attr import dataclass
import attr
from .formatted_string import FormattedString, EntityType

class AbstractEntity(ABC):

    def __init__(self, type: EntityType, offset: int, length: int, extra_info: Dict[(str, Any)]) -> None:
        pass

    @abstractmethod
    def copy(self) -> 'AbstractEntity':
        pass

    @abstractmethod
    def adjust_offset(self, offset: int, max_length: int=-1) -> Optional['AbstractEntity']:
        pass


class SemiAbstractEntity(AbstractEntity, ABC):
    offset: int
    length: int

    def adjust_offset(self, offset: int, max_length: int=-1) -> Optional['SemiAbstractEntity']:
        entity = self.copy()
        entity.offset += offset
        if entity.offset < 0:
            entity.length += entity.offset
            entity.offset = 0
        else:
            if entity.offset > max_length > -1:
                return
        if entity.offset + entity.length > max_length > -1:
            entity.length = max_length - entity.offset
        return entity


@dataclass
class SimpleEntity(SemiAbstractEntity):
    type: EntityType
    offset: int
    length: int
    extra_info = attr.ib(factory=dict)
    extra_info: Dict[(str, Any)]

    def copy(self) -> 'SimpleEntity':
        return attr.evolve(self)


TEntity = TypeVar('TEntity', bound=AbstractEntity)
TEntityType = TypeVar('TEntityType')

class EntityString(Generic[(TEntity, TEntityType)], FormattedString):
    text: str
    _entities: List[TEntity]
    entity_class = SimpleEntity
    entity_class: Type[AbstractEntity]

    def __init__(self, text: str='', entities: List[TEntity]=None) -> None:
        self.text = text
        self._entities = entities or []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text='{self.text}', entities={self.entities})"

    def __str__(self) -> str:
        return self.text

    @property
    def entities(self) -> List[TEntity]:
        return self._entities

    @entities.setter
    def entities(self, val: Iterable[TEntity]) -> None:
        self._entities = [entity for entity in val if entity is not None]

    def _offset_entities(self, offset: int) -> 'EntityString':
        self.entities = (entity.adjust_offset(offset, len(self.text)) for entity in self.entities)
        return self

    def append(self, *args: Union[(str, 'FormattedString')]) -> 'EntityString':
        for msg in args:
            if isinstance(msg, EntityString):
                self.entities += (entity.adjust_offset(len(self.text)) for entity in msg.entities)
                self.text += msg.text
            else:
                self.text += str(msg)

        return self

    def prepend(self, *args: Union[(str, 'FormattedString')]) -> 'EntityString':
        for msg in args:
            if isinstance(msg, EntityString):
                self.text = msg.text + self.text
                self.entities = chain(msg.entities, (entity.adjust_offset(len(msg.text)) for entity in self.entities))
            else:
                text = str(msg)
                self.text = text + self.text
                self.entities = (entity.adjust_offset(len(text)) for entity in self.entities)

        return self

    def format(self, entity_type: TEntityType, offset: int=None, length: int=None, **kwargs) -> 'EntityString':
        self.entities.append(self.entity_class(type=entity_type, offset=(offset or 0), length=(length or len(self.text)),
          extra_info=kwargs))
        return self

    def trim(self) -> 'EntityString':
        orig_len = len(self.text)
        self.text = self.text.lstrip()
        diff = orig_len - len(self.text)
        self.text = self.text.rstrip()
        self._offset_entities(-diff)
        return self

    def split(self, separator, max_items: int=-1) -> List['EntityString']:
        text_parts = self.text.split(separator, max_items - 1)
        output = []
        offset = 0
        for part in text_parts:
            msg = type(self)(part)
            msg.entities = (entity.adjust_offset(-offset, len(part)) for entity in self.entities)
            output.append(msg)
            offset += len(part)
            offset += len(separator)

        return output

    @classmethod
    def join(cls, items: Sequence[Union[(str, 'EntityString')]], separator: str=' ') -> 'EntityString':
        main = cls()
        for msg in items:
            if not isinstance(msg, EntityString):
                msg = cls(text=(str(msg)))
            main.entities += [entity.adjust_offset(len(main.text)) for entity in msg.entities]
            main.text += msg.text + separator

        if len(separator) > 0:
            main.text = main.text[:-len(separator)]
        return main