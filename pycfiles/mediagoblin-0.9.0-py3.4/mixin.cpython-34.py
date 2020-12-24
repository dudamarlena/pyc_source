# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/db/mixin.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 22403 bytes
"""
This module contains some Mixin classes for the db objects.

A bunch of functions on the db objects are really more like
"utility functions": They could live outside the classes
and be called "by hand" passing the appropiate reference.
They usually only use the public API of the object and
rarely use database related stuff.

These functions now live here and get "mixed in" into the
real objects.
"""
import uuid, re
from datetime import datetime
from pytz import UTC
from werkzeug.utils import cached_property
from mediagoblin.media_types import FileTypeNotSupported
from mediagoblin.tools import common, licenses
from mediagoblin.tools.pluginapi import hook_handle
from mediagoblin.tools.text import cleaned_markdown_conversion
from mediagoblin.tools.url import slugify
from mediagoblin.tools.translate import pass_to_ugettext as _

class CommentingMixin(object):
    __doc__ = '\n    Mixin that gives classes methods to get and add the comments on/to it\n\n    This assumes the model has a "comments" class which is a ForeignKey to the\n    Collection model. This will hold a Collection of comments which are\n    associated to this model. It also assumes the model has an "actor"\n    ForeignKey which points to the creator/publisher/etc. of the model.\n\n    NB: This is NOT the mixin for the Comment Model, this is for\n        other models which support commenting.\n    '

    def get_comment_link(self):
        from mediagoblin.db.models import Comment, GenericModelReference
        gmr = GenericModelReference.query.filter_by(obj_pk=self.id, model_type=self.__tablename__).first()
        if gmr is None:
            return
        link = Comment.query.filter_by(comment_id=gmr.id).first()
        return link

    def get_reply_to(self):
        link = self.get_comment_link()
        if link is None or link.target_id is None:
            return
        return link.target()

    def soft_delete(self, *args, **kwargs):
        link = self.get_comment_link()
        if link is not None:
            link.delete()
        super(CommentingMixin, self).soft_delete(*args, **kwargs)


class GeneratePublicIDMixin(object):
    __doc__ = "\n    Mixin that ensures that a the public_id field is populated.\n\n    The public_id is the ID that is used in the API, this must be globally\n    unique and dereferencable. This will be the URL for the API view of the\n    object. It's used in several places, not only is it used to give out via\n    the API but it's also vital information stored when a soft_deletion occurs\n    on the `Graveyard.public_id` field, this is needed to follow the spec which\n    says we have to be able to provide a shell of an object and return a 410\n    (rather than a 404) when a deleted object has been deleted.\n\n    This requires a the urlgen off the request object (`request.urlgen`) to be\n    provided as it's the ID is a URL.\n    "

    def get_public_id(self, urlgen):
        if 'public_id' not in self.__table__.columns.keys():
            raise Exception('Model has no public_id field')
        if self.public_id is None:
            self.save(commit=False)
            self.public_id = urlgen('mediagoblin.api.object', object_type=self.object_type, id=str(uuid.uuid4()), qualified=True)
            self.save()
        return self.public_id


class UserMixin(object):
    object_type = 'person'

    @property
    def bio_html(self):
        return cleaned_markdown_conversion(self.bio)

    def url_for_self(self, urlgen, **kwargs):
        """Generate a URL for this User's home page."""
        return urlgen('mediagoblin.user_pages.user_home', user=self.username, **kwargs)


class GenerateSlugMixin(object):
    __doc__ = '\n    Mixin to add a generate_slug method to objects.\n\n    Depends on:\n     - self.slug\n     - self.title\n     - self.check_slug_used(new_slug)\n    '

    def generate_slug(self):
        """
        Generate a unique slug for this object.

        This one does not *force* slugs, but usually it will probably result
        in a niceish one.

        The end *result* of the algorithm will result in these resolutions for
        these situations:
         - If we have a slug, make sure it's clean and sanitized, and if it's
           unique, we'll use that.
         - If we have a title, slugify it, and if it's unique, we'll use that.
         - If we can't get any sort of thing that looks like it'll be a useful
           slug out of a title or an existing slug, bail, and don't set the
           slug at all.  Don't try to create something just because.  Make
           sure we have a reasonable basis for a slug first.
         - If we have a reasonable basis for a slug (either based on existing
           slug or slugified title) but it's not unique, first try appending
           the entry's id, if that exists
         - If that doesn't result in something unique, tack on some randomly
           generated bits until it's unique.  That'll be a little bit of junk,
           but at least it has the basis of a nice slug.
        """
        if self.slug:
            slug = slugify(self.slug)
        else:
            if self.title:
                slug = slugify(self.title)
            else:
                return
        if slug == '':
            return
        if self.check_slug_used(slug):
            if self.id:
                slug_with_id = '%s-%s' % (slug, self.id)
                if not self.check_slug_used(slug_with_id):
                    self.slug = slug_with_id
                    return
            slug += '-' + uuid.uuid4().hex[:4]
            while self.check_slug_used(slug):
                slug += uuid.uuid4().hex[:4]

        self.slug = slug


class MediaEntryMixin(GenerateSlugMixin, GeneratePublicIDMixin):

    def check_slug_used(self, slug):
        from mediagoblin.db.util import check_media_slug_used
        return check_media_slug_used(self.actor, slug, self.id)

    @property
    def object_type(self):
        """ Converts media_type to pump-like type - don't use internally """
        return self.media_type.split('.')[(-1)]

    @property
    def description_html(self):
        """
        Rendered version of the description, run through
        Markdown and cleaned with our cleaning tool.
        """
        return cleaned_markdown_conversion(self.description)

    def get_display_media(self):
        """Find the best media for display.

        We try checking self.media_manager.fetching_order if it exists to
        pull down the order.

        Returns:
          (media_size, media_path)
          or, if not found, None.

        """
        fetch_order = self.media_manager.media_fetch_order
        if not fetch_order:
            return
        media_sizes = self.media_files.keys()
        for media_size in fetch_order:
            if media_size in media_sizes:
                return (media_size, self.media_files[media_size])

    def main_mediafile(self):
        pass

    @property
    def slug_or_id(self):
        if self.slug:
            return self.slug
        else:
            return 'id:%s' % self.id

    def url_for_self(self, urlgen, **extra_args):
        """
        Generate an appropriate url for ourselves

        Use a slug if we have one, else use our 'id'.
        """
        uploader = self.get_actor
        return urlgen('mediagoblin.user_pages.media_home', user=uploader.username, media=self.slug_or_id, **extra_args)

    @property
    def thumb_url(self):
        """Return the thumbnail URL (for usage in templates)
        Will return either the real thumbnail or a default fallback icon."""
        if 'thumb' in self.media_files:
            thumb_url = self._app.public_store.file_url(self.media_files['thumb'])
        else:
            manager = self.media_manager
            thumb_url = self._app.staticdirector(manager['default_thumb'])
        return thumb_url

    @property
    def original_url(self):
        """ Returns the URL for the original image
        will return self.thumb_url if original url doesn't exist"""
        if 'original' not in self.media_files:
            return self.thumb_url
        return self._app.public_store.file_url(self.media_files['original'])

    @property
    def icon_url(self):
        """Return the icon URL (for usage in templates) if it exists"""
        try:
            return self._app.staticdirector(self.media_manager['type_icon'])
        except AttributeError:
            return

    @cached_property
    def media_manager(self):
        """Returns the MEDIA_MANAGER of the media's media_type

        Raises FileTypeNotSupported in case no such manager is enabled
        """
        manager = hook_handle(('media_manager', self.media_type))
        if manager:
            return manager(self)
        raise FileTypeNotSupported('MediaManager not in enabled types. Check media_type plugins are enabled in config?')

    def get_fail_exception(self):
        """
        Get the exception that's appropriate for this error
        """
        if self.fail_error:
            try:
                return common.import_component(self.fail_error)
            except ImportError:
                return

    def get_license_data(self):
        """Return license dict for requested license"""
        return licenses.get_license_by_url(self.license or '')

    def exif_display_iter(self):
        if not self.media_data:
            return
        exif_all = self.media_data.get('exif_all')
        for key in exif_all:
            label = re.sub('(.)([A-Z][a-z]+)', '\\1 \\2', key)
            yield (label.replace('EXIF', '').replace('Image', ''), exif_all[key])

    def exif_display_data_short(self):
        """Display a very short practical version of exif info"""
        if not self.media_data:
            return
        exif_all = self.media_data.get('exif_all')
        exif_short = {}
        if 'Image DateTimeOriginal' in exif_all:
            takendate = datetime.strptime(exif_all['Image DateTimeOriginal']['printable'], '%Y:%m:%d %H:%M:%S').date()
            taken = takendate.strftime('%B %d %Y')
            exif_short.update({'Date Taken': taken})
        aperture = None
        if 'EXIF FNumber' in exif_all:
            fnum = str(exif_all['EXIF FNumber']['printable']).split('/')
            if len(fnum) == 2:
                pass
            aperture = 'f/%.1f' % (float(fnum[0]) / float(fnum[1]))
        else:
            if fnum[0] != 'None':
                aperture = 'f/%s' % fnum[0]
            if aperture:
                exif_short.update({'Aperture': aperture})
            short_keys = [
             ('Camera', 'Image Model', None),
             (
              'Exposure', 'EXIF ExposureTime', lambda x: '%s sec' % x),
             ('ISO Speed', 'EXIF ISOSpeedRatings', None),
             (
              'Focal Length', 'EXIF FocalLength', lambda x: '%s mm' % x)]
            for label, key, fmt_func in short_keys:
                try:
                    val = fmt_func(exif_all[key]['printable']) if fmt_func else exif_all[key]['printable']
                    exif_short.update({label: val})
                except KeyError:
                    pass

            return exif_short


class TextCommentMixin(GeneratePublicIDMixin):
    object_type = 'comment'

    @property
    def content_html(self):
        """
        the actual html-rendered version of the comment displayed.
        Run through Markdown and the HTML cleaner.
        """
        return cleaned_markdown_conversion(self.content)

    def __unicode__(self):
        return '<{klass} #{id} {actor} "{comment}">'.format(klass=self.__class__.__name__, id=self.id, actor=self.get_actor, comment=self.content)

    def __repr__(self):
        return '<{klass} #{id} {actor} "{comment}">'.format(klass=self.__class__.__name__, id=self.id, actor=self.get_actor, comment=self.content)


class CollectionMixin(GenerateSlugMixin, GeneratePublicIDMixin):
    object_type = 'collection'

    def check_slug_used(self, slug):
        from mediagoblin.db.util import check_collection_slug_used
        return check_collection_slug_used(self.actor, slug, self.id)

    @property
    def description_html(self):
        """
        Rendered version of the description, run through
        Markdown and cleaned with our cleaning tool.
        """
        return cleaned_markdown_conversion(self.description)

    @property
    def slug_or_id(self):
        return self.slug or self.id

    def url_for_self(self, urlgen, **extra_args):
        """
        Generate an appropriate url for ourselves

        Use a slug if we have one, else use our 'id'.
        """
        creator = self.get_actor
        return urlgen('mediagoblin.user_pages.user_collection', user=creator.username, collection=self.slug_or_id, **extra_args)

    def add_to_collection(self, obj, content=None, commit=True):
        """ Adds an object to the collection """
        from mediagoblin.db.models import CollectionItem
        self.save(commit=False)
        item = CollectionItem()
        item.collection = self.id
        item.get_object = obj
        if content is not None:
            item.note = content
        self.num_items = self.num_items + 1
        self.save(commit=commit)
        item.save(commit=commit)
        return item


class CollectionItemMixin(object):

    @property
    def note_html(self):
        """
        the actual html-rendered version of the note displayed.
        Run through Markdown and the HTML cleaner.
        """
        return cleaned_markdown_conversion(self.note)


class ActivityMixin(GeneratePublicIDMixin):
    object_type = 'activity'
    VALID_VERBS = [
     'add', 'author', 'create', 'delete', 'dislike', 'favorite',
     'follow', 'like', 'post', 'share', 'unfavorite', 'unfollow',
     'unlike', 'unshare', 'update', 'tag']

    def get_url(self, request):
        return request.urlgen('mediagoblin.user_pages.activity_view', username=self.get_actor.username, id=self.id, qualified=True)

    def generate_content(self):
        """ Produces a HTML content for object """
        verb_to_content = {'add': {'simple': _('{username} added {object}'), 
                 'targetted': _('{username} added {object} to {target}')}, 
         'author': {'simple': _('{username} authored {object}')},  'create': {'simple': _('{username} created {object}')},  'delete': {'simple': _('{username} deleted {object}')},  'dislike': {'simple': _('{username} disliked {object}')},  'favorite': {'simple': _('{username} favorited {object}')},  'follow': {'simple': _('{username} followed {object}')},  'like': {'simple': _('{username} liked {object}')},  'post': {'simple': _('{username} posted {object}'), 
                  'targetted': _('{username} posted {object} to {target}')}, 
         'share': {'simple': _('{username} shared {object}')},  'unfavorite': {'simple': _('{username} unfavorited {object}')},  'unfollow': {'simple': _('{username} stopped following {object}')},  'unlike': {'simple': _('{username} unliked {object}')},  'unshare': {'simple': _('{username} unshared {object}')},  'update': {'simple': _('{username} updated {object}')},  'tag': {'simple': _('{username} tagged {object}')}}
        object_map = {'image': _('an image'), 
         'comment': _('a comment'), 
         'collection': _('a collection'), 
         'video': _('a video'), 
         'audio': _('audio'), 
         'person': _('a person')}
        obj = self.object()
        target = None if self.target_id is None else self.target()
        actor = self.get_actor
        content = verb_to_content.get(self.verb, None)
        if content is None or self.object is None:
            return
        if hasattr(obj, 'title') and obj.title.strip(' '):
            object_value = obj.title
        else:
            if obj.object_type in object_map:
                object_value = object_map[obj.object_type]
            else:
                object_value = _('an object')
            if target is not None and 'targetted' in content:
                if hasattr(target, 'title') and target.title.strip(' '):
                    target_value = target.title
                else:
                    if target.object_type in object_map:
                        target_value = object_map[target.object_type]
                    else:
                        target_value = _('an object')
                self.content = content['targetted'].format(username=actor.username, object=object_value, target=target_value)
            else:
                self.content = content['simple'].format(username=actor.username, object=object_value)
        return self.content

    def serialize(self, request):
        href = request.urlgen('mediagoblin.api.object', object_type=self.object_type, id=self.id, qualified=True)
        published = UTC.localize(self.published)
        updated = UTC.localize(self.updated)
        obj = {'id': href, 
         'actor': self.get_actor.serialize(request), 
         'verb': self.verb, 
         'published': published.isoformat(), 
         'updated': updated.isoformat(), 
         'content': self.content, 
         'url': self.get_url(request), 
         'object': self.object().serialize(request), 
         'objectType': self.object_type, 
         'links': {'self': {'href': href}}}
        if self.generator:
            obj['generator'] = self.get_generator.serialize(request)
        if self.title:
            obj['title'] = self.title
        if self.target_id is not None:
            obj['target'] = self.target().serialize(request)
        return obj

    def unseralize(self, data):
        """
        Takes data given and set it on this activity.

        Several pieces of data are not written on because of security
        reasons. For example changing the author or id of an activity.
        """
        if 'verb' in data:
            self.verb = data['verb']
        if 'title' in data:
            self.title = data['title']
        if 'content' in data:
            self.content = data['content']