# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/formatter/markdown_string.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2573 bytes
from typing import List, Sequence, Union
from .formatted_string import FormattedString, EntityType

class MarkdownString(FormattedString):
    text: str

    def __init__(self, text: str='') -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text

    def append(self, *args: Union[(str, 'FormattedString')]) -> 'MarkdownString':
        self.text += ''.join(str(arg) for arg in args)
        return self

    def prepend(self, *args: Union[(str, 'FormattedString')]) -> 'MarkdownString':
        self.text = ''.join(str(arg) for arg in args + (self.text,))
        return self

    def format(self, entity_type: EntityType, **kwargs) -> 'MarkdownString':
        if entity_type == EntityType.BOLD:
            self.text = f"**{self.text}**"
        else:
            if entity_type == EntityType.ITALIC:
                self.text = f"_{self.text}_"
            else:
                if entity_type == EntityType.STRIKETHROUGH:
                    self.text = f"~~{self.text}~~"
                else:
                    if entity_type == EntityType.UNDERLINE:
                        self.text = self.text
                    else:
                        if entity_type == EntityType.URL:
                            if kwargs['url'] != self.text:
                                self.text = f"[{self.text}]({kwargs['url']})"
                        else:
                            if entity_type == EntityType.EMAIL:
                                self.text = self.text
                            else:
                                if entity_type == EntityType.PREFORMATTED:
                                    self.text = f"```{kwargs['language']}\n{self.text}\n```"
                                else:
                                    if entity_type == EntityType.INLINE_CODE:
                                        self.text = f"`{self.text}`"
                                    else:
                                        if entity_type == EntityType.BLOCKQUOTE:
                                            children = self.trim().split('\n')
                                            children = [child.prepend('> ') for child in children]
                                            self.text = self.join(children, '\n').text
                                        else:
                                            if entity_type == EntityType.HEADER:
                                                prefix = '#' * kwargs['size']
                                                self.text = f"{prefix} {self.text}"
        return self

    def trim(self) -> 'MarkdownString':
        self.text = self.text.strip()
        return self

    def split(self, separator, max_items: int=-1) -> List['MarkdownString']:
        return [MarkdownString(text) for text in self.text.split(separator, max_items)]

    @classmethod
    def join(cls, items: Sequence[Union[(str, 'FormattedString')]], separator: str=' ') -> 'MarkdownString':
        return cls(separator.join(str(item) for item in items))