# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: scrp/__init__.py
# Compiled at: 2018-02-17 10:40:37
import random, re
from bs4.element import Comment, Doctype, NavigableString, Tag
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from numpy import mean, median, std
from urlparse import urlparse
from re import IGNORECASE, match, MULTILINE, sub, UNICODE
flags = IGNORECASE | MULTILINE | UNICODE
from error_page import *
import firefox
from headers import *
from http import *
from statements import *

def getDomainFromUrlString(url):
    url_parsed = urlparse(url)
    return url_parsed.scheme + '://' + url_parsed.netloc


def isHrefDocument(href):
    return href[-4:] in ('.pdf', '.doc', '.xls', '.xml')


def isHrefFile(href):
    return href[-4:] in ('.pdf', '.doc', '.xls', 'xlsx', '.xml', '.mp3', '.mp4', 'webm',
                         '.mov')


def isHrefHttp(href):
    return urlparse(href).scheme in ('http', 'https', '')


def isUrlRelevant(url):
    return not any(word in url for word in ['about', 'amazon', 'ads', 'captcha', 'condition', 'contact', 'cookie', 'copyright', 'wikipedia.org/w/index.php?title=', 'log', 'privacy', 'registrat', 'robot', 'sign', 'term'])


def isEnoughText(text):
    totalNumberOfChars = len(text)
    totalNumberOfBlankChars = text.count(' ') + text.count('\n') + text.count('\r')
    totalNumberOfNonBlankChars = totalNumberOfChars - totalNumberOfBlankChars
    if totalNumberOfNonBlankChars > 20:
        return True
    else:
        return False


def isHtml(text):
    return text.count('<') > 5 and text.count('>') > 5


def isJavaScript(inputString):
    numberOfCharacters = len(inputString)
    if numberOfCharacters != 0:
        countOfSpecial = inputString.count(';') + inputString.count('=') + inputString.count('var') + inputString.count('{') + inputString.count('}') + inputString.count(':') + inputString.count('"')
        percentage = float(countOfSpecial) / float(numberOfCharacters)
        if percentage > 0.01:
            return True
    return False


def isWikipediaArticle(text):
    return 'From Wikipedia, the free encyclopedia' in text


def reformHref(domain, href):
    domain_parsed = urlparse(domain)
    href_parsed = urlparse(href)
    if href_parsed.scheme == '':
        if domain_parsed.scheme == '':
            url_string = 'http'
        else:
            url_string = domain_parsed.scheme
    else:
        url_string = href_parsed.scheme
    url_string += '://'
    if href_parsed.netloc in ('', '..') or '.' not in href_parsed.netloc:
        url_string += domain_parsed.netloc
    else:
        url_string += href_parsed.netloc
    if href_parsed.path[:3] == '://':
        url_string += href_parsed[2:]
    else:
        url_string += href_parsed.path
    if href_parsed.scheme == '' and href_parsed.netloc == '' and href_parsed.path == '' and href_parsed.params == '' and href_parsed.query == '':
        url_string += '#' + href_parsed.fragment
    if url_string.count('//') > 1:
        pass
    return url_string


def getRandomUserAgentString():
    listOfUserAgentStrings = [
     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; ARM; Trident/6.0)', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0', 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0', 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0']
    return random.choice(listOfUserAgentStrings)


def getTitleFromSoup(soup):
    soup_title = str(soup.title)
    if soup_title:
        return soup_title.replace('<title>', '').replace('</title>', '').split(' -')[0].strip().split(' |')[0].strip()
    else:
        return
        return


def isHeader(text):
    text = text.lower()
    return sum(word in text for word in ('about', 'contact', 'goals', 'principles')) >= 4


def getMostRepeatedContentFromSoup(soup, test=None, testTagName=None, testChildren=None):
    candidates = []
    for index, element in enumerate(list(soup.descendants)):
        if not isinstance(element, Doctype) and not isinstance(element, NavigableString) and not isinstance(element, Comment):
            children = list(element.children)
            children = [ c for c in children if c.name and c.text.strip() ]
            number_of_children = len(children)
            if number_of_children >= 5:
                names = [ child.name for child in children ]
                counter = Counter(names)
                tagName, count = counter.most_common(1)[0]
                if tagName is None:
                    tagName, count = counter.most_common(2)[1]
                if tagName and count >= 5 and testTagName(tagName) if testTagName else True:
                    freq = float(count) / float(number_of_children)
                    if freq > 0.5:
                        if test(element):
                            posts = [ child for child in children if child.name == tagName ]
                            if 100 < median([ len(child.text) for child in posts ]) < 1000:
                                candidate = {}
                                candidate['element'] = element
                                candidate['children'] = posts
                                candidates.append(candidate)

    number_of_candidates = len(candidates)
    if number_of_candidates == 0:
        pass
    elif number_of_candidates == 1:
        return list(candidates[0]['children'])
    if number_of_candidates > 1:
        for candidate in candidates:
            candidate['average_length_of_child'] = median([ len(child.text) for child in candidate['children'] ])

        candidates.sort(key=lambda x: -1 * x['average_length_of_child'])
    return


def getPostUrlsFromSoup(soup):
    script = '\n    var candidates = [];\n    var elements = document.body.querySelector("*");\n    for (var a = 0; a < elements.length; a++) {\n        var element = elements[a];\n    }\n\n    '
    return driver.execute_script(script)


GET_POST_ELEMENTS_JAVASCRIPT = '\n\n    var posts = [];\n\n    var elements = Array.prototype.slice.call(document.body.getElementsByTagName("*"));\n\n    elements = elements.filter(function(element){\n        return element.textContent.length > 100;\n    });\n\n    elements = elements.filter(function(element){\n        return element.clientHeight > 500;\n    });\n\n    elements = elements.filter(function(element){\n        return element.clientWidth > 300;\n    });\n\n\n    for (var a = 0 ; a < elements.length; a++) {\n        element = elements[a];\n        children = Array.prototype.slice.call(element.children);\n        children = children.filter(function(child){\n            return child.textContent.length > 0;\n        });\n\n        if (children.length >= 5) {\n            names = children.map(function(child){return child.tagName;});\n            counter = {};\n            names.forEach(function(name) {\n                counter[name] = counter[name] + 1 || 1\n            });\n            most_common_tag_name = 0; most_common_count = 0;\n            for (var tagName in counter) {\n                if (counter[tagName] > most_common_count) {\n                    most_common_count = counter[tagName];\n                    most_common_tag_name = tagName;\n                }\n            }\n\n            if (most_common_count >= 5) {\n                console.log("children are", children);\n                posts = posts.concat(children);\n            }\n        }\n    }\n\n'

def getPostsFromSoup(soup, selector_for_posts=None):
    print 'starting getPostsFromSoup with ', type(soup), str(soup)[:200]
    if selector_for_posts:
        posts = soup.select(selector_for_posts)
        if posts:
            return posts
    candidates = []
    for index, element in enumerate(list(soup.descendants)):
        if not isinstance(element, Doctype) and not isinstance(element, NavigableString) and not isinstance(element, Comment):
            element_text = element.text
            if not isHeader(element_text) and len(element_text) > 100:
                children = list(element.children)
                children = [ c for c in children if c.name and c.text.strip() ]
                number_of_children = len(children)
                if number_of_children >= 5:
                    names = [ child.name for child in children ]
                    counter = Counter(names)
                    tagName, count = counter.most_common(1)[0]
                    if tagName is None:
                        tagName, count = counter.most_common(2)[1]
                    if tagName and count >= 5 and tagName not in ('p', 'head', 'script'):
                        freq = float(count) / float(number_of_children)
                        if freq > 0.5:
                            posts = [ child for child in children if child.name == tagName ]
                            number_of_posts = len(posts)
                            counter_of_classes = Counter()
                            for post in posts:
                                counter_of_classes.update(post.get('class'))

                            shared_classes = []
                            for classname, count in counter_of_classes.iteritems():
                                if count >= number_of_posts - 1:
                                    shared_classes.append(classname)

                            if len(shared_classes) >= 4:
                                posts = [ p for p in posts if any([ sc in p.get('class') for sc in shared_classes ]) ]
                            texts = [ post.text.replace(' ', '').replace('\n', '') for post in posts ]
                            lengths_of_posts = [ len(text) for text in texts ]
                            median_of_posts = median(lengths_of_posts)
                            standard_deviation_of_posts = std(lengths_of_posts)
                            if 100 < median_of_posts < 2000 and standard_deviation_of_posts < 200:
                                candidate = {}
                                candidate['element'] = element
                                candidate['children'] = posts
                                candidates.append(candidate)

    number_of_candidates = len(candidates)
    if number_of_candidates == 0:
        pass
    elif number_of_candidates == 1:
        return list(candidates[0]['children'])
    if number_of_candidates > 1:
        for candidate in candidates:
            candidate['average_length_of_child'] = median([ len(child.text) for child in candidate['children'] ])

        candidates_with_keywords = [ c for c in candidates if findStatementsHrefFromSoup(c['element']) ]
        number_of_candidates_with_keyword = len(candidates_with_keywords)
        if number_of_candidates_with_keyword == 0:
            candidates.sort(key=lambda x: -1 * x['average_length_of_child'])
            return candidates[0]['children']
        if number_of_candidates_with_keyword == 1:
            return candidates_with_keywords[0]['children']
        if number_of_candidates_with_keyword > 1:
            candidates_with_keywords.sort(key=lambda x: -1 * x['average_length_of_child'])
            return candidates_with_keywords[0]['children']
    return


def OLDgetAPostsFromSoup(soup):
    testChildren = lambda x: mean([ len(e) for e in x ]) > 100
    testTagName = lambda tagName: tagName not in ('p', 'head', 'script')
    return getMostRepeatedContentFromSoup(soup, test=test, testTagName=testTagName, testChildren=testChildren)


def getPostsFromText(text):
    return getPostsFromSoup(BeautifulSoup(text, 'html.parser'))


def removeCommentsFromElement(element):
    descendants = list(element.descendants)
    for tag in descendants:
        if tag and isinstance(tag, Comment):
            try:
                tag.extract()
            except:
                pass

    return element


def trimElement(soup):
    descendants = list(soup.descendants)
    for tag in soup.descendants:
        if isinstance(tag, Comment):
            tag.extract()
        elif isinstance(tag, NavigableString):
            pass
        elif isinstance(tag, Tag):
            continue

    return soup


def getVisibleTextFromElement(element):
    [ e.decompose() for e in body('script') ]
    [ e.decompose() for e in body('style') ]
    [ e.decompose() for e in body('title') ]
    [ e.extract() for e in body(text=lambda x: isinstance(x, Comment))
    ]
    return (' ').join([ unicode(e) for e in element(text=True) ])


def getMainPartFromSoup(soup, selector=None):
    found_via_selector = False
    if selector:
        soup_select_selector = soup.select(selector)
        if len(soup_select_selector) == 1:
            element = soup_select_selector[0]
            selected = {'element': element, 'text': element.text, 'selector': selector}
            found_via_selector = True
    if not found_via_selector:
        body = soup.body
        regex_side = re.compile('.*side.*')
        [ e.decompose() for e in body('iframe') ]
        [ e.decompose() for e in body('script') ]
        [ e.decompose() for e in body('style') ]
        [ e.decompose() for e in body('title') ]
        [ e.extract() for e in body(text=lambda x: isinstance(x, Comment)) ]
        [ e.extract() for e in body(id=regex_side) ]
        [ e.extract() for e in body(class_='articles_section') ]
        [ e.extract() for e in body('header') ]
        [ e.extract() for e in body(id=re.compile('.*header.*')) ]
        [ e.extract() for e in body(class_='header') ]
        [ e.extract() for e in body('footer') ]
        [ e.extract() for e in body(id=re.compile('.*footer.*')) ]
        [ e.extract() for e in body(class_='footer') ]
        text = body.text
        length = len(text)
        selected = {'element': body, 'length': length, 'text': text}
        count = 0
        while True:
            max_length = 0
            candidate = None
            children = selected['element'].contents
            for child in children:
                if not isinstance(child, Doctype) and not isinstance(child, NavigableString):
                    if child.name not in ('script', 'link') and child.get('id') not in ('ja-right',
                                                                                        'ja-left'):
                        text = child.text
                        length = len(text)
                        if length > max_length:
                            max_length = length
                            candidate = {'element': child, 'length': length, 'text': text}

            if candidate and float(candidate['length']) / float(selected['length']) > 0.5:
                selected = candidate
            else:
                break
            if count > 2000:
                break
            else:
                count += 1

        selected['selector'] = getSelectorFromElement(selected['element'].parent) + ' > ' + getSelectorFromElement(selected['element'])
    text = sub('[\r\n]+[\r\n\t ]*[\r\n]+', '\r\n\r\n', selected['text'], flags=flags)
    text = sub('\t+', ' ', text)
    text = text.replace('\xa0', ' ')
    selected['text'] = text
    text = text.strip()
    return selected


def getSelectorFromElement(element):
    selector = element.name
    element_id = element.get('id')
    if element_id:
        selector += '#' + element_id
    classAsList = element.get('class')
    if classAsList:
        selector += '.' + ('.').join(classAsList)
    return selector


def getMainPartFromText(text, selector=None):
    mainPart = getMainPartFromSoup(BeautifulSoup(text, 'html5lib'), selector=selector)
    return mainPart


def getCleanTextFromSoup(soup):
    body = soup.body
    regex_side = re.compile('.*side.*')
    [ e.decompose() for e in body('script') ]
    [ e.decompose() for e in body('style') ]
    [ e.decompose() for e in body('title') ]
    [ e.extract() for e in body(text=lambda x: isinstance(x, Comment)) ]
    [ e.extract() for e in body(id=regex_side) ]
    [ e.extract() for e in body(class_='articles_section') ]
    [ e.extract() for e in body('header') ]
    [ e.extract() for e in body(id=re.compile('.*header.*')) ]
    [ e.extract() for e in body(class_='header') ]
    [ e.extract() for e in body('footer') ]
    [ e.extract() for e in body(id=re.compile('.*footer.*')) ]
    [ e.extract() for e in body(class_='footer') ]
    text = body.text
    text = sub('[\r\n]+[\r\n\t ]*[\r\n]+', '\r\n\r\n', text, flags=flags)
    text = sub('\t+', ' ', text)
    text = text.replace('\xa0', ' ')
    return text


def getCleanTextFromText(text):
    return getCleanTextFromSoup(BeautifulSoup(text, 'html5lib'))


def getMainTextFromSoup(text):
    return getMainPartFromSoup(soup)['text']


def getMainTextFromText(text):
    return getMainPartFromSoup(BeautifulSoup(text, 'html5lib'))['text']


def getMainTextFromUrl(url):
    return getMainTextFromText(getAnonymouslyViaCurl(url)['html'])


x = getMainTextFromText
terms = {}
terms['ar'] = ('ar', 'arabic', 'عربي')
terms['en'] = ('en', 'english')
terms['fr'] = ('fr', 'french')
terms['tr'] = ('tr', 'turkish', 'Türkçe')
terms['ku'] = ('ku', 'kurdish')
terms['ku-so'] = ('sorani', 'كوردى')
terms['ku-ku'] = ('kurmanci', 'kurmanji', 'kurmangi', 'Kurdî', 'Daxuyanî')

def getLanguageVersionUrlsFromDriver(driver):
    d = {}
    script = '\n    result = {};\n    var terms = {};\n    terms.ar = ["ar","arabic","\\u0639\\u0631\\u0628\\u064a","\\u0061\\u0072\\u0061\\u0062\\u0069\\u0063  \\u0639\\u0631\\u0628\\u064a"];\n    terms.en = ["en","english"];\n    terms.fr = ["fr","french"];\n    terms.tr = ["tr","turkish"];\n    terms.ku = ["ku","kurdish"];\n    terms.ku_so = ["sorani"];\n    terms.ku_ku = ["kurmanci","kurmanji","kurmangi"];\n    var a_tags = document.getElementsByTagName("a");\n    for (var i = 0; i < a_tags.length; i++) {\n        a_tag = a_tags[i];\n        href = a_tag.href;\n        if (href) {\n            // the regex trims it\n            text = a_tag.textContent.toLocaleLowerCase().replace(/^\\s+|\\s+$/g, \'\');\n            if (text) {\n                for (var key in terms) {\n                    var key_terms = terms[key];\n                    if (key_terms.indexOf(text) > -1) {\n                        if (href.startsWith("http")) {\n                            result[key] = href;\n                        }\n                        else {\n                            result[key] = document.location.origin + href;\n                        }\n                    }\n                }\n            }\n        }\n    }\n    return result;\n    '
    return driver.execute_script(script)


def getLanguageVersionUrlsFromSoup(soup, domain):
    d = {}
    for a in soup.findAll('a', href=True):
        text = a.text.lower().strip()
        href = a['href']
        for key, values in terms.iteritems():
            if text in values:
                if href.startswith('http'):
                    d[key] = href
                else:
                    d[key] = domain + href

    return d


def getLanguageVersionUrlsFromText(text):
    return getLanguageVersionUrlsFromSoup(BeautifulSoup(text))


def guessLanguageOfUrl(url):
    for key, values in terms.iteritems():
        if re.search('(' + ('|').join(values) + ')', url):
            return key


def getUrlsFromSoup(soup, domain, selectors_for_post=None):
    domain = domain.lower()
    print '\nstarting getUrlsFromSoup with', type(soup), 'and', domain
    posts = getPostsFromSoup(soup, selectors_for_post)
    print '\tposts from getPostsFromSoup = ', len(posts or [])
    if posts:
        hrefs = []
        for post in posts:
            for a in post.findAll('a', href=True):
                href = a['href']
                href_lower = href.lower()
                if not any(href_lower.endswith(ext) for ext in ('gif', 'jpeg', 'jpg',
                                                                'png')):
                    if href_lower.startswith('http'):
                        if href_lower.startswith(domain):
                            hrefs.append(href)
                    elif href_lower.startswith('javascript'):
                        pass
                    else:
                        hrefs.append(domain + href)

        return hrefs


def getUrlsFromText(text, domain):
    open('/tmp/text.html', 'wb').write(text.encode('utf-8'))
    return getUrlsFromSoup(BeautifulSoup(text, 'html5lib'), domain)