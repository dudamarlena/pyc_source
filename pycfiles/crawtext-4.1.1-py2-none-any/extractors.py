# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/c24b/projets/crawtext/newspaper/videos/extractors.py
# Compiled at: 2014-11-06 08:50:32
from .videos import Video
VIDEOS_TAGS = [
 'iframe', 'embed', 'object', 'video']
VIDEO_PROVIDERS = ['youtube', 'vimeo', 'dailymotion', 'kewego']

class VideoExtractor(object):
    """Extracts a list of video from Article top node
    """

    def __init__(self, config, top_node):
        self.config = config
        self.parser = self.config.get_parser()
        self.top_node = top_node
        self.candidates = []
        self.movies = []

    def get_embed_code(self, node):
        return ('').join([ line.strip() for line in self.parser.nodeToString(node).splitlines()
                         ])

    def get_embed_type(self, node):
        return self.parser.getTag(node)

    def get_width(self, node):
        return self.parser.getAttribute(node, 'width')

    def get_height(self, node):
        return self.parser.getAttribute(node, 'height')

    def get_src(self, node):
        return self.parser.getAttribute(node, 'src')

    def get_provider(self, src):
        if src:
            for provider in VIDEO_PROVIDERS:
                if provider in src:
                    return provider

        return

    def get_video(self, node):
        """Create a video object from a video embed
        """
        video = Video()
        video.embed_code = self.get_embed_code(node)
        video.embed_type = self.get_embed_type(node)
        video.width = self.get_width(node)
        video.height = self.get_height(node)
        video.src = self.get_src(node)
        video.provider = self.get_provider(video.src)
        return video

    def get_iframe_tag(self, node):
        return self.get_video(node)

    def get_video_tag(self, node):
        """Extract html video tags
        """
        return Video()

    def get_embed_tag(self, node):
        parent = self.parser.getParent(node)
        if parent is not None:
            parent_tag = self.parser.getTag(parent)
            if parent_tag == 'object':
                return self.get_object_tag(node)
        return self.get_video(node)

    def get_object_tag(self, node):
        child_embed_tag = self.parser.getElementsByTag(node, 'embed')
        if child_embed_tag and child_embed_tag[0] in self.candidates:
            self.candidates.remove(child_embed_tag[0])
        src_node = self.parser.getElementsByTag(node, tag='param', attr='name', value='movie')
        if not src_node:
            return None
        else:
            src = self.parser.getAttribute(src_node[0], 'value')
            provider = self.get_provider(src)
            if not provider:
                return None
            video = self.get_video(node)
            video.provider = provider
            video.src = src
            return video

    def get_videos(self):
        self.candidates = self.parser.getElementsByTags(self.top_node, VIDEOS_TAGS)
        for candidate in self.candidates:
            tag = self.parser.getTag(candidate)
            attr = 'get_%s_tag' % tag
            if hasattr(self, attr):
                movie = getattr(self, attr)(candidate)
                if movie is not None and movie.provider is not None:
                    self.movies.append(movie)

        return list(self.movies)