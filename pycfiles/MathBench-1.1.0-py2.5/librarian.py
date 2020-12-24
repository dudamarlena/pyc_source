# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathbench/basement/librarian.py
# Compiled at: 2008-04-09 11:14:20
"""
Management of the documentation of mathbench and its plugins.
"""
import os, logging, re, wx.py.dispatcher as dispatcher

def DefangHTML(txt):
    """
        Defang html symbols.
        
        Inspired from :
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81330
        """
    symbol_dict = {'&': '&amp;', 
       '>': '&gt;', 
       '<': '&lt;', 
       'é': '&eacute;', 
       'è': '&egrave;', 
       'à': '&agrave;', 
       '\n': ' \n<br>'}
    re_match_pattern = '(%s)' % ('|').join(map(re.escape, symbol_dict.keys()))
    return re.sub(re_match_pattern, lambda m: symbol_dict[m.group()], txt)


class MathBenchSearchEngine(object):
    """
        A simple search engine to index the documentation of MathBench's
        basic usages.
        """
    MATHBENCH_WEBSITE = 'http://mathbench.sourceforge.net/'

    def __init__(self):
        """
                Create the indexing dictionary
                """
        self.search_dict = {'mathbench help shell idea completion python test idea': (
                                                                   self.MATHBENCH_WEBSITE + 'doc-basic-usage.html',
                                                                   'Basic usage of the shell'), 
           'mathbench help editor execute execution python refine work': (
                                                                        self.MATHBENCH_WEBSITE + 'doc-editor-work.html',
                                                                        'Working with the editor'), 
           'mathbench help librarydesk documentation search query': (
                                                                   self.MATHBENCH_WEBSITE + 'doc-library-use.html',
                                                                   'Search the documentation via the library desk'), 
           'mathbench help extend plugin install': (
                                                  self.MATHBENCH_WEBSITE + 'doc-plugins.html',
                                                  'Adapt the application to your needs with plugins')}

    def search(self, search_query):
        """
                Search the documentation
                """
        search_query_kw = search_query.split()
        result_dict = {}
        for key in self.search_dict.keys():
            count = 0
            for item in search_query_kw:
                if key.find(str(item)) != -1:
                    count += 1

            if count != 0:
                if result_dict.has_key(count):
                    result_dict[count].append(self.search_dict[key])
                else:
                    result_dict[count] = [
                     self.search_dict[key]]

        ranks = result_dict.keys()
        ranks.sort()
        ranks.reverse()
        results = []
        for r in ranks:
            results.extend(result_dict[r])

        return results


class LibrarianSingleton(object):
    """
        A singleton class in charge of building, updating the library
        and also performing the searches.

        The librarian is in charge of creating the library desk display
        and then must be informed of which DeskFacory to use to create
        this desk.

        The display widget created must also send a 'LibraryDeskClosed'
        signal when it is closed.
        """
    __instance = None

    def __init__(self):
        """
                Initialisation: this class should not be initialised
                explicitly and the ``get`` classmethod must be called instead.
                """
        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")
        mbse = MathBenchSearchEngine()
        self.__search_methods = {'MathBench': mbse.search}
        self.__desk_factory = None
        self.__desk = None
        return

    def show(self, txt):
        """
                Show the results in a frame.
                """
        if self.__desk == None:
            self.__desk = self.__desk_factory()
            dispatcher.connect(receiver=self._desk_closed, signal='LibraryDeskClosed', sender=self.__desk)
        self.__desk.showPage(txt)
        return

    def _desk_closed(self):
        """
                When the desk is closed
                """
        self.__desk = None
        return

    def compile_results(self, search_query):
        """
                Compile the search results in a unique html page.
                """
        search_res = [
         '<html>\n<title>Search results</title>\n\n<body>\n<H1> Search results for "%s" </H1>\n<br>' % search_query]
        temp_search_res = []
        for context in self.__search_methods.keys():
            res_list = self.__search_methods[context](search_query)
            if len(res_list) == 0:
                continue
            else:
                temp_search_res.append('<br>\n<H2>From %s</H2>\n<br>\n<ul>' % DefangHTML(context))
                for item in res_list:
                    temp_search_res.append("<li><a href='%s'>%s</a></li>\n<br>" % item)

                temp_search_res.append('</ul>\n<br>')

        if len(temp_search_res) == 0:
            search_res = [
             '<html>\n<title>Search results</title>\n\n<body>\n<H1> Sorry, no result for "%s" </H1>\n<br>' % search_query]
        else:
            search_res.extend(temp_search_res)
        search_res.append('</body>\n</html>\n')
        return os.linesep.join(search_res)

    def show_welcome(self):
        """
                Display the welcome text in a widget
                """
        welcome_txt = '<html>\n\n<title>Welcome</title>\n\n<body>\n\n<H1> Library Desk </H1>\n\n<H2> About this desk</H2>\n\nIf you\'re looking for a precise answer, you may enter a search query\nin the text area of the toolbar, press "Enter" (on your keyboard) and\nthe available answers will be shown to you.\n\n<br>\n<br>\n\nPlease also note that this viewer is buggy with external websites,\nhence you should prefer going to online websites with your own\nwebbrowser.\n\n\n<H2> About Python </H2>\n\n<H3> References</H3>\n<ul>\n  <li><a href="http://python.org">Python language</a> \n<pre>http://python.org</pre></li>\n  <li><a href="http://docs.python.org/modindex.html">Modules index</a> \n<pre>http://docs.python.org/modindex.html</pre></li>\n  <li><a href="http://starship.python.net/crew/theller/pyhelp.cgi">Online search</a> \n<pre>http://starship.python.net/crew/theller/pyhelp.cgi</pre></li>\n</ul>\n\n<H3>Quick introductions</H3>\n<ul>\n  <li><a href="http://docs.python.org/tut/tut.html">Python tutorial</a> \n<pre>http://docs.python.org/tut/tut.html</pre></li>\n  <li><a href="http://wiki.python.org/moin/SimplePrograms">Simple code samples</a> \n<pre>http://wiki.python.org/moin/SimplePrograms</pre></li>\n</ul>\n\n<H2> About Mathbench</H2>\n\n<ul>\n  <li><a href="http://mathbench.sourceforge.net/">Mathbench Project</a> \n<pre>http://mathbench.sourceforge.net</pre></li>\n</ul>\n\n</body>\n \n</html>\n'
        self.show(welcome_txt)

    def setSearchMethod(self, search_method, context_name):
        """
                Set the search method
                """
        self.__search_methods[context_name] = search_method

    def record_search(self, txt):
        """
                Record the previous search items
                """
        self.__desk.addToHistory(txt)

    def get(self):
        """
                Actually create an instance
                """
        if self.__instance is None:
            self.__instance = LibrarianSingleton()
            logging.debug('LibrarianSingleton initialised')
        return self.__instance

    get = classmethod(get)

    def register(self, search_method, context_name):
        """
                Register a search method for a specific context (usually the
                library imported by a precise plugin.)
                """
        librarian = self.get()
        librarian.setSearchMethod(search_method, context_name)
        logging.debug('Adding the search method from %s to the LibrarianSingleton' % context_name)

    register = classmethod(register)

    def setDeskFactory(self, desk_factory):
        """
                Set the factory that will be in charge of creating the desk
                (ie the widget displaying the search results)
                """
        librarian = self.get()
        librarian.__desk_factory = desk_factory

    setDeskFactory = classmethod(setDeskFactory)

    def search(self, search_query):
        """
                Return a HTML formated text providing links to all the search results.
                """
        if search_query.strip() == '':
            return
        librarian = LibrarianSingleton.get()
        search_res = librarian.compile_results(search_query)
        librarian.show(search_res)
        librarian.record_search(search_query)

    search = classmethod(search)

    def welcome(self):
        """
                Display a welome page
                """
        librarian = LibrarianSingleton.get()
        librarian.show_welcome()

    welcome = classmethod(welcome)

    def popup(self):
        """
                Put the desk on top of the other frames
                """
        librarian = self.get()
        if librarian.__desk is None:
            self.welcome()
        else:
            librarian.__desk.Show(False)
            librarian.__desk.Show(True)
        return

    popup = classmethod(popup)