# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/minimatic/__init__.py
# Compiled at: 2010-01-19 05:11:51
import re, os, logging, StringIO, posixpath as path, shutil, time, cssutils
from cssutils.serialize import CSSSerializer
from pylons import config
from pylons.decorators.cache import beaker_cache
from webhelpers.html.tags import javascript_link as __javascript_link
from webhelpers.html.tags import stylesheet_link as __stylesheet_link
from minimatic.jsmin import JavascriptMinify
__all__ = [
 'javascript_link', 'stylesheet_link']
log = logging.getLogger(__name__)
beaker_kwargs = dict(key='sources', expire='never', type='memory')
js_minify = JavascriptMinify()

def css_strip(css):
    """Strip whitespace and comments from a css string.

Given a string containing css rules css_strip returns a string with all
sequential whitespace changed to one space

    >>> css_strip('''
    ... body
    ... {
    ...     color: #ffffff;
    ... }''')
    'body { color: #ffffff; }'

The css comments are stripped as well

    >>> css_strip('''
    ... /* Page Header */
    ... #top { /*margin: 0px;*/ border: none }
    ... ''')
    '#top { border: none }'

Check some comment edge cases. Comments at the beginning and end:

    >>> css_strip('''/* Comment in the beginning */
    ... some_css/*comment here*/{url: /some/url/*remove_me*/;}
    ... /* Comment in the end */''')
    'some_css {url: /some/url ;}'

Invalid comments:

    >>> css_strip('''/* Unfinished comment - leave it
    ... though it's a mistake /''')
    "/* Unfinished comment - leave it though it's a mistake /"
    >>> css_strip('''/ Unfinished comment - leave it
    ... though it's a mistake */''')
    "/ Unfinished comment - leave it though it's a mistake */"
    """
    parts = []
    text_start = 0
    while True:
        text_end = css.find('/*', text_start)
        if text_end == -1:
            break
        if text_start < text_end:
            parts.extend(css[text_start:text_end].split())
        text_start = css.find('*/', text_end + 2)
        if text_start == -1:
            break
        text_start += 2

    if text_start > -1 and text_start < len(css) - 1:
        parts.extend(css[text_start:].split())
    elif text_start == -1 and text_end < len(css) - 1:
        parts.extend(css[text_end:].split())
    css = (' ').join(filter(None, parts))
    return css


def process_sources(sources, ext, fs_root, combined=False, timestamp=False):
    """Use utilities to combine and/or minify two or more files together.
    For more info see :func:`base_link`.
    
    :param sources: Paths of source files (strings or dicts)
    :param ext: Type of files
    :param fs_root: Root of file (normally public dir)
    :param combined: Filename of the combined files
    :param timestamp: Should the timestamp be added to the link
    :type sources: string
    :type ext: js or css
    :type fs_root: string
    :type filename: string
    :type timestamp: bool

    :returns: List of paths to processed sources
    """
    if not sources:
        return []
    if len(sources) == 1 and isinstance(sources, (str, unicode)):
        return sources
    base = '/'
    for i in range(len(sources)):
        source = sources[i]
        if isinstance(source, (str, unicode)):
            source = sources[i] = dict(file=source)
        if not combined and source.get('minify') and not source.get('dest'):
            raise ValueError('Either "combined" must be specified or "dest" for every file')
        source['file_path'] = path.join(fs_root, source['file'].lstrip('/'))
        if source.get('dest'):
            source['dest_path'] = path.join(fs_root, source['dest'].lstrip('/'))
            source['dest_link'] = path.join(base, source['dest'].lstrip('/'))
        else:
            source['dest_link'] = source['file']
        source['modts'] = path.getmtime(source['file_path'])

    if combined:
        fname = combined.lstrip('/')
        fpath = path.join(fs_root, fname)
        refresh_needed = False
        if path.exists(fpath):
            last_mod = path.getmtime(fpath)
            refresh_needed = last_mod < max([ s['modts'] for s in sources ])
        else:
            refresh_needed = True
        buffer = StringIO.StringIO()
    else:
        refresh_needed = True
        buffer = None
    if refresh_needed:
        for source in sources:
            dest = buffer
            if not dest:
                dest = source.get('dest_path')
                if not dest or path.exists(dest) and source['modts'] <= path.getmtime(dest):
                    continue
                dirs = path.dirname(dest)
                try:
                    os.makedirs(dirs, 448)
                except OSError:
                    pass
                else:
                    dest = open(dest, 'w')
            if 'js' in ext:
                f = open(source['file_path'], 'r')
                if source.get('minify') == 'minify':
                    js_minify.minify(f, dest)
                else:
                    dest.write(f.read())
                    f.close()
            elif 'css' in ext:
                if source.get('minify') == 'minify':
                    sheet = cssutils.parseFile(source['file_path'])
                    sheet.setSerializer(CSSUtilsMinificationSerializer())
                    cssutils.ser.prefs.useMinified()
                    dest.write(sheet.cssText)
                elif source.get('minify') == 'strip':
                    f = open(source['file_path'], 'r')
                    dest.write(css_strip(f.read()))
                    f.close()
                else:
                    f = open(source['file_path'], 'r')
                    dest.write(f.read())
                    f.close()
            else:
                raise ValueError('Source type unknown: %s' % ext)
            if buffer:
                buffer.write('\n')
            else:
                dest.close()

        if buffer:
            dirs = path.dirname(fpath)
            try:
                os.makedirs(dirs, 448)
            except OSError:
                pass
            else:
                f = open(fpath, 'w')
                f.write(buffer.getvalue())
                f.close()
    if buffer:
        last_mod = path.getmtime(fpath)
        link = path.join(base, fname)
        if timestamp:
            timestamp = int(last_mod)
            link = '%s?t=%s' % (link, timestamp)
        return [
         link]
    else:
        links = []
        for s in sources:
            last_mod = path.getmtime(s.get('dest_path', s['file_path']))
            link = s['dest_link']
            if timestamp:
                timestamp = int(last_mod)
                link = '%s?t=%s' % (link, timestamp)
            links.append(link)

        return links
    return


def base_link(ext, *sources, **options):
    """Base function that glues all logic together.

    It parses options and calls :func:`process_sources`.

    :param ext: js or css helper
    :param sources: a list of source files. Can be a dicts with keys:
            file='/script.js':              a path to your file
            minify=False|'strip'|'minify':  should this file be minified,
                                            stripped or left as it is?
            dest='/script.min.js':          minified file destination (needed if
                                            files are not combined)
        Alternatively you can provide strings in which case they will be treated
        as
            {file='<your string>', minify=False}
        In this case the files will not be minified and 'combined' must be
        provided
    :param combined: the combined file name if the files need to be combined.
        Otherwise they have to have 'dest' keys
    :param beaker_kwargs: Beaker options to pass to caching decorators
    :param timestamp: append timestamp to links, eg. test.js?t=123012343
    :type ext: string
    :type sources: list of strings or dicts or any combination
    :type combined: string
    :type beaker_kwargs: dict
    :type timestamp: bool
    :returns: HTML source code
    
    .. versionadded:: 0.3.1
        `beaker_kwargs` parameter

    .. versionadded:: 0.3.2
        `combined_filename` parameter

    .. versionadded:: 0.3.5
        `timestamp` parameter
    """
    combined = options.pop('combined', False)
    timestamp = options.pop('timestamp', False)
    beaker_options = options.pop('beaker_kwargs', False)
    fs_root = config.get('pylons.paths').get('static_files')
    sources = list(sources)
    if not (config.get('debug', False) or options.get('builtins', False)):
        if beaker_options:
            beaker_kwargs.update(beaker_options)
        sources = beaker_cache(**beaker_kwargs)(process_sources)(sources, ext, fs_root, combined, timestamp)
    for i in range(len(sources)):
        if isinstance(sources[i], dict):
            sources[i] = sources[i]['file']

    if 'js' in ext:
        return __javascript_link(*sources, **options)
    if 'css' in ext:
        return __stylesheet_link(*sources, **options)


def javascript_link(*sources, **options):
    """Calls :func:`base_link` with first argument ``js``
    
    All other arguments are passed on.
    """
    return base_link('js', *sources, **options)


def stylesheet_link(*sources, **options):
    """Calls :func:`base_link` with first argument ``css``
    
    All other arguments are passed on.
    """
    return base_link('css', *sources, **options)


class CSSUtilsMinificationSerializer(CSSSerializer):
    DOT_ZERO_REGEX = re.compile('(?<=[^\\d])0(\\.\\d+)')
    ZERO_PX_REGEX = re.compile('([^\\d][0])(?:px|em|pt)')

    def do_css_CSSStyleDeclaration(self, style, separator=None):
        try:
            color = style.getPropertyValue('color')
            if color and color is not '':
                color = self.change_colors(color)
                style.setProperty('color', color)
        except:
            pass

        output = CSSSerializer.do_css_CSSStyleDeclaration(self, style, separator)
        output = self.ZERO_PX_REGEX.sub('\\1', output)
        return self.DOT_ZERO_REGEX.sub('\\1', output)

    def change_colors(self, color):
        if color.startswith('#') and len(color) == 7:
            if color[1] == color[2] and color[3] == color[4] and color[5] == color[6]:
                color = '#%s%s%s' % (color[1], color[3], color[5])
        return color