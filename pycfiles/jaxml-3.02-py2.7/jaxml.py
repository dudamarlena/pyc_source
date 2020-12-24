# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jaxml.py
# Compiled at: 2010-08-07 18:33:56
import sys, os, string, cStringIO, time
__version__ = '3.02'
__doc__ = '\nThis python module defines a class named XML_document which will\nallow you to generate XML documents (yeah !) more easily than\nusing print or similar functions.\n\nHere\'s a list of available methods:\n===================================\n\n        __init__(version, encoding)\n                The instance constructor, automatically called\n                when you create a new instance of XML_document.\n                you can optionnally pass a version and encoding\n                string, the defaults are "1.0" and "iso-8859-1".\n\n        _indentstring(istr)\n                istr is the new indentation string used\n                to nicely present your XML documents. By\n                default istr is equal to 4 space characters.\n\n        _output(filearg)\n                use it to save the XML document to a file.\n                The optionnal filearg argument may be:\n                    None, "", or "-" which stands for sys.stdout.\n                    a file name.\n                    any file object.\n\n        _text(sometext)\n                use it to insert plain text at the current position\n                in the document.\n\n        _push()\n                saves the current position in the XML document.\n                use it if you\'re going to create a bunch of nested\n                XML tags and want to escape from them later to continue\n                your document at the same indentation level.\n                you can pass an optional \'name\' argument, to mark\n                a position by its name.\n\n        _pop()\n                restores the latest saved position.\n                use it to escape from nested tags and continue\n                your XML document at the same indentation level than\n                the latest time you called _push().\n                you can pass an optional \'name\' argument, to continue\n                at the same indentation level as when you called _push()\n                with the same \'name\' argument.\n\n        _template(file, **vars)\n                loads a template file and insert it as plain text at the current\n                position in the document, replacing ##varname## variables\n                in the template file with their corresponding value passed\n                in vars[varname]\n\n        _updatemapping(newmap)\n                updates the internal mapping used for replacing some strings with\n                others when rendering. This can be used as an easy way to\n                do templating without the need of an external file.\n                Pass None or no argument to reset the mapping to an empty one.\n                This method returns the new mapping\'s content.\n\n        Some more methods are available but not meant to be used directly, they\nare: __nonzero__, __getitem__, __setitem__, __delitem__, __coerce__, __add__,\n__radd__, __mul__, __rmul__, and __copy__. They are used automatically when doing\nspecial things, read the source for details.\n\n        ANY and ALL other method you may call will be treated as an XML\ntag, unless it already exists as a method in XML_document or a subclass of it,\nor its name begins with "__". I suggest you to only add methods whose names\nbegin with \'_\' to keep things simple and clear: "__" is reserved for future\nuse.\n\nThe file test/test.py is an example program which generates\nsome documents, just play with it (use and modify) and you\'ll\nlearn quickly how to use jaxml. Its source code is documented and\nattempts at describing and trying all jaxml\'s possibilities, so reading\nit is probably the best way to become powerful with jaxml in less than\n10 minutes.\n\nReally, PLEASE READ the file test/test.py to learn all possibilities.\n\n=========================================================================\n\nSince version 2.00, jaxml integrates the full functionnalities of the\nold jahtml module via the HTML_document and CGI_document classes, however\nthe API for these two classes has changed to be cleaner and don\'t use any\npredefined set of tags.\n\nThe HTML_document() and CGI_document() classes both inherit from XML_document()\nand all its methods (see above), but also feature some useful helper methods.\n\nPlease read the jaxml module sources and the test/test.py program to learn how\nto use them.\n\n=========================================================================\n\nThe only difficult things are:\n------------------------------\n\n        * you have to use the _push() and _pop() methods if you need\n          to get out of a bunch of nested tags.\n\n        * if you call a method (tag) with a string as the first\n          unnamed parameter, you\'ll don\'t need _push() or _pop()\n          because your tag will be automatically closed immediately.\n          \n        * if you call a method (tag) with a python mapping as the\n          first or second unamed parameter, this mapping is used\n          to correctly handle XML namespaces or attributes\n          which are python reserved words (e.g. class), please\n          look at test/test.py to see an example.\n'

class _TAGGED_document():
    """This class defines a tagged document"""

    class Tag:
        """This class defines a tag

                   This is largely inspired from a post in comp.lang.python
                   by Kragen Sitaker at the end of September 2000. Many
                   thanks to him !!!
                """

        def __init__(self, parent, tagname):
            """Save a link to the parent and the name of the tag for future reference

                           parent
                                The parent object, probably a _TAGGED_document instance.

                           tagname
                                The name of this tag
                        """
            self.__parent = parent
            self.__tagname = tagname

        def __call__(self, _text_=None, *nsattributes, **attributes):
            """Inserts the tag and its attributes in the document

                           _text_
                                eventually a string to be enclosed in the tag. the
                                name _text_ was chosen to not conflict with a probable user's attribute
                                called 'text'
                        """
            if type(_text_) == type({}):
                nsattributes = (
                 _text_,)
                _text_ = None
            nsargs = ''
            lg = len(nsattributes)
            if lg > 1:
                raise ValueError, 'jaxml: Invalid attributes %s' % str(nsattributes[0])
            elif lg:
                nsattr = nsattributes[0]
                try:
                    for ns in nsattr.keys():
                        tags = nsattr[ns]
                        try:
                            for tag in tags.keys():
                                nsargs = nsargs + ' %s%s%s="%s"' % (ns, ns and ':', tag, str(tags[tag]))

                        except AttributeError:
                            nsargs = nsargs + ' %s="%s"' % (ns, str(tags))

                except AttributeError:
                    raise ValueError, 'jaxml: Invalid attributes %s' % str(nsattr)

            if attributes:
                arg = string.join(map(lambda x, a=attributes: ' %s="%s"' % (x, str(a[x])), attributes.keys()), '')
            else:
                arg = ''
            if _text_ is not None:
                self.__parent._text('<%s%s>%s</%s>' % (self.__tagname, arg + nsargs, str(_text_), self.__tagname))
            else:
                self.__parent._tag__(self.__tagname, arg + nsargs)
            return self.__parent

        def __getattr__(self, name):
            """Handles naming spaces (Space:Tag)

                           name
                                The name of the (sub)tag part

                           The current tag's name becomes the naming space's name.
                           name becomes the new tag's name.
                        """
            return self.__parent.Tag(self.__parent, '%s:%s' % (self.__tagname, name))

    def __init__(self):
        """Initialize local datas"""
        self.__page = []
        self.__pushed = []
        self.__pusheddict = {}
        self.__position = 0
        self._updatemapping()
        self._indentstring()

    def __copy__(self):
        """Creates a copy of the current document"""
        new = self.__class__()
        new.__page = self.__page[:]
        new.__pushed = self.__pushed[:]
        new.__pusheddict = self.__pusheddict.copy()
        new.__position = self.__position
        new.__indentstring = self.__indentstring
        new.__mapping = self.__mapping.copy()
        for key, value in self.__dict__.items():
            if key[:2] == '__' and key[-2:] == '__' and not callable(getattr(self, key)):
                setattr(new, key, value)

        return new

    def __mul__(self, number):
        """Allows a document to be repeated

                   number
                        The number of times to repeat the document

                   allows constructs like: mydoc * 3
                """
        if type(number) != type(1):
            raise TypeError, 'jaxml.py: __mul__ operation not permitted on these operands.'
        if number < 0:
            raise ValueError, "jaxml.py: can't repeat a document a negative number of times."
        if number == 0:
            return self.__class__()
        else:
            new = self.__copy__()
            for i in range(number - 1):
                new = new + self

            return new

    def __rmul__(self, number):
        """Allows a document to be repeated

                   number
                        The number of times to repeat the document

                   allows construts like: 3 * mydoc
                """
        return self * number

    def __add__(self, other):
        """Allows two documents to be concatenated

                   other
                        The document or string of text to concatenate to self

                   This is not a real concatenation: the second
                   document (other) is in fact inserted at the current
                   position in the first one (self).

                   Also allows constructs like: mydoc + "some text"
                """
        if not isinstance(other, _TAGGED_document) and type(other) != type(''):
            raise TypeError, 'jaxml.py: __add__ operation not permitted on these operands.'
        new = self.__copy__()
        new.__mapping.update(other.__mapping)
        new._text(_TAGGED_document.__str__(other)[:-1])
        return new

    def __radd__(self, other):
        """Allows two documents to be concatenated

                   other
                        The document or string of text to which self will be concatenated

                   This is not a real concatenation: the first
                   document (self) is in fact inserted at the current
                   position in the second one (other).

                   Also allows constructs like: "some text" + mydoc
                """
        return other + self

    def __coerce__(self, other):
        """Try to convert two documents to a common type"""
        if isinstance(other, _TAGGED_document):
            return (
             self, other)
        else:
            if type(other) == type(''):
                new = self.__class__()
                new._text(other)
                return (
                 self, new)
            else:
                if type(other) == type(1):
                    return (
                     self, other)
                return

            return

    def __getattr__(self, name):
        """Here's the magic: we create tags on demand

                   name
                        The name of the tag we want to create
                """
        if name[:2] != '__':
            return self.Tag(self, name)

    def __nonzero__(self):
        """For truth value testing, returns 1 when the document is not empty"""
        if self.__page:
            return 1
        else:
            return 0

    def __getitem__(self, key):
        """returns key's value in the internal mapping"""
        return self.__mapping[key]

    def __setitem__(self, key, value):
        """sets key's value in the internal mapping"""
        self.__mapping[key] = value

    def __delitem__(self, key):
        """deletes this key from the internal mapping"""
        del self.__mapping[key]

    def __str__(self):
        """returns the document as a string of text"""
        outstr = cStringIO.StringIO()
        indentation = ''
        lgindent = len(self.__indentstring)
        lastopened = None
        for text, arg, offset in self.__page:
            if offset == -1:
                indentation = indentation[:-lgindent]
                if text != lastopened:
                    outstr.write('%s</%s>\n' % (indentation, text))
                else:
                    outstr.seek(-2, 1)
                    outstr.write(' />\n')
                lastopened = None
            elif offset == 1:
                outstr.write('%s<%s%s>\n' % (indentation, text, arg))
                indentation = indentation + self.__indentstring
                lastopened = text
            else:
                outstr.write('%s%s\n' % (indentation, text))
                lastopened = None

        outstr.flush()
        retval = outstr.getvalue()
        outstr.close()
        for key, value in self.__mapping.items():
            retval = string.replace(retval, key, value)

        return retval

    def __repr__(self):
        """Returns a printable representation of the document, same as str() for now"""
        return str(self)

    def __adjust_stack(self, offset):
        """Adjust the stack of pushed positions.

                   offset
                        offset by which adjust the stack
                """
        if self.__pushed:
            pos, oldoffset = self.__pushed.pop()
            self.__pushed.append((pos, oldoffset + offset))

    def _tag__(self, tag, arg):
        self.__page.insert(self.__position, (tag, arg, 1))
        self.__position = self.__position + 1
        self.__page.insert(self.__position, (tag, None, -1))
        self.__adjust_stack(2)
        return

    def _push(self, name=None):
        """Push the current tag's position.

                   useful before a block of nested tags
                   
                   name : can be used to name the pushed position and pop it later directly
                """
        if name:
            self.__pusheddict[name] = len(self.__pushed)
        self.__pushed.append((self.__position, 0))

    def _pop(self, name=None):
        """Restore the latest pushed position.

                   useful to get out of a block of nested tags
                   
                   name : can be used to restore a named position, not necessarily the latest.
                """
        if self.__pushed:
            maxindex = len(self.__pushed) - 1
            if name:
                try:
                    index = self.__pusheddict[name]
                    del self.__pusheddict[name]
                except KeyError:
                    raise KeyError, "jaxml named position %s doesn't exist" % name

            else:
                index = maxindex
            while maxindex >= index:
                pos, offset = self.__pushed.pop()
                self.__position = pos + offset
                self.__adjust_stack(offset)
                maxindex = maxindex - 1

    def _text(self, text):
        """Insert plain text in the document

                   text
                        text to be inserted
                """
        self.__page.insert(self.__position, (str(text), None, 0))
        self.__position = self.__position + 1
        self.__adjust_stack(1)
        return

    def _indentstring(self, newindentstring='    '):
        """Sets the indentation string for the output (default is 4 space characters)"""
        self.__indentstring = newindentstring

    def _updatemapping(self, newmap=None):
        """Updates the internal mapping for the new templating facility,
                   and returns the new mapping's content

                   newmap
                        a Python mapping object to initialise or extend the
                        mapping. If None then the mapping is reset to an empty dictionnary
                        which is the default value.
                """
        if newmap == None:
            self.__mapping = {}
            return self.__mapping
        else:
            if type(newmap) == type({}):
                self.__mapping.update(newmap)
                return self.__mapping
            raise TypeError, "jaxml.py: _updatemapping's parameter must be a Python mapping object."
            return

    def _output(self, file='-'):
        """Ouput the page, with indentation.

                   file
                        the optional file object or filename to output to
                        ("-" or None or "" means sys.stdout)
                """
        isopen = 0
        if type(file) == type('') or file is None:
            if file and file != '-':
                outf = open(file, 'w')
                isopen = 1
            else:
                outf = sys.stdout
        else:
            outf = file
        outf.write('%s' % str(self))
        outf.flush()
        if isopen:
            outf.close()
        return


class XML_document(_TAGGED_document):
    """This class defines an XML document"""

    def __init__(self, version='1.0', encoding='iso-8859-1'):
        """Initialize local datas.

                   arguments:
                       version:  xml version string
                       encoding: xml encoding language
                """
        _TAGGED_document.__init__(self)
        self.__version__ = version
        self.__encoding__ = encoding

    def __str__(self):
        """returns the XML document as a string of text"""
        tagdocstr = _TAGGED_document.__str__(self)
        if tagdocstr:
            return '<?xml version="%s" encoding="%s"?>\n' % (self.__version__, self.__encoding__) + tagdocstr
        else:
            return ''

    def __subst_lines(self, lines, **vars):
        """Substitues var names with their values.

                   parts of this function come from the Whiz package
                   THANKS TO Neale Pickett ! Here follows the original license terms for Whiz:
                        ## Author: Neale Pickett <neale@lanl.gov>
                        ## Time-stamp: <99/02/11 10:45:42 neale>

                        ## This software and ancillary information (herein called "SOFTWARE")
                        ## called html.py made avaiable under the terms described here.  The
                        ## SOFTWARE has been approved for release with associated LA-CC Number
                        ## 89-47.

                        ## Unless otherwise indicated, this SOFTWARE has been authored by an
                        ## employee or employees of the University of California, operator of
                        ## the Los Alamos National Laboratory under contract No. W-7405-ENG-36
                        ## with the U.S. Department of Energy.  The U.S. Government has rights
                        ## to use, reproduce, and distribute this SOFTWARE.  The public may
                        ## copy, distribute, prepare derivative works and publicly display this
                        ## SOFTWARE without charge, provided that this Notice and any statement
                        ## of authorship are reproduced on all copies.  Neither the Government
                        ## nor the University makes any warranty, express or implied, or assumes
                        ## any liability or responsibility for the use of this SOFTWARE.

                        ## If SOFTWARE is modified to produce derivative works, such modified
                        ## SOFTWARE should be clearly marked, so as not to confuse it with the
                        ## version available from LANL.
                """
        import regex
        container = regex.compile('\\(<!-- \\)?##\\([-_A-Za-z0-9]+\\)##\\( -->\\)?')
        for line in lines:
            while container.search(line) != -1:
                try:
                    replacement = str(vars[container.group(2)])
                except KeyError:
                    replacement = str('<!-- Unmatched variable: ' + container.group(2) + ' -->')

                pre = line[:container.regs[0][0]]
                post = line[container.regs[0][1]:]
                if string.strip(pre) == '':
                    lines = string.split(replacement, '\n')
                    new = [lines[0]]
                    for l in lines[1:]:
                        new.append(pre + l)

                    replacement = string.join(new, '\n')
                line = '%s%s%s' % (pre, replacement, post)

            self._text(line)

    def _template(self, file='-', **vars):
        """Include an external file in the current doc 
                   and replaces ##vars## with their values.

                   Parts of this function come from the Whiz package
                   THANKS TO Neale Pickett ! Here follows the original license terms for Whiz:
                        ## Author: Neale Pickett <neale@lanl.gov>
                        ## Time-stamp: <99/02/11 10:45:42 neale>

                        ## This software and ancillary information (herein called "SOFTWARE")
                        ## called html.py made avaiable under the terms described here.  The
                        ## SOFTWARE has been approved for release with associated LA-CC Number
                        ## 89-47.

                        ## Unless otherwise indicated, this SOFTWARE has been authored by an
                        ## employee or employees of the University of California, operator of
                        ## the Los Alamos National Laboratory under contract No. W-7405-ENG-36
                        ## with the U.S. Department of Energy.  The U.S. Government has rights
                        ## to use, reproduce, and distribute this SOFTWARE.  The public may
                        ## copy, distribute, prepare derivative works and publicly display this
                        ## SOFTWARE without charge, provided that this Notice and any statement
                        ## of authorship are reproduced on all copies.  Neither the Government
                        ## nor the University makes any warranty, express or implied, or assumes
                        ## any liability or responsibility for the use of this SOFTWARE.

                        ## If SOFTWARE is modified to produce derivative works, such modified
                        ## SOFTWARE should be clearly marked, so as not to confuse it with the
                        ## version available from LANL.
                """
        if file is None or type(file) == type(''):
            if file and file != '-':
                inf = open(file, 'r')
            else:
                inf = sys.stdin
        else:
            inf = file
        lines = map(lambda l: l[:-1], inf.readlines())
        if inf != sys.stdin:
            inf.close()
        apply(self.__subst_lines, (lines,), vars)
        return


class HTML_document(XML_document):
    """This class defines a useful method to output a default header,
           as well as some methods defined for easying the use of this module and
           keep porting from the old jahtml module easy too.
        """

    def _default_header(self, title='JAXML Default HTML Document', **modifiers):
        """Begins a normal document.

                   title
                        the title of the document
                   modifiers
                        usual meta name= content= tags (keywords, description, etc...)
                        WARNING: doesn't work with other meta tags
                """
        self.html()
        self._push()
        self.head()
        self.title(title)
        for mod in modifiers.keys():
            if modifiers[mod] != None:
                self._push()
                self.meta(name=string.upper(mod), content=modifiers[mod])
                self._pop()

        self._pop()
        return

    def __fake_input(self, _text_=None, **args):
        self._push()
        retcode = apply(self.input, (None, ), args)
        self._pop()
        return retcode

    def _submit(self, **args):
        """Submit button input type, beware of the leading underscore"""
        args['type'] = 'submit'
        return apply(self.__fake_input, (None, ), args)

    def _reset(self, **args):
        """Reset button input type, beware of the leading underscore"""
        args['type'] = 'reset'
        return apply(self.__fake_input, (None, ), args)

    def _radio(self, **args):
        """Radio button input type, beware of the leading underscore"""
        args['type'] = 'radio'
        return apply(self.__fake_input, (None, ), args)

    def _checkbox(self, **args):
        """Checkbox input type, beware of the leading underscore"""
        args['type'] = 'checkbox'
        return apply(self.__fake_input, (None, ), args)

    def _password(self, **args):
        """Password input type, beware of the leading underscore"""
        args['type'] = 'password'
        return apply(self.__fake_input, (None, ), args)

    def _hidden(self, **args):
        """Hidden input type, beware of the leading underscore"""
        args['type'] = 'hidden'
        return apply(self.__fake_input, (None, ), args)

    def _textinput(self, **args):
        """Text input type, beware of the leading underscore and the trailing 'input'"""
        args['type'] = 'text'
        return apply(self.__fake_input, (None, ), args)

    def _button(self, **args):
        """Button input type, beware of the leading underscore"""
        args['type'] = 'button'
        return apply(self.__fake_input, (None, ), args)

    def _file(self, **args):
        """File input type, beware of the leading underscore"""
        args['type'] = 'file'
        return apply(self.__fake_input, (None, ), args)

    def _image(self, **args):
        """Image input type, beware of the leading underscore"""
        args['type'] = 'image'
        return apply(self.__fake_input, (None, ), args)

    def _meta(self, **args):
        """The META tag, beware of the leading underscore"""
        self._push()
        retcode = apply(self.meta, (None, ), args)
        self._pop()
        return retcode

    def _br(self, **args):
        """The BR tag, beware of the leading underscore"""
        self._push()
        retcode = apply(self.br, (None, ), args)
        self._pop()
        return retcode

    def _hr(self, **args):
        """The HR tag, beware of the leading underscore"""
        self._push()
        retcode = apply(self.hr, (None, ), args)
        self._pop()
        return retcode


class CGI_document(HTML_document):
    """
    This class defines a CGI document.

    it inherits from the HTML_document class, but more methods are present
    """
    __possibleargs = {'version': '1.0', 'encoding': 'iso-8859-1', 'content_type': 'text/html', 'content_disposition': '', 'expires': '', 'pragma': '', 'redirect': '', 'status': '', 'statmes': '', 'debug': None}

    def __init__(self, **args):
        """
        Initialise local datas.
        """
        HTML_document.__init__(self)
        for key in self.__possibleargs.keys():
            if args.has_key(key):
                value = args[key]
            else:
                value = self.__possibleargs[key]
            setattr(self, '__' + key + '__', value)

    def __str__(self):
        """Returns the CGI output as a string."""
        if self.__redirect__:
            return 'Location: %s\n\n' % self.__redirect__
        else:
            val = 'Content-type: %s\n' % self.__content_type__
            if self.__status__:
                val = val + 'Status: %s %s\n' % (self.__status__, self.__statmes__)
            if self.__pragma__:
                val = val + 'Pragma: %s\n' % self.__pragma__
            if self.__expires__:
                val = val + 'Expires: %s\n' % self.__expires__
            if self.__content_disposition__:
                val = val + 'Content-Disposition: %s\n' % self.__content_disposition__
            return val + '\n' + HTML_document.__str__(self)

    def _set_debug(self, file):
        """Sets the flag to send the output to a file too."""
        self.__debug_file__ = file

    def _set_pragma(self, pragma):
        """Defines the pragma value.

           pragma
                The pragma's value
        """
        self.__pragma__ = pragma

    def _set_expires(self, expires):
        """Defines the expiration date of the CGI output.

           expires
                The expiration date
        """
        self.__expires__ = expires

    def _set_redirect(self, url):
        """Defines the redirection url.

           url
                The redirection url to send
        """
        self.__redirect__ = url

    def _set_content_type(self, content_type='text/html'):
        """Defines the content type of the CGI output.

           content_type
                The new content type, default is text/html
        """
        self.__content_type__ = content_type

    def _set_content_disposition(self, content_disposition=''):
        """Defines the content disposition of the CGI output.

           content_disposition
                The new disposition, default is ""
        """
        self.__content_disposition__ = content_disposition

    def _set_status(self, status, message=''):
        """Defines the status to return.

           statsus
                The status value
           message
                The message following the status value
        """
        self.__status__ = status
        self.__statmes__ = message

    def _do_nothing(self, message='No response'):
        """Set status to 204 (do nothing)."""
        self._set_status('204', message)

    def _envvar(self, varname):
        """Returns the variable value or None."""
        if os.environ.has_key(varname):
            return os.environ[varname]

    def _server_software(self):
        """Returns the SERVER_SOFTWARE environment variable value."""
        return self._envvar('SERVER_SOFTWARE')

    def _server_name(self):
        """Returns the SERVER_NAME environment variable value."""
        return self._envvar('SERVER_NAME')

    def _gateway_interface(self):
        """Returns the GATEWAY_INTERFACE environment variable value."""
        return self._envvar('GATEWAY_INTERFACE')

    def _server_protocol(self):
        """Returns the SERVER_PROTOCOL environment variable value."""
        return self._envvar('SERVER_PROTOCOL')

    def _server_port(self):
        """Returns the SERVER_PORT environment variable value."""
        return self._envvar('SERVER_PORT')

    def _request_method(self):
        """Returns the REQUEST_METHOD environment variable value."""
        return self._envvar('REQUEST_METHOD')

    def _path_info(self):
        """Returns the PATH_INFO environment variable value."""
        return self._envvar('PATH_INFO')

    def _path_translated(self):
        """Returns the PATH_TRANSLATED environment variable value."""
        return self._envvar('PATH_TRANSLATED')

    def _document_root(self):
        """Returns the DOCUMENT_ROOT environment variable value."""
        return self._envvar('DOCUMENT_ROOT')

    def _script_name(self):
        """Returns the SCRIPT_NAME environment variable value."""
        return self._envvar('SCRIPT_NAME')

    def _query_string(self):
        """Returns the QUERY_STRING environment variable value."""
        return self._envvar('QUERY_STRING')

    def _remote_host(self):
        """Returns the REMOTE_HOST environment variable value."""
        return self._envvar('REMOTE_HOST')

    def _remote_addr(self):
        """Returns the REMOTE_ADDR environment variable value."""
        return self._envvar('REMOTE_ADDR')

    def _auth_type(self):
        """Returns the AUTH_TYPE environment variable value."""
        return self._envvar('AUTH_TYPE')

    def _remote_user(self):
        """Returns the REMOTE_USER environment variable value."""
        return self._envvar('REMOTE_USER')

    def _remote_ident(self):
        """Returns the REMOTE_IDENT environment variable value."""
        return self._envvar('REMOTE_IDENT')

    def _content_type(self):
        """Returns the CONTENT_TYPE environment variable value."""
        return self._envvar('CONTENT_TYPE')

    def _content_length(self):
        """Returns the CONTENT_LENGTH environment variable value."""
        return self._envvar('CONTENT_LENGTH')

    def _http_accept(self):
        """Returns the HTTP_ACCEPT environment variable value."""
        return self._envvar('HTTP_ACCEPT')

    def _http_user_agent(self):
        """Returns the HTTP_USER_AGENT environment variable value."""
        return self._envvar('HTTP_USER_AGENT')

    def _http_referer(self):
        """Returns the HTTP_REFERER environment variable value."""
        return self._envvar('HTTP_REFERER')

    def _log_message(self, msg='Error in a CGI Script made with jaxml', level='error'):
        """Logs a message to the HTTP server's error log file (usually on stderr)."""
        sys.stderr.write('[%s] [%s] %s\n' % (time.asctime(time.localtime(time.time())), level, msg))

    def _log_message_and_exit(self, msg='Fatal Error in a CGI Script made with jaxml', level='error'):
        """Logs a message to the HTTP server's error log file (usually on stderr) and exits unsuccessfully."""
        self.log_message(msg, level)
        sys.exit(-1)

    def _output(self, file='-'):
        """Prints the CGI script output to stdout or file.

           If self.__debug_file__ is defined it is used as a file
           to which send the output to too.
        """
        HTML_document._output(self, file)
        if self.__debug_file__:
            HTML_document._output(self, self.__debug_file__)


class Html_document():
    """This class warns the programmer when used, and exits the program.
           This is done to say that the jahtml module is now obsolete"""

    def __init__(self):
        """Warns and Exit"""
        sys.stderr.write("EXITING: The jaxml.Html_document() class shouldn't be used anymore.\nUse jaxml.HTML_document() instead, and modify your programs according to the new API.\n")
        sys.exit(-1)