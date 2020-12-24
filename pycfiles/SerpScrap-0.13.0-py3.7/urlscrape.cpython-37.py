# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\serpscrap\urlscrape.py
# Compiled at: 2018-08-26 07:33:12
# Size of source mod 2**32: 6702 bytes
"""SerpScrap.UrlScrape"""
import chardet, hashlib, html2text, json, re, urllib.request, os
from bs4 import BeautifulSoup

class UrlScrape:
    meta_robots_pattern = re.compile('<meta\\sname=["\\\']robots["\\\']\\scontent=["\\\'](.*?)["\\\']\\s/>')
    meta_title_pattern = re.compile('<title[^>]*>([^<]+)</title>')
    results = []

    def __init__(self, config=None):
        self.cache_dir = config['cachedir']
        self.url_threads = config['url_threads']
        UrlScrape.assure_path_exists(self.cache_dir)

    @staticmethod
    def assure_path_exists(cache_dir):
        cache_dir = os.path.dirname(cache_dir)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    @staticmethod
    def adjust_encoding(data):
        """detect and adjust encoding of data return data decoded to utf-8"""
        check_encoding = chardet.detect(data)
        if 'utf-8' not in check_encoding['encoding']:
            try:
                data = data.decode(check_encoding['encoding']).encode('utf-8')
            except:
                pass

        try:
            data = data.decode('utf-8')
        except:
            data = data.decode('utf-8', 'ignore')

        return {'encoding':check_encoding['encoding'], 
         'data':data}

    def scrap_url(self, url):
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        cache_file = os.path.join(self.cache_dir, m.hexdigest() + '.json')
        try:
            with open(cache_file) as (json_data):
                result = json.load(json_data)
                json_data.close()
                UrlScrape.results.append(result)
        except:
            try:
                result = UrlScrape.fetch_url(url, cache_file)
            except:
                pass

        return result

    @staticmethod
    def fetch_url(url, cache_file):
        result = {}
        try:
            with urllib.request.urlopen(url) as (response):
                html = response.read()
                encoded = UrlScrape.adjust_encoding(data=html)
                html = encoded['data']
                for sign in ('[', ']', '(', ')'):
                    html = html.replace(sign, ' ')

                for sign in ('»', ):
                    html = html.replace(sign, '')

                meta_robots = UrlScrape.meta_robots_pattern.findall(html)
                meta_title = UrlScrape.meta_title_pattern.findall(html)
                if len(meta_robots) > 0:
                    result.update({'meta_robots': meta_robots[0][0:15]})
                else:
                    result.update({'meta_robots': ''})
                if len(meta_title) > 0:
                    result.update({'meta_title': meta_title[0]})
                else:
                    result.update({'meta_title': ''})
                result.update({'status': response.getcode()})
                result.update({'url': response.geturl()})
                result.update({'encoding': encoded['encoding']})
                headers = dict(response.getheaders())
                if 'Last-Modified' in headers.keys():
                    result.update({'last_modified': headers['Last-Modified']})
                else:
                    result.update({'last_modified': None})
                h = html2text.HTML2Text()
                h.ignore_links = True
                h.ignore_images = True
                txt = split_into_sentences(BeautifulSoup(h.handle(html), 'html.parser').get_text().replace('\n', ' '))
                row_count = len(txt)
                word_sum = 0
                tmp_txt = []
                for row in txt:
                    row = row.replace('*', '').replace('#', '').replace('_', '').replace('\t', '').replace('   ', ' ').replace('  ', ' ')
                    row = ' '.join([word for word in row.split(' ') if len(word) > 1])
                    word_sum += len(row.split(' '))
                    tmp_txt.append(row)

                avg_row_length = int(word_sum / row_count)
                clean_txt = ''
                for row in tmp_txt:
                    word_count = len(row.split(' '))
                    if 2 < word_count < avg_row_length * 3:
                        clean_txt += row + '\n'

                result.update({'text_raw': clean_txt})
                with open(cache_file, 'w') as (fp):
                    json.dump(result, fp)
        except:
            pass

        return result


ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = ascii_lowercase.upper()
abbr_capped = '|'.join([
 'ala|ariz|ark|calif|colo|conn|del|fla|ga|ill|ind|kan|ky|la|md|mass|mich|minn|miss|mo|mont|neb|nev|okla|ore|pa|tenn|vt|va|wash|wis|wyo',
 'u.s',
 'mr|ms|mrs|msr|dr|gov|pres|sen|sens|rep|reps|prof|gen|messrs|col|sr|jf|sgt|mgr|fr|rev|jr|snr|atty|supt|hr',
 'ave|blvd|st|rd|hwy',
 'jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec',
 '|'.join(ascii_lowercase)]).split('|')
abbr_lowercase = 'etc|v|vs|viz|al|pct'
exceptions = 'U.S.|U.N.|E.U.|F.B.I.|C.I.A.'.split('|')

def is_abbreviation(dotted_word):
    clipped = dotted_word[:-1]
    if clipped[0] in ascii_uppercase:
        if clipped.lower() in abbr_capped:
            return True
        return False
    else:
        if clipped in abbr_lowercase:
            return True
        return False


def is_sentence_ender(word):
    if word in exceptions:
        return False
    else:
        if word[(-1)] in ('?', '!', ' .', ' .'):
            return True
        if len(re.sub('[^A-Z]', '', word)) > 1:
            return True
        if word[(-1)] == '.':
            return is_abbreviation(word) or True
    return False


def split_into_sentences(text):
    potential_end_pat = re.compile(''.join([
     "([\\w\\.'’&\\]\\)]+[\\.\\?!])",
     '([‘’“”\'\\"\\)\\]]*)',
     '(\\s+(?![a-z\\-–—]))']), re.U)
    dot_iter = re.finditer(potential_end_pat, text)
    end_indices = [x.start() + len(x.group(1)) + len(x.group(2)) for x in dot_iter if is_sentence_ender(x.group(1))]
    spans = zip([None] + end_indices, end_indices + [None])
    sentences = [text[start:end].strip() for start, end in spans]
    return sentences