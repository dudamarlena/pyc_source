# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/microformats2/discovery.py
# Compiled at: 2018-04-03 13:26:10
from enum import Enum
from urllib.parse import urlparse
import re

def is_url(value):
    if type(value) == dict:
        value = value.get('properties', {}).get('url', [''])[0]
    try:
        parsed = urlparse(value)
        if len(parsed.scheme) == 0:
            return False
        if len(parsed.netloc) == 0:
            return False
        return True
    except:
        return False


class PostTypes(Enum):
    event = 'event'
    rsvp = 'rsvp'
    repost = 'repost'
    like = 'like'
    reply = 'reply'
    video = 'video'
    photo = 'photo'
    note = 'note'
    article = 'article'
    bookmark = 'bookmark'
    review = 'review'
    recipe = 'recipe'
    resume = 'resume'


def safe_get(l, index):
    try:
        return l[index]
    except IndexError:
        return

    return


def get_post_type(mf2, extended=False):
    content = None
    props = mf2.get('properties', {})
    if safe_get(mf2.get('type', ['']), 0) == 'h-event':
        return PostTypes.event
    else:
        if safe_get(props.get('rsvp', ['']), 0) in ('yes', 'no', 'maybe', 'interested'):
            return PostTypes.rsvp
        if is_url(safe_get(props.get('repost-of', ['']), 0)):
            return PostTypes.repost
        if is_url(safe_get(props.get('like-of', ['']), 0)):
            return PostTypes.like
        if extended and is_url(safe_get(props.get('bookmark-of', ['']), 0)):
            return PostTypes.bookmark
        if is_url(safe_get(props.get('in-reply-to', ['']), 0)):
            return PostTypes.reply
        if is_url(safe_get(props.get('video', ['']), 0)):
            return PostTypes.video
        if is_url(safe_get(props.get('photo', ['']), 0)):
            return PostTypes.photo
        if len(props.get('content', [])):
            for prop in props['content']:
                if isinstance(prop, dict):
                    if len(prop.get('value', '')):
                        content = prop['value']
                        break
                    elif len(prop.get('html', '')):
                        content = prop['html']
                        break
                    if isinstance(prop, str) and len(prop):
                        content = prop
                        break

        if content is None and len(props.get('summary', [])):
            for summary in prop['summary']:
                if len(summary):
                    content = summary
                    break

        if content is None:
            return PostTypes.note
        if not props.get('name') or props.get('name', [''])[0] == '':
            return PostTypes.note
        for name in props['name']:
            if len(name):
                name = name.strip()
                exp = re.compile('\\W+')
                name = exp.sub(' ', name)
                content = content.strip()
                content = exp.sub(' ', content)
                if not content.startswith(name):
                    return PostTypes.article
                return PostTypes.note

        return PostTypes.note