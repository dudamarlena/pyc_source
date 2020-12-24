# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kinopoisk/utils.py
# Compiled at: 2018-08-23 15:22:19
from __future__ import unicode_literals
import re, six, unicodedata
from builtins import str
HEADERS = {b'User-Agent': b'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.1.8) Gecko/20100214 Linux Mint/8 (Helena) Firefox/3.5.8', 
   b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
   b'Accept-Language': b'ru,en-us;q=0.7,en;q=0.3', 
   b'Accept-Encoding': b'deflate', 
   b'Accept-Charset': b'windows-1251,utf-8;q=0.7,*;q=0.7', 
   b'Keep-Alive': b'300', 
   b'Connection': b'keep-alive', 
   b'Referer': b'http://www.kinopoisk.ru/', 
   b'Cookie': b'users_info[check_sh_bool]=none; search_last_date=2010-02-19; search_last_month=2010-02;                                        PHPSESSID=b6df76a958983da150476d9cfa0aab18'}

class Manager(object):
    kinopoisk_object = None
    search_url = None

    def __init__(self):
        import requests
        self.request = requests.Session()

    def search(self, query):
        url, params = self.get_url_with_params(query)
        response = self.request.get(url, params=params, headers=HEADERS)
        response.connection.close()
        content = response.content.decode(b'windows-1251', b'ignore')
        if len(response.history) and (b'/film/' in response.url or b'/name/' in response.url):
            instance = self.kinopoisk_object()
            instance.get_source_instance(b'main_page', instance=instance, content=content, request=self.request).parse()
            return [
             instance]
        if content.find(b'<h2 class="textorangebig" style="font:100 18px">') != -1:
            return []
        content_results = content[content.find(b'<div class="search_results">'):content.find(b'<div style="height: 40px"></div>')]
        if content_results:
            from bs4 import BeautifulSoup
            soup_results = BeautifulSoup(content_results, b'html.parser')
            results = soup_results.findAll(b'div', attrs={b'class': re.compile(b'element')})
            if not results:
                raise ValueError(b'No objects found in search results by request "%s"' % response.url)
            instances = []
            for result in results:
                instance = self.kinopoisk_object.get_parsed(b'link', str(result))
                if instance.id:
                    instances += [instance]

            return instances
        raise ValueError(b'Unknown html layout found by request "%s"' % response.url)

    def get_url_with_params(self, query):
        return (
         b'http://www.kinopoisk.ru/index.php', {b'kp_query': query})

    def get_first(self, query):
        self.search(query)


class KinopoiskObject(object):
    id = None
    objects = None
    _urls = {}
    _sources = []
    _source_classes = {}

    def __init__(self, id=None, **kwargs):
        if id:
            self.id = id
        self.set_defaults()
        self.__dict__.update(kwargs)

    def set_defaults(self):
        pass

    def parse(self, name, content):
        """Parse using registered parser `name` and content"""
        self.get_source_instance(name, instance=self, content=content).parse()

    def get_content(self, name):
        """Populate instance with data from source `name`"""
        self.get_source_instance(name, instance=self).get()

    @classmethod
    def get_parsed(cls, name, content):
        """Initialize, parse and return instance"""
        instance = cls()
        instance.parse(name, content)
        return instance

    def register_source(self, name, class_name):
        try:
            self.set_url(name, class_name.url)
        except AttributeError:
            pass

        self.set_source(name)
        self._source_classes[name] = class_name

    def set_url(self, name, url):
        self._urls[name] = url

    def get_url(self, name, postfix=b'', **kwargs):
        url = self._urls.get(name)
        if not url:
            raise ValueError(b'There is no urlpage with name "%s"' % name)
        if not self.id:
            raise ValueError(b'ID of object is empty')
        kwargs[b'id'] = self.id
        return (b'http://www.kinopoisk.ru' + url).format(**kwargs) + postfix

    def set_source(self, name):
        if name not in self._sources:
            self._sources += [name]

    def get_source_instance(self, name, **kwargs):
        class_name = self._source_classes.get(name)
        if not class_name:
            raise ValueError(b'There is no source with name "%s"' % name)
        instance = class_name(name, **kwargs)
        return instance


class KinopoiskImage(KinopoiskObject):

    def __init__(self, id=None):
        super(KinopoiskImage, self).__init__(id)
        self.set_url(b'picture', b'/picture/{id}/')

    def get_url(self, name=b'picture', postfix=b'', **kwargs):
        return super(KinopoiskImage, self).get_url(name, postfix=postfix, **kwargs)


class KinopoiskPage(object):
    content = None

    def __init__(self, source_name, instance, content=None, request=None):
        import requests
        self.request = request or requests.Session()
        self.source_name = source_name
        self.instance = instance
        if content is not None:
            self.content = content
        return

    @property
    def element(self):
        return self.content

    @property
    def xpath(self):
        raise NotImplementedError()

    def extract(self, name, to_str=False, to_int=False, to_float=False):
        if name in self.xpath:
            xpath = self.xpath[name]
            elements = self.element.xpath(xpath)
            if xpath[-7:] == b'/text()' or b'/@' in xpath:
                value = (b' ').join(elements) if elements else b''
            else:
                value = elements
            if value:
                if to_str:
                    value = self.prepare_str(value)
                if to_int:
                    value = self.prepare_int(value)
                if to_float:
                    value = float(value)
            return value
        raise ValueError((b'Xpath element with name `{}` is not configured').format(name))

    def prepare_str(self, value):
        if six.PY2:
            value = re.compile(b'\xa0').sub(b' ', value)
            value = re.compile(b'\x97').sub(b'—', value)
            value = re.compile(b', \\.\\.\\.').sub(b'', value)
        else:
            value = unicodedata.normalize(b'NFKC', value)
        value = restore_characters(value)
        return value.strip()

    def prepare_int(self, value):
        value = self.prepare_str(value)
        value = value.replace(b' ', b'')
        value = int(value)
        return value

    def prepare_date(self, value):
        value = self.prepare_str(value).strip()
        if not value:
            return None
        else:
            months = [
             b'января', b'февраля', b'марта', b'апреля', b'мая', b'июня',
             b'июля', b'августа', b'сентября', b'октября', b'ноября', b'декабря']
            for i, month in enumerate(months, start=1):
                if month in value:
                    value = value.replace(month, b'%02d' % i)
                    break

            value = value.replace(b'\xa0', b'-')
            from dateutil import parser
            return parser.parse(value, dayfirst=True).date()

    def prepare_profit(self, value):
        profit = value
        if b'=' in profit:
            profit = profit[profit.index(b'=') + 1:]
        profit = (b'').join(profit.split())
        profit = profit[1:]
        return self.prepare_int(profit)

    def find_profit(self, td):
        for tag in [td.find(b'a'), td.find(b'div')]:
            if tag:
                for value in tag.contents:
                    if b'$' in value:
                        return self.prepare_profit(value)

    def cut_from_to(self, content, after, before):
        start = content.find(after)
        end = content.find(before)
        if start != -1 and end != -1:
            content = content[start:end]
        return content

    def get(self):
        if self.instance.id:
            response = self.request.get(self.instance.get_url(self.source_name), headers=HEADERS)
            response.connection.close()
            self.content = response.content.decode(b'windows-1251', b'ignore')
            self.parse()
            return
        raise NotImplementedError(b'This method must be implemented in subclass')

    def parse(self):
        raise NotImplementedError(b'You must implement KinopoiskPage.parse() method')


class KinopoiskImagesPage(KinopoiskPage):
    """
    Parser of kinopoisk images page
    """
    field_name = None

    def get(self, page=1):
        response = self.request.get(self.instance.get_url(self.source_name, postfix=(b'page/{}/').format(page)), headers=HEADERS)
        response.connection.close()
        content = response.content.decode(b'windows-1251', b'ignore')
        if re.findall(b'<h1 class="main_title">', content):
            return False
        content = content[content.find(b'<div style="padding-left: 20px">'):content.find(b'        </td></tr>')]
        from bs4 import BeautifulSoup
        soup_content = BeautifulSoup(content, b'html.parser')
        table = soup_content.findAll(b'table', attrs={b'class': re.compile(b'^fotos')})
        if table:
            self.content = str(table[0])
            self.parse()
            if len(getattr(self.instance, self.field_name)) % 21 == 0:
                try:
                    self.get(page + 1)
                except ValueError:
                    return

        else:
            raise ValueError(b'Parse error. Do not found posters for movie %s' % self.instance.get_url(b'posters'))

    def parse(self):
        urls = getattr(self.instance, self.field_name, [])
        from bs4 import BeautifulSoup
        links = BeautifulSoup(self.content, b'html.parser').findAll(b'a')
        for link in links:
            img_id = re.compile(b'/picture/(\\d+)/').findall(link[b'href'])
            picture = KinopoiskImage(int(img_id[0]))
            response = self.request.get(picture.get_url(), headers=HEADERS)
            response.connection.close()
            content = response.content.decode(b'windows-1251', b'ignore')
            img = BeautifulSoup(content, b'html.parser').find(b'img', attrs={b'id': b'image'})
            if img:
                img_url = img[b'src']
                if img_url not in urls:
                    urls.append(img_url)

        setattr(self.instance, self.field_name, urls)
        self.instance.set_source(self.source_name)


def restore_characters(s):
    """Replace C1 control characters in the Unicode string s by the
    characters at the corresponding code points in Windows-1252,
    where possible.
    """

    def restore(match):
        try:
            return bytes([ord(match.group(0))]).decode(b'windows-1251')
        except UnicodeDecodeError:
            return b''

    return re.sub(b'[\x80-\x99]', restore, s)