# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/playlist/templatetags/playlist_template_tags.py
# Compiled at: 2011-01-05 07:46:00
from django import template
from playlist.models import ScheduledPlaylist
register = template.Library()

@register.tag
def get_current_playlist_entry(parser, token):
    try:
        (tag_name, for_arg, obj, as_arg, as_varname) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('get_current_playlist_entry tag requires 2 arguments (obj, as_varname), %s given' % (len(token.split_contents()) - 1))

    return GetCurrentPlaylistEntryNode(obj, as_varname)


class GetCurrentPlaylistEntryNode(template.Node):

    def __init__(self, obj, as_varname):
        self.obj = template.Variable(obj)
        self.as_varname = as_varname

    def render(self, context):
        obj = self.obj.resolve(context)
        context[self.as_varname] = ScheduledPlaylist.get_current_playlist_entry_for(obj)
        return ''


@register.tag
def get_next_playlist_entry(parser, token):
    try:
        (tag_name, for_arg, obj, as_arg, as_varname) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('get_next_playlist_entry tag requires 2 arguments (obj, as_varname), %s given' % (len(token.split_contents()) - 1))

    return GetNextPlaylistEntryNode(obj, as_varname)


class GetNextPlaylistEntryNode(template.Node):

    def __init__(self, obj, as_varname):
        self.obj = template.Variable(obj)
        self.as_varname = as_varname

    def render(self, context):
        obj = self.obj.resolve(context)
        context[self.as_varname] = ScheduledPlaylist.get_next_playlist_entry_for(obj)
        return ''