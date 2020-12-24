# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ooyala/templatetags/ooyala_tags.py
# Compiled at: 2011-08-18 05:15:41
from django import template
from ooyala.models import UrlVideoLink, OoyalaItem, OoyalaChannelList
from ooyala.library import OoyalaThumbnail
from ooyala.conf import RENDER_SIZES, NO_THUMB
register = template.Library()

@register.simple_tag
def ooyala_video(for_url, width=RENDER_SIZES['regular'][0], height=RENDER_SIZES['regular'][1]):
    try:
        video = UrlVideoLink.objects.get(url=for_url)
    except UrlVideoLink.DoesNotExist:
        return ''

    return '\n        <div class="ooyala-video">\n            <script src="http://www.ooyala.com/player.js?wmode=transparent&width=%d&height=%d&embedCode=%s"></script>\n        </div>\n    ' % (width, height, video.item.embed_code)


@register.simple_tag
def ooyala_for_object(video_object, width=RENDER_SIZES['large'][0], height=RENDER_SIZES['large'][1]):
    try:
        return '\n           <script src="http://www.ooyala.com/player.js?wmode=transparent&width=%d&height=%d&wmode=transparent&embedCode=%s"></script>\n        ' % (width, height, video_object.embed_code)
    except AttributeError:
        return ''


@register.inclusion_tag('ooyala/tags/channel_list.html')
def ooyala_channel_list(limit=None):
    channels = OoyalaItem.objects.all().filter(content_type='channel')
    if limit:
        channels = channels[:limit]
    return {'channels': channels}


@register.inclusion_tag('ooyala/tags/facebook_headers.html')
def ooyala_facebook_headers(video_object):
    return {'video': video_object}


@register.inclusion_tag('ooyala/tags/thumbnail_list.html')
def ooyala_recent_items(limit=5):
    """ Returns recently viewed items
        TODO: actually implement that, for now random poll
    """
    return {'items': OoyalaItem.objects.all().order_by('?')[:limit]}


@register.inclusion_tag('ooyala/tags/thumbnail_list.html')
def ooyala_channel_more(video):
    """ Returns more OoyalaItems which are in the same channel
    as our current video. Takes the first channel it finds for now.
    If we get a channel as an item then return all its videos. """
    if video.content_type == 'Channel':
        try:
            channel = OoyalaChannelList.objects.get(channel=video)
            similiar_list = channel.videos.all()
        except OoyalaChannelList.DoesNotExist:
            similiar_list = None

    else:
        try:
            channel = OoyalaChannelList.objects.filter(videos=video)[0]
            similiar_list = channel.videos.all().exclude(pk=video.pk)
        except IndexError:
            similiar_list = (None, )

    return {'items': similiar_list}


@register.simple_tag
def ooyala_thubmnail(embed_code, resolution='320x240', indicies='0-25', cache=True):
    """ Grab one of the custom thumbnail images - ooyala may return bigger
    images than requested at a higher compression rate so they should be also
    force-sized in your CSS. Indicies will return a number of thumbs, ones
    in the middle tend to be "better" suited to display """
    thumb = None
    try:
        if cache:
            video = OoyalaItem.objects.get(embed_code=embed_code)
            thumb = video.thumbnail
        if not thumb:
            thumbs = OoyalaThumbnail(embed_code=embed_code, resolution=resolution, indicies=indicies).process()
            thumbs_data = thumbs.getElementsByTagName('thumbnail')
            idx = len(thumbs_data) / 2
            thumb = thumbs_data[idx].firstChild.nodeValue
        if cache:
            video.thumbnail = thumb
            video.save()
        return thumb
    except (IndexError, AttributeError):
        return NO_THUMB

    return