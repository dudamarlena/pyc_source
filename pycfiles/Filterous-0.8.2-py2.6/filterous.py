# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/filterous/filterous.py
# Compiled at: 2010-06-29 05:38:08
r"""Filterous - Delicious Command Line Filter <http://filterous.sourceforge.net/>

Default syntax:

filterous [options]

Options:
--tag      Tag search string (@tag)
--ntag     Negated tag search string (@tag)
--desc     Description search string (@description)
--ndesc    Negated description search string (@description)
--note     Note search string (@extended)
--nnote    Negated note search string (@extended)
--url      URL search string (@href)
--nurl     Negated URL search string (@href)
--help     Show this information (use pydoc for more)
-T         Output tab separated list for easier parsing
-t         Show tags
-d         Show descriptions
-n         Show notes
-b         Show Delicious bookmarking link

Description:
Will search the tags of the XML file downloaded from
<https://api.del.icio.us/v1/posts/all>. To avoid the slow load of that page in
a web browser, you can use one of the following commands:

curl -ku username:password https://api.del.icio.us/v1/posts/all

wget --no-check-certificate --user=username --password=password -O all.xml https://api.del.icio.us/v1/posts/all

Examples:

filterous -t --tag video --tag tosee --ntag seen < all.xml
    Unseen videos with tags.

filterous --nurl example.org < all.xml
    Links to example.org.

filterous -dntT --tag ★★★★★ < all.xml
    Returns great links as a tab-separated list with URL, description, notes and
    tags.

filterous -b --url index. < all.xml
filterous -b --url # < all.xml
filterous -b --url \& < all.xml
filterous -b --url //www. < all.xml
    Bookmarks that could be shortened, with their bookmarking link for quick
    correction.

filterous -b --tag read --ntag toread < all.xml
filterous -b --tag seen --ntag tosee < all.xml
filterous -b --tag done --ntag todo < all.xml
    Strange tag combinations.

filterous < all.xml | xargs -d\\n linkchecker -r0 --no-warnings --no-status > diagnosis.txt
    Check links for errors
"""
__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'
from datetime import datetime
import getopt
from lxml import etree
import signal, sys
from urllib import quote
TAG_SEPARATOR = ' '
POSITIVE_MATCHES = set(['tag', 'desc', 'note', 'url'])
NEGATIVE_MATCHES = set(['ntag', 'ndesc', 'nnote', 'nurl'])
SS_STRING_MATCHES = set(['tag', 'ntag'])
SUBSTRING_MATCHES = set(['desc', 'ndesc', 'note', 'nnote', 'url', 'nurl'])
OPTION_ATTRIBUTES = {'tag': 'tag', 
   'ntag': 'tag', 
   'desc': 'description', 
   'ndesc': 'description', 
   'note': 'extended', 
   'nnote': 'extended', 
   'url': 'href', 
   'nurl': 'href'}
ATTRIBUTES_READABLE = {'tag': 'Tags', 
   'description': 'Title', 
   'extended': 'Notes', 
   'href': 'URL', 
   'bookmark': 'Bookmark'}
ATTRIBUTES_REQUIRED = [
 'href', 'description']
ERRM_SUBMIT_BUG = 'Please submit a bug report at <https://sourceforge.net/tracker/?func=add&group_id=303845&atid=1280761>, including the output of this script.'
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

class DeliciousBookmark:
    """Container for Delicious bookmarks"""

    def __init__(self, element):
        """
        Initialize element

        @param element: XML element
        """
        self.element = element

    def _format_value(self, include, human_readable):
        """
        Get printable value from attribute value

        @param include: Name of the value
        @param human_readable: Print human readable (otherwise parseable)?
        @return: Formatted string
        """
        if include == 'bookmark':
            value = self.element.get('href')
            value_hash = self.element.get('hash')
        else:
            value = self.element.get(include)
        if include == 'time' and human_readable:
            return str(datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ'))
        else:
            if include == 'bookmark':
                return 'http://delicious.com/save' + '?url=%s' % quote(value) + '&hash=%s' % quote(value_hash) + '&edit=yes&noui=1&jump=doclose'
            return value

    def prettyprint(self, out, includes, human_readable):
        """
        Output bookmark

        @param out: Output stream
        @param includes: Which things to include
        @param human_readable: Print human readable (otherwise parseable)?
        """
        assert includes is not None
        assert len(includes) != 0
        if human_readable and len(includes) != 1:
            post_separator = '\n\n'
            show_prefix = True
        else:
            post_separator = '\n'
            show_prefix = False
        if human_readable:
            include_separator = '\n'
        else:
            include_separator = '\t'
        for include in includes:
            if show_prefix:
                out.write(ATTRIBUTES_READABLE[include] + ': ')
            text_value = self._format_value(include, human_readable)
            if text_value is not None:
                out.write(text_value.encode('utf-8'))
            if include != includes[(-1)]:
                out.write(include_separator)
            else:
                out.write(post_separator)

        return


def _get_search_xpath(terms):
    """
    XPath expression to search on each post.

    @param terms: Dictionary of terms, each with a list of values to search for
    @return: XPath
    """
    result = ''
    for (term, values) in terms.items():
        if term not in OPTION_ATTRIBUTES:
            raise NameError('Not a valid search term: %s' % term)
        attribute = OPTION_ATTRIBUTES[term]
        xpaths = []
        for index in range(len(values)):
            value = values[index]
            if isinstance(value, str):
                values[index] = value.decode('utf-8')

        if term in SS_STRING_MATCHES:
            for value in values:
                xpaths.append("contains(concat(' ', @%(x_attribute)s, ' '), concat(' ', '%(x_value)s', ' '))" % {'x_attribute': attribute, 
                   'x_value': value})

        elif term in SUBSTRING_MATCHES:
            for value in values:
                xpaths.append("contains(@%(x_attribute)s, '%(x_value)s')" % {'x_attribute': attribute, 
                   'x_value': value})

        else:
            raise NameError('Method unknown for search term: %s' % term)
        if xpaths != []:
            if term in NEGATIVE_MATCHES:
                xpaths = [ 'not(%s)' % xpath for xpath in xpaths ]
            elif term not in POSITIVE_MATCHES:
                raise NameError('Unsupported search term: %s' % term)
            xpaths = [ '[%s]' % xpath for xpath in xpaths ]
        result += ('').join(xpaths)

    return etree.XPath('/posts/post' + result)


def search(file_pointer, out, terms, includes, human_readable=True):
    """
    Get only the posts that match the terms.

    @param file_pointer: Delicious bookmark export file pointer
    @param terms: Dictionary of search terms
    @param includes: Which attributes to output
    @param out: Output stream
    """
    search_xpath = _get_search_xpath(terms)
    context = etree.iterparse(file_pointer, tag='posts')
    for event_elem in context:
        matches = search_xpath(event_elem[1])
        if matches is None:
            print 'No matches found.'
            return
        for match in matches:
            bookmark = DeliciousBookmark(match)
            bookmark.prettyprint(out, includes, human_readable)

    return


class UsageError(ValueError):
    """Raise in case of invalid parameters."""

    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    """Option and argument handling."""
    if argv is None:
        argv = sys.argv
    output_opts = {'b': 'bookmark', 
       'd': 'description', 
       'n': 'extended', 
       't': 'tag'}
    output_options = [ '-' + option for option in output_opts.keys() ]
    includes = ['href']
    human_readable = True
    search_option_names = OPTION_ATTRIBUTES.keys()
    search_opts = [ option + '=' for option in search_option_names ]
    opts = search_opts + ['help']
    search_options = [ '--' + option for option in search_option_names ]
    search_params = {}
    for search_option in search_option_names:
        search_params[search_option] = []

    try:
        try:
            opts = getopt.getopt(argv[1:], ('').join(output_opts) + 'T', opts)[0]
        except getopt.GetoptError, err:
            sys.stdout.write(__doc__)
            return 1
        else:
            for (option, value) in opts:
                if option in search_options:
                    search_params[option[2:]].append(value)
                elif option in output_options:
                    if output_opts[option[1:]] not in includes:
                        includes.append(output_opts[option[1:]])
                elif option == '-T':
                    human_readable = False
                else:
                    if option == '--help':
                        sys.stdout.write(__doc__)
                        return 0
                    raise UsageError("Unhandled option '%(x_option)s'. %(x_user_action)s" % {'x_option': option, 
                       'x_user_action': ERRM_SUBMIT_BUG})

    except UsageError, err:
        sys.stderr.write(err.msg + '\n')
        return 2

    search(sys.stdin, sys.stdout, search_params, includes, human_readable)
    return


if __name__ == '__main__':
    sys.exit(main())