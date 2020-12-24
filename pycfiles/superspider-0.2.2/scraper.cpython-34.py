# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\calder\Documents\GitHub\superspider\superspider\scraper.py
# Compiled at: 2017-03-18 13:41:07
# Size of source mod 2**32: 11372 bytes
import urllib.request as req, sys, nltk, string, json, datetime
from bs4 import BeautifulSoup as bsoup
from nltk.corpus import brown

def getBlogSections(tree, silent=False):
    """Gets the sections of a blog."""
    from nltk import word_tokenize
    x = ffilter(tree)
    if len(x) > 1:
        if not silent:
            print('Warning! Found more than one content window!')
        if len(x) == 0:
            if not silent:
                print('Error! No main content window found')
    else:
        if not silent:
            print('Attempting to find sections of text...')
        sectionList = []
        for i in x:
            sectionList.extend(util.getSections(i))

        if not silent:
            print('Stripping json from text found...')
        for i in range(len(sectionList)):
            try:
                json.loads(sectionList[i][1].text)
                if sectionList[i][1].text.strip(string.punctuation) == '':
                    print('DUDE')
                    raise Exception
            except:
                pass
            else:
                sectionList.pop(i)
                if not silent:
                    print('Popped %s' % i)
                    continue

    for i in range(len(sectionList)):
        sectionList[i] = [[], sectionList[i][1].text]

    tIndex = util.data.brown_words
    if not silent:
        print('Associating arbitrary headers with paragraphs...')
    headers = []
    good_headers = []
    for z in x:
        for i in range(1, 7):
            headers.extend([j.text for j in z.findAll('h%s' % i)])

    for i in headers:
        tx = i.strip(string.punctuation.strip('$@#&%')).split(' ')
        try:
            tx = nltk.pos_tag(tx)
        except:
            if not silent:
                print('Hit Error using nltk on a header. Skipping')
            continue

        for i in tx:
            if i[1] == 'NNP' and i[0].strip(string.punctuation) != '':
                try:
                    tIndex[i[0]]
                except KeyError:
                    good_headers.append(i[0])

                if tIndex[i[0]].find('NN') >= 0:
                    good_headers.append(i[0])
                else:
                    continue

    return (
     good_headers, sectionList)


def getGatewaySections(tree):
    raise Exception('FEATURE NOT IMPLIMENTED.')


def printUnscrapable(tree):
    raise Exception('Web page portrays no signifying features, and is too small to scrape.')


def getCompanySections(tree):
    raise Exception('FEATURE NOT IMPLIMENTED.')


def getMiniSections(tree, silent=False):
    """Attempts to find something that is being described by a small, intricate website."""
    from nltk.corpus import stopwords
    from nltk import word_tokenize
    t = tree.text.replace(tree.head.text, '').replace('\n', '').replace('\t\t', '').replace('   ', '').lower()
    t = t.strip(string.punctuation)
    stop = set(stopwords.words('english'))
    t = word_tokenize(t)
    t = [w for w in t if w not in stop]
    count = {}
    for i in t:
        try:
            if util.data.brown_words[i] == 'NNP':
                if i in count:
                    count[i] += 1
                else:
                    count[i] = 1
        except KeyError:
            if i in count:
                count[i] += 1
            else:
                count[i] = 1

    count = [(k, count[k]) for k in count]
    count = sorted(count, reverse=True, key=lambda tup: tup[1])[:5]
    keywords = [x[0] for x in count]
    sections = tree.findAll('p')
    sectionList = []
    for section in sections:
        for i in keywords:
            if ''.join(section.text).lower().find(i.lower()) >= 0:
                sectionList.append([[], section.text])
                break

    return (
     keywords, sectionList)


class util:
    __doc__ = 'Useful fundamental properties and methods.'
    structures = {'blog': getBlogSections, 
     'gateway': getGatewaySections, 
     'unscrapeable': printUnscrapable, 
     'company_home': getCompanySections, 
     'mini': getMiniSections}

    class data:
        content_words = [
         'main', 'content', 'body']
        tags = ['<!DOCTYPE>', '<a>', '<abbr>', '<acronym>', '<address>', '<applet>', '<area>', '<article>', '<aside>', '<audio>', '<b>', '<base>', '<basefont>', '<bdi>', '<bdo>', '<big>', '<blockquote>', '<body>', '<br>', '<button>', '<canvas>', '<caption>', '<center>', '<cite>', '<code>', '<col>', '<colgroup>', '<datalist>', '<dd>', '<del>', '<details>', '<dfn>', '<dialog>', '<dir>', '<div>', '<dl>', '<dt>', '<em>', '<embed>', '<fieldset>', '<figcaption>', '<figure>', '<font>', '<footer>', '<form>', '<frame>', '<frameset>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>', '<header>', '<hr>', '<html>', '<i>', '<iframe>', '<img>', '<input>', '<ins>', '<kbd>', '<keygen>', '<label>', '<legend>', '<li>', '<link>', '<main>', '<map>', '<mark>', '<menu>', '<menuitem>', '<meta>', '<meter>', '<nav>', '<noframes>', '<noscript>', '<object>', '<ol>', '<optgroup>', '<option>', '<output>', '<p>', '<param>', '<picture>', '<pre>', '<progress>', '<q>', '<rp>', '<rt>', '<ruby>', '<s>', '<samp>', '<script>', '<section>', '<select>', '<small>', '<source>', '<span>', '<strike>', '<strong>', '<style>', '<sub>', '<summary>', '<sup>', '<table>', '<tbody>', '<td>', '<textarea>', '<tfoot>', '<th>', '<thead>', '<time>', '<title>', '<tr>', '<track>', '<tt>', '<u>', '<ul>', '<var>', '<video>', '<wbr>']
        brown_words = dict(brown.tagged_words())

    def grabSite(url):
        """Returns a website, already parsed by bs4's BeautifulSoup."""
        try:
            r = req.urlopen(url)
        except:
            raise Exception('unable to GET website [%s].' % url)
        else:
            try:
                t = bsoup(r.read(), 'html.parser')
            except:
                raise Exception('Unable to parse website using BeautifulSoup.')
            else:
                return t

    def getSections(node):

        def divSpider(div):
            total = []
            currentHeader = []
            for n in div.children:
                if n.name:
                    if n.name == 'div':
                        s = divSpider(n)
                        total.extend(s)
                    else:
                        if n.name[0] == 'h' and len(n) == 2:
                            currentHeader = [
                             n.text]
                        else:
                            if n.text.strip() != '':
                                if [].extend(currentHeader):
                                    total.append([[].extend(currentHeader), n])
                                else:
                                    total.append([[], n])
                                currentHeader = []
                            else:
                                continue

            return total

        return divSpider(node)


def rank_tags(tree, silent=False):
    """Goes through all possible html5 tags, and then spits out a list greatest to least. The tuple is as follows: (tag_name,tag_count)."""
    tags = []
    excludes = [
     'body', 'head', '!DOCTYPE', 'title', 'style', 'span', 'html']
    myTags = util.data.tags
    for i in excludes:
        try:
            myTags.remove('<' + i + '>')
        except:
            if not silent:
                print('Intereseting... %s is not in the document.' % ('<' + i + '>'))

    def doStrip(x):
        return x.strip('<>!')

    myTags = list(map(doStrip, myTags))
    for i in myTags:
        x = len(tree.findAll(i))
        if x > 0:
            tags.append((i, x))
            continue

    tags = sorted(tags, reverse=True, key=lambda tup: tup[1])
    return tags


def ffilter(tree, structure='high'):
    """Trys to find a "main content" node in the webpage."""
    good_divs = []
    Ttags = [
     'div', 'section']
    for tag in Ttags:
        for i in util.data.content_words:
            for j in ['id', 'class']:
                good_divs.extend(tree.findAll(tag, {j: i}))

    pops = []
    for p, i in enumerate(good_divs):
        arr = [[p2, z] for p2, z in enumerate(good_divs)]
        arr.pop(p)
        for j in arr:
            if str(i) in str(j):
                pops.append(j[0])
                continue

    for pop in pops:
        good_divs.pop(pop)

    return good_divs


def getHeaders(tree, silent=False):
    """Trys to find the number of headers on the page, out of all the tags that could represent one."""
    ranking = rank_tags(tree, silent=silent)
    headCount = 0
    headerTCount = None
    for tag, count in ranking:
        if tag[0] == 'h':
            if len(tag) == 2:
                headCount += count
        if tag == 'header':
            headerTCount = count
            continue

    if headerTCount != None:
        if headerTCount < headCount:
            headCount = headerTCount
    return headCount


def getSiteType(tree, silent=False):
    """Where the magic happens. Probably the most "algorithm-like" part of the program."""
    LINK_TO_PARAGRAPH_MAX_QUOTIENT = 4
    COMPANY_IMAGE_TO_PARACOUNT_MIN_QUOTIENT = 3
    COMPANY_HEAD_TO_PARA_MIN_QUOTIENT = 2
    COMPANY_MIN_HEAD = 6
    MIN_TEXT = 4000
    MIN_GATEWAY_WINDOWS = 6
    mainWindow = ffilter(tree)
    imgCount = len(tree.findAll('img'))
    paraCount = len(tree.findAll('p'))
    headCount = getHeaders(tree, silent=silent)
    if imgCount / paraCount > COMPANY_IMAGE_TO_PARACOUNT_MIN_QUOTIENT or headCount / paraCount >= COMPANY_HEAD_TO_PARA_MIN_QUOTIENT and headCount >= COMPANY_MIN_HEAD:
        return 'company_home'
    if len(mainWindow) > 0:
        if len(mainWindow) > MIN_GATEWAY_WINDOWS:
            return 'gateway'
        mainWindow = mainWindow[0]
        ranking = rank_tags(mainWindow, silent=silent)
        rankIndex = dict(ranking)
        headers = getHeaders(tree, silent=silent)
        if 'p' in rankIndex:
            if headers > 0:
                if 'a' in rankIndex:
                    if rankIndex['a'] / rankIndex['p'] <= LINK_TO_PARAGRAPH_MAX_QUOTIENT:
                        return 'blog'
                    return 'gateway'
    else:
        ranking = rank_tags(tree, silent=silent)
        rankIndex = dict(ranking)
        headers = getHeaders(tree, silent=silent)
        if 'p' in rankIndex:
            if headers > 0:
                if 'a' in rankIndex:
                    if rankIndex['a'] / rankIndex['p'] > LINK_TO_PARAGRAPH_MAX_QUOTIENT:
                        return 'gateway'
                    if 'img' in rankIndex:
                        if rankIndex['a'] / rankIndex['p'] > LINK_TO_PARAGRAPH_MAX_QUOTIENT / 2 and rankIndex['a'] / rankIndex['img'] >= COMPANY_IMAGE_TO_PARACOUNT_MIN_QUOTIENT:
                            return 'gateway'
            bad = '#$%&"\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            textt = tree.text.replace(tree.head.text, '').strip(bad).replace('\n', '').replace('\t', '').replace(' ', '')
            for i in bad:
                textt = textt.replace(i, '')

            if len(tree.text.strip()) < MIN_TEXT:
                return 'unscrapeable'
            else:
                return 'mini'


def scrape(url, silent=False):
    """Really the "main()" function of the program."""
    global x
    if not silent:
        print('GETting [%s]...' % url)
    x = util.grabSite(url)
    if not silent:
        print('filtering tags in html tree...')
    Stype = getSiteType(x, silent=silent)
    sectionList = None
    if Stype in util.structures:
        if not silent:
            print('IDENTIFIED %s' % Stype)
        good_headers, sectionList = util.structures[Stype](x, silent=silent)
        if sectionList != None:
            good_headers = set(good_headers)
            for title in good_headers:
                for p2, i in enumerate(sectionList):
                    if title.lower() in str(i[1]).lower():
                        sectionList[p2][0].append(title)
                        continue

            output = {'data': sectionList, 
             'time': str(datetime.datetime.now()), 
             'type': Stype}
            return output
    elif not silent:
        print('I AINT GOT NO TYPE')