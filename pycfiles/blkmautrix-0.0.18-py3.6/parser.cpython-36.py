# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/formatter/parser.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 8867 bytes
from typing import List, Tuple, Pattern, Type, Optional, TypeVar, Generic, Callable
import re
from ...types import UserID, RoomAlias
from .formatted_string import FormattedString, EntityType
from .markdown_string import MarkdownString
from .html_reader import HTMLNode, read_html

class RecursionContext:
    strip_linebreaks: bool
    ul_depth: int
    _inited: bool

    def __init__(self, strip_linebreaks: bool=True, ul_depth: int=0):
        self.strip_linebreaks = strip_linebreaks
        self.ul_depth = ul_depth
        self._inited = True

    def __setattr__(self, key, value):
        if getattr(self, '_inited', False) is True:
            raise TypeError("'RecursionContext' object is immutable")
        super(RecursionContext, self).__setattr__(key, value)

    def enter_list(self) -> 'RecursionContext':
        return RecursionContext(strip_linebreaks=(self.strip_linebreaks), ul_depth=(self.ul_depth + 1))

    def enter_code_block(self) -> 'RecursionContext':
        return RecursionContext(strip_linebreaks=False, ul_depth=(self.ul_depth))


T = TypeVar('T', bound=FormattedString)

class MatrixParser(Generic[T]):
    mention_regex: Pattern = re.compile('https://matrix.to/#/(@.+:.+)')
    room_regex: Pattern = re.compile('https://matrix.to/#/(#.+:.+)')
    block_tags = ('p', 'pre', 'blockquote', 'ol', 'ul', 'li', 'h1', 'h2', 'h3', 'h4',
                  'h5', 'h6', 'div', 'hr', 'table')
    block_tags: Tuple[(str, ...)]
    list_bullets = ('●', '○', '■', '‣')
    list_bullets: Tuple[(str, ...)]
    e = EntityType
    e: Type[EntityType]
    fs = MarkdownString
    fs: Type[T]
    read_html = read_html
    read_html: Callable[([str], HTMLNode)]

    @classmethod
    def list_bullet(cls, depth: int) -> str:
        return cls.list_bullets[((depth - 1) % len(cls.list_bullets))] + ' '

    @classmethod
    def list_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        ordered = node.tag == 'ol'
        tagged_children = cls.node_to_tagged_fstrings(node, ctx)
        counter = 1
        indent_length = 0
        if ordered:
            try:
                counter = int(node.attrib.get('start', '1'))
            except ValueError:
                counter = 1

            longest_index = counter - 1 + len(tagged_children)
            indent_length = len(str(longest_index))
        indent = (indent_length + 4) * ' '
        children = []
        for child, tag in tagged_children:
            if tag != 'li':
                pass
            else:
                if ordered:
                    prefix = f"{counter}. "
                    counter += 1
                else:
                    prefix = cls.list_bullet(ctx.ul_depth)
                child = child.prepend(prefix)
                parts = child.split('\n')
                parts = parts[:1] + [part.prepend(indent) for part in parts[1:]]
                child = cls.fs.join(parts, '\n')
                children.append(child)

        return cls.fs.join(children, '\n')

    @classmethod
    def blockquote_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        msg = cls.tag_aware_parse_node(node, ctx)
        return msg.format(cls.e.BLOCKQUOTE)

    @classmethod
    def header_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        children = cls.node_to_fstrings(node, ctx)
        length = int(node.tag[1])
        return cls.fs.join(children, '').format((cls.e.HEADER), size=length)

    @classmethod
    def basic_format_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        msg = cls.tag_aware_parse_node(node, ctx)
        if node.tag in ('b', 'strong'):
            msg = msg.format(cls.e.BOLD)
        else:
            if node.tag in ('i', 'em'):
                msg = msg.format(cls.e.ITALIC)
            else:
                if node.tag in ('s', 'strike', 'del'):
                    msg = msg.format(cls.e.STRIKETHROUGH)
                else:
                    if node.tag in ('u', 'ins'):
                        msg = msg.format(cls.e.UNDERLINE)
        return msg

    @classmethod
    def link_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        msg = cls.tag_aware_parse_node(node, ctx)
        href = node.attrib.get('href', '')
        if not href:
            return msg
        else:
            if href.startswith('mailto:'):
                return cls.fs(href[len('mailto:'):]).format(cls.e.EMAIL)
            else:
                mention = cls.mention_regex.match(href)
                if mention:
                    new_msg = cls.user_pill_to_fstring(msg, UserID(mention.group(1)))
                    if new_msg:
                        return new_msg
                room = cls.room_regex.match(href)
                if room:
                    new_msg = cls.room_pill_to_fstring(msg, RoomAlias(room.group(1)))
                    if new_msg:
                        return new_msg
            return cls.url_to_fstring(msg, href)

    @classmethod
    def url_to_fstring(cls, msg: T, url: str) -> Optional[T]:
        return msg.format((cls.e.URL), url=url)

    @classmethod
    def user_pill_to_fstring(cls, msg: T, user_id: UserID) -> Optional[T]:
        return msg.format((cls.e.USER_MENTION), user_id=user_id)

    @classmethod
    def room_pill_to_fstring(cls, msg: T, room_alias: RoomAlias) -> Optional[T]:
        return msg.format((cls.e.ROOM_MENTION), room_alias=room_alias)

    @classmethod
    def custom_node_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> Optional[T]:
        pass

    @classmethod
    def node_to_fstring(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        custom = cls.custom_node_to_fstring(node, ctx)
        if custom:
            return custom
        if node.tag == 'mx-reply':
            return cls.fs('')
        if node.tag == 'blockquote':
            return cls.blockquote_to_fstring(node, ctx)
        if node.tag == 'ol':
            return cls.list_to_fstring(node, ctx)
        if node.tag == 'ul':
            return cls.list_to_fstring(node, ctx.enter_list())
        if node.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            return cls.header_to_fstring(node, ctx)
        if node.tag == 'br':
            return cls.fs('\n')
        if node.tag in ('b', 'strong', 'i', 'em', 's', 'del', 'u', 'ins'):
            return cls.basic_format_to_fstring(node, ctx)
        if node.tag == 'a':
            return cls.link_to_fstring(node, ctx)
        if node.tag == 'p':
            return cls.tag_aware_parse_node(node, ctx).append('\n')
        if node.tag == 'pre':
            lang = ''
            try:
                if node[0].tag == 'code':
                    node = node[0]
                    lang = node.attrib['class'][len('language-'):]
            except (IndexError, KeyError):
                pass

            return cls.parse_node(node, ctx.enter_code_block()).format((cls.e.PREFORMATTED), language=lang)
        else:
            if node.tag == 'code':
                return cls.parse_node(node, ctx.enter_code_block()).format(cls.e.INLINE_CODE)
            return cls.tag_aware_parse_node(node, ctx)

    @classmethod
    def text_to_fstring(cls, text: str, ctx: RecursionContext) -> T:
        if ctx.strip_linebreaks:
            text = text.replace('\n', '')
        return cls.fs(text)

    @classmethod
    def node_to_tagged_fstrings(cls, node: HTMLNode, ctx: RecursionContext) -> List[Tuple[(T, str)]]:
        output = []
        if node.text:
            output.append((cls.text_to_fstring(node.text, ctx), 'text'))
        for child in node:
            output.append((cls.node_to_fstring(child, ctx), child.tag))
            if child.tail:
                output.append((cls.text_to_fstring(child.tail, ctx), 'text'))

        return output

    @classmethod
    def node_to_fstrings(cls, node: HTMLNode, ctx: RecursionContext) -> List[T]:
        return [msg for msg, tag in cls.node_to_tagged_fstrings(node, ctx)]

    @classmethod
    def tag_aware_parse_node(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        msgs = cls.node_to_tagged_fstrings(node, ctx)
        output = cls.fs()
        prev_was_block = False
        for msg, tag in msgs:
            if tag in cls.block_tags:
                msg = msg.append('\n')
                if not prev_was_block:
                    msg = msg.prepend('\n')
                prev_was_block = True
            output = output.append(msg)

        return output.trim()

    @classmethod
    def parse_node(cls, node: HTMLNode, ctx: RecursionContext) -> T:
        return cls.fs.join(cls.node_to_fstrings(node, ctx))

    @classmethod
    def parse(cls, data: str) -> T:
        msg = cls.node_to_fstring(cls.read_html(f"<body>{data}</body>"), RecursionContext())
        return msg