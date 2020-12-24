# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/static_thumbnails/templatetags/static_thumbnails.py
# Compiled at: 2019-10-15 10:47:58
# Size of source mod 2**32: 8241 bytes
import six
from django.core.files.storage import FileSystemStorage
from django.template import Library
from django.template import TemplateSyntaxError
from django.template import VariableDoesNotExist
from django.template import Node
from django.conf import settings
from django.utils.html import escape
from easy_thumbnails.alias import aliases
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.templatetags.thumbnail import VALID_OPTIONS
from easy_thumbnails.templatetags.thumbnail import split_args
from easy_thumbnails.templatetags.thumbnail import RE_SIZE
register = Library()

class StaticThumbnailStorage(FileSystemStorage):

    def __init__(self, *args, **kw):
        (super(StaticThumbnailStorage, self).__init__)(args, location=settings.STATIC_ROOT, base_url=settings.STATIC_URL, **kw)


static_storage = StaticThumbnailStorage()

class StaticThumbnailNode(Node):

    def __init__(self, source_var, opts, context_name=None):
        self.source_var = source_var
        self.opts = opts
        self.context_name = context_name

    def render(self, context):
        raise_errors = settings.THUMBNAIL_DEBUG
        try:
            source = self.source_var.resolve(context)
        except VariableDoesNotExist:
            if raise_errors:
                raise VariableDoesNotExist("Variable '%s' does not exist." % self.source_var)
            return self.bail_out(context)
        else:
            if not source:
                if raise_errors:
                    raise TemplateSyntaxError("Variable '%s' is an invalid source." % self.source_var)
                return self.bail_out(context)
        try:
            opts = {}
            for key, value in six.iteritems(self.opts):
                if hasattr(value, 'resolve'):
                    value = value.resolve(context)
                opts[str(key)] = value

        except Exception:
            if raise_errors:
                raise
            return self.bail_out(context)
        else:
            size = opts['size']
            if isinstance(size, six.string_types):
                m = RE_SIZE.match(size)
                if m:
                    opts['size'] = (
                     int(m.group(1)), int(m.group(2)))
                else:
                    alias = aliases.get(size, target=source)
                    if alias:
                        del opts['size']
                        opts = dict(alias, **opts)
                    else:
                        if raise_errors:
                            raise TemplateSyntaxError('%r is not a valid size.' % size)
                        return self.bail_out(context)
            if 'quality' in opts:
                try:
                    opts['quality'] = int(opts['quality'])
                except (TypeError, ValueError):
                    if raise_errors:
                        raise TemplateSyntaxError('%r is an invalid quality.' % opts['quality'])
                    return self.bail_out(context)

            if 'subsampling' in opts:
                try:
                    opts['subsampling'] = int(opts['subsampling'])
                except (TypeError, ValueError):
                    if raise_errors:
                        raise TemplateSyntaxError('%r is an invalid subsampling level.' % opts['subsampling'])
                    return self.bail_out(context)

        try:
            thumbnailer = get_thumbnailer(static_storage, relative_name=source)
            thumbnail = thumbnailer.get_thumbnail(opts)
            highres_infix = thumbnailer.thumbnail_highres_infix
            regular_url = thumbnail.url.split('.')
            highres_url = '%s%s.%s' % ('.'.join(regular_url[:-1]), highres_infix, regular_url[(-1)])
            setattr(thumbnail, 'highres_url', highres_url)
        except Exception:
            if raise_errors:
                raise
            return self.bail_out(context)
        else:
            if self.context_name is None:
                return escape(thumbnail.url)
            context[self.context_name] = thumbnail
            return ''

    def bail_out(self, context):
        if self.context_name:
            context[self.context_name] = ''
        return ''


@register.tag
def static_thumbnail(parser, token):
    """
    Creates a thumbnail of an ImageField.

    Basic tag Syntax::

        {% thumbnail [source] [size] [options] %}

    *source* must be a ``File`` object, usually an Image/FileField of a model
    instance.

    *size* can either be:

    * the name of an alias

    * the size in the format ``[width]x[height]`` (for example,
      ``{% thumbnail person.photo 100x50 %}``) or

    * a variable containing a valid size (i.e. either a string in the
      ``[width]x[height]`` format or a tuple containing two integers):
      ``{% thumbnail person.photo size_var %}``.

    *options* are a space separated list of options which are used when
    processing the image to a thumbnail such as ``sharpen``, ``crop`` and
    ``quality=90``.

    If *size* is specified as an alias name, *options* are used to override
    and/or supplement the options defined in that alias.

    The thumbnail tag can also place a
    :class:`~easy_thumbnails.files.ThumbnailFile` object in the context,
    providing access to the properties of the thumbnail such as the height and
    width::

        {% thumbnail [source] [size] [options] as [variable] %}

    When ``as [variable]`` is used, the tag doesn't output anything. Instead,
    use the variable like a standard ``ImageFieldFile`` object::

        {% thumbnail obj.picture 200x200 upscale as thumb %}
        <img src="{{ thumb.url }}"
             width="{{ thumb.width }}"
             height="{{ thumb.height }}" />

    **Debugging**

    By default, if there is an error creating the thumbnail or resolving the
    image variable then the thumbnail tag will just return an empty string (and
    if there was a context variable to be set then it will also be set to an
    empty string).

    For example, you will not see an error if the thumbnail could not
    be written to directory because of permissions error. To display those
    errors rather than failing silently, set ``THUMBNAIL_DEBUG = True`` in
    your Django project's settings module.

    """
    args = token.split_contents()
    tag = args[0]
    if len(args) > 4 and args[(-2)] == 'as':
        context_name = args[(-1)]
        args = args[:-2]
    else:
        context_name = None
    if len(args) < 3:
        raise TemplateSyntaxError("Invalid syntax. Expected '{%% %s source size [option1 option2 ...] %%}' or '{%% %s source size [option1 option2 ...] as variable %%}'" % (
         tag, tag))
    opts = {}
    source_var = parser.compile_filter(args[1])
    size = args[2]
    match = RE_SIZE.match(size)
    if match:
        size = '"%s"' % size
    opts['size'] = parser.compile_filter(size)
    args_list = split_args(args[3:]).items()
    for arg, value in args_list:
        if arg in VALID_OPTIONS:
            if value:
                if value is not True:
                    value = parser.compile_filter(value)
            opts[arg] = value
        else:
            raise TemplateSyntaxError("'%s' tag received a bad argument: '%s'" % (
             tag, arg))

    return StaticThumbnailNode(source_var, opts=opts, context_name=context_name)