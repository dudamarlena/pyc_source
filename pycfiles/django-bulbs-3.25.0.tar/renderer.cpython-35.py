# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/instant_articles/renderer.py
# Compiled at: 2016-09-28 18:54:18
# Size of source mod 2**32: 5093 bytes
import re
from django.template import loader
from bs4 import BeautifulSoup

class BaseRenderer:

    def generate_body(self, intermediate):
        body = []
        for item in intermediate:
            for key, values in item.items():
                body.append(self.render_item(key, values).strip())

        return '\n'.join(body)

    def render_item(self, key, body):
        if key == 'text':
            return body['raw']
        if key == 'betty':
            return self.render(self.BETTY_TEMPLATE, body)
        if key == 'facebook':
            return self.render(self.FACEBOOK_TEMPLATE, body)
        if key == 'imgur':
            return self.render(self.IMGUR_TEMPLATE, body)
        if key == 'instagram':
            return self.render(self.INSTAGRAM_TEMPLATE, body)
        if key == 'onion_video':
            return self.render(self.ONION_VIDEO_TEMPLATE, body)
        if key == 'soundcloud':
            return self.render(self.SOUNDCLOUD_TEMPLATE, body)
        if key == 'twitter':
            return self.render(self.TWITTER_TEMPLATE, body)
        if key == 'vimeo':
            return self.render(self.VIMEO_TEMPLATE, body)
        if key == 'youtube':
            return self.render(self.YOUTUBE_TEMPLATE, body)
        raise Exception('Key not implemented')

    def render(self, template, body):
        return loader.render_to_string(template, body)


class InstantArticleRenderer(BaseRenderer):
    BETTY_TEMPLATE = 'instant_article/embeds/_ia_betty_embed.html'
    FACEBOOK_TEMPLATE = 'instant_article/embeds/_ia_facebook_embed.html'
    IMGUR_TEMPLATE = 'instant_article/embeds/_ia_imgur_embed.html'
    INSTAGRAM_TEMPLATE = 'instant_article/embeds/_ia_instagram_embed.html'
    ONION_VIDEO_TEMPLATE = 'instant_article/embeds/_ia_onion_video_embed.html'
    SOUNDCLOUD_TEMPLATE = 'instant_article/embeds/_ia_soundcloud_embed.html'
    TWITTER_TEMPLATE = 'instant_article/embeds/_ia_twitter_embed.html'
    VIMEO_TEMPLATE = 'instant_article/embeds/_ia_vimeo_embed.html'
    YOUTUBE_TEMPLATE = 'instant_article/embeds/_ia_youtube_embed.html'


class AmpRenderer(BaseRenderer):
    BETTY_TEMPLATE = 'amp/embeds/_amp_betty_embed.html'
    FACEBOOK_TEMPLATE = 'amp/embeds/_amp_facebook_embed.html'
    IMGUR_TEMPLATE = 'amp/embeds/_amp_imgur_embed.html'
    INSTAGRAM_TEMPLATE = 'amp/embeds/_amp_instagram_embed.html'
    ONION_VIDEO_TEMPLATE = 'amp/embeds/_amp_onion_video_embed.html'
    SOUNDCLOUD_TEMPLATE = 'amp/embeds/_amp_soundcloud_embed.html'
    TWITTER_TEMPLATE = 'amp/embeds/_amp_twitter_embed.html'
    VIMEO_TEMPLATE = 'amp/embeds/_amp_vimeo_embed.html'
    YOUTUBE_TEMPLATE = 'amp/embeds/_amp_youtube_embed.html'

    def generate_body(self, intermediate):
        body = []
        for item in intermediate:
            for key, values in item.items():
                values = self.clean_item(key, values)
                body.append(self.render_item(key, values).strip())

        return '\n'.join(body)

    def clean_item(self, key, values):
        if key == 'betty':
            values = self.clean_betty(values)
            return values
        if key == 'facebook':
            values = self.clean_facebook(values)
            return values
        if key == 'instagram':
            values = self.clean_instagram(values)
            return values
        if key == 'twitter':
            values = self.clean_twitter(values)
            return values
        if key == 'vimeo':
            pass

    def clean_betty(self, values):
        if values['ratio'] == '1x1':
            values['width'] = 500
            values['height'] = 500
        else:
            if values['ratio'] == '3x1':
                values['width'] = 1200
                values['height'] = 400
            else:
                values['width'] = 1920
                values['height'] = 1080
        return values

    def clean_facebook(self, values):
        src = BeautifulSoup(values['iframe']).iframe['src']
        link = re.compile('\\?href=(\\S+)').search(src).group(1)
        url = link.replace('%3A', ':').replace('%2F', '/')
        values['type'] = 'video' if '/videos/' in url else 'post'
        values['url'] = re.compile('(https:\\/\\/)(www.facebook.com)\\/(\\S+)\\/(\\S)+\\/(\\d+)').search(url).group()
        return values

    def clean_twitter(self, values):
        blockquote = BeautifulSoup(values['blockquote']).blockquote
        blockquote.attrs['placeholder'] = ''
        values['blockquote'] = blockquote
        import pdb
        pdb.set_trace()
        values['tweet_id'] = re.compile('(http(s)*:\\/\\/)((www.)*twitter.com)\\/(\\S+)\\/status\\/(\\d+)').search(blockquote.a['href']).group(6)
        return values