# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/classparser.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 15599 bytes
from __future__ import absolute_import, unicode_literals
from io import open
from builtins import str
from os import path
from re import sub, findall, IGNORECASE
import logging

class FileRegexMap(object):
    __doc__ = ' Given a file path including the file extension it maps the detected file extension to a regex pattern.\n\n    **Process:**\n\n    - Comments, template variables, or javascript syntax patterns are removed/replaced first with re.sub().\n\n    - Class selector sets are extracted using re.findall().\n\n    **Supported Javascript, Typescript, VueJs vue-loader extensions:** .js, .ts, .vue\n\n    Javascript has a number of cases where a special substitution is performed. These cases are stored in ``js_case``.\n    A check is performed if the re.sub() should do a special substitution of text that begins with the ``js_substring``.\n    The ``js_substring`` helps to uniquely designate the locations of class selector sets.\n\n    Javascript can occur in a standalone file or embedded <script> tags inside a file of another type.\n\n    **Supported HTML extension:** .html\n\n    HTML comments are removed.\n\n    **Supported jinja and django template extensions:** .jinja, .jinja2, .jnj, .ja, .djt, .djhtml\n\n    **Jinja sub_regexes regex explained:**\n\n    | Remove {{...}} and {%...%} where \'...\' is any character.\n    | ``{`` -- Substring must start with ``{``.\n    | ``.*`` -- Matches any character.\n    | ``?`` -- Do not be greedy.\n    | ``}`` -- Match with an ending ``}``.\n    | ``?}`` -- Optionally allow one more ``}``\n\n    **Supported XHTML, asp.net, c#, and ruby template extensions:** .aspx, .ascx, .master, .cs, .erb\n\n    **XHTML sub_regexes regex explained:**\n\n    | Remove <%...%> patterns where \'...\' is any character\n    | ``<%`` -- Substring must start with ``<%``.\n    | ``.*`` -- Matches any character.\n    | ``?`` -- Do not be greedy.\n    | ``%>`` -- Substring must end with ``%>``.\n\n    | **Raises OSError** if the ``_path`` does not exist.\n\n    | **Parameters:**\n\n    | **_path** (*str*) -- Relative or full path to the parsable file.\n\n    **Examples:**\n\n    >>> from blowdrycss.classparser import FileRegexMap\n    >>> file_regex_map = FileRegexMap(path=\'Default.aspx\')\n    >>> file_regex_map.regex_dict\n    {\n        \'sub_regexes\': r\'<%.*?%>\',\n        \'findall_regexes\': r\'class="(.*?)"\'\n    }\n\n    '

    def __init__(self, file_path=''):
        self.file_path = file_path.strip()
        self._regex_dict = dict()
        self.name = ''
        self.extension = ''
        self.js_replacement = ''
        self.js_case = ()
        self.file_type_dict = dict()
        if path.isfile(self.file_path):
            self.name, self.extension = path.splitext(self.file_path)
            sub_uri = ('://', )
            js_substring = 'extract__class__set'
            self.js_replacement = js_substring + '("'
            self.js_case = ('(domClass.add\\(\\s*.*?,\\s*["\\\'])', '(domClass.add\\(\\s*.*?,\\s*["\\\'])',
                            '(dojo.addClass\\(\\s*.*?,\\s*["\\\'])', '(domClass.remove\\(\\s*.*?,\\s*["\\\'])',
                            '(dojo.removeClass\\(\\s*.*?,\\s*["\\\'])', '(YAHOO.util.Dom.addClass\\(\\s*.*?,\\s*["\\\'])',
                            '(YAHOO.util.Dom.hasClass\\(\\s*.*?,\\s*["\\\'])', '(YAHOO.util.Dom.removeClass\\(\\s*.*?,\\s*["\\\'])',
                            '(.addClass\\(\\s*["\\\'])', '(.removeClass\\(\\s*["\\\'])',
                            '(\\$\\(\\s*["\\\']\\.)')
            sub_js = ('//.*?\\n', '\\n', '/\\*.*?\\*/', '(domClass.add\\(\\s*.*?,\\s*["\\\'])',
                      '(domClass.add\\(\\s*.*?,\\s*["\\\'])', '(dojo.addClass\\(\\s*.*?,\\s*["\\\'])',
                      '(domClass.remove\\(\\s*.*?,\\s*["\\\'])', '(dojo.removeClass\\(\\s*.*?,\\s*["\\\'])',
                      '(YAHOO.util.Dom.addClass\\(\\s*.*?,\\s*["\\\'])', '(YAHOO.util.Dom.hasClass\\(\\s*.*?,\\s*["\\\'])',
                      '(YAHOO.util.Dom.removeClass\\(\\s*.*?,\\s*["\\\'])', '(.addClass\\(\\s*["\\\'])',
                      '(.removeClass\\(\\s*["\\\'])', '(\\$\\(\\s*["\\\']\\.)')
            sub_html = sub_uri + sub_js + ('<!--.*?-->', )
            sub_jinja = ('{.*?}?}', ) + sub_html + ('{#.*?#}', )
            sub_csharp = ('//.*?\\n', '\\n', '/\\*.*?\\*/')
            sub_dotnet = sub_html + ('<%--.*?--%>', '<%.*?%>')
            sub_ruby = sub_html + ('<%--.*?--%>', '<%.*?%>')
            sub_php = sub_html
            class_regex = ('class=[\\\'"](.*?)["\\\']', )
            findall_regex_js = (
             '.classList.add\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)',
             '.classList.remove\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)',
             '.className\\s*\\+?=\\s*.*?[\\\'"](.*?)["\\\']',
             '.getElementsByClassName\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)',
             '.setAttribute\\(\\s*[\\\'"]class["\\\']\\s*,\\s*[\\\'"](.*?)["\\\']\\s*\\)',
             js_substring + '\\(\\s*[\\\'"](.*?)["\\\']\\s*\\)')
            findall_regex_cs = class_regex + ('.CssClass\\s*\\+?=\\s*.*?[\\\'"](.*?)["\\\']',
                                              '.Attributes.Add\\(\\s*[\\\'"]class["\\\'],\\s*.*?[\\\'"](.*?)["\\\']\\s*\\)')
            findall_regex = class_regex + findall_regex_js
            self.file_type_dict = {'.js':{'sub_regexes':sub_js, 
              'findall_regexes':findall_regex}, 
             '.ts':{'sub_regexes':sub_js, 
              'findall_regexes':findall_regex}, 
             '.vue':{'sub_regexes':sub_html, 
              'findall_regexes':findall_regex}, 
             '.html':{'sub_regexes':sub_html, 
              'findall_regexes':findall_regex}, 
             '.jinja':{'sub_regexes':sub_jinja, 
              'findall_regexes':findall_regex}, 
             '.jinja2':{'sub_regexes':sub_jinja, 
              'findall_regexes':findall_regex}, 
             '.jnj':{'sub_regexes':sub_jinja, 
              'findall_regexes':findall_regex}, 
             '.ja':{'sub_regexes':sub_jinja, 
              'findall_regexes':findall_regex}, 
             '.djt':{'sub_regexes':sub_jinja, 
              'findall_regexes':findall_regex}, 
             '.djhtml':{'sub_regexes':sub_jinja, 
              'findall_regexes':findall_regex}, 
             '.cs':{'sub_regexes':sub_csharp, 
              'findall_regexes':findall_regex_cs}, 
             '.aspx':{'sub_regexes':sub_dotnet, 
              'findall_regexes':findall_regex}, 
             '.ascx':{'sub_regexes':sub_dotnet, 
              'findall_regexes':findall_regex}, 
             '.master':{'sub_regexes':sub_dotnet, 
              'findall_regexes':findall_regex}, 
             '.erb':{'sub_regexes':sub_ruby, 
              'findall_regexes':findall_regex}, 
             '.php':{'sub_regexes':sub_php, 
              'findall_regexes':findall_regex}}
        else:
            raise OSError('"' + self.file_path + '" does not exist.')

    def is_valid_extension(self):
        """ Validates the extension. Returns whether True or False based on whether the extension is a key in
        ``file_type_dict``.

        :return: (*bool*) -- Returns True if the extension is a key in file_type_dict. Returns False otherwise.
        """
        return self.extension in self.file_type_dict

    @property
    def regex_dict(self):
        """ Validates ``self.extension`` and returns the associated regex dictionary for that extension.

        :return: Returns the regular expression dictionary associated with ``self.extension``.

        """
        self.is_valid_extension()
        return self.file_type_dict[self.extension]


class ClassExtractor(object):
    __doc__ = ' Given a file_regex_map of any type along with a substitution regex patterns and a findall regex patterns.\n    Returns a minimum set of class selectors as ``class_set``.\n\n    | **Parameters:**\n\n    | **file_path** (*str*) -- Path to the file_regex_map to be parsed.\n\n    | **sub_pattern** (*tuple of regexes*) -- Zero or more regex patterns to be removed from the file_regex_map text\n      before further processing.\n\n    | **findall_pattern** (*tuple of regexes*) -- Zero or more regex patterns used to find all class selectors\n      in a given file.\n\n    **Example Usage:**\n\n    >>> from blowdrycss.classparser import ClassExtractor\n    >>> # Assuming Default.aspx is located in the same directory\n    >>> aspx_file = \'Default.aspx\'\n    >>> aspx_sub = r\'<%.*?%>\'\n    >>> aspx_findall = r\'class="(.*?)"\'\n    >>> class_extractor = ClassExtractor(file_path=aspx_file)\n    >>> class_extractor.class_set\n    {\'row\', \'padding-top-30\', \'padding-bottom-30\', \'bgc-green\'}\n    >>> jinja2_file = \'index.jinja2\'\n    >>> jinja2_sub = r\'{.*?}?}\'\n    >>> jinja2_findall = r\'class="(.*?)"\'\n    >>> class_extractor = ClassExtractor(file_path=jinja2_file, sub_regexes=jinja2_sub, findall_regexes=jinja2_findall)\n    >>> class_extractor.class_set\n    {\'purple\', \'padding-left-5\', \'squirrel\', \'text-align-center\', \'large-up\', \'border-1\', \'row\', \'text-align-center\'}\n\n    '

    def __init__(self, file_path=''):
        if path.isfile(file_path):
            self.file_path = file_path
            self.file_regex_map = FileRegexMap(file_path=file_path)
            regex_dict = self.file_regex_map.regex_dict
            self.sub_regexes = regex_dict['sub_regexes']
            self.findall_regexes = regex_dict['findall_regexes']
        else:
            raise OSError('"' + file_path + '" does not exist.')

    @property
    def raw_class_list(self):
        """ Uses all sub_regexs and findall_regexes to extract space-delimited CSS class selector strings.
        Raw means space-delimited.

        Example: Look for the findall_regexes 'class="..."'. Extract the '...' part.

        sub_regexes() is used to remove template variables from quoted class selector strings in file text.
        findall_regexes() is used to find all class selector strings in a given files text.

        :return: (*list of strings*) -- Returns a list of raw class selector strings.

        """
        class_list = []
        with open((self.file_path), 'r', encoding='utf-8') as (_file):
            text = _file.read()
            for sub_regex in self.sub_regexes:
                if sub_regex in self.file_regex_map.js_case:
                    text = sub(sub_regex, self.file_regex_map.js_replacement, text)
                else:
                    text = sub(sub_regex, '', text)

            for findall_regex in self.findall_regexes:
                class_list += findall(findall_regex, text, IGNORECASE)

            logging.debug('classectractor.rawclasslist text: ' + text)
        return class_list

    @property
    def class_set(self):
        """ Reduce the list of quoted class selector strings to a minimum set of classes. Returns the ``class_set``.

        :return: (*set of strings*) -- Return the minimum set of individual class selector strings.

        """
        class_set = set()
        logging.debug(msg=('classextractor.raw_class_list:\t' + str(self.raw_class_list)))
        for classes in self.raw_class_list:
            class_set = set.union(set(classes.split()), class_set)

        logging.debug(msg=('classextractor.class_set:\t' + str(class_set)))
        return class_set


class ClassParser(object):
    __doc__ = " Parses all project files provided by file_dict. All file types are sent to ``ClassExtractor`` as of v0.1.7.\n\n    **Parameters**\n\n    **file_dict** (*dict*) -- Expecting FileFinder.file_dict as input.\n\n    **Returns** None\n\n    **Example**\n\n    >>> from os import getcwd, chdir, path\n    >>> from blowdrycss.filehandler import FileFinder\n    >>> from blowdrycss.classparser import ClassParser\n    >>> current_dir = getcwd()\n    >>> chdir('..')\n    >>> project_directory = path.join(current_dir, 'examplesite')\n    >>> chdir(current_dir)    # Change it back.\n    >>> file_finder = FileFinder(project_directory=project_directory)\n    >>> file_dict = file_finder.file_dict\n    >>> general_class_parser = ClassParser(file_dict=file_dict)\n    >>> general_class_parser.class_set\n    { Returns a complete set of all the classes discovered after looking in at all file paths. }\n\n    "

    def __init__(self, file_dict):
        self.class_set = set()
        self.file_dict = file_dict
        self.file_path_list = []
        self.build_file_path_list()
        logging.debug(msg=('classparser.html_class_parser.class_set:\t' + str(self.class_set)))
        self.build_class_set()

    def build_file_path_list(self):
        """ Builds a list of all of the file paths regardless of type.

        :return: None

        """
        keys = list(self.file_dict)
        for key in keys:
            self.file_path_list += self.file_dict[key]

    def build_class_set(self):
        """ Builds a complete set of all the classes discovered after looking in at all file paths.

        :return: None

        """
        for file_path in self.file_path_list:
            class_extractor = ClassExtractor(file_path=file_path)
            logging.debug(msg=('classparser.class_extractor.class_set:\t' + str(class_extractor.class_set)))
            self.class_set = self.class_set.union(class_extractor.class_set)

        logging.debug(msg=('classparser final class_set:\t' + str(self.class_set)))