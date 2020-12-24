# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ll/toxic.py
# Compiled at: 2008-01-07 06:22:06
'''
<p>This module is an &xist; namespace. It can be used for
generating Oracle database functions that return &xml; strings.
This is done by embedding processing instructions containing
PL/SQL code into &xml; files and transforming those files with &xist;.</p>

<p>An example that generates an &html; table containing the result
of a search for names in a <lit>person</lit> table might look
like this:</p>

<example>
<prog>
from ll.xist import xsc
from ll.xist.ns import html, htmlspecials
from ll import toxic

class search(xsc.Element):
        def convert(self, converter):
                e = xsc.Frag(
                        toxic.args("search varchar2"),
                        toxic.vars("i integer;"),
                        toxic.type("varchar2(32000);"),
                        htmlspecials.plaintable(
                                toxic.code("""
                                        i := 1;
                                        for row in (select name from person where name like search) loop
                                                """),
                                                html.tr(
                                                        html.th(toxic.expr("i"), align="right"),
                                                        html.td(toxic.expr("xmlescape(row.name)"))
                                                ),
                                                toxic.code("""
                                                i := i+1;
                                        end loop;
                                """)
                        )
                )
                return e.convert(converter)

print toxic.xml2ora(search().conv().asString(encoding"us-ascii")).encode("us-ascii")
</prog>
</example>

<p>Running this script will give the following output
(the indentation will be different though):</p>

<prog>
(
        search varchar2
)
return varchar2
as
        c_out varchar2(32000);
        i integer;
begin
        c_out := c_out || '&lt;table cellpadding="0" border="0" cellspacing="0"&gt;';
        i := 1;
        for row in (select name from person where name like search) loop
                c_out := c_out || '&lt;tr&gt;&lt;th align="right"&gt;';
                c_out := c_out || i;
                c_out := c_out || '&lt;/th&gt;&lt;td&gt;';
                c_out := c_out || xmlescape(row.name);
                c_out := c_out || '&lt;/td&gt;&lt;/tr&gt;';
                i := i+1;
        end loop;
        c_out := c_out || '&lt;/table&gt;';
        return c_out;
end;
</prog>

<p>Instead of generating the &xml; from a single &xist; element,
it's of course also possible to use an &xml; file. One that generates
the same function as the one above looks like this:</p>

<example>
<prog>
&lt;?args
        search varchar2
?&gt;
&lt;?vars
        i integer;
?&gt;
&lt;plaintable class="search"&gt;
        &lt;?code
                i := 1;
                for row in (select name from person where name like search) loop
                        ?&gt;
                        &lt;tr&gt;
                                &lt;th align="right"&gt;&lt;?expr i?&gt;&lt;/th&gt;
                                &lt;td&gt;&lt;?expr xmlescape(row.name)?&gt;&lt;/td&gt;
                        &lt;/tr&gt;
                        &lt;?code
                        i := i + 1;
                end loop;
        ?&gt;
&lt;/plaintable&gt;
</prog>
</example>

<p>When we save the file above as <filename>search.sqlxsc</filename> then
parsing the file, transforming it and printing the function body
works like this:</p>

<example>
<prog>
from ll.xist import parsers
from ll.xist.ns import html, htmlspecials
from ll import toxic

node = parsers.parseFile("search.sqlxsc")
node = node.conv()
print toxic.xml2ora(node.asString(encoding="us-ascii")).encode("us-ascii")
</prog>
</example>
'''
import cStringIO
from ll import misc
from ll.xist import xsc, publishers
xmlns = 'http://xmlns.livinglogic.de/toxic'

def stringify(string, nchar=False):
    """
        Format <arg>string</arg> as multiple PL/SQL string constants or expressions.
        <arg>nchar</arg> specifies if a <lit>NVARCHAR</lit> constant should be
        generated or a <lit>VARCHAR</lit>. This is a generator.
        """
    current = []
    for c in string:
        if ord(c) < 32:
            if current:
                if nchar:
                    yield "N'%s'" % ('').join(current)
                else:
                    yield "'%s'" % ('').join(current)
                current = []
            yield 'chr(%d)' % ord(c)
        else:
            if c == "'":
                c = "''"
            current.append(c)
            if len(current) > 1000:
                if nchar:
                    yield "N'%s'" % ('').join(current)
                else:
                    yield "'%s'" % ('').join(current)
                current = []

    if current:
        if nchar:
            yield "N'%s'" % ('').join(current)
        else:
            yield "'%s'" % ('').join(current)


def xml2ora(string):
    """
        The <class>unicode</class> object <arg>string</arg> must be an &xml; string.
        <func>xml2ora</func> extracts the relevant processing instructions
        and creates the body of an Oracle function from it.
        """
    foundproc = False
    foundargs = []
    foundvars = []
    foundplsql = []
    foundtype = 'clob'
    for (t, s) in misc.tokenizepi(string):
        if t is None:
            foundplsql.append((-1, s))
        elif t == 'code':
            foundplsql.append((0, s))
        elif t == 'expr':
            foundplsql.append((1, s))
        elif t == 'args':
            foundargs.append(s)
        elif t == 'vars':
            foundvars.append(s)
        elif t == 'type':
            foundtype = s
        elif t == 'proc':
            foundproc = True
        else:
            raise ValueError('PI target %r unknown' % t)

    result = []
    if foundargs:
        result.append('(\n\t%s\n)\n' % (',\n\t').join(foundargs))
    plaintype = foundtype
    if '(' in plaintype:
        plaintype = plaintype[:plaintype.find('(')]
    isclob = plaintype.lower() in ('clob', 'nclob')
    if not foundproc:
        result.append('return %s\n' % plaintype)
    result.append('as\n')
    if not foundproc:
        result.append('\tc_out %s;\n' % foundtype)
    if foundvars:
        result.append('\t%s\n' % ('').join(foundvars))
    nchar = foundtype.lower().startswith('n')
    if isclob:
        for arg in ('clob', 'varchar2'):
            result.append('\tprocedure write(p_text in %s%s)\n' % (plaintype.rstrip('clob'), arg))
            result.append('\tas\n')
            result.append('\t\tbegin\n')
            if arg == 'clob':
                result.append('\t\t\tif p_text is not null and length(p_text) != 0 then\n')
                result.append('\t\t\t\tdbms_lob.append(c_out, p_text);\n')
            else:
                result.append('\t\t\tif p_text is not null then\n')
                result.append('\t\t\t\tdbms_lob.writeappend(c_out, length(p_text), p_text);\n')
            result.append('\t\tend if;\n')
            result.append('\tend;\n')

    result.append('begin\n')
    if isclob:
        result.append('\tdbms_lob.createtemporary(c_out, true);\n')
    for (mode, string) in foundplsql:
        if mode == -1:
            for s in stringify(string, nchar):
                if isclob:
                    result.append('\twrite(%s);\n' % s)
                else:
                    result.append('\tc_out := c_out || %s;\n' % s)

        elif mode == 0:
            result.append(string)
            result.append('\n')
        elif isclob:
            result.append('\twrite(%s);\n' % string)
        else:
            result.append('\tc_out := c_out || %s;\n' % string)

    if not foundproc:
        result.append('\treturn c_out;\n')
    result.append('end;\n')
    return ('').join(result)


def prettify(string):
    """
        Try to fix the indentation of the PL/SQL snippet passed in.
        """
    lines = [ line.lstrip('\t') for line in string.split('\n') ]
    newlines = []
    indents = {'(': (0, 1), 
       ');': (-1, 0), 
       ')': (-1, 0), 
       'as': (0, 1), 
       'begin': (0, 1), 
       'loop': (0, 1), 
       'end;': (-1, 0), 
       'end': (-1, 0), 
       'exception': (-1, 1), 
       'if': (0, 1), 
       'for': (0, 1), 
       'while': (0, 1), 
       'elsif': (-1, 1), 
       'else': (-1, 1)}
    indent = 0
    firstafteras = False
    for line in lines:
        if not line:
            newlines.append('')
        else:
            prefix = line.split(None, 1)[0]
            (pre, post) = indents.get(prefix, (0, 0))
            if line.endswith('('):
                post = 1
            elif firstafteras and prefix == 'begin':
                pre = -1
            indent = max(0, indent + pre)
            newlines.append('%s%s' % ('\t' * indent, line))
            indent = max(0, indent + post)
            if prefix == 'as':
                firstafteras = True

    return ('\n').join(newlines)


class args(xsc.ProcInst):
    """
        <p>Specifies the arguments to be used by the generated function. For example:</p>
        <example>
        <prog>
        &lt;?args
                key in integer,
                lang in varchar2
        ?&gt;
        </prog>
        </example>
        <p>If <class>args</class> is used multiple times, the contents will simple
        be concatenated.</p>
        """
    pass


class vars(xsc.ProcInst):
    """
        <p>Specifies the local variables to be used by the function.
        For example:</p>
        <example>
        <prog>
        &lt;?vars
                buffer varchar2(200) := 'foo';
                counter integer;
        ?&gt;
        </prog>
        </example>
        <p>If <class>vars</class> is used multiple times, the contents will simple
        be concatenated.</p>
        """
    pass


class code(xsc.ProcInst):
    """
        <p>A PL/SQL code fragment that will be embedded literally in the
        generated function. For example:</p>
        <example>
        <prog>
        &lt;?code select user into v_user from dual;?&gt;
        </prog>
        </example>
        """
    pass


class expr(xsc.ProcInst):
    """
        The data of an <class>expr</class> processing instruction
        must contain a PL/SQL expression whose value will be embedded
        in the string returned by the generated function. This value will
        not be escaped in any way, so you can generate &xml; tags with
        <class>expr</class> PIs but you must make sure to generate
        the value in the encoding that the caller of the generated
        function expects.
        """
    pass


class proc(xsc.ProcInst):
    """
        When this processing instruction is found in the source
        <pyref function="xml2ora"><func>xml2ora</func></pyref>
        will no longer generate a function as a result, but a procedure.
        This procedure must have <lit>c_out</lit> as an <z>out</z> variable
        (of the appropriate type (see <pyref class="type"><class>type</class></pyref>)
        where the output will be written to.
        """
    pass


class type(xsc.ProcInst):
    """
        <p>Can be used to specify the return type of the generated
        function. The default is <lit>clob</lit>.
        """
    pass