# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/htmlCleaner.py
# Compiled at: 2016-10-08 10:29:41
"""
*using the Readability API to clean up a local html file*

:Author:
    David Young

:Date Created:
    October  1, 2016
"""
import sys, os, codecs, re
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from polygot import authenticate

class htmlCleaner:
    """
    *A parser/cleaner to strip a webpage article of all cruft and neatly present it with some nice css*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``url`` -- the URL to the HTML page to parse and clean
        - ``outputDirectory`` -- path to the directory to save the output html file to
        - ``title`` -- title of the document to save. If *False* will take the title of the HTML page as the filename. Default *False*.
        - ``style`` -- add polygot's styling to the HTML document. Default *True*
        - ``metadata`` -- include metadata in generated HTML. Default *True*
        - ``h1`` -- include title as H1 at the top of the doc. Default *True*

    **Usage:**

        To generate the HTML page, using the title of the webpage as the filename:

        .. code-block:: python 

            from polygot import htmlCleaner
            cleaner = htmlCleaner(
                log=log,
                settings=settings,
                url="http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html",
                outputDirectory="/tmp"
            )
            cleaner.clean()  

        Or specify the title of the document and remove styling, metadata and title:

        .. code-block:: python 

            from polygot import htmlCleaner
            cleaner = htmlCleaner(
                log=log,
                settings=settings,
                url="http://www.thespacedoctor.co.uk/blog/2016/09/26/mysqlSucker-index.html",
                outputDirectory="/tmp",
                title="my_clean_doc",
                style=False,
                metadata=False,
                h1=False
            )
            cleaner.clean() 

    """

    def __init__(self, log, settings, url, outputDirectory=False, title=False, style=True, metadata=True, h1=True):
        self.log = log
        log.debug("instansiating a new 'htmlCleaner' object")
        self.settings = settings
        self.url = url
        self.outputDirectory = outputDirectory
        self.title = title
        self.style = style
        self.metadata = metadata
        self.h1 = h1
        self.parser_client = authenticate.authenticate(log=self.log, settings=self.settings).get()
        return

    def clean(self):
        """*parse and clean the html document with readability parser*

        **Return:**
            - ``filePath`` -- path to the cleaned HTML document

        **Usage:**

            See class usage 
        """
        self.log.info('starting the ``clean`` method')
        url = self.url
        parser_response = self.parser_client.get_article(self.url)
        if '503' in str(parser_response):
            return
        else:
            article = parser_response.json()
            if self.style:
                moduleDirectory = os.path.dirname(__file__)
                cssFile = moduleDirectory + '/css/main.css'
                pathToReadFile = cssFile
                readFile = codecs.open(pathToReadFile, encoding='utf-8', mode='r')
                thisCss = readFile.read()
                readFile.close()
            else:
                thisCss = ''
            if 'error' in article and article['error'] == True:
                print title
                print '    ' + article['messages']
                return
            try:
                text = article['content']
            except:
                print "Can't decode the text of %(title)s - moving on" % locals()
                return

            regex = re.compile('<span class="mw-editsection"><span class="mw-editsection-bracket">.*"mw-editsection-bracket">]')
            text = regex.sub('', text)
            regex2 = re.compile('\\<sup class="noprint.*better\xa0source\xa0needed\\<\\/span\\>\\<\\/a\\>\\<\\/i\\>\\]\\<\\/sup\\>', re.I)
            text = regex2.sub('', text)
            regex2 = re.compile('\\<a href="https\\:\\/\\/en\\.wikipedia\\.org\\/wiki\\/.*(\\#.*)"\\>\\<span class="tocnumber"\\>', re.I)
            text = regex2.sub('<a href="\\g<1>"><span class="tocnumber">', text)
            if self.title == False:
                title = article['title'].encode('utf-8', 'ignore')
                title = title.decode('utf-8')
                title = title.encode('ascii', 'ignore')
                rstrings = ':/"&\\\''
                for i in rstrings:
                    title = title.replace(i, '')

                if len(title) == 0:
                    from datetime import datetime, date, time
                    now = datetime.now()
                    title = now.strftime('%Y%m%dt%H%M%S')
                self.title = title
            title = self.title.replace('.html', '')
            pageTitle = title.replace('_', ' ')
            filePath = self.outputDirectory + '/' + title + '.html'
            writeFile = codecs.open(filePath, encoding='utf-8', mode='w')
            if self.metadata:
                metadata = '<title>%(title)s</title>' % locals()
            else:
                metadata = ''
            if self.h1:
                h1 = '<h1>%(pageTitle)s</h1>' % locals()
            else:
                h1 = ''
            content = '\n<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n%(metadata)s \n\n<style>\n%(thisCss)s\n</style>\n\n</head>\n<body>\n\n%(h1)s \n<a href="%(url)s">original source</a>\n</br></br>\n\n\n%(text)s \n</body>\n</html>' % locals()
            writeFile.write(content)
            writeFile.close()
            self.log.info('completed the ``clean`` method')
            return filePath