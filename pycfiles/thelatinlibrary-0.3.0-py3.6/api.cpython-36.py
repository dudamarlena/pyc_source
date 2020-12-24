# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thelatinlibrary/api.py
# Compiled at: 2019-01-13 09:45:03
# Size of source mod 2**32: 6931 bytes
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from thelatinlibrary import settings
from thelatinlibrary.authors import Author
from thelatinlibrary.exceptions import NoAuthorException
from thelatinlibrary.tools import titleize
_authors = []
_endpoint = 'http://www.thelatinlibrary.com/'
_exceptions = ['christian.html', 'classics.html', 'index.html',
 'medieval.html', 'misc.html', 'neo.html', 'readme.html']

def get_author(url: str, reload: Optional[bool]=None, save: Optional[bool]=None) -> Author:
    """
    Used to return an Author by passing
    an URL as an argument.

    Args:
        url (str): The URL that should be used to get the author.
        reload (Optional[bool]): If the response should be reloaded and the already stored content ignored.
        save (Optional[bool]): If the response should be saved.

    Example:
        All authors are associated to a link, so it is easy to get an author
        using it.

        >>> import thelatinlibrary
        >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
        >>> caesar
        Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')

    Returns:
      Author: The Author object.
    """
    global _authors
    if reload is None:
        reload = settings.reload
    else:
        if save is None:
            save = settings.save_on_methods
        else:
            url = url.replace('https://', 'http://')
            if not url.startswith(_endpoint):
                url = _endpoint + url
            if _authors:
                if not reload:
                    try:
                        return next(filter(lambda writer: writer.link == url, _authors))
                    except StopIteration:
                        pass

        text = requests.get(url).text
        parser = BeautifulSoup(text, 'html5lib')
        if '404' in parser.title.string:
            raise NoAuthorException('No author has been found on %s' % url)
        else:
            author = Author(link=url, name=(titleize(parser.title.string)))
            if save:
                if author not in _authors:
                    _authors.append(author)
            return author


def get_author_by_name(name: str, reload: Optional[bool]=None, save: Optional[bool]=None) -> Author:
    """
    Used to return an Author by passing
    a name as an argument.

    Args:
        name (str): The name that should be used to get the author.
        reload (Optional[bool]): If the response should be reloaded and the already stored content ignored.
        save (Optional[bool]): If the response should be saved.

    Example:
        All authors are listed in thelatinlibrary.com index, so it is
        easy to get an author using it.

        >>> import thelatinlibrary
        >>> caesar = thelatinlibrary.get_author_by_name("caesar")
        >>> caesar
        Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')

    Raises:
        NoAuthorException: If no author has been found.

    Returns:
        Author: The Author object.
    """
    if reload is None:
        reload = settings.reload
    else:
        if save is None:
            save = settings.save_on_methods
        if _authors:
            if not reload:
                try:
                    return next(filter(lambda writer: writer.name.lower() == name.lower(), _authors))
                except StopIteration:
                    pass

    text = requests.get(_endpoint + 'indices.html').text
    parser = BeautifulSoup(text, 'html5lib')
    tables = parser.find_all('td')
    for table in tables:
        links = table.find_all('a')
        for link in links:
            if link['href'] not in _exceptions:
                if link.string.strip().rstrip().lower() == name.lower():
                    author = Author(link=(_endpoint + link['href']), name=(titleize(link.string)))
                    if save:
                        if author not in _authors:
                            _authors.append(author)
                    return author

    raise NoAuthorException("There's no %s in the thelatinlibrary.com index." % name)


def get_authors(reload: Optional[bool]=None, save: Optional[bool]=None) -> List[Author]:
    """
    Used to return a list of all the classic
    authors found on thelatinlibrary.com.

    Args:
        reload (Optional[bool]): If the response should be reloaded and the already stored content ignored.
        save (Optional[bool]): If the response should be saved.

    Example:
        There's thelatinlibrary.com index, the function just returns it.

        >>> import thelatinlibrary
        >>> authors = thelatinlibrary.get_authors()
        >>> authors
        [Author(link='http://www.thelatinlibrary.com/abel.historia.html', name='Abelard'), ...,
        Author(link='http://www.thelatinlibrary.com/waardenburg.html', name='Waardenburg')]

    Raises:
        NoAuthorException: If no author has been found.

    Returns:
        List[Author]: A list of all the class authors.
    """
    global _authors
    if reload is None:
        reload = settings.reload
    else:
        if save is None:
            save = settings.save_on_methods
        if _authors:
            if not reload:
                return _authors
        text = requests.get(_endpoint + 'indices.html').text
        parser = BeautifulSoup(text, 'html.parser')
        authors, books, tomes = [], [], []
        tables = parser.find_all('td')
        for table in tables:
            links = table.find_all('a')
            for link in links:
                if link['href'] not in _exceptions:
                    authors.append(Author(link=(_endpoint + link['href']), name=(titleize(link.string))))

        if save:
            _authors = authors
    return authors