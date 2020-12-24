# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/text.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 3846 bytes
import collections, wtforms, markdown
from lxml.html.clean import Cleaner
from mediagoblin import mg_globals
from mediagoblin.tools import url
HTML_CLEANER = Cleaner(scripts=True, javascript=True, comments=True, style=True, links=True, page_structure=True, processing_instructions=True, embedded=True, frames=True, forms=True, annoying_tags=True, allow_tags=[
 'div', 'b', 'i', 'em', 'strong', 'p', 'ul', 'ol', 'li', 'a', 'br',
 'pre', 'code'], remove_unknown_tags=False, safe_attrs_only=True, add_nofollow=True, host_whitelist=(), whitelist_tags=set([]))

def clean_html(html):
    if not html:
        return ''
    return HTML_CLEANER.clean_html(html)


def convert_to_tag_list_of_dicts(tag_string):
    """
    Filter input from incoming string containing user tags,

    Strips trailing, leading, and internal whitespace, and also converts
    the "tags" text into an array of tags
    """
    slug_to_name = collections.OrderedDict()
    if tag_string:
        stripped_tag_string = ' '.join(tag_string.strip().split())
        for tag in stripped_tag_string.split(','):
            tag = tag.strip()
            if tag:
                slug_to_name[url.slugify(tag)] = tag
                continue

    return [{'name': v,  'slug': k} for k, v in slug_to_name.items()]


def media_tags_as_string(media_entry_tags):
    """
    Generate a string from a media item's tags, stored as a list of dicts

    This is the opposite of convert_to_tag_list_of_dicts
    """
    tags_string = ''
    if media_entry_tags:
        tags_string = ', '.join([tag['name'] for tag in media_entry_tags])
    return tags_string


TOO_LONG_TAG_WARNING = 'Tags must be shorter than %s characters.  Tags that are too long: %s'

def tag_length_validator(form, field):
    """
    Make sure tags do not exceed the maximum tag length.
    """
    tags = convert_to_tag_list_of_dicts(field.data)
    too_long_tags = [tag['name'] for tag in tags if len(tag['name']) > mg_globals.app_config['tags_max_length']]
    if too_long_tags:
        raise wtforms.ValidationError(TOO_LONG_TAG_WARNING % (mg_globals.app_config['tags_max_length'],
         ', '.join(too_long_tags)))


UNSAFE_MARKDOWN_INSTANCE = markdown.Markdown()

def cleaned_markdown_conversion(text):
    """
    Take a block of text, run it through MarkDown, and clean its HTML.
    """
    if not text:
        return ''
    return clean_html(UNSAFE_MARKDOWN_INSTANCE.convert(text))