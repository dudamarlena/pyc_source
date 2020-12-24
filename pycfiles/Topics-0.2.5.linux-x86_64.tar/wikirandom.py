# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/onlineldavb/wikirandom.py
# Compiled at: 2013-03-04 07:17:16
import sys, urllib2, re, string, time, threading

def get_random_wikipedia_article():
    """
    Downloads a randomly selected Wikipedia article (via
    http://en.wikipedia.org/wiki/Special:Random) and strips out (most
    of) the formatting, links, etc. 

    This function is a bit simpler and less robust than the code that
    was used for the experiments in "Online VB for LDA."
    """
    failed = True
    while failed:
        articletitle = None
        failed = False
        try:
            req = urllib2.Request('http://en.wikipedia.org/wiki/Special:Random', None, {'User-Agent': 'x'})
            f = urllib2.urlopen(req)
            while not articletitle:
                line = f.readline()
                result = re.search('title="Edit this page" href="/w/index.php\\?title=(.*)\\&amp;action=edit" /\\>', line)
                if result:
                    articletitle = result.group(1)
                    break
                elif len(line) < 1:
                    sys.exit(1)

            req = urllib2.Request(('http://en.wikipedia.org/w/index.php?title=Special:Export/{0:s}&action=submit').format(articletitle), None, {'User-Agent': 'x'})
            f = urllib2.urlopen(req)
            all = f.read()
        except (urllib2.HTTPError, urllib2.URLError):
            print 'oops. there was a failure downloading %s. retrying...' % articletitle
            failed = True
            continue

        print 'downloaded %s. parsing...' % articletitle
        try:
            all = re.search('<text.*?>(.*)</text', all, flags=re.DOTALL).group(1)
            all = re.sub('\\n', ' ', all)
            all = re.sub('\\{\\{.*?\\}\\}', '', all)
            all = re.sub('\\[\\[Category:.*', '', all)
            all = re.sub('==\\s*[Ss]ource\\s*==.*', '', all)
            all = re.sub('==\\s*[Rr]eferences\\s*==.*', '', all)
            all = re.sub('==\\s*[Ee]xternal [Ll]inks\\s*==.*', '', all)
            all = re.sub('==\\s*[Ee]xternal [Ll]inks and [Rr]eferences==\\s*', '', all)
            all = re.sub('==\\s*[Ss]ee [Aa]lso\\s*==.*', '', all)
            all = re.sub('http://[^\\s]*', '', all)
            all = re.sub('\\[\\[Image:.*?\\]\\]', '', all)
            all = re.sub('Image:.*?\\|', '', all)
            all = re.sub('\\[\\[.*?\\|*([^\\|]*?)\\]\\]', '\\1', all)
            all = re.sub('\\&lt;.*?&gt;', '', all)
        except:
            print 'oops. there was a failure parsing %s. retrying...' % articletitle
            failed = True
            continue

    return (
     all, articletitle)


class WikiThread(threading.Thread):
    articles = list()
    articlenames = list()
    lock = threading.Lock()

    def run(self):
        article, articlename = get_random_wikipedia_article()
        WikiThread.lock.acquire()
        WikiThread.articles.append(article)
        WikiThread.articlenames.append(articlename)
        WikiThread.lock.release()


def get_random_wikipedia_articles(n):
    """
    Downloads n articles in parallel from Wikipedia and returns lists
    of their names and contents. Much faster than calling
    get_random_wikipedia_article() serially.
    """
    maxthreads = 8
    WikiThread.articles = []
    WikiThread.articlenames = []
    wtlist = []
    for i in range(0, n, maxthreads):
        print 'downloaded %d/%d articles...' % (i, n)
        for j in range(i, min(i + maxthreads, n)):
            wtlist.append(WikiThread())
            wtlist[(len(wtlist) - 1)].start()

        for j in range(i, min(i + maxthreads, n)):
            wtlist[j].join()

    return (
     WikiThread.articles, WikiThread.articlenames)


if __name__ == '__main__':
    t0 = time.time()
    articles, articlenames = get_random_wikipedia_articles(1)
    for i in range(len(articles)):
        print articlenames[i]

    t1 = time.time()
    print 'took %f' % (t1 - t0)