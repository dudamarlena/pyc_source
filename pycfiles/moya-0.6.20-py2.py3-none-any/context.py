# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/context.py
# Compiled at: 2017-07-03 12:47:35
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from ..elements.elementbase import LogicElement, ReturnContainer, Attribute
from ..context import Context, Expression
from ..context.expressiontime import ExpressionDateTime, TimeSpan
from ..context import dataindex
from ..context.errors import ContextKeyError
from ..containers import OrderedDict
from ..render import render_object
from ..progress import Progress
from ..tools import make_cache_key
from .. import namespaces
from ..logic import DeferNodeContents, SkipNext, Unwind, EndLogic, BreakLoop, ContinueLoop, MoyaException
from ..console import style as console_style
from ..render import HTML
from ..html import escape as escape_html
from ..compat import zip_longest, raw_input, text_type, string, xrange, PY3
import json, weakref, getpass, time
from collections import defaultdict
from datetime import datetime
from random import choice
from copy import copy
from time import sleep
from textwrap import dedent
import sys, locale, logging
log = logging.getLogger(b'moya.runtime')
try:
    import readline
except ImportError:
    pass

class ContextElementBase(LogicElement):
    pass


class If(ContextElementBase):
    """
    Conditional [i]IF[/i] tag, executes the enclosing block if a condition evaluates to [i]true[/i]. If the condition evaluates to [i]false[/i], the enclosing block is skipped. May be followed by [tag]else[/tag] or [tag]elif[/tag].

    """

    class Help:
        synopsis = b'execute block if a condition is true'
        example = b'\n        <if test="coffee==0">\n            <echo>Get more coffee</echo>\n        </if>'

    test = Attribute(b'Test expression', required=True, metavar=b'CONDITION', type=b'expression')

    def logic(self, context):
        if self.test(context):
            yield DeferNodeContents(self)
            yield SkipNext((self.xmlns, b'else'), (self.xmlns, b'elif'))


class IfPost(ContextElementBase):
    """
    Executes the enclosing block if the current request is a POST request.

    Basically a shorthand for:

    [code xml]<if test=".request.method=='POST'">[/code]

    May be followed by [tag]else[/tag] or [tag]elif[/tag].

    """

    class Help:
        synopsis = b'execute a block if this is a POST request'
        example = b'<if-post>\n    <!-- validate form -->\n</if-post>\n<else>\n    <!-- not a post request -->\n</else>'

    def logic(self, context):
        if context.get(b'.request.method', None) == b'POST':
            yield DeferNodeContents(self)
            yield SkipNext((self.xmlns, b'else'), (self.xmlns, b'elif'))
        return


class IfGet(ContextElementBase):
    """
    Executes the enclosing block if the current request is a GET request.

    Basically a shorthand for:

    [code xml]<if test=".request.method=='GET'">[/code]

    May be followed by [tag]else[/tag] or [tag]elif[/tag].

    """

    class Help:
        synopsis = b'exectute a block if this is a GET request'

    def logic(self, context):
        if context.get(b'.request.method', None) == b'GET':
            yield DeferNodeContents(self)
            yield SkipNext((self.xmlns, b'else'), (self.xmlns, b'elif'))
        return


class Else(ContextElementBase):
    """Execute the enclosed block if a previous [tag]if[/tag] statement is false."""

    class Help:
        synopsis = b'execute a block if the previous <if> statement is false'
        example = b'\n<if test="coffee==0">\n    <echo>Get more coffee</echo>\n</if>\n<else>\n    <echo>Have a cup of coffee</echo>\n</else>\n\n'

    def logic(self, context):
        yield DeferNodeContents(self)


class Elif(ContextElementBase):
    """Executes the enclosed block if a previous [tag]if[/tag] (or [tag]elif[/tag]) statement is false, and another condition is true."""

    class Help:
        synopsis = b'an <else> with a condition'
        example = b'<if test="hobbits == 0">\n    <echo>There are no hobbits</echo>\n</if>\n<elif test="hobbits == 1">\n    <echo>There is one hobbit</echo>\n</elif>\n<else>\n    <echo>There are many hobbits</echo>\n</else>\n'

    test = Attribute(b'Test expression', required=True, metavar=b'CONDITION', type=b'expression')

    def logic(self, context):
        if self.test(context):
            yield DeferNodeContents(self)
            yield SkipNext((self.xmlns, b'else'), (self.xmlns, b'elif'))


class Try(ContextElementBase):
    """Executes the enclosed block as part of a [tag]try[/tag][tag]catch[/tag] structure. """

    class Meta:
        is_try = True

    class Help:
        synopsis = b'detect exceptions within a block'
        example = b'\n<try>\n    <echo>${1/0}</echo>  <!-- will throw a math exception -->\n</try>\n<catch exception="*">\n    <echo>The try block threw an exception</echo>\n</catch>\n'

    def logic(self, context):
        yield DeferNodeContents(self)


class ExceptionProxy(object):

    def __init__(self, msg, type, info):
        self.msg = msg
        self.type = type
        self.info = info

    def __repr__(self):
        return (b"<exception '{}'>").format(self.msg)


class Catch(ContextElementBase):
    """Catches any [link moyacode#exceptions]exceptions[/link] from the previous block."""

    class Help:
        synopsis = b'catch exceptions from the previous block'
        example = b'\n<try>\n    <echo>${1/0}</echo>  <!-- will throw a math exception -->\n</try>\n<catch exception="math.divistion-error">\n    <echo>The try block threw an exception</echo>\n</catch>\n\n<!-- A <try> block is only necessary if there are multiple statements you want to catch exceptions for -->\n<echo>${1/0}<echo>\n<catch exception="math.division-error">\n    <echo>You can\'t divide by zero!</echo>\n</catch>\n\n        '

    exception = Attribute(b'Type of exception to catch', type=b'commalist', default=b'*', evaldefault=True)
    dst = Attribute(b'Destination to store exception object', type=b'reference')

    class Meta:
        logic_skip = True

    @classmethod
    def compare_exception(cls, type, catch_types):
        type_tokens = type.split(b'.')
        for catch_type in catch_types:
            for c, e in zip_longest(catch_type.split(b'.'), type_tokens, fillvalue=None):
                if c == b'*':
                    return True
                if c != e:
                    break
            else:
                return True

        return False

    def check_exception_type(self, context, type):
        catch_type = self.exception(context)
        return self.compare_exception(type, catch_type)

    def set_exception(self, context, exception):
        dst = self.dst(context)
        if dst is not None:
            context[dst] = ExceptionProxy(exception.msg, exception.type, exception.info)
        return


class Attempt(ContextElementBase):
    """Repeat a block of code if an exception is thrown. This is useful in situations where you are creating a database object
    with a random token, and you want to repeat the code if the random token happens to exist. The [c]wait[/c] attribute can set a timespan
    to wait between attempts, which may be appropriate for connecting to servers, for example.

    If an exception occurs, after [c]times[/c] attempts, then it will be thrown normally.

    [aside]Always set [c]times[/c] to a reasonable value. Programming errors could result in Moya getting stuck in a pointless loop.[/aside]

    """

    class Help:
        synopsis = b'repeat a block until it is successful'
        example = b'\n        <attempt times="10" catch="db.*">\n            <db:create model="#ValidateEmail" let:user="user" dst="validate_email" />\n        </attempt>\n\n        '

    times = Attribute(b'Maximum number of times to repeat attempt block', type=b'integer', required=True)
    catch = Attribute(b'Type of exception to catch', type=b'commalist', default=b'*', evaldefault=True)
    wait = Attribute(b"Time to wait between syncs (default doesn't wait)", type=b'timespan', default=None, required=False)

    class Meta:
        trap_exceptions = True

    def on_exception(self, context, exception):
        stack = context.set_new_call(b'._attempt_stack', list)
        try:
            top = stack[(-1)]
        except IndexError:
            return

        if not Catch.compare_exception(exception.type, top[b'type']):
            return
        else:
            top[b'times'] -= 1
            if top[b'times'] > 0:
                if top[b'wait']:
                    time.sleep(top[b'wait'])
                return DeferNodeContents(self)
            return

    def logic(self, context):
        attempt_times = self.times(context)
        exception_type = self.catch(context)
        wait = self.wait(context)
        stack = context.set_new_call(b'._attempt_stack', list)
        stack.append({b'times': attempt_times, b'type': exception_type, 
           b'wait': wait})
        try:
            yield DeferNodeContents(self)
        except:
            stack.pop()


class With(ContextElementBase):
    """Merge values with the current scope in the enclosed block. The values in the let map will persist only in the enclosed block."""

    class Help:
        synopsis = b'create a new data scope'
        example = b'\n<with let:hobbit="Sam">\n    <echo>${hobbit} is my favorite hobbit.\n</with>\n<!-- \'hobbit\' will no longer exist at this point -->\n<echo if="missing:hobbit">Where is the hobbit?</echo>\n\n'

    def logic(self, context):
        let_map = self.get_let_map(context)
        with context.data_scope(let_map):
            yield DeferNodeContents(self)


class DataSetterBase(ContextElementBase):
    default = None
    dst = Attribute(b'Destination', type=b'reference', default=None)

    class Help:
        undocumented = True

    def get_default(self):
        return self.default

    def set_context(self, context, dst, value):
        try:
            if dst is None:
                obj = context.obj
                append = getattr(obj, b'append', None)
                if append is not None:
                    append(value)
                    return text_type(len(obj) - 1)
                return dst
            else:
                context[dst] = value
                return dst
        except ValueError as e:
            msg = b"unable to set '{key}' to {value} ({e})"
            msg = msg.format(key=context.to_expr(dst), value=context.to_expr(value), e=text_type(e))
            self.throw(b'let.fail', msg)

        return

    def logic(self, context):
        self.set_context(context, self.dst(context), self.get_value(context))

    def get_value(self, context):
        if self.text:
            return self.process_value(context, self.text)
        return self.default

    def process_value(self, context, value):
        return value


class DataSetter(DataSetterBase):
    default = None
    dst = Attribute(b'Destination', type=b'reference', default=None)
    value = Attribute(b'Value', type=b'expression', default=None)

    class Help:
        undocumented = True


class Var(DataSetter):
    """Set a variable"""

    class Help:
        synopsis = b'create a value'
        example = b'\n<var dst="count">10</var>\n'

    def logic(self, context):
        dst, value = self.get_parameters(context, b'dst', b'value')
        if not self.has_parameter(b'value'):
            value = context.eval(context.sub(self.text))
        self.set_context(context, dst, value)


class SetItem(LogicElement):
    """Set a value in a container"""

    class Help:
        synopsis = b'set an indexed value on a collection'
        example = b'\n        <dict dst="moya" />\n        <set-item src="moya" index="\'crew\'" value="[\'john\', \'rygel\'] />\n        '

    src = Attribute(b'collection object', type=b'expression', required=True)
    index = Attribute(b'index to set', type=b'expression', required=True)
    value = Attribute(b'value to set', type=b'expression', required=True)

    def logic(self, context):
        src, index, value = self.get_parameters(context, b'src', b'index', b'value')
        src[index] = value


class Let(DataSetter):
    """Sets multiple variable from expressions."""

    class Help:
        synopsis = b'create variables from expressions'
        example = b'\n<let count="10" hobbit="\'Sam\'" hobbits="count * hobbit" />\n        '

    class Meta:
        all_attributes = True

    _reserved_attribute_names = [
     b'if']
    preserve_attributes = [b'expressions']

    def post_build(self, context, _parse=dataindex.parse, _Expression=Expression, setter=Context.set, simple_setter=Context.set_simple):
        self.expressions = []
        append = self.expressions.append
        for k, v in self._attributes.items():
            if k not in self._reserved_attribute_names:
                indices = _parse(k)
                if indices.from_root or len(indices) > 1:
                    append((setter, indices, _Expression(v).eval))
                else:
                    append((simple_setter, indices.tokens[0], _Expression(v).eval))

    def logic(self, context):
        try:
            for setter, indices, _eval in self.expressions:
                setter(context, indices, _eval(context))

        except ContextKeyError as e:
            self.throw(b'let.fail', text_type(e))


class LetParallel(Let):
    """
    Sets multiple variables in parallel.

    Like [tag]let[/tag], this tag sets values to the results of expressions, but evaluates all the expressions before assignment.

    One use for this, is to [i]swap[/i] variables without using an intermediate.
    """

    class Help:
        synopsis = b'set values in parallel.'
        example = b'\n        <str dst="a">foo</str>\n        <str dst="b">bar</str>\n        <let-parallel a="b" b="a" />\n        '

    class Meta:
        all_attributes = True

    _reserved_attribute_names = [
     b'if']

    def logic(self, context):
        values = [ _eval(context) for setter, indices, _eval in self.expressions ]
        try:
            for (setter, indices, _eval), value in zip(self.expressions, values):
                setter(context, indices, value)

        except ContextKeyError as e:
            self.throw(b'let.fail', text_type(e))


class LetStr(DataSetter):
    """Like [tag]let[/tag] but sets variables as strings. Setting strings with [tag]let[/tag] can look a little clumsy because of the requirement to escape the text twice. [tag]let-str[/tag] treats attributes as strings and not expressions."""

    class Help:
        synopsis = b'create string variables'
        example = b'\n<let-str hobbit="Sam" dwarf="Durin" />\n'

    class Meta:
        all_attributes = True

    _reserved_attribute_names = [
     b'if']
    preserve_attributes = [b'expressions']

    def post_build(self, context):
        self.expressions = []
        append = self.expressions.append
        for k, v in self._attributes.items():
            if k not in self._reserved_attribute_names:
                append((dataindex.parse(k), v))

    def logic(self, context):
        sub = context.sub
        for k, v in self.expressions:
            context[k] = sub(v)


class Int(DataSetter):
    """Set an integer value."""
    default = 0

    class Help:
        synopsis = b'create an integer'
        example = b'\n<int dst="count" value="10"/>\n<int dst="position" /> <!-- defaults to 0 -->\n\n'

    def process_value(self, context, value):
        return int(value)

    def logic(self, context):
        dst, value = self.get_parameters(context, b'dst', b'value')
        if not self.has_parameter(b'value'):
            value = context.sub(self.text) or 0
        self.set_context(context, dst, int(value))


class Float(DataSetter):
    """Set a float value"""
    default = 0.0

    class Help:
        synopsis = b'create a floating point value'
        example = b'\n    <int dst="count" value="10"/>\n    <int dst="position" /> <!-- defaults to 0.0 -->\n\n    '

    def logic(self, context):
        dst, value = self.get_parameters(context, b'dst', b'value')
        if not self.has_parameter(b'value'):
            value = context.sub(self.text) or 0.0
        self.set_context(context, dst, float(value))


class Str(DataSetter):
    """Sets a string value to text contexts."""

    class Help:
        synopsis = b'create a string'
        example = b'\n<str dst="hobbit">Sam</str>\n<str dst="text"/> <!-- defaults to empty string -->\n'

    default = b''
    value = Attribute(b'Value', type=b'expression', default=None)

    def get_value(self, context):
        if self.has_parameter(b'value'):
            return self.value(context)
        return context.sub(self.text)


class Replace(DataSetter):
    """
    Replace occurrences of a regex in a string.

    """

    class Help:
        synopsis = b'replace occurrences of a regex.'
        example = b'\n<str dst="mail_template">\n    Dear NAME,\n\n    Welcome!\n</str>\n<replace src="mail_template" dst="mail" regex="NAME">\n    <return-str>John</return-str>\n</replace>\n        '

    src = Attribute(b'Source object to fill in fields', type=b'reference')
    regex = Attribute(b'Regular Expression', type=b'regex', required=True)

    class Meta:
        is_call = True

    def logic(self, context):
        dst, src, regex = self.get_parameters(context, b'dst', b'src', b'regex')
        text = text_type(context.get(src))
        output = []
        pos = 0
        start = None
        end = None
        for match in regex.finditer(text):
            start, end = match.span(0)
            if start > pos:
                output.append(text[pos:start])
                pos = end
            self.push_call(context, match.groupdict().copy())
            try:
                yield DeferNodeContents(self)
            finally:
                call = self.pop_call(context)

            if b'_return' in call:
                value = _return = call[b'_return']
                if hasattr(_return, b'get_return_value'):
                    value = _return.get_return_value()
            else:
                value = None
            repl = text_type(value or b'')
            output.append(repl)

        if start is None:
            output.append(text)
        elif end is not None:
            output.append(text[end:])
        new_text = (b'').join(output)
        self.set_context(context, dst, new_text)
        return


class WrapTag(DataSetter):
    """Wraps text in a HTML tag."""

    class Help:
        synopsis = b'wrap a string in a HTML tag'
        example = b'\n        <!-- Wrap the string "Hello, World" in a P tag -->\n        <wrap-tag tag="p" dst="paragraph">Hello, World!</wrap-tag>\n        <echo>${paragraph}</echo>\n        '

    tag = Attribute(b'Tag', default=b'span')

    def get_value(self, context):
        tag = self.tag(context)
        _let = self.get_let_map(context)
        if _let:
            attribs = b' ' + (b' ').join((b'{}="{}"').format(k, escape_html(v)) for k, v in _let.items())
        else:
            attribs = b''
        return (b'<{tag}{attribs}>{text}</{tag}>').format(tag=tag, attribs=attribs, text=escape_html(context.sub(self.text)))


class Dedent(DataSetter):
    """Removes common whitespace from the start of lines."""

    class Help:
        synopsis = b'remove common whitespace from a string'
        example = b'\n        <dedent dst="text">\n            This text will have the initial whitespace removed\n                This will start with only 4 spaces\n            Back to column 0\n        </dedent>\n        '

    def get_value(self, context):
        text = context.sub(self.value(context) or self.text)
        dedent_text = dedent(text)
        return dedent_text


class HTMLTag(DataSetter):
    """Sets a variable to HTML."""

    class Help:
        synopsis = b'create raw html'
        example = b'\n        <html dst="my_html"><![CDATA[\n           <h1>Hello, World!</h1>\n        ]]></html>\n        '

    class Meta:
        tag_name = b'html'

    def get_value(self, context):
        if self.has_parameter(b'value'):
            text = self.value(context)
        else:
            text = context.sub(self.text)
        return HTML(text)


class _TimeSpan(DataSetter):
    """Create a datetime object"""

    class Help:
        synopsis = b'create a timespan object'
        example = b'\n        <time-span dst="span" value="1d"/>\n        '

    value = Attribute(b'Value', type=b'text', default=b'')

    def get_value(self, context):
        text = self.value(context) or context.sub(self.text)
        if not text:
            self.throw(b'time-span.invalid', b'no timespan value specified')
        try:
            return TimeSpan(text)
        except ValueError as e:
            self.throw(b'time-span.invalid', text_type(e))


class Datetime(DataSetter):
    """
    Create a Moya [i]datetime[/i] object.

    Datetime objects have the following properties:

    [definitions]
        [define year]The year (integer)[/define]
        [define month]The month (integer) (1 is January)[/define]
        [define day]The day (integer)[/define]
        [define hour]The hours in the time[/define]
        [define minute]The number of minutes in the time[/define]
        [define second]The number of seconds in the time[/define]
        [define microseconds]The number of microseconds in the time[/define]
        [define isoformat]The date/time in [url http://en.wikipedia.org/wiki/ISO_8601]ISO 8601[/url] format[/define]
        [define next_day]The date/time + 24 hours[/define]
        [define previous_day]The date/time - 24 hours[/define]
        [define year_start]January 1st at the beginning of the year[/define]
        [define day_start]The beginning of the day (midnight)[/define]
        [define next_year]January 1st of the next year[/define]
        [define next_month]First day of the next month[/define]
        [define next_day]The start of the next day[/define]
        [define previous_day]The start of the previous day[/define]
        [define previous_year]Jan 1st of the previous year[/define]
        [define previous_monthy]First date of the previous month[/define]
        [define days_in_month]Number of days in the current month[/define]
        [define epoch]Number of seconds since Jan 1st 1970[/define]
        [define html5_datatime]Date/Time in HTML5 format[/define]
        [define html5_data]Date in HTML5 format[/define]
        [define html_time]Time in HTML5 format[/define]
        [define utc]Date/Time in UTC timezone[/define]
        [define local]DateTime in local timezone (references [c].tz[/c])[/define]
    [/definitions]

    """

    class Help:
        synopsis = b'create a date/time object'
        example = b'\n        <datetime year="1974" month="7" day="5" dst="birthday" />\n        <echo>Your birthday is ${localize:birthday}</echo>\n        '

    year = Attribute(b'Year', type=b'integer', required=True)
    month = Attribute(b'Month', type=b'integer', required=False, default=1)
    day = Attribute(b'Month', type=b'integer', required=False, default=1)
    hour = Attribute(b'Hour', type=b'integer', required=False, default=0)
    minute = Attribute(b'Minute', type=b'integer', required=False, default=0)
    second = Attribute(b'Second', type=b'integer', required=False, default=0)

    def get_value(self, context):
        try:
            return ExpressionDateTime(*self.get_parameters(context, b'year', b'month', b'day', b'hour', b'minute', b'second'))
        except Exception as e:
            self.throw(b'datetime.invalid', text_type(e))


class Bool(DataSetter):
    """Create a boolean (True or False value)."""

    class Help:
        synopsis = b'create a boolean'
        example = b'\n        <bool dst="bool"/> <!-- False -->\n        <bool dst="bool">yes</bool> <!-- True -->\n        <bool dst="bool">no</bool> <!-- False -->\n        <bool dst="bool" value="1"/> <!--True -->\n        <bool dst="bool" value="0"/> <!-- False -->\n        '

    default = False

    def logic(self, context):
        if self.text:
            value = self.text.lower() in ('yes', 'true')
        else:
            value = self.value(context)
        self.set_context(context, self.dst(context), bool(value))


class True_(DataSetter):
    """Creates a boolean with a value of True."""

    class Help:
        synopsis = b'create a True boolean'
        example = b'\n        <true dst="bool"/> <!-- Always True -->\n        '

    default = True

    def get_value(self, context):
        return True


class False_(DataSetter):
    """Creates a boolean with a value of False."""

    class Help:
        synopsis = b'create a False boolean'
        example = b'\n        <false dst="bool"/> <!-- Always False -->\n        '

    default = False

    def get_value(self, context):
        return False


class None_(DataSetter):
    """Create a None value."""

    class Help:
        synopsis = b'Create a value of None'
        example = b'\n        <none dst="hobbits"/>\n        <echo>Hobbits in England: ${hobbits}</echo>\n        '

    default = None

    def get_value(self, context):
        return


class Now(DataSetter):
    """Create a datetime objects for the current time. The datetime is in UTC, use the [c]localize:[/c] modifier to display a time in the user's current timezone."""

    class Help:
        synopsis = b'get the current date/time'
        example = b'\n        <now dst="now" />\n        <echo>The time is ${localize:now}</now>\n        '

    def logic(self, context):
        self.set_context(context, self.dst(context), datetime.utcnow())


class List(DataSetter):
    """Creates a list. Any data items in the enclosed block are added to the list."""

    class Help:
        synopsis = b'create a list'
        example = b'\n        <list dst="hobbits">\n            <str>Sam</str>\n            <str>Bilbo</str>\n            <str>Frodo</str>\n        </list>\n        <echo>${commalist:hobbits}</echo>\n        <list dst="empty"/>\n        '

    def logic(self, context):
        dst = self.set_context(context, self.dst(context), [])
        context.push_scope(dst)
        try:
            yield DeferNodeContents(self)
        finally:
            context.pop_scope()


class Lines(DataSetter):
    """
    Create a list from lines.

    This tag create a list of strings from the lines in the enclosed text. Lines are striped of whitespace.

    The following two examples are equivalent:

    [code python]
    <list dst="hobbits">
        <str>Sam</str>
        <str>Bilbo</str>
        <str>Frodo</str>
    </list>
    [/code]
    [code]
    <lines dst="hobbits">
        Sam
        Bilbo
        Frodo
    </lines>
    [/code]
    """

    class Help:
        synopsis = b'create a list from lines'
        example = b'\n        <lines dst="hobbits">\n            Sam\n            Bilbo\n            Frodo\n        </lines>\n        '

    def get_value(self, context):
        return [ s.strip() for s in context.sub(self.text).strip().splitlines() ]


class Sum(DataSetter):
    """Sums a sequence of values together."""

    class Help:
        synopsis = b'sums a sequence of values'
        example = b'\n        <sum dst="moluae">\n            <int>2</int>\n            <int>40</int>\n        </sum>\n        <echo>${moluae}</echo>\n        '

    def logic(self, context):
        container = []
        list_index = self.set_context(context, self.dst(context), container)
        context.push_scope(list_index)
        try:
            yield DeferNodeContents(self)
        finally:
            context.pop_scope()

        self.set_context(context, self.dst(context), sum(container))


class AppendableSet(set):
    """A set with an 'append' method that is an alias for 'add'"""

    def append(self, value):
        return self.add(value)


class Set(DataSetter):
    """Create a [i]set[/i] object. A set is a container, where each item may only appears once. Any data items in the enclosed block are added to the set."""

    class Help:
        synopsis = b'create a set object'
        example = b'\n        <set dst="hobbits">\n            <str>Sam</str>\n            <str>Bilbo</str>\n            <str>Frodo</str>\n            <str>Bilbo</str>\n            <str>Sam</str>\n        </set>\n        <!-- Will display 3, because duplicates are removed -->\n        <echo>There are ${len:hobbits} in the set.</echo>\n\n        '

    def logic(self, context):
        dst = self.set_context(context, self.dst(context), AppendableSet())
        context.push_scope(dst)
        try:
            yield DeferNodeContents(self)
        finally:
            context.pop_scope()


class Dict(DataSetter):
    """Create a [i]dictionary[/i] object. A dictionary maps [i]keys[/i] on to [i]values[/i]. The keys and values are defined in the enclosing block, or via the [i]let map[/i]."""

    class Help:
        synopsis = b'create a dict object'
        example = b'\n        <dict dst="species">\n            <str dst="Bibo">Hobbit</dst>\n            <str dst="Gandalph">Wizard</dst>\n        </dict>\n        <!-- Alternatively -->\n        <dict dst="species" let:Bilbo="Hobbit" let:Gandalph="Wizard" />\n        <echo>Bilbo is a ${species[\'Bilbo\']}</echo>\n\n        '

    default = Attribute(b'Default return for missing keys', type=b'expression', required=False, default=None)
    sequence = Attribute(b'Optional sequence of key / value pairs to initialize the dict', type=b'expression', required=False)
    _default_types = {b'dict': OrderedDict, b'list': list, 
       b'int': int, 
       b'float': float}

    def logic(self, context):
        sequence = self.sequence(context)
        if self.has_parameter(b'default'):
            default = self.default(context)
            obj = defaultdict(lambda : copy(default))
        else:
            obj = {}
        obj.update(self.get_let_map(context))
        if sequence:
            obj.update(sequence)
        dst = self.set_context(context, self.dst(context), obj)
        with context.scope(dst):
            yield DeferNodeContents(self)


class Unpack(DataSetter):
    """Unpack the keys and values in an object, and set them on the parent"""
    obj = Attribute(b'Object to unpack', type=b'expression')

    def logic(self, context):
        obj = self.obj(context)
        try:
            items = obj.items()
        except:
            self.throw(b'bad-value.map-required', b'a dict or other mapping is required for obj')

        for k, v in items:
            self.set_context(context, context.escape(k), v)


class MakeToken(DataSetter):
    """Generates a token of random characters. This is useful for creating unique IDs for database objects."""

    class Help:
        synopsis = b'make an opaque token'
        example = b'\n        <maketoken dst="authorization_token" size="16" />\n        '

    lowercase = Attribute(b'Use lower case characters', type=b'boolean', default=True, required=False)
    uppercase = Attribute(b'Use upper case characters', type=b'boolean', default=True, required=False)
    digits = Attribute(b'Use digits', type=b'boolean', default=True, required=False)
    punctuation = Attribute(b'Use punctuation', type=b'boolean', default=False, required=False)
    size = Attribute(b'Size', type=b'integer', default=20, required=False)

    def get_value(self, context):
        size, lowercase, uppercase, digits, punctuation = self.get_parameters(context, b'size', b'lowercase', b'uppercase', b'digits', b'punctuation')
        choices = b''
        if lowercase:
            choices += string.lowercase
        if uppercase:
            choices += string.uppercase
        if digits:
            choices += string.digits
        if punctuation:
            choices += string.punctuation
        if not choices:
            self.throw(b'token', b'No characters to choice from')
        token = (b'').join(choice(choices) for _ in xrange(size))
        return token


class ODict(Dict):
    """Like <dict> but creates an [i]ordered[/i] dictionary (maintains the order data was inserted)/"""

    def logic(self, context):
        dst = self.set_context(context, self.dst(context), OrderedDict(self.get_let_map(context)))
        context.push_scope(dst)
        yield DeferNodeContents(self)


class Throw(Dict):
    """Throw a Moya exception. An exception consists of a name in dotted notation with an optional message.

    Custom exceptions should be named to start with the [i]long name[/i] of the library. Moya reserves exceptions with a single dot for internal use. These [i]may[/i] be thrown if appropriate.

    """

    class Help:
        synopsis = b'throw an exception'
        example = b'\n        <try>\n            <throw exception="middle.earth.cant" msg="One can\'t simply do that!"/>\n        </try>\n        <except exception="middle.earth.*" dst="error">\n            <echo>Error: ${error.msg}</echo>\n        </except>\n\n        '

    exception = Attribute(b'Type of exception', required=True)
    msg = Attribute(b'Message', default=b'exception thrown', required=False)

    def logic(self, context):
        exception, msg = self.get_parameters(context, b'exception', b'msg')
        info = context[b'_e'] = {}
        with context.scope(b'_e'):
            yield DeferNodeContents(self)
        raise MoyaException(exception, msg, info)


class Choose(DataSetter):
    """Pick a random element from a sequence."""

    class Help:
        synopsis = b'choose a random value from a collection'
        example = b'\n        <choose dst="hobbit" from="[\'bilbo\',\'sam\',\'frodo\']"/>\n        <echo>Hobbit: ${hobbit}</echo>\n        '

    _from = Attribute(b'Container', required=True, type=b'expression')
    dst = Attribute(b'Destination', default=None, metavar=b'DESTINATION', type=b'reference', required=True)

    def logic(self, context):
        _from, dst = self.get_parameters(context, b'from', b'dst')
        self.set_context(context, dst, choice(_from))


class JSON(DataSetter):
    """Sets data from JSON (JavasSript Object Notation)."""
    src = Attribute(b'JSON source', type=b'expression', required=False)

    class Help:
        synopsis = b'create data from JSON'
        example = b'\n        <json dst="hobbits">\n            ["Bilbo", "Sam", "Frodo"]\n        </json>\n\n        '

    def logic(self, context):
        self.set_context(context, self.dst(context), self.get_value(context))

    def get_value(self, context):
        if self.has_parameter(b'src'):
            text = self.src(context)
        else:
            text = self.text
        try:
            return json.loads(text)
        except Exception as e:
            self.throw(b'json.invalid', text_type(e))


class Slice(ContextElementBase):
    """Slice a sequence of values (extract a range of indexed values)."""

    class Help:
        synopsis = b"get a 'slice' of a collection"
        example = b'\n        <slice src="hobbits" start="1" stop="3" dst="slice_of_hobbits"/>\n\n        '

    src = Attribute(b'Value to slice', required=True, type=b'reference', metavar=b'ELEMENTREF')
    dst = Attribute(b'Destination for slice', required=True, type=b'reference', metavar=b'ELEMENTREF')
    start = Attribute(b'Start point', type=b'expression', default=None)
    stop = Attribute(b'End point', type=b'expression', default=None)

    def logic(self, context):
        src, dst, start, stop = self.get_parameters(context, b'src', b'dst', b'start', b'stop')
        src_obj = context[src]
        if hasattr(src_obj, b'slice'):
            context[dst] = src_obj.slice(start or 0, stop)
        else:
            context[dst] = src_obj[start:stop]


class Page(ContextElementBase):
    """Chop a sequence in to a [i]page[/i].

    This breaks up a sequence in to a page, based on a page size and index. Useful for paginating search results.
    """

    class Help:
        synopsis = b'get a page of results'
        example = b'\n        <page src="results" page="2" pagesize="10" />\n        '

    src = Attribute(b'Value to slice', required=True, type=b'reference', metavar=b'ELEMENTREF')
    dst = Attribute(b'Destination for slice', required=True, type=b'reference', metavar=b'ELEMENTREF')
    page = Attribute(b'Page', type=b'expression', required=False, default=b'.request.GET.page or 1', evaldefault=True)
    pagesize = Attribute(b'Page size', type=b'expression', required=False, default=10)

    def logic(self, context):
        src, dst, page, pagesize = self.get_parameters(context, b'src', b'dst', b'page', b'pagesize')
        try:
            page = int(page or 1)
        except ValueError:
            page = 1

        start = (page - 1) * pagesize
        stop = page * pagesize
        src_obj = context[src]
        if hasattr(src_obj, b'slice'):
            context[dst] = src_obj.slice(start, stop)
        else:
            context[dst] = src_obj[start:stop]


class Inc(ContextElementBase):
    """Increment (add 1 to) a value."""

    class Help:
        synopsis = b'increment a value'
        example = b'\n        <let hobbit_count="1" />\n        <inc dst="hobbit_count" />\n        <echo>${hobbit_count}</echo> <!-- 2 -->\n        '

    dst = Attribute(b'Value to increment', required=True, type=b'reference', metavar=b'ELEMENTREF')

    def logic(self, context):
        try:
            context[self.dst(context)] += 1
        except:
            self.throw(b'inc.fail', b'unable to increment')


class Dec(ContextElementBase):
    """Decrement (subtract 1 from) a value."""

    class Help:
        synopsis = b'decrement a value'
        example = b'\n        <let hobbit_count="2" />\n        <dec dst="hobbit_count" />\n        <echo>${hobbit_count}</echo> <!-- 1 -->\n        '

    dst = Attribute(b'Value to decrement', required=True, type=b'reference')

    def logic(self, context):
        try:
            context[self.dst(context)] -= 1
        except:
            self.throw(b'dec.fail', b'unable to decrement')


class Copy(ContextElementBase):
    """Copy a variable from one location to another"""

    class Help:
        synopsis = b'copy a value'
        example = b'\n        <str dst="foo">Kirk</str>\n        <copy src="foo" dst="bar" />\n        <echo>${bar}</echo>\n        '

    src = Attribute(b'Source', required=True, type=b'reference')
    dst = Attribute(b'Destination', required=True, type=b'reference')

    def logic(self, context):
        context.copy(*self.get_parameters(context, b'src', b'dst'))


class Link(ContextElementBase):
    """Create a [i]link[/i] in the context. Similar to a symlink in the filesystem, a link creates a variable that references another value."""

    class Help:
        synopsis = b'link variables'
        example = b'\n        <str dst="foo">Hello</str>\n        <link src="foo" dst="bar" />\n        <str dst="bar">World</str>\n        <echo>${foo}</bar> <!-- World -->\n        <echo>${bar}</bar> <!-- World -->\n\n        '

    src = Attribute(b'Source', required=True, type=b'reference')
    dst = Attribute(b'Destination', required=True, type=b'reference')

    def logic(self, context):
        context.link(*self.get_parameters(context, b'dst', b'src'))


class Append(ContextElementBase):
    """Append a value to a list or other collection."""

    class Help:
        synopsis = b'append a value to a list'
        example = b'\n        <list dst="crew">\n            <str>John</str>\n        </list>\n        <append src="crew" value="\'Scorpius\'"/>\n        '

    class Meta:
        one_of = [
         ('value', 'values')]

    value = Attribute(b'Value to append', type=b'expression', missing=False, required=False)
    values = Attribute(b'A sequence of values to append', type=b'expression', missing=False, required=False)
    src = Attribute(b'Collection to append to', type=b'expression', required=True, missing=False)

    def logic(self, context):
        value, values, src = self.get_parameters(context, b'value', b'values', b'src')
        if self.has_parameter(b'value'):
            values = [
             value]
        for v in values:
            try:
                src.append(v)
            except:
                if not hasattr(src, b'append'):
                    self.throw(b'bad-value.not-supported', b'src does not support append operation', diagnosis=b'Not all objects may be appended to, try using a list or list-like object.')
                else:
                    self.throw(b'append.fail', b'unable to append', diagnosis=b'Check the value you are appending is the type expected.')


class Remove(ContextElementBase):
    """Remove a value from a collection"""

    class Help:
        synopsis = b'remove a value from a collection'
        example = b'\n        <list dst="crew">\n            <str>John</str>\n            <str>Scorpius/str>\n        </list>\n        <remove src="crew" value="\'Scorpius\'"/>\n        '

    class Meta:
        one_of = [
         ('value', 'values')]

    value = Attribute(b'Value to remove', type=b'expression', missing=False, required=False)
    values = Attribute(b'A sequence of values to remove', type=b'expression', missing=False, required=False)
    src = Attribute(b'Collection to remove from', type=b'expression', required=True, missing=False)

    def logic(self, context):
        value, values, src = self.get_parameters(context, b'value', b'values', b'src')
        if value is not None:
            values = [
             value]
        for v in values:
            try:
                src.remove(v)
            except ValueError:
                continue
            except:
                if not hasattr(src, b'remove'):
                    self.throw(b'bad-value.not-supported', b'src does not support remove operation')
                else:
                    self.throw(b'remove.fail', b'unable to remove')

        return


class Extend(ContextElementBase):
    """Extend a sequence with values from another sequence."""

    class Help:
        synopsis = b'add values from one sequence to another'
        example = b'\n        <list dst="crew">\n            <str>John</str>\n        </list>\n        <extend dst="crew" src="[\'Scorpius\', \'Aeryn\']"/>\n        '

    src = Attribute(b'Collection to append to', type=b'expression')
    values = Attribute(b'value(s) to extend with', type=b'reference')

    def logic(self, context):
        src, values = self.get_parameters(context, b'src', b'values')
        try:
            src.extend(values)
        except:
            if not hasattr(src, b'extend'):
                self.throw(b'bad-value.not-supported', b'src does not support extend')
            else:
                self.throw(b'extend.fail', b'unable to extend')


class Update(ContextElementBase):
    """Update a dictionary (or other mapping collection) with keys and values from another dictionary."""

    class Help:
        synopsis = b'add new values to a dictionary'
        example = b'\n        <dict dst="species"/>\n        <update dst="species" src="john=\'human\', scorpius=\'unknown\'"/>\n        '

    src = Attribute(b'Collection to update', type=b'expression')
    values = Attribute(b'Values to update with', type=b'expression')

    def logic(self, context):
        src, values = self.get_parameters(context, b'src', b'values')
        try:
            src.update(values)
        except:
            if not hasattr(src, b'update'):
                self.throw(b'bad-value.not-supported', b'src does not support update')
            else:
                self.throw(b'update.fail', b'failed to update')


class Pop(DataSetter):
    """Remove and return a value from a dictionary."""

    class Help:
        synopsis = b'remove a value from a dictionary'
        example = b'\n        <dict dst="species">\n            <let john="human"/>\n            <let scorpius="unknown"/>\n        </dict>\n        <pop src="species" key="scorpius" dst="scorpius_species"/>\n        <echo>${scorpius_species}</echo> <!-- "unknown" -->\n        '

    src = Attribute(b'Source', type=b'expression')
    dst = Attribute(b'Destination', type=b'reference', required=False, default=None)
    key = Attribute(b'Key', type=b'expression', required=False)

    def logic(self, context):
        src, dst, key = self.get_parameters(context, b'src', b'dst', b'key')
        try:
            if self.has_parameter(b'key'):
                value = src.pop(key)
            else:
                value = src.pop()
        except IndexError:
            self.throw(b'pop.empty', b"can't pop from an empty list")
        except:
            self.throw(b'pop.fail', b'unable to pop from src')

        if dst is not None:
            self.set_context(context, dst, value)
        return


class Echo(ContextElementBase):
    """Write text to the console. This is typically used in commands or for debugging. Bear in mind that in a production environment there is no console."""

    class Help:
        synopsis = b'write text to the console'
        example = b'<echo>Hello, World</echo>'

    obj = Attribute(b'If given, then the value of this expression will be written to the console', type=b'expression', required=False, default=None)
    table = Attribute(b'A table to display. If given this value should be a list of lists.', type=b'expression', required=False, default=None)
    header = Attribute(b'A list of headers for the table (if given)', type=b'commalist', required=False, default=None)
    indent = Attribute(b'Number of indents', type=b'expression', required=False, default=0)
    style = Attribute(b'Console style', required=False, default=b'bold cyan')

    def logic(self, context):
        obj = self.obj(context)
        tabs = self.indent(context)
        table = self.table(context)
        header = self.header(context)
        style = console_style(self.style(context))
        console = context.root.get(b'console', None)
        if console is None:
            from .. import pilot
            console = pilot.console
        if self.archive.debug_echo:
            line_msg = (b'[file "{}", line {}]\n').format(self._location, self.source_line)
            console(line_msg, fg=b'yellow')
        if self.has_parameter(b'table'):
            console.table(table, header_row=header)
        elif obj is not None:
            console.obj(context, obj, **style)
        else:
            console.text(context.sub(b'    ' * tabs + self.text), **style)
        return


class Exit(ContextElementBase):
    """Exit the current command. When Moya sees this tag it stops running the current command and returns an exit code. It will also write any enclosed text to the console."""

    class Help:
        synopsis = b'exit the current command'
        example = b'<exit code="-5" if="not continue">User cancelled</exit>'

    code = Attribute(b'Return code', type=b'expression', default=0, map_to=b'exit_code')

    def logic(self, context):
        exit_code = self.exit_code(context)
        if self.text.strip():
            context.root[b'console'].text(context.sub(self.text.strip()), fg=b'cyan', bold=True)
        raise EndLogic(exit_code)


class Debug(ContextElementBase):
    """Executes a block only if Moya is in debug mode. You can enable debug mode the setting 'debug' under the project section. This tag is equivalent to the following:

[code xml]
<if test=".debug">
    <echo>Moya is in debug mode. Relax.</echo>
</if>
[/code]

[alert]Be careful to not do anything inside this tag that your project may depend on. It will not execute in a production environment![/alert]

    """

    class Help:
        synopsis = b'execute debug code'
        example = b'\n        <debug>\n            <echo>Moya is in debug mode. Relax.</echo>\n        </debug>\n        '

    def logic(self, context):
        if context.get(b'.debug', False):
            yield DeferNodeContents(self)


class For(ContextElementBase):
    """Execute a block of code for each value in a sequence. This tag [i]iterates[/i] over a sequence, and executes the enclosed block for each value."""

    class Help:
        synopsis = b'iterate over a sequence'
        example = b'\n        <for src="[\'John\', \'Scorpius\', \'Rygel\']" dst="crew_member" filter="crew_member != \'Rygel\'">\n            <echo>${crew_member} is on board!</echo>\n        </for>\n\n        '

    class Meta:
        is_loop = True

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    dst = Attribute(b'Destination value', required=True, type=b'commalist')
    filter = Attribute(b'If given, then only those values which match this condition will cause the enclosed block to execute.', required=False, type=b'expression', default=True)

    def logic(self, context, _defer=DeferNodeContents):
        objects, dst = self.get_parameters(context, b'src', b'dst')
        filter = self.filter
        try:
            iter_objects = iter(objects)
        except TypeError:
            self.throw(b'bad-value.not-iterable', b'source is not iterable')

        if len(dst) == 1:
            dst = dst[0]
            for obj in iter_objects:
                context[dst] = obj
                if filter(context):
                    yield _defer(self)

        else:
            for obj in iter_objects:
                try:
                    for set_dst, set_value in zip(dst, obj):
                        context[set_dst] = set_value

                except TypeError:
                    self.throw(b'bad-value.not-iterable', b'Object in sequence does not support iteration')

                if filter(context):
                    yield _defer(self)


class Switch(ContextElementBase):
    """
    Jump to a location with in a code block, based in an input value.

    This tag takes a value ([c]on[/c]) and jumps to a [tag]case[/tag] in the enclosed block that has a matching value.
    If there is no matching [tag]case[/tag], then execution will move to the enclosed [tag]default-case[/tag]. If no default case exists, the entire block is skipped.

    This tag is useful in situations where a chain of [tag]if[/tag] and [tag]elif[/tag] tags would otherwise be used. Here's an example:

    [code xml]
    <switch on="species">
        <case>human</case>
        <echo>Humans come from Earth</echo>

        <case>hynerian</case>
        <echo>Hynerians come from Hyneria</echo>

        <default-case/>
        <echo>I have no idea where ${species}s come from</echo>
    </switch>
    [/code]

    The above code is equivalent to the following:

    [code xml]
    <if test="species=='human'">
        <echo>Humans come from Earth</echo>
    </if>
    <elif test="species=='hynerian'">
        <echo>Hynerians come from Hyneria</echo>
    </elif>
    <else>
        <echo>I have no idea where ${species}s come from</echo>
    </else>
    [/code]

    The [tag]switch[/tag] version is generally clearer, especially with a large number of conditions.

    If the [c]on[/c] attribute is [i]not[/i] given, then the case's [c]if[/c] attribute is checked. Here's the previous example, implemented without the [c]on[/c] attribute:

    [code xml]
    <switch>
        <case if="species=='human'"/>
        <echo>Humans come from Earth</echo>

        <case if="species=='hynerian'"/>
        <echo>Hynerians come from Hyneria</echo>

        <default-case/>
        <echo>I have no idea where ${species}s come from</echo>
    </switch>
    [/code]

    """

    class Help:
        synopsis = b'jump to matching case'

    class Meta:
        is_loop = True

    on = Attribute(b'Value to test', type=b'expression', required=False)

    def logic(self, context):
        case_tags = [
         (
          namespaces.default, b'case'), (namespaces.default, b'default-case')]
        if self.has_parameter(b'on'):
            switch_on = self.on(context)
            iter_children = iter(self)
            while 1:
                child = next(iter_children, None)
                if child is None:
                    return
                if child._element_type in case_tags and child.test(context, switch_on):
                    for child in iter_children:
                        yield child

                    break

        else:
            iter_children = iter(self)
            while 1:
                child = next(iter_children, None)
                if child is None:
                    return
                if child._element_type in case_tags and child._if(context):
                    for child in iter_children:
                        yield child

                    break

        return


class Case(ContextElementBase):
    """
    Defines a case in a [tag]switch[/tag] tag.

    If a [c]value[/c] attribute is given, it will be used as the comparison values, otherwise the tag text will be used.

    """

    class Help:
        synopsis = b'define a case in a switch'

    value = Attribute(b'Value to compare in a switch', type=b'expression', required=False)

    def check(self, context):
        return True

    def test(self, context, switch_value):
        if self.has_parameter(b'value'):
            value = self.value(context)
        else:
            value = context.sub(self.text.strip())
        return value == switch_value

    def logic(self, context):
        raise BreakLoop()


class DefaultCase(ContextElementBase):
    """
    Defines the [i]default[/i] case in a [tag]switch[/tag] tag.

    """

    class Help:
        synopsis = b'default case in a switch'

    def check(self, context):
        return True

    def test(self, context, switch_value):
        return True

    def logic(self, cotnext):
        raise BreakLoop()


class ProgressElement(ContextElementBase):
    """Like a for loop but renders an ascii progress bar in the console, which will look something like the following:

    [code]
    [###        ] 30% working...
    [/code]

    This is useful for commands that may take some time to execute.

    """

    class Help:
        synopsis = b'render an ascii progress bar'

    src = Attribute(b'Source', required=True, type=b'expression')
    dst = Attribute(b'Destination', required=True, type=b'commalist')
    filter = Attribute(b'If given, then only those values which match this condition will cause the enclosed block to execute.', required=False, type=b'expression', default=True)
    msg = Attribute(b'Message on progress bar', required=False, default=b'working...')
    steps = Attribute(b'Number of steps in the sequence', required=False, type=b'integer')

    class Meta:
        tag_name = b'progress'
        is_loop = True

    def logic(self, context):
        objects, dst, msg, steps = self.get_parameters(context, b'src', b'dst', b'msg', b'steps')
        console = context.root[b'console']
        if steps is None:
            try:
                steps = len(objects)
            except:
                self.throw(b'moya.progress.no-length', (b'Unable to get length of {!r}').format(objects))

        filter = self.filter
        progress = Progress(console, msg, width=20, num_steps=steps)
        context[b'.progress'] = progress
        progress.render()
        try:
            iter_objects = iter(objects)
        except TypeError:
            self.throw(b'bad-value.not-iterable', b'Source is not iterable')
        else:
            msg = self.msg(context)
            try:
                console.show_cursor(False)
                if len(dst) == 1:
                    dst = dst[0]
                    for obj in iter_objects:
                        context[dst] = obj
                        progress.step()
                        if filter(context):
                            yield DeferNodeContents(self)

                else:
                    for obj in iter_objects:
                        try:
                            for set_dst, set_value in zip(dst, obj):
                                context[set_dst] = set_value

                        except TypeError:
                            self.throw(b'bad-value.not-iterable', b'Object in sequence does not support iteration')

                        if filter(context):
                            yield DeferNodeContents(self)
                        progress.step()

            finally:
                console.show_cursor(True)
                progress.done()

        return


class ProgressMsg(ContextElementBase):
    """
    Set a progress message.

    Must appear inside a [tag]progress[/tag] tag.

    """

    class Help:
        synopsis = b'set a progress message'
        example = b'\n        <progress-msg>reading post ${post}</progress-msg>\n        '

    def logic(self, context):
        msg = context.sub(self.text)
        context[b'.progress.msg'] = msg


class Sleep(ContextElementBase):
    """Do nothing for a period of time"""

    class Help:
        synopsis = b'wait for while'
        example = b'<sleep for="10s"/> <!-- do nothing for 10 seconds -->'

    _for = Attribute(b'Amount of time to sleep for', required=True, type=b'timespan')

    def logic(self, context):
        t = self.get_parameter(context, b'for')
        sleep(float(t))


class Map(DataSetter):
    """Create a list by mapping an expression on to a sequence"""

    class Help:
        synopsis = b'map an expression on to sequence'
        example = b'\n        <list dst="crew">\n            <dict let:name="\'john\'" let:species="\'human\'" />\n            <dict let:name="\'rygel\'" let:species="\'hynerian\'" />\n            <dict let:name="\'aeryn\'" let:species="\'peacekeeper\'" />\n        </list>\n        <map src="crew" dst="manifest"\n            value="sub:\'${title:name} is ${species}\'" />\n        <!-- [\'John is human\', \'Rygen is hynerian\', \'Aeryn is peacekeeper\'] -->\n        '

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    dst = Attribute(b'Destination', required=False, type=b'reference')
    value = Attribute(b'Expression', required=True, type=b'function')
    _filter = Attribute(b'Skip item if this expression is false', required=False, type=b'function')

    def get_value(self, context):
        objects, dst, func, _filter = self.get_parameters(context, b'src', b'dst', b'value', b'filter')
        func = func.get_scope_callable(context)
        if _filter is None:
            result = [ func(obj) for obj in objects ]
        else:
            _filter = _filter.get_scope_callable(context)
            result = [ func(obj) for obj in objects if _filter(obj) ]
        return result


class Group(DataSetter):
    """
    Group a sequence in to a list of values with common keys.

    """

    class Help:
        synopsis = b'group a sequence by common keys'
        example = b'\n        <list dst="crew">\n            <dict let:name="\'Rygel\'" let:species="\'hynerian\'" />\n            <dict let:name="\'Aeryn\'" let:species="\'peacekeeper\'" />\n            <dict let:name="\'Jothee\'" let:species="\'luxan\'" />\n            <dict let:name="\'D\'Argo\'" let:species="\'luxan\'" />\n        </list>\n        <group src="crew" key="species" value="name" dst="by_species" />\n        <!-- {\'hynerian\': [\'Rygel\'], \'peacekeeper\': [\'Aeryn\'], \'luxan\': [\'Jothee\', \'D\'Argo\']} -->\n\n        '

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    dst = Attribute(b'Destination', required=False, type=b'reference')
    key = Attribute(b'Key', required=True, type=b'function')
    value = Attribute(b'Expression', required=False, type=b'function', default=b'$$', evaldefault=True)

    def get_value(self, context):
        result = OrderedDict()
        objects, dst, _key, _value = self.get_parameters(context, b'src', b'dst', b'key', b'value')
        key_func = _key.get_scope_callable(context)
        value_func = _value.get_scope_callable(context)
        for obj in objects:
            key = key_func(obj)
            value = value_func(obj)
            result.setdefault(key, []).append(value)

        return result


class MapDict(DataSetter):
    """Create a list of dictionaries from a sequence."""

    class Help:
        synopsis = b'generate a list of dictionaries'
        example = b'\n        <list dst="crew">\n            <dict let:name="\'john\'" let:species="\'human\'" />\n            <dict let:name="\'rygel\'" let:species="\'hynerian\'" />\n            <dict let:name="\'aeryn\'" let:species="\'peacekeeper\'" />\n        </list>\n        <map-dict src="crew" dst="crew" let:name="title:name" let:human="species == \'human\'"/>\n        <!-- [{\'name\':John, \'human\':yes}, {\'name\':Rygel, \'human\':no}, {\'name\':\'Aeryn\',  \'human\':no}] -->\n        '

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    dst = Attribute(b'Destination', required=False, type=b'reference')
    _filter = Attribute(b'Skip item if this expression is false', required=False, type=b'function')

    def logic(self, context):
        objects, dst, _filter = self.get_parameters(context, b'src', b'dst', b'filter')
        if _filter is None:
            predicate = lambda obj: True
        else:
            predicate = _filter.get_scope_callable(context)
        map_result = []
        for obj in objects:
            with context.data_scope(obj):
                if not predicate(obj):
                    continue
                value = self.get_let_map(context)
                with context.data_scope(value):
                    yield DeferNodeContents(self)
                map_result.append(value)

        self.set_context(context, dst, map_result)
        return


class Max(DataSetter):
    """Get the maximum value in a sequence."""

    class Help:
        synopsis = b'get the maximum value in a sequence'

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    key = Attribute(b'Key', type=b'function', required=False, default=None, missing=False)

    def logic(self, context):
        objects, dst, key = self.get_parameters(context, b'src', b'dst', b'key')
        if not objects:
            self.throw(b'max.empty', b'src is empty', diagnosis=b"Moya can't calculate the maximum of an empty sequence.")
        if key is None:
            result = max(objects)
        else:
            key_callable = key.get_scope_callable(context)
            result = max(key_callable(obj) for obj in objects)
        self.set_context(context, dst, result)
        return


class Min(DataSetter):
    """Get the minimum value in a sequence."""

    class Help:
        synopsis = b'get the minimum value in a sequence'

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    key = Attribute(b'Key', type=b'function', required=False, default=None, missing=False)

    def logic(self, context):
        objects, dst, key = self.get_parameters(context, b'src', b'dst', b'key')
        if not objects:
            self.throw(b'min.empty', b'src is empty', diagnosis=b"Moya can't calculate the minimum of an empty sequence.")
        if key is None:
            result = min(objects)
        else:
            key_callable = key.get_scope_callable(context)
            result = min(key_callable(obj) for obj in objects)
        self.set_context(context, dst, result)
        return


class FilterSeq(DataSetter):
    """Filter members of a collection which don't pass a condition."""

    class Help:
        synopsis = b'filter values from a sequence'
        example = b'\n        <dict dst="crew">\n            <dict let:name="john" let:species="human" />\n            <dict let:name="rygel" let:species="hynerian" />\n            <dict let:name="aeryn" let:species="peacekeeper" />\n        </dict>\n        <filter-seq src="items:crew dst="crew" test="species !- \'hyneria\'"/>\n        <!-- [{\'name\': \'john\', \'species\':\'human\'}, {\'name\':\'aeryn\', \'species\':\'peacemaker\'}] -->\n\n        '

    src = Attribute(b'Source', required=True, type=b'expression')
    dst = Attribute(b'Destination', required=False, type=b'reference', default=None)
    test = Attribute(b'Condition', required=True, type=b'function')

    def get_value(self, context):
        objects, dst, func = self.get_parameters(context, b'src', b'dst', b'test')
        predicate = func.get_scope_callable(context)
        return [ item for item in objects if predicate(item) ]


class Sort(DataSetter):
    """Sort a sequence"""

    class Help:
        synopsis = b'sort a sequence'
        example = b'\n        <dict dst="crew">\n            <dict let:name="John" let:species="human" />\n            <dict let:name="Rygel" let:species="hynerian" />\n            <dict let:name="Aeryn" let:species="peacekeeper" />\n        </dict>\n        <sort src="crew" dst="crew" key="lower:name" />\n        '

    src = Attribute(b'Source sequence', required=True, type=b'expression')
    dst = Attribute(b'Destination', required=False, type=b'reference', default=None)
    key = Attribute(b'Key expression', required=True, type=b'function')
    reverse = Attribute(b'Reverse order?', type=b'boolean', required=False, default=False)

    def get_value(self, context):
        objects, dst, func, reverse = self.get_parameters(context, b'src', b'dst', b'key', b'reverse')
        get_key = func.get_scope_callable(context)
        return sorted(objects, reverse=reverse, key=get_key)


class Repeat(ContextElementBase):
    """Repeat a block a set number of times, or indefinitely. You can leave a repeat loop prematurely with the [tag]break[/tag] tag.

    [alert Note]Be careful not to create infinite loops with this tag[/alert]

    """

    class Help:
        synopsis = b'repeat a block'
        example = b'\n        <repeat times="5">\n            <echo>Candyman</echo>\n        </repeat>\n        '

    times = Attribute(b'Number of times to repeat (default is infinite)', type=b'expression', default=None)

    class Meta:
        is_loop = True

    def logic(self, context):
        times = self.times(context)
        if times is not None:
            try:
                times = int(times)
            except:
                self.throw(b'bad-value.not-a-number', b"'times' must be a number if given")

        if times is None:
            while 1:
                yield DeferNodeContents(self)

        else:
            count = max(0, times)
            while count:
                yield DeferNodeContents(self)
                count -= 1

        return


class While(ContextElementBase):
    """Repeat a block of code while a condition is true, or a [tag]break[/tag] tag is reached.

    [alert Note]Be careful not to create an [i]infinite[/i] loop with this tag.[/alert]

    """

    class Help:
        synopsis = b'repeat a block while a condition is true'
        example = b'\n\n        <let i="5"/>\n        <while test="i gt 0">\n            <echo>${i}</echo>\n            <let i="i-1"/>\n        </while>\n\n\n        '

    class Meta:
        is_loop = True

    test = Attribute(b'Condition', required=True, type=b'expression')

    def logic(self, context, _defer=DeferNodeContents):
        test = self.test
        while test(context):
            yield _defer(self)


class Do(ContextElementBase):
    """Repeat a block of code until a condition becomes true, or a [tag]break[/tag] is reached.

    Note that, unlike [tag]while[/tag] this tag will execute the enclosed block at least once.

    If the [c]until[/c] attribute isn't given, the enclosed block will be executed just once.

    """

    class Help:
        synopsis = b'repeat a block until a condition becomes true'
        example = b'\n\n        <let i="1"/>\n        <do until="i==2">\n            <echo>${i}</echo>\n            <let i="i+1"/>\n        </do>\n        <!-- prints "1" -->\n\n        '

    class Meta:
        is_loop = True

    until = Attribute(b'Condition', required=False, type=b'expression')

    def logic(self, context):
        if not self.has_parameter(b'until'):
            yield DeferNodeContents(self)
        else:
            test = self.test
            while 1:
                yield DeferNodeContents(self)
                if test(context):
                    break


class Break(ContextElementBase):
    """This tag will [i]break[/i] a loop such as [tag]while[/tag], [tag]for[/tag]. When Moya encounters this tag, it jumps to the statement after the loop."""

    class Help:
        synopsis = b'end a loop prematurely'
        example = b'\n\n        <let crew="[\'John\', \'Rygel\', \'Scorpius\', \'Aeryn\']"/>\n        <for src="crew" dst="character">\n            <if test="character == \'Scorpius\'">\n                <echo>Taking off before Scorpius gets on board!</eco>\n                <break>\n            </if>\n            <echo>${character} is on board</echo>\n        </for>\n\n        '

    def logic(self, context):
        raise BreakLoop()


class Continue(ContextElementBase):
    """When Moya encounters this tag in a loop, such as [tag]while[/tag] or [tag]for[/tag], it ignores the remaining code in the block and [i]continues[/i] to the next item in the loop."""

    class Help:
        synopsis = b'skip remaining code in a loop'
        example = b'\n\n        <let crew="[\'John\', \'Rygel\', \'Scorpius\', \'Aeryn\']"/>\n        <for src="crew" dst="character">\n            <if test="character == \'Scorpius\'">\n                <echo>Scorpius is not allowed on board!</eco>\n                <continue/>\n            </if>\n            <echo>${character} is on board</echo>\n        </for>\n\n\n        '

    def logic(self, context):
        raise ContinueLoop()


class Macro(ContextElementBase):
    """Defines a [link moyacode#macros]macro[/link]."""

    class Help:
        synopsis = b'define a re-usable block of code'
        example = b'\n        <macro docname="greet">\n            <echo>Hello, ${name}!<echo>\n        </macro>\n        '

    def lib_finalize(self, context):
        for signature in self.children(b'signature'):
            self.validator = signature.validator
            self.validate_call = self.validator.validate


class Preflight(Macro):
    """A pre-flight check is used to detect potential problems, such as missing settings."""

    class Help:
        synopsis = b'check initial settings'


class ReturnDict(ContextElementBase):
    """
    Shortcut to return a dictionary. For example, the following macro returns a dictionary:

    [code xml]
    <macro docname="get_character">
        <return>
            <dict>
                <str dst="rygel">Hynerian</str>
                <str dst="john">Human</str>
            </dict>
        </return>
    </macro>
    [/code]

    We could shorten the above using the [tag]return-dict[/tag] as follows:

    [code xml]
    <macro docname="get_character">
        <return-dict>
            <str dst="rygel">Hynerian</str>
            <str dst="john">Human</str>
        </return-dict>
    </macro>
    [/code]

    """

    class Help:
        synopsis = b'shortcut to return a dictionary'

    def logic(self, context):
        data = self.get_let_map(context).copy()
        context[b'_return'] = data
        with context.scope(b'_return'):
            yield DeferNodeContents(self)
        raise Unwind()


class ReturnScope(ContextElementBase):
    """
    Return values from the current scope.

    This tag is useful in macros, widgets, and other callable tags where you want to return a number of values in a dictionary.

    For example, the following will return a dictionary containing two keys:

    [code xml]
    <return-scope values="foo, bar"/>
    [/code]

    This is equivalent to the following:

    [code xml]
    <return value="{'foo': foo, 'bar': bar}"/>
    [/code]

    If you *don't* specify the [c]values[/c] attribute, Moya will read the values from the enclosed text (one key per line).
    The following code is equivalent to the above:

    [code xml]
    <return-scope>
        foo
        bar
    </return-scope>
    [/code]

    """
    values = Attribute(b'Values to return', type=b'commalist', required=False, default=None)
    default = Attribute(b'Default for missing values', type=b'expression', required=False, default=None)

    class Help:
        synopsis = b'return values from the current scope'

    def logic(self, context):
        names, default = self.get_parameters(context, b'values', b'default')
        if names is None:
            names = [ l.strip() for l in context.sub(self.text).splitlines() if not l.isspace() ]
        get = context.get
        context[b'_return'] = {name:get(name, default) for name in names}
        raise Unwind()
        return


class ReturnStr(ContextElementBase):
    """A shortcut to returning a string."""

    class Help:
        synopsis = b'shortcut to return a string'
        example = b'\n        <macro docname="get_text">\n            <return-str>Hello, World</return-str>\n        </macro>\n        '

    def logic(self, context):
        context[b'_return'] = context.sub(self.text)
        raise Unwind()


class ReturnFalse(ContextElementBase):
    """
    A shortcut to return False.

    The following two lines are equivalent:

    [code xml]
    <return-false/>
    <return value="no" />
    [/code]

    """

    class Help:
        synopsis = b'shortcut to return false'

    def logic(self, context):
        context[b'_return'] = False
        raise Unwind


class ReturnTrue(ContextElementBase):
    """
    A shortcut to return True.

    The following two lines are equivalent:

    [code xml]
    <return-true/>
    <return value="yes" />
    [/code]

    """

    class Help:
        synopsis = b'shortcut to return true'

    def logic(self, context):
        context[b'_return'] = True
        raise Unwind


class Return(ContextElementBase):
    """
    Used in a callable block such as a [tag]macro[/tag] or [tag]view[/tag] to return data.

    If you enclose any [i]data setter[/i] tag ([tag]int[/tag], [tag]str[/tag], [tag]list[/tag] etc.) in the return block, the result will be returned. For example, the following macro will return a list of three items:

    [code xml]
    <macro libname="get_crew">
        <return>
            <list>
                <str>John</str>
                <str>Scorpius</str>
                <str>Rygel</str>
            </list>
        </return>
    </macro>
    [/code]

    Alternatively, you may use the [c]value[/c] attribute to return the result of an expression. The following code is equivalent to the above:

    [code xml]
    <macro libname="get_crew">
        <return value="['John', 'Scorpius', 'Rygel']" />
    </macro>
    [/code]

    """

    class Help:
        synopsis = b'return data from a macro or other callable'

    value = Attribute(b'Value to return', type=b'expression', default=None)

    def logic(self, context):
        if self.has_parameter(b'value'):
            context[b'_return'] = ReturnContainer(value=self.value(context))
        else:
            context[b'_return'] = ReturnContainer()
            with context.scope(b'_return'):
                yield DeferNodeContents(self)
        raise Unwind()


class CacheReturn(ContextElementBase):
    """
    Return a value from a cache, if it exists. Otherwise, execute the enclosed block.

    This tag can be used to [i]memoize[/i] a [tag]macro[/tag] or other callable. Essentially, this means that if you call the macro a second time with the same parameters, it returns the previously calculated result. For macros that are slow to execute, this can result in significant speedups.

    For example, the following code calculates the [url http://en.wikipedia.org/wiki/Factorial]factorial[/url] of a number:

    [code xml]
    <moya xmlns="http://moyaproject.com"
        xmlns:let="http://moyaproject.com/let">

        <macro docname="fact">
            <signature>
                <argument name="n"/>
            </signature>
            <cache-return key="n">
                <echo>calculating ${n}!</echo>
                <let f="1"/>
                <while test="n">
                    <let f="f*n" n="n-1"/>
                </while>
                <return value="f"/>
            </cache-return>
        </macro>

        <macro docname="main">
            <call macro="fact" let:n="7" dst="result"/>
            <echo>${result}</echo>
            <call macro="fact" let:n="7" dst="result"/>
            <echo>${result}</echo>
            <call macro="fact" let:n="7" dst="result"/>
            <echo>${result}</echo>
        </macro>

    </moya>
    [/code]

    If you run the above code, you will get the following output:

    [code]
    $ moya run cachereturn.xml
    calculating 7!
    5040
    5040
    5040
    [/code]

    The first time the [c]fact[/c] macro is called, Moya displays "calculating 7!" in the terminal. The second and third time, the text is [i]not[/i] displayed because the result is retrieved from the cache -- without the need to execute the code within [tag]cache-return[/tag].

    """

    class Help:
        synopsis = b'cache returned values'

    cache = Attribute(b'Cache name', required=False, default=b'runtime')
    _for = Attribute(b'Time to cache for', required=False, default=0, type=b'timespan')
    key = Attribute(b'Cache key', required=False)
    keydata = Attribute(b'Cache data', type=b'expression', required=False)
    local = Attribute(b'Should the value be cached for this tag only?', type=b'boolean', default=True)

    class Meta:
        is_call = True
        one_of = [('key', 'keydata')]

    def logic(self, context):
        cache_name, cache_time, cache_key, cache_key_data, cache_local = self.get_parameters(context, b'cache', b'for', b'key', b'keydata', b'local')
        if cache_key is None:
            cache_key = make_cache_key(cache_key_data)
        if cache_local:
            cache_key = (b'{}--{}').format(self.libid, cache_key)
        cache = self.archive.get_cache(cache_name)
        cache_result = cache.get(cache_key, Ellipsis)
        if cache_result is Ellipsis:
            call = context.get(b'.call', {})
            yield DeferNodeContents(self)
            if b'_return' in call:
                value = _return = call[b'_return']
                if hasattr(_return, b'get_return_value'):
                    value = _return.get_return_value()
            else:
                value = None
            cache.set(cache_key, value, time=int(cache_time))
            context[b'_return'] = ReturnContainer(value=value)
            raise Unwind()
        else:
            context[b'_return'] = ReturnContainer(value=cache_result)
            raise Unwind()
        return


class Done(ContextElementBase):
    """Exists the current callable immediately with no return value. Note, this is not equivalent to [tag]return[/tag] which returns [c]None[/c]."""

    class Help:
        synopsis = b'return from a macro or callable without any data'

    def logic(self, context):
        raise Unwind()


class Input(DataSetter):
    """
    Get data from the console.

    [alert WARNING]This tag should only be used in an interactive context, such as a [tag]command[/tag] tag.[/alert]

    """

    class Help:
        synopsis = b'ask the user for information in a command'
        example = b'\n        <input dst="name">What is your name?</input>\n\n        '

    default = b''
    _default = Attribute(b'Value to use if response is empty', default=b'', map_to=b'default')
    password = Attribute(b'Use password input?', default=False, type=b'boolean')

    def logic(self, context):
        default = self.default(context)
        text = context.sub(self.text) or b''
        if default:
            text += (b' ({})').format(default)
        if text:
            text += b' '
        console = context.root[b'console']
        if self.password(context):
            response = getpass.getpass(text)
        else:
            try:
                if PY3:
                    response = input(text)
                else:
                    response = raw_input(text).decode(sys.stdin.encoding or locale.getpreferredencoding(True))
            except EOFError:
                self.throw(b'input.eof', b'User hit Ctrl+D')

        if not response:
            response = default
        self.set_context(context, self.dst(context), response)


class Ask(DataSetter):
    """
    Ask the user a yes / no question.

    [alert WARNING]This tag should only be used in an interactive context, such as a [tag]command[/tag] tag.[/alert]

    """

    class Help:
        synopsis = b'ask a yes / no question'
        example = b'\n        <ask dst="take_off">Would you like to take off?</ask>\n        <echo if="take_off">Taking off!</echo>\n        '

    default = False

    def logic(self, context):
        try:
            response = raw_input(b'%s (Y/N) ' % (self.text.strip() or b''))
        except EOFError:
            self.throw(b'ask.eof', b'User hit Ctrl+D')

        response_bool = response.strip().lower() in ('yes', 'y')
        self.set_context(context, self.dst(context), response_bool)


class _LazyCallable(object):

    def __init__(self, context, _callable, args, kwargs):
        self.context = weakref.ref(context)
        self.callable = _callable
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        context = self.context()
        try:
            with context.frame():
                if getattr(self.callable, b'_require_context', False):
                    result = self.callable(context, *self.args, **self.kwargs)
                else:
                    result = self.callable(*self.args, **self.kwargs)
        except Exception as e:
            log.exception(b'lazy error %s', e)
            raise
        else:
            if hasattr(result, b'get_return_value'):
                result = result.get_return_value()
            return result


class Call(ContextElementBase):
    """Call a [link moyacode#macros]macro[/link]."""

    class Help:
        synopsis = b'invoke a macro'
        example = b'<call macro="moya.auth#login" />'

    class Meta:
        is_call = True

    macro = Attribute(b'Macro', required=True)
    dst = Attribute(b'Destination for return value', type=b'reference')
    lazy = Attribute(b'If True the result will be evaluated lazily (i.e. when next referenced)', type=b'boolean')
    _from = Attribute(b'Application', default=None, type=b'application')

    def logic(self, context):
        macro, dst, lazy, app = self.get_parameters(context, b'macro', b'dst', b'lazy', b'from')
        items_map = self.get_let_map(context)
        app = app or self.get_app(context, check=False)
        if self.has_children:
            call = self.push_funccall(context)
            call.update(items_map)
            try:
                yield DeferNodeContents(self)
            finally:
                self.pop_funccall(context)

            args, kwargs = call.get_call_params()
        else:
            call = {}
            args = []
            kwargs = items_map
        lazy_callable = None
        if lazy:
            if not dst:
                self.throw(b'call.missing-dst', b"A value for 'dst' is required for lazy calls")
            macro_app, macro_element = self.get_element(macro, app)
            if hasattr(macro_element, b'validate_call'):
                macro_element.validate_call(context, macro_element, kwargs)
            element_callable = self.archive.get_callable_from_element(macro_element, app=macro_app or app)
            lazy_callable = _LazyCallable(context, element_callable, args, kwargs)
            context.set_lazy(dst, lazy_callable)
        else:
            macro_app, macro_element = self.get_element(macro, app)
            if macro_element._meta.app_first_arg:
                call = {b'args': [macro_app] + args}
            else:
                call = {}
                if args:
                    call[b'args'] = args
            call.update(kwargs)
            if hasattr(macro_element, b'validate_call'):
                macro_element.validate_call(context, macro_element, call)
            self.push_call(context, call, app=macro_app)
            try:
                if hasattr(macro_element, b'run'):
                    for el in macro_element.run(context):
                        yield el

                else:
                    yield DeferNodeContents(macro_element)
            finally:
                call = self.pop_call(context)

            if b'_return' in call:
                value = _return = call[b'_return']
                if hasattr(_return, b'get_return_value'):
                    value = _return.get_return_value()
            else:
                value = None
            if dst is None:
                getattr(context.obj, b'append', lambda a: None)(value)
            else:
                context[dst] = value
        return


class CallElement(ContextElementBase):
    """
    Call a element object.

    This tag calls an element retrieved with tags such as [tag]get-element[/tag]. For a general purpose call tag, see [tag]call[/tag].

    """

    class Help:
        synopsis = b'invoke a macro element'
        example = b'\n        <get-element name="sushifinder#macro.check_stock" dst="element" />\n        <call-element element="element" dst="result"/>\n\n        '

    class Meta:
        is_call = True

    element = Attribute(b'An element object', type=b'expression', required=True)
    dst = Attribute(b'Destination for return value', type=b'reference')

    def logic(self, context):
        macro, dst = self.get_parameters(context, b'element', b'dst')
        try:
            macro_element = macro.__moyaelement__()
            macro_app = macro.app
        except:
            self.throw(b'call-element.not_element', b'must be called with an element object')

        if self.has_children:
            call = self.push_funccall(context)
            try:
                yield DeferNodeContents(self)
            finally:
                self.pop_funccall(context)

            args, kwargs = call.get_call_params()
            call = {b'args': args}
            call.update(kwargs)
            call.update(self.get_let_map(context))
        else:
            call = self.get_let_map(context)
        if hasattr(macro_element, b'validate_call'):
            macro_element.validate_call(context, macro_element, call)
        self.push_call(context, call, app=macro_app)
        try:
            yield DeferNodeContents(macro_element)
        finally:
            call = self.pop_call(context)

        if b'_return' in call:
            value = _return = call[b'_return']
            if hasattr(_return, b'get_return_value'):
                value = _return.get_return_value()
        else:
            value = None
        if dst is None:
            getattr(context.obj, b'append', lambda a: None)(value)
        else:
            context[dst] = value
        return


class Defer(ContextElementBase):
    """Defer to a given element, such as a [tag]macro[/tag]. [i]Deferring[/i] to a macro is similar to calling it, but no new [i]scope[/i] is created. This means that the macro has access to the same variables where defer was called."""

    class Help:
        synopsis = b'jump to another element'
        example = b'\n        <macro docname="board">\n            <echo>${character} is on board</echo>\n        </macro>\n\n        <macro docname="main">\n            <let crew="[\'John\', \'Rygel\', \'Scorpius\']"/>\n            <for src="crew" dst="character">\n                <defer to="board"/>\n            </for>\n        </macro>\n\n        '

    element = Attribute(b'Element', type=b'expression', required=False, default=None)
    _to = Attribute(b'Element reference', required=False, default=None, map_to=b'element_ref')
    _from = Attribute(b'Application', default=None, type=b'application')

    def logic(self, context):
        element, element_ref, app = self.get_parameters(context, b'element', b'element_ref', b'from')
        app = app or self.get_app(context)
        if element is not None:
            if not hasattr(element, b'__moyaelement__'):
                self.throw(b'bad-value.not-an-element', (b"Can't defer to '{!r}' because it's not an element").format(element))
            element = element.__moyaelement__()
        elif element_ref is not None:
            app, element = self.get_element(element_ref, app)
        else:
            self.throw(b'bad-value.missing-element', b"No value given for 'element' or 'element_ref'")
        if element._element_class != b'logic':
            self.throw(b'defer.not-logic', b'This element can not be deferred to')
        if element.has_children:
            with self.defer(context, app):
                yield DeferNodeContents(element)
        return


class Scope(LogicElement):
    """Creates a new temporary [i]scope[/i] from an object."""

    class Help:
        synopsis = b'create a temporary scope'
        example = b'\n        <dict dst="species">\n            <let john="human"/>\n            <let rygel="hynerian"/>\n        </dict>\n        <scope object="species">\n            John is a ${john}, Rygel is a ${rygel}\n        </scope>\n        '

    object_ = Attribute(b'Object', type=b'expression', name=b'object', required=True)

    def logic(self, context):
        obj = self.object(context)
        with context.data_scope(obj):
            yield DeferNodeContents(self)