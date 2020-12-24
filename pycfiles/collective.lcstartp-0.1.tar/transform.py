# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/transform.py
# Compiled at: 2017-10-02 13:30:56
from collective.lazysizes.interfaces import ILazySizesSettings
from collective.lazysizes.logger import logger
from lxml import etree
from plone import api
from plone.registry.interfaces import IRegistry
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.component import getUtility
from zope.interface import implementer
PLACEHOLDER = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAAA1BMVEXy8vJkA4prAAAAC0lEQVQI12MgEQAAADAAAWV61nwAAAAASUVORK5CYII='
ROOT_SELECTOR = '//*[@id="content"]'
CLASS_SELECTOR = '//*[contains(concat(" ", normalize-space(@class), " "), " {0} ")]'

@implementer(ITransform)
class LazySizesTransform(object):
    """Transform a response to lazy load <img> and <iframe> elements."""
    order = 8888

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def _parse(self, result):
        """Create an XMLSerializer from an HTML string, if needed."""
        content_type = self.request.response.getHeader('Content-Type')
        if not content_type or not content_type.startswith('text/html'):
            return
        try:
            return getHTMLSerializer(result)
        except (AttributeError, TypeError, etree.ParseError):
            return

    def _lazyload_img(self, element):
        """Process <img> tags for lazy loading by using the `src`
        attribute as `data-src` and loading a placeholder instead.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the image to be lazy loaded
        :rtype: str
        """
        assert element.tag == 'img'
        if 'src' not in element.attrib:
            url = self.request['URL']
            logger.error('<img> tag without src attribute in: ' + url)
            return
        element.attrib['data-src'] = element.attrib['src']
        element.attrib['src'] = PLACEHOLDER
        return element.attrib['data-src']

    def _lazyload_iframe(self, element):
        """Process <iframe> tags for lazy loading by replacing the
        `src` attribute with a `data-src`.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the iframe to be lazy loaded
        :rtype: str
        """
        assert element.tag == 'iframe'
        if 'src' not in element.attrib:
            return
        element.attrib['data-src'] = element.attrib['src']
        del element.attrib['src']
        return element.attrib['data-src']

    def _lazyload_tweet(self, element):
        """Process tweets for lazy loading. Twitter describes tweets
        using <blockquote> tags with a `twitter-tweet` class and loads
        a widget in a sibling <script> tag. To lazy load we need to add
        a `data-twitter` attribute and remove the widget.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the tweet to be lazy loaded
        :rtype: str
        """
        assert element.tag == 'blockquote'
        element.attrib['data-twitter'] = 'twitter-tweet'
        sibling = element.getnext()
        if sibling is None:
            return
        else:
            widget = '//platform.twitter.com/widgets.js'
            if sibling.tag == 'script' and widget in sibling.attrib['src']:
                parent = element.getparent()
                parent.remove(sibling)
                logger.debug("Twitter's widget <script> tag removed")
            try:
                return element.find('a').attrib['href']
            except AttributeError:
                return

            return

    def _lazyload(self, element):
        """Inject attributes needed by lazysizes to lazy load elements.
        For more information, see: https://afarkas.github.io/lazysizes
        """
        assert element.tag in ('img', 'iframe', 'blockquote')
        classes = element.attrib.get('class', '').split(' ')
        if 'lazyload' in classes:
            return
        else:
            if element.tag == 'img':
                src = self._lazyload_img(element)
            else:
                if element.tag == 'iframe':
                    src = self._lazyload_iframe(element)
                elif element.tag == 'blockquote':
                    if 'twitter-tweet' not in classes:
                        return
                    src = self._lazyload_tweet(element)
                    if src is not None:
                        classes.remove('twitter-tweet')
                if src is None:
                    return
            classes.append('lazyload')
            element.attrib['class'] = (' ').join(classes).strip()
            msg = '<{0}> tag with src="{1}" was processed for lazy loading'
            logger.debug(msg.format(element.tag, src))
            return

    def _blacklist(self, result, blacklisted_classes):
        """Return a list of blacklisted elements."""
        if not blacklisted_classes:
            return ()
        path = []
        for css_class in blacklisted_classes:
            path.append(('{0}{1}|{0}{1}//img|{0}{1}//iframe|{0}{1}//blockquote').format(ROOT_SELECTOR, CLASS_SELECTOR.format(css_class)))

        path = ('|').join(path)
        return result.tree.xpath(path)

    def transformBytes(self, result, encoding):
        pass

    def transformUnicode(self, result, encoding):
        pass

    def transformIterable(self, result, encoding):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILazySizesSettings, check=False)
        if not api.user.is_anonymous():
            enabled = getattr(settings, 'lazyload_authenticated', False)
            if not enabled:
                return
        result = self._parse(result)
        if result is None:
            return
        else:
            css_class_blacklist = getattr(settings, 'css_class_blacklist', set())
            blacklist = self._blacklist(result, css_class_blacklist)
            path = ('{0}//img|{0}//iframe|{0}//blockquote').format(ROOT_SELECTOR)
            for el in result.tree.xpath(path):
                if el in blacklist:
                    continue
                self._lazyload(el)

            return result