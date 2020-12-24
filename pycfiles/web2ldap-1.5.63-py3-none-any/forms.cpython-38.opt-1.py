# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/web/forms.py
# Compiled at: 2019-12-04 13:09:21
# Size of source mod 2**32: 32882 bytes
"""
web2ldap.web.forms - class library for handling <FORM> input

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import cgi, codecs, sys, re, urllib.parse, uuid
from . import escape_html
from . import helper

class Field:
    __doc__ = '\n    Base class for all kind of single input fields.\n\n    In most cases this class is not used directly\n    since derivate classes for most types of input fields exist.\n    '

    def __init__(self, name, text, maxLen, maxValues, pattern, required=0, default=None, accesskey=''):
        """
        name
            Field name used in <input name="..">
        text
            User-friendly text describing this field
        maxLen
            maximum length of a single input value [Bytes]
        maxValues
            maximum amount of input values
        default
            default value to be used in method inputfield()
        required
            flag which marks field as mandantory input field
        accesskey
            key for accessing this field to be displayed by method input_html()
        pattern
            regex pattern of valid values either as string
            or tuple (pattern,options)
        """
        self.value = []
        self.name = name
        self.text = text
        self.maxLen = maxLen
        self.maxValues = maxValues
        self.required = required
        self.accesskey = accesskey
        self._charset = 'utf-8'
        self.set_default(default)
        self.setRegex(pattern)

    def _accesskey_attr(self):
        if not self.accesskey:
            return ''
        return 'accesskey="%s" ' % self.accesskey

    def id_attr(self, id_value):
        if id_value is None:
            return ''
        return 'id="%s" ' % id_value

    def set_default(self, default):
        """
        Set the default of a field.

        Mainly this is used by the application if self.default shall
        be changed after initializing the field object.
        """
        if isinstance(default, list):
            self.default = [i for i in default if i is not None]
        self.default = default or ''

    def _regex_with_options(self, pattern):
        """
        The result is a tuple (pattern string, pattern options).

        pattern
            Either a string containing a regex pattern,
            a tuple (pattern string, pattern options) or None.
        """
        if pattern is None:
            return (None, 0)
        if isinstance(pattern, tuple):
            return pattern
        if isinstance(pattern, str):
            return (
             pattern, 0)
        raise TypeError('Expected pattern to be None, str or tuple, got %r' % (pattern,))

    def setRegex(self, pattern: str):
        """
        Set the regex pattern for validating this field.

        Mainly this is used if self._re shall be changed after
        the field object was initialized.

        pattern
            Either a string containing a regex pattern,
            a tuple (pattern string, pattern options) or None.
            If None regex checking in _validate_format is switched off
            (not recommended).
        """
        patternstring, patternoptions = self._regex_with_options(pattern)
        if patternstring is None:
            self._re = None
        else:
            patternoptions = patternoptions | re.U
            self._re = re.compile('%s$' % patternstring, patternoptions)

    def _validate_len(self, value):
        """Check length of the user's value for this field."""
        if len(value) > self.maxLen:
            raise InvalidValueLen(self.name, self.text, len(value), self.maxLen)

    def _validate_format(self, value):
        """
        Check format of the user's value for this field.

        Empty input (zero-length string) are valid in any case.
        You might override this method to change this behaviour.
        """
        if self._re is not None:
            if value:
                rm = self._re.match(value)
                if rm is None:
                    raise InvalidValueFormat(self.name, self.text, value.encode(self.charset))

    def _validate_val_count(self):
        if len(self.value) >= self.maxValues:
            raise TooManyValues(self.name, self.text, len(self.value), self.maxValues)

    def _decodeValue(self, value):
        """
        Return str to be stored in self.value
        """
        try:
            value = value.decode(self.charset)
        except UnicodeError:
            value = value.decode('iso-8859-1')
        else:
            return value

    def set_value(self, value):
        """
        Store the user's value into the field object.

        This method can be used to modify the user's value
        before storing it into self.value.
        """
        assert isinstance(value, (str, bytes)), TypeError('Expected value to be str or bytes, was %r' % (value,))
        if isinstance(value, bytes):
            value = self._decodeValue(value)
        self._validate_len(value)
        self._validate_format(value)
        self._validate_val_count()
        self.value.append(value)

    @property
    def charset(self):
        """Return the character set used for the field"""
        return self._charset

    @charset.setter
    def charset(self, charset):
        """Set the character set used for the field"""
        self._charset = charset

    def _defaultValue(self, default):
        """returns default value"""
        return default or self.__dict__.get('default', '')

    def titleHTML(self, title):
        """HTML output of default."""
        return escape_html(title or self.text)

    def _default_html(self, default):
        """HTML output of default."""
        return escape_html(self._defaultValue(default))


class Textarea(Field):
    __doc__ = '\n    Multi-line input field:\n    <textarea>\n    '

    def __init__(self, name, text, maxLen, maxValues, pattern, required=0, default=None, accesskey='', rows=10, cols=60):
        self.rows = rows
        self.cols = cols
        Field.__init__(self, name, text, maxLen, maxValues, None, required, default, accesskey)

    def setRegex(self, pattern: str):
        """
        Like Field.setRegex() but pattern options re.S and re.M are
        automatically added.
        """
        patternstring, patternoptions = self._regex_with_options(pattern)
        patternoptions = patternoptions | re.M | re.S
        Field.setRegex(self, (patternstring, patternoptions))

    def input_html(self, default=None, id_value=None, title=None):
        """Returns string with HTML input field."""
        return '<textarea %stitle="%s" name="%s" %s rows="%d" cols="%d">%s</textarea>' % (
         self.id_attr(id_value),
         self.titleHTML(title),
         self.name,
         self._accesskey_attr(),
         self.rows,
         self.cols,
         self._default_html(default))


class Input(Field):
    __doc__ = '\n    Normal one-line input field:\n    <input>\n    '
    input_type = None

    def __init__(self, name, text, maxLen, maxValues, pattern, required=0, default=None, accesskey='', size=None):
        self.size = size or maxLen
        Field.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)

    def input_html(self, default=None, id_value=None, title=None):
        if self.input_type is not None:
            type_attr = ' type="%s"' % escape_html(self.input_type)
        else:
            type_attr = ''
        if self._re is not None:
            pattern_attr = ' pattern="%s"' % escape_html(self._re.pattern)
        else:
            pattern_attr = ''
        return '<input %stitle="%s" name="%s" %s maxlength="%d" size="%d"%s%s value="%s">' % (
         self.id_attr(id_value),
         self.titleHTML(title),
         self.name,
         self._accesskey_attr(),
         self.maxLen,
         self.size,
         type_attr,
         pattern_attr,
         self._default_html(default))


class HiddenInput(Input):
    __doc__ = '\n    Hidden input field:\n    <input type="hidden">\n    '

    def __init__(self, name, text, maxLen, maxValues, pattern, required=0, default=None, accesskey=''):
        Input.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)

    def input_html(self, default=None, id_value=None, title=None, show=0):
        default_html = self._default_html(default)
        if show:
            default_str = default_html
        else:
            default_str = ''
        return '<input type="hidden" %stitle="%s" name="%s" %s  value="%s">%s' % (
         self.id_attr(id_value),
         self.titleHTML(title),
         self.name,
         self._accesskey_attr(),
         default_html,
         default_str)


class BytesInput(Input):

    def setRegex(self, pattern: str):
        """
        Set the bytes regex pattern for validating this field.
        """
        patternstring, patternoptions = self._regex_with_options(pattern)
        if patternstring is None:
            self._re = None
        else:
            patternoptions = patternoptions
            self._re = re.compile('%s$' % patternstring.encode('iso-8859-1'), patternoptions)

    def _decodeValue(self, value):
        return value


class File(Input):
    __doc__ = '\n    File upload field\n    <input type="file">\n    '
    mimeType = 'application/octet-stream'

    def _validate_format(self, value):
        """Binary data is assumed to be valid all the time"""
        pass

    def _decodeValue(self, value):
        """
        Return bytes to be stored in self.value
        """
        return value

    def input_html(self, default=None, id_value=None, title=None, mimeType=None):
        return '<input type="file" %stitle="%s" name="%s" %s accept="%s">' % (
         self.id_attr(id_value),
         self.titleHTML(title),
         self.name,
         self._accesskey_attr(),
         mimeType or self.mimeType)


class Password(Input):
    __doc__ = '\n    Password input field:\n    <input type="password">\n    '
    input_type = 'password'


class Radio(Field):
    __doc__ = '\n    Radio buttons:\n    <input type="radio">\n    '

    def __init__(self, name, text, maxValues=1, required=0, default=None, accesskey='', options=None):
        """
        pattern and maxLen are determined from __init__ params
        Additional parameters:
        options
          List of options. Either just a list of strings
          ['value1','value2',..] for simple options
          or a list of tuples of string pairs
          [('value1','description1),('value2','description2),..]
          for options with different option value and description.
        """
        self.setOptions(options)
        self.set_default(default)
        Field.__init__(self, name, text, self.maxLen, maxValues, '', required, default, accesskey)

    def _validate_format(self, value):
        """
        Check format of the user's value for this field.

        Empty input (zero-length string) are valid in any case.
        You might override this method to change this behaviour.
        """
        if value:
            if value not in self.optionValues:
                raise InvalidValueFormat(self.name, self.text.encode(self.charset), value.encode(self.charset))

    def setOptions(self, options):
        self.optionValues = {}
        self.maxLen = 0
        if options:
            for i in options:
                if isinstance(i, tuple):
                    optionValue = i[0]
                else:
                    optionValue = i
                self.optionValues[optionValue] = None
            else:
                self.maxLen = max(map(len, self.optionValues.keys()))

        self.options = list(options)

    def input_html(self, default=None, id_value=None, title=None):
        s = []
        default_value = self._defaultValue(default)
        for i in self.options:
            if isinstance(i, tuple):
                optionValue, optionText = i
            else:
                optionValue = optionText = i
            s.append('\n                <input\n                  type="radio"\n                  %s\n                  title="%s"\n                  name="%s"\n                  %s\n                  value="%s"\n                  %s\n                >%s<br>\n                ' % (
             self.id_attr(id_value),
             self.titleHTML(title),
             self.name.encode(self.charset),
             self._accesskey_attr(),
             optionValue.encode(self.charset),
             ' checked' * (optionValue == default_value),
             optionText.encode(self.charset)))
        else:
            return '\n'.join(s)

    def set_default(self, default):
        """
        Set the default of a default field.

        Mainly this is used if self.default shall be changed after
        initializing the field object.
        """
        option_vals = set()
        for i in self.options:
            if isinstance(i, tuple):
                option_vals.add(i[0])
            else:
                option_vals.add(i)
        else:
            if isinstance(default, str):
                if default not in option_vals:
                    self.options.append(default)
            elif isinstance(default, list):
                self.options.extend([v for v in default if v not in option_vals])
            else:
                if default is not None:
                    raise TypeError('Expected None, str or list for argument default, got %r' % (default,))
            self.default = default


class Select(Radio):
    __doc__ = '\n    Select field:\n    <select multiple>\n      <option value="value">description</option>\n    </select>\n    '

    def __init__(self, name, text, maxValues, required=0, default=None, accesskey='', options=None, size=1, ignoreCase=0, multiSelect=0):
        """
        Additional parameters:
        size
          Integer for the size of displayed select field.
        ignorecase
          Integer flag. If non-zero the case of input strings is ignored
          when checking input values.
        multiSelect
          Integer flag. If non-zero the select field has HTML attribute
          "multiple" set.
        """
        self.size = size
        self.multiSelect = multiSelect
        self.ignoreCase = ignoreCase
        Radio.__init__(self, name, text, maxValues, required, default, accesskey, options)

    def _defaultValue(self, default):
        """returns default value"""
        if default:
            return default
        if self.multiSelect:
            return self.default or set()
        return self.default

    def input_html(self, default=None, id_value=None, title=None):
        res = [
         '<select %stitle="%s" name="%s" %s  size="%d" %s>' % (
          self.id_attr(id_value),
          self.titleHTML(title),
          self.name,
          self._accesskey_attr(),
          self.size,
          ' multiple' * (self.multiSelect > 0))]
        default_value = self._defaultValue(default)
        for i in self.options:
            if isinstance(i, tuple):
                try:
                    optionValue, optionText, optionTitle = i
                except ValueError:
                    optionTitle = None
                    optionValue, optionText = i

            else:
                optionTitle = None
                optionValue = optionText = i
            if self.multiSelect:
                option_selected = optionValue in default_value
            else:
                option_selected = optionValue == default_value or self.ignoreCase and optionValue.lower() == default_value.lower()
            if optionTitle:
                optionTitle_attr = ' title="%s"' % escape_html(optionTitle)
            else:
                optionTitle_attr = ''
            res.append('<option value="%s"%s%s>%s</option>' % (
             escape_html(optionValue),
             optionTitle_attr,
             ' selected' * option_selected,
             escape_html(optionText)))
        else:
            res.append('</select>')
            return '\n'.join(res)


class DataList(Input, Select):
    __doc__ = '\n    Input field combined with HTML5 <datalist>\n    '

    def __init__(self, name, text, maxLen=100, maxValues=1, pattern=None, required=0, default=None, accesskey='', options=None, size=None, ignoreCase=0):
        Input.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)
        if size is None:
            size = max([len(option) for option, _ in options or []])
        self.size = size or 20
        self.multiSelect = 0
        self.ignoreCase = ignoreCase
        self.setOptions(options)
        self.set_default(default)

    def input_html(self, default=None, id_value=None, title=None):
        datalist_id = str(uuid.uuid4())
        s = [
         '<input %stitle="%s" name="%s" %s maxlength="%d" size="%d" value="%s" list="%s">' % (
          self.id_attr(id_value),
          self.titleHTML(title),
          self.name,
          self._accesskey_attr(),
          self.maxLen,
          self.size,
          self._default_html(default),
          datalist_id)]
        s.append(Select.input_html(self,
          default=default,
          id_value=datalist_id,
          title=title).replace('<select ', '<datalist ').replace('</select>', '</datalist>'))
        return '\n'.join(s)


class Checkbox(Field):
    __doc__ = '\n    Check boxes:\n    <input type="checkbox">\n    '

    def __init__(self, name, text, maxValues=1, required=0, accesskey='', default=None, checked=0):
        """
        pattern and maxLen are determined by default
        """
        pattern = default
        maxLen = len(default or '')
        self.checked = checked
        Field.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)

    def input_html(self, default=None, id_value=None, title=None, checked=None):
        if checked is None:
            checked = self.checked
        return '<input type="checkbox" %stitle="%s" name="%s" %s value="%s"%s>' % (
         self.id_attr(id_value),
         self.titleHTML(title),
         self.name,
         self._accesskey_attr(),
         self._default_html(default),
         ' checked' * checked)


class FormException(Exception):
    __doc__ = '\n    Base exception class to indicate form processing errors.\n\n    Attributes:\n    args          unstructured List of parameters\n    '

    def __init__(self, *args, **kwargs):
        self.args = args
        for key, value in kwargs.items():
            setattr(self, key, value)

    def html(self):
        return escape_html(str(self))


class InvalidFormEncoding(FormException):
    __doc__ = '\n    The form data is malformed.\n\n    Attributes:\n    param         name/value causing the exception\n    '

    def __init__(self, param):
        FormException.__init__(self, ())
        self.param = param

    def __str__(self):
        return 'The form data is malformed.'


class ContentLengthExceeded(FormException):
    __doc__ = '\n    Overall length of input data too large.\n\n    Attributes:\n    content_length         received content length\n    maxContentLength      maximum valid content length\n    '

    def __init__(self, content_length, maxContentLength):
        FormException.__init__(self, ())
        self.content_length = content_length
        self.maxContentLength = maxContentLength

    def __str__(self):
        return 'Input length of %d bytes exceeded the maximum of %d bytes.' % (
         self.content_length,
         self.maxContentLength)


class InvalidFieldName(FormException):
    __doc__ = '\n    Parameter with undeclared name attribute received.\n\n    Attributes:\n    name          name of undeclared field\n    '

    def __init__(self, name):
        FormException.__init__(self, ())
        self.name = name

    def __str__(self):
        return 'Unknown parameter %s.' % self.name


class ParamsMissing(FormException):
    __doc__ = '\n    Required parameters are missing.\n\n    Attributes:\n    missingParamNames     list of strings containing all names of missing\n                          input fields.\n    '

    def __init__(self, missingParamNames):
        FormException.__init__(self, ())
        self.missingParamNames = missingParamNames

    def __str__(self):
        return 'Required fields missing: %s' % ', '.join(map(lambda i: '%s (%s)' % (i[1], i[0]), self.missingParamNames))


class InvalidValueFormat(FormException):
    __doc__ = "\n    The user's input does not match the required format.\n\n    Attributes:\n    name          name of input field (Field.name)\n    text          textual description of input field (Field.text)\n    value         input value received\n    "

    def __init__(self, name, text, value):
        FormException.__init__(self, ())
        self.name = name
        self.text = text
        self.value = value

    def __str__(self):
        return 'Invalid input value %r for field %s (%s)' % (
         self.value, self.name, self.text)


class InvalidValueLen(FormException):
    __doc__ = '\n    Length of user input value invalid.\n\n    Attributes:\n    name          name of input field (Field.name)\n    text          textual description of input field (Field.text)\n    valueLen      integer number of received value length\n    maxValueLen   integer number of maximum value length\n    '

    def __init__(self, name, text, valueLen, maxValueLen):
        FormException.__init__(self, ())
        self.name = name
        self.text = text
        self.valueLen = valueLen
        self.maxValueLen = maxValueLen

    def __str__(self):
        return 'Content too long. Field %s (%s) has %d characters but is limited to %d.' % (
         self.text,
         self.name,
         self.valueLen,
         self.maxValueLen)


class TooManyValues(FormException):
    __doc__ = "\n    User's input contained too many values for same parameter.\n\n    Attributes:\n    name                  name of input field (Field.name)\n    text                  textual description of input field (Field.text)\n    valueCount            integer number of values counted with name\n    maxValueCount         integer number of maximum values with name allowed\n    "

    def __init__(self, name, text, valueCount, maxValueCount):
        FormException.__init__(self, ())
        self.name = name
        self.text = text
        self.valueCount = valueCount
        self.maxValueCount = maxValueCount

    def __str__(self):
        return '%d values for field %s (%s). Limited to %d input values.' % (
         self.valueCount,
         self.text,
         self.name,
         self.maxValueCount)


class Form:
    __doc__ = '\n    Class for declaring and processing a whole <form>\n    '

    def __init__(self, inf, env):
        """
        Initialize a Form
        inf                 Read from this file object if method is POST.
        env                 Dictionary holding the environment vars.
        """
        self.field = {}
        self.input_field_names = set()
        self.env = env
        self.inf = inf or sys.stdin
        self.request_method = env['REQUEST_METHOD']
        self.script_name = env['SCRIPT_NAME']
        self.http_accept_charset = helper.AcceptCharsetDict('HTTP_ACCEPT_CHARSET', env)
        self.http_accept_language = helper.AcceptHeaderDict('HTTP_ACCEPT_LANGUAGE', env)
        self.accept_language = self.http_accept_language.keys()
        self.http_accept_encoding = helper.AcceptHeaderDict('HTTP_ACCEPT_ENCODING', env)
        self.query_string = env.get('QUERY_STRING', '')
        self._set_charset()
        for field in self.fields():
            self.add_field(field)

    @property
    def accept_charset(self):
        return self.http_accept_charset.preferred()

    def getContentType(self):
        """
        Determine the HTTP content type of HTTP request
        """
        if self.request_method == 'POST':
            return self.env.get('CONTENT_TYPE', 'application/x-www-form-urlencoded').lower() or None
        return 'application/x-www-form-urlencoded'

    def fields(self):
        """
        Return a list of Field instances to be added to this Form instance.
        """
        return []

    def add_field(self, field):
        """
        Add a input field object f to the form.
        """
        field.charset = self.accept_charset
        self.field[field.name] = field

    def getInputValue(self, name, default=None):
        """
        Return input value of a field defined by name if presented
        in form input. Return default else.
        """
        if name in self.input_field_names:
            return self.field[name].value
        if name in self.field:
            return default
        raise KeyError('Invalid field name %r requested for %s' % (name, self.__class__.__name__))

    def allInputFields(self, fields=None, ignore_fields=None):
        """
        Return list with all former input parameters.

        ignore_fields
            Names of parameters to be excluded.
        """
        ignore_fields = set(ignore_fields or [])
        result = list(fields) or []
        for f in [self.field[p] for p in self.input_field_names - ignore_fields]:
            for val in f.value:
                result.append((f.name, val))
            else:
                return result

    def hidden_fields(self, outf=sys.stdout, ignore_fields=None):
        """
        Output all parameters as hidden fields.

        outf
            File object for output.
        ignore_fields
            Names of parameters to be excluded.
        """
        ignore_fields = ignore_fields or []
        for field in [self.field[p] for p in self.input_field_names - ignore_fields]:
            for val in field.value:
                outf.write('<input type="hidden" name="%s" value="%s">\n\r' % (
                 field.name,
                 escape_html(val)))

    def _add_fields(self):
        """
        can be overwritten to add Field instances to the form
        """
        pass

    def _set_charset(self):
        form_codec = codecs.lookup(self.accept_charset)
        self.uc_encode, self.uc_decode = form_codec[0], form_codec[1]

    def _parse_url_encoded(self, max_content_length):
        if self.request_method == 'POST':
            query_string = self.uc_decode(self.inf.read(int(self.env['CONTENT_LENGTH'])))[0]
        else:
            if self.request_method == 'GET':
                query_string = self.env.get('QUERY_STRING', '')
            else:
                self.inf.close()
                return query_string or None
            content_length = 0
            for name, value in urllib.parse.parse_qsl(query_string,
              keep_blank_values=True,
              strict_parsing=True,
              encoding=(self.accept_charset),
              errors='strict',
              max_num_fields=None):
                if name not in self.field:
                    raise InvalidFieldName(name)
                content_length += len(value)
                if content_length > max_content_length:
                    raise ContentLengthExceeded(content_length, max_content_length)
                self.field[name].set_value(value)
                self.input_field_names.add(name)

    def _parse_mime_multipart(self, max_content_length):
        _, pdict = cgi.parse_header(self.env['CONTENT_TYPE'])
        pdict['boundary'] = pdict['boundary'].encode('ascii')
        pdict['CONTENT-LENGTH'] = self.env['CONTENT_LENGTH'].encode('ascii')
        parts = cgi.parse_multipart(self.inf, pdict)
        content_length = 0
        for name in parts.keys():
            if name not in self.field:
                raise InvalidFieldName(name)

        for value in parts[name]:
            content_length += len(value)
            if content_length > max_content_length:
                raise ContentLengthExceeded(content_length, max_content_length)
            self.field[name].set_value(value)
            self.input_field_names.add(name)

    def getInputFields(self):
        """
        Process user's <form> input and store the values in each
        field instance's content attribute.

        When a processing error occurs FormException (or derivatives)
        are raised.
        """
        maxContentLength = 0
        for _, field in self.field.items():
            maxContentLength += field.maxValues * field.maxLen
        else:
            content_type = self.getContentType()
            if content_type.startswith('application/x-www-form-urlencoded'):
                self._parse_url_encoded(maxContentLength)
            else:
                if content_type.startswith('multipart/form-data'):
                    self._parse_mime_multipart(maxContentLength)
                else:
                    raise FormException('Invalid content received: %r' % content_type)
            missing_params = []
            for _, field in self.field.items():
                if field.required:
                    if field.name not in self.input_field_names:
                        missing_params.append((field.name, field.text))
                    if missing_params:
                        raise ParamsMissing(missing_params)