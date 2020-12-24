# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/content.py
# Compiled at: 2017-07-23 08:33:39
from __future__ import unicode_literals
from __future__ import print_function
from ..elements.elementbase import Attribute, LogicElement
from ..tags.context import ContextElementBase, DataSetter
from ..render import HTML, is_renderable, Unsafe, render_object, is_safe
from ..context.dataindex import makeindex
from .. import logic
from .. import errors
from ..html import escape
from ..console import Console
from ..content import Content, Section, IncludePathCSS, IncludePathJS
from ..tools import url_join, textual_list
from ..context.missing import is_missing
from ..markup import Markup, get_installed_markups
from ..template import Template as MoyaTemplate
from ..compat import string_types, text_type
from collections import defaultdict

class Renderable(object):
    moya_render_targets = [
     b'html']


class TemplateRenderable(Renderable):
    moya_safe = True

    def __init__(self, template, td):
        self.template = template
        self.td = td
        self.children = []

    def moya_render(self, archive, context, target, options):
        engine = archive.get_template_engine(b'moya')
        template = self.template
        if isinstance(template, string_types):
            html = engine.render(template, self.td, base_context=context)
        else:
            html = engine.render_template(template, self.td, base_context=context)
        return HTML(html)

    def add_renderable(self, renderable):
        self.children.append(renderable)


class ContentElementMixin(object):

    def resolve_template(self, app, template, element=None):
        """Get template path relative to templates filesystem"""
        if element is None:
            element = self
        if template is None:
            return
        else:
            template_engine = self.archive.get_template_engine()
            _template = app.resolve_template(template)
            if not template_engine.exists(_template):
                raise errors.ContentError((b"missing template '{}'").format(template), element=element, diagnosis=b'You can check what templates are installed with **moya fs templates --tree**.')
            return _template

    def resolve_templates(self, app, templates, element=None):
        """Get first template path that exists"""
        if templates is None:
            return
        else:
            if element is None:
                element = self
            template_exists = self.archive.get_template_engine().exists
            for _template in templates:
                template = app.resolve_template(_template)
                if template_exists(template):
                    return template

            if len(templates) == 1:
                raise errors.ContentError((b"missing template '{}'").format(templates[0]), element=element, diagnosis=b'You can check what templates are installed with **moya fs templates --tree**.')
            else:
                raise errors.ContentError((b'missing templates ').format(textual_list(template)), element=element, diagnosis=b'You can check what templates are installed with **moya fs templates --tree**.')
            return

    def push_content_frame(self, context, content):
        content_stack = context.set_new_call(b'.contentstack', list)
        content_stack.append(content)
        context[b'.content'] = content
        template_data_index = makeindex(b'.contentstack', len(content_stack) - 1, b'td')
        context.push_scope(template_data_index)

    def pop_content_frame(self, context):
        context.pop_scope()
        stack = context[b'.contentstack']
        value = stack.pop()
        if stack:
            context[b'.content'] = stack[(-1)]
        else:
            del context[b'.content']
        return value

    def get_content(self, context):
        content_stack = context[b'.contentstack']
        if not content_stack:
            raise logic.FatalMoyaException(b'content.content-not-found', b'Content not found (did you forget the <content> tag)?')
        return content_stack[(-1)]

    def generate_content(self, context, element_ref, app, td):
        app, element = self.get_element(element_ref, app or None)
        merge_content = []
        for content_app, content_element in element.get_extends_chain(context, app=app):
            templates = content_element.templates(context)
            template = self.resolve_templates(content_app, templates, content_element) if content_app else templates[0]
            content = Content(content_app, template, td=td)
            merge_content.append(content)
            if content_element.has_children:
                self.push_content_frame(context, content)
                try:
                    self.push_defer(context, content_app)
                    try:
                        yield logic.DeferNodeContents(content_element)
                    finally:
                        self.pop_defer(context)

                finally:
                    self.pop_content_frame(context)

        sections = defaultdict(list)
        for _content in merge_content:
            for k, v in _content._section_elements.items():
                sections[k].extend(v)

        for section, elements in list(sections.items()):
            new_elements = []
            merge = b'replace'
            for _app, _element, _merge in elements:
                if _merge != b'inherit':
                    merge = _merge
                if merge == b'replace':
                    new_elements[:] = [
                     (
                      _app, _element, merge)]
                elif merge == b'append':
                    new_elements.append((_app, _element, merge))
                elif merge == b'prepend':
                    new_elements.insert(0, (_app, _element, merge))
                else:
                    raise ValueError((b'unknown merge value ({})').format(merge))

            sections[section][:] = new_elements

        content = merge_content[0]
        for extended_content in merge_content[1:]:
            content.merge_content(extended_content)

        for section, elements in sections.items():
            for app, section_el, merge in elements:
                self.push_content_frame(context, content)
                try:
                    self.push_defer(context, app)
                    try:
                        for el in section_el.generate(context, content, app, merge):
                            yield el

                    finally:
                        self.pop_defer(context)

                finally:
                    self.pop_content_frame(context)

        if content.template is None:
            content.template = app.default_template
        if not content.template:
            raise errors.ElementError(b'content has no template', element=self, diagnosis=b'You can specify a template on the &lt;content&gt; definition')
        context[b'_content'] = content
        return


class ContentElement(ContextElementBase):
    """
    Begin a [link content]content[/link] definition.

    Content is a high level description of a page.

    """

    class Help:
        synopsis = b'define content'
        example = b'\n        <content libname="content.crew.manifest">\n            <title>Crew Manifest</title>\n            <section name="content">\n                <for src="crew" dst="character">\n                    <moya:crew character="character"/>\n                </form>\n            </section>\n            <section name="footer">\n                <markdown>Brought to you by **Moya**.</markdown>\n            </section>\n        </content>\n\n        '

    template = Attribute(b'Template name(s)', type=b'templates', required=False, default=None, map_to=b'templates')
    extends = Attribute(b'Extend content element', type=b'elementref')
    final = Attribute(b'Stop extending with this content element?', type=b'boolean', default=False)
    preserve_attributes = [
     b'template', b'extends', b'_merge']

    class Meta:
        tag_name = b'content'
        translate = False

    def get_extends_chain(self, context, app=None):
        element_refs = set()
        app = app or context.get(b'.app', None)
        node = self
        nodes = [(app, node)]
        extends_ref = node.extends
        while extends_ref:
            if node.final:
                break
            element_refs.add(extends_ref)
            node_app, node = self.document.detect_app_element(context, extends_ref, app=app)
            app = node_app or app
            if node is None:
                break
            nodes.append((app, node))
            extends_ref = node.extends
            if extends_ref in element_refs:
                raise errors.ContentError((b"element '{}' has already been extended").format(extends_ref), element=self, diagnosis=b"Check the 'extends' attribute in your content tags.")

        if not node.final:
            base_content = context.get(b'.sys.site.base_content')
            if base_content:
                app, node = self.document.get_element(base_content, lib=node.lib)
                nodes.append((app, node))
        chain = nodes[::-1]
        return chain

    def post_build(self, context):
        self.extends = self.extends(context)
        self.final = self.final(context)


class SectionElement(LogicElement, ContentElementMixin):
    """
    Defines a section container for content. A [i]section[/i] is a top level container for content, and is used to break up the content in to function groups, which may be rendered independently. For example, here is a content definition with two sections; 'body' and 'sidebar':

    [code xml]
    <content libname="content.front" template="front.html">
        <section name="body">
            <!-- main body content goes here -->
        </section>
        <section name="sidebar">
            <!-- sidebar content here -->
        </section>
    </content>
    [/code]

    The template for the above content would render the sections with the [link templates#render]{% render %}[/link] template tag, For example:

    [code moyatemplate]
    <html>
        <body>
            <div id="sidebar>
            {% render sections.sidebar %}
            </div>
            <h1>Content example</h1>
            {% render sections.body %}
        </body>
    </html>
    [/code]
    """

    class Help:
        synopsis = b'create a content section'

    name = Attribute(b'The name of the section', required=True)
    template = Attribute(b'Template', required=False, default=None)
    merge = Attribute(b'Merge method', default=b'inherit', choices=[b'inherit', b'append', b'prepend', b'replace'])

    class Meta:
        tag_name = b'section'

    def logic(self, context):
        name, template, merge = self.get_parameters(context, b'name', b'template', b'merge')
        content = self.get_content(context)
        app = self.get_app(context)
        content.add_section_element(name, app, self, merge)

    def generate(self, context, content, app, merge):
        name, template = self.get_parameters(context, b'name', b'template')
        content.new_section(name, app.resolve_template(template), merge=merge)
        with content.section(name):
            yield logic.DeferNodeContents(self)


def make_default_section(name):
    _name = name

    class _Section(SectionElement):
        __moya_doc__ = (b'\n            Define a content [tag]section[/tag] called \'{name}\'.\n\n            This is a shortcut for the following:\n            [code xml]\n            <section name="{name}">\n                <!-- content tags here... -->\n            </section>\n            [/code]').format(name=_name)

        class Help:
            synopsis = (b"add a '{}' content section").format(_name)
            example = (b'\n            <section-{}>\n            <!-- content tags here... -->\n            </section>\n            ').format(_name)

        class Meta:
            tag_name = b'section-' + _name

        name = Attribute(b'The name of the section', required=False, default=_name)

    return _Section


SectionHead = make_default_section(b'head')
SectionCss = make_default_section(b'css')
SectionIncludecss = make_default_section(b'includecss')
SectionJs = make_default_section(b'js')
SectionJsfoot = make_default_section(b'jsfoot')
SectionIncludejs = make_default_section(b'includejs')
SectionBody = make_default_section(b'body')
SectionContent = make_default_section(b'content')
SectionFooter = make_default_section(b'footer')

class Node(LogicElement, ContentElementMixin):
    """
    Create a template node in a content definition. A node is essentially a reference to a template with associated data. Here's an example of a content definition containing a template node:

    [code xml]
    <content libname="content.example" template="front.html">
        <section name="body">
            <node template="newscontainer.html" let:style="splash"/>
                <html:p>${news}</html:p>
            </node>
        </section>
    </content>
    [/code]

    Here's what newscontainer.html might look like. Note the use of [link templates#children]{% children %}[/link] which will render the content contained inside a node:

    [code moyatemplate]
    <div style="${style}">
        <h3>The Latest News</h3>
        {% children %}
    </div>
    [/code]
    """

    class Help:
        synopsis = b'creates a template node in content'

    template = Attribute(b'Template', type=b'template', required=False, default=None)
    withscope = Attribute(b'Is current context when rendering template', type=b'boolean', default=False, required=False)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)
    ifexists = Attribute(b'Skip if the template can not be found', type=b'boolean', required=False, default=False)

    def logic(self, context):
        template, withscope, ifexists = self.get_parameters(context, b'template', b'withscope', b'ifexists')
        content = self.get_content(context)
        app = self.get_app(context)
        template = app.resolve_template(template)
        if ifexists:
            engine = self.archive.get_template_engine(b'moya')
            if not engine.exists(template):
                return
        if withscope:
            td = {}
            td.update(context.capture_scope())
        else:
            td = self.get_let_map(context)
        content.add_template(b'node', template, td, app=app)
        if self.has_children:
            with content.node():
                yield logic.DeferNodeContents(self)


class ScopeNode(Node):
    """
    Create a template node that uses the current scope as the template data.

    This node is identical to [tag]node[/tag], with the [c]withscope[/c] attribute set to [c]yes[/c].

    """

    class Help:
        synopsis = b'creates a template node using the current scope'

    withscope = Attribute(b'Is current context when rendering template', type=b'boolean', default=True, required=False)


class RenderBase(LogicElement):
    obj = Attribute(b'Object to render', type=b'index')

    class Help:
        undocumented = True

    class Meta:
        translate = True

    def render_children(self, context):
        for child in self.children(element_class=b'renderable'):
            pass

    def include_css(self, context, media, app, path):
        if isinstance(app, text_type):
            app = self.archive.get_app_from_lib(app)
        path = self.archive.get_media_url(context, app, media, path)
        content = context[b'.content']
        content.include(b'css', IncludePathCSS(path))


class RenderContent(DataSetter, ContentElementMixin):
    """Render content"""

    class Help:
        synopsis = b'render content'

    class Meta:
        is_call = True

    content = Attribute(b'Reference to renderable content', type=b'elementref', required=False, default=None)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)
    withscope = Attribute(b'Use current scope?', default=False, type=b'boolean')
    template = Attribute(b'Template', required=False, default=None)

    def logic(self, context):
        content, withscope, template, dst = self.get_parameters(context, b'content', b'withscope', b'template', b'dst')
        app = self.get_app(context)
        template = app.resolve_template(template)
        if withscope:
            scope = context[b'.call']
        let = self.get_let_map(context)
        td = {}
        if self.has_children:
            call = self.push_funccall(context)
            try:
                yield logic.DeferNodeContents(self)
            finally:
                self.pop_funccall(context)

            args, kwargs = call.get_call_params()
            if withscope:
                new_kwargs = scope
                new_kwargs.update(kwargs)
                kwargs = new_kwargs
            td.update(kwargs)
        td.update(let)
        for defer in self.generate_content(context, content, app, td=td):
            yield defer

        content_obj = context[b'_content']
        result = render_object(content_obj, self.archive, context, b'html')
        self.set_context(context, dst, result)


class ServeContent(LogicElement, ContentElementMixin):
    """Render content and immediately serve it. Note that this tag will stop processing any more logic code."""

    class Help:
        synopsis = b'render and serve content'
        example = b'\n        <serve-content content="#content.front" let:date=".now"/>\n\n        '

    content = Attribute(b'Reference to renderable content', type=b'elementref', required=False, default=None)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)
    withscope = Attribute(b'Use current scope?', default=False, type=b'boolean')
    template = Attribute(b'Template', required=False, default=None)
    status = Attribute(b'Status code', type=b'httpstatus', required=False, default=200)

    class Meta:
        is_call = True

    def logic(self, context):
        content, withscope, template = self.get_parameters(context, b'content', b'withscope', b'template')
        app = self.get_app(context)
        template = app.resolve_template(template)
        if withscope:
            scope = context[b'.call']
        let = self.get_let_map(context)
        td = {}
        if self.has_children:
            call = self.push_funccall(context)
            try:
                yield logic.DeferNodeContents(self)
            finally:
                self.pop_funccall(context)

            args, kwargs = call.get_call_params()
            if withscope:
                new_kwargs = scope
                new_kwargs.update(kwargs)
                kwargs = new_kwargs
            td.update(kwargs)
        td.update(let)
        for defer in self.generate_content(context, content, app, td=td):
            yield defer

        content_obj = context[b'_content']
        content_obj.http_status = self.status(context)
        raise logic.EndLogic(content_obj)


class Title(LogicElement):
    """Set the title for content. This tag simply sets a value called [c]title[/c] on the context, which can be rendered in a templates. Here's an example:

    [code xml]
    <content libname="content.front" template="front.html">
        <title>Welcome!<title>
    </content>
    [/code]

    A reference to [c]title[/c] would appear somewhere in the template associated with the content. For example:

    [code moyatemplate]
    <html>
       <head>
           <title>${title}</title>
        </head>
        <body>
            {% render sections.body %}
        </body>
    </html>
    [/code]
    """

    class Help:
        synopsis = b'set content title'

    class Meta:
        translate = True

    def logic(self, context):
        context[b'title'] = context.sub(self.text)


class SimpleRenderable(Renderable):
    moya_safe = True

    class Help:
        undocumented = True

    def __init__(self, format_string, **kwargs):
        self.html = format_string.format(**kwargs)

    def __repr__(self):
        html = self.html
        if len(self.html) > 50:
            html = html[:50] + b'[...]'
        return b'<SimpleRenderable "%s">' % html

    def moya_render(self, archive, context, target, options):
        return HTML(self.html)


class MediaURL(DataSetter):
    """Get URL to media"""

    class Help:
        synopsis = b'get a URL to media'

    path = Attribute(b'Path in media')
    media = Attribute(b'Media name', required=False, default=b'media')
    _from = Attribute(b'Application containing the media', type=b'application', default=None)
    dst = Attribute(b'Destination to store media URL', required=False, type=b'reference')

    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        media_path = self.archive.get_media_url(context, app, params.media)
        url = url_join(media_path, params.path)
        self.set_context(context, params.dst, url)


class IncludeCSS(LogicElement, ContentElementMixin):
    """
    Add a CSS path to be included in the content. The list of paths will be added to a value called [c]include[/c] when the template is rendered. Here's an example:

    [code xml]
    <content libname="content.front" template="front.html">
        <include-css path="css/news.css" />
    </content>
    [/code]

    The CSS paths can be rendered in a template as follows:

    [code moyatemplate]
    {% render include.css %}
    [/code]

    """

    class Help:
        synopsis = b'include CSS with content'

    type = Attribute(b'Type of link', required=False, default=b'css')
    media = Attribute(b'Media name', required=False, default=b'media')
    path = Attribute(b'Path to CSS', required=False, default=None)
    _from = Attribute(b'Application', type=b'application', default=None)
    url = Attribute(b'External URL', required=False, default=None)

    class Meta:
        one_of = [
         ('path', 'url')]

    def logic(self, context):
        params = self.get_parameters(context)
        content = self.get_content(context)
        app = self.get_app(context)
        if params.url:
            path = params.url
        elif params.path.startswith(b'/'):
            path = params.path
        else:
            media_path = self.archive.get_media_url(context, app, params.media)
            path = url_join(media_path, params.path)
        self.add_include(context, content, params, path)

    def add_include(self, context, content, params, path):
        content.include(params.type, IncludePathCSS(path))


class IncludeJS(IncludeCSS):
    """
    Like [tag]include-css[/tag], but inserts a link to a JS file.

    The JS files may be inserted in to the template as follows:

    [code moyatemplate]
    {% render include.js %}
    [/code]

    This is equivalent to the following:

    [code moyatemplate]
    {%- for include in include.js %}
    <script type="text/javascript" href="${include.path}"/>
    {%- endfor %}
    [/code]

    """

    class Help:
        synopsis = b'include a JS file in content'

    type = Attribute(b'Type of link', required=False, default=b'js')
    defer = Attribute(b'Defer script execution?', type=b'boolean', default=False)
    async = Attribute(b'Load script asynchronously?', type=b'boolean', default=False)

    def add_include(self, context, content, params, path):
        content.include(params.type, IncludePathJS(path, async=params.async, defer=params.defer))


class RenderProxy(object):

    def __init__(self, obj, td, target):
        self.obj = obj
        self.td = td
        self.target = target
        if hasattr(obj, b'moya_render_targets'):
            self.moya_render_targets = obj.moya_render_targets
        if hasattr(obj, b'html_safe'):
            self.html_safe = obj.html_safe

    def on_content_insert(self, context):
        if hasattr(self.obj, b'on_content_insert'):
            return self.obj.on_content_insert(context)

    def moya_render(self, archive, context, target, options):
        if hasattr(self.obj, b'moya_render'):
            options[b'with'] = self.td
            rendered = self.obj.moya_render(archive, context, self.target or target, options)
        else:
            rendered = render_object(self.obj, archive, context, self.target)
        return rendered


class Render(DataSetter, ContentElementMixin):
    """
    Render a [i]renderable[/i] object.

    """

    class Help:
        synopsis = b'render an object in content'
        example = b'\n        <render src="form" />\n        '

    src = Attribute(b'Object to render', required=False, type=b'expression', missing=False)
    dst = Attribute(b'Destination to store rendered content', required=False, type=b'reference')
    target = Attribute(b'Render target', required=False, default=b'html')

    def logic(self, context):
        content_container = context.get(b'.content', None)
        src, dst, target = self.get_parameters(context, b'src', b'dst', b'target')
        td = self.get_let_map(context)
        if src is None:
            section = Section(None, td=td, name=self.libid)
            self.push_content_frame(context, section)
            try:
                yield logic.DeferNodeContents(self)
            finally:
                self.pop_content_frame(context)

            obj = section
        else:
            obj = src
        if not is_renderable(obj) and not is_safe(obj):
            obj = Unsafe(obj)
        if content_container is not None:
            content_container.add_renderable(self._tag_name, RenderProxy(obj, td, target))
        else:
            rendered = render_object(obj, self.archive, context, target)
            self.set_context(context, dst, rendered)
        return


class RenderAll(DataSetter, ContentElementMixin):
    """
    Render a sequence of renderable objects.
    """

    class Help:
        synopsis = b'render a sequence of renderable objects'

    src = Attribute(b'Object to render', required=False, type=b'expression')
    dst = Attribute(b'Destination to store rendered content', required=False, type=b'reference')
    target = Attribute(b'Render target', required=False, default=b'html')

    def logic(self, context):
        content_container = context.get(b'.content', None)
        src, dst, target = self.get_parameters(context, b'src', b'dst', b'target')
        try:
            obj_iter = iter(src)
        except:
            self.throw(b'render-all.not-a-sequence', b'src is not a sequence', diagnosis=(b'Moya was unable to iterate over {}').format(context.to_expr(src)))

        for obj in obj_iter:
            if not is_renderable(obj) and not is_safe(obj):
                obj = Unsafe(obj)
            if content_container is not None:
                content_container.add_renderable(self._tag_name, obj)
            else:
                rendered = render_object(obj, self.archive, context, target)
                self.set_context(context, dst, rendered)

        return


class Template(RenderBase):
    markup = Attribute(b'Markup', required=False, default=b'html', choices=get_installed_markups)

    def finalize(self, context):
        self.template = MoyaTemplate(self.text, self._location)

    def logic(self, context):
        rendered_content = self.template.render(context.obj, context=context)
        markup = Markup(rendered_content, self.markup(context))
        context[b'.content'].add_renderable(self._tag_name, markup)


class Raw(RenderBase):

    def logic(self, context):
        context[b'.content'].add_renderable(self._tag_name, HTML(context.sub(self.text)))


class Wrap(RenderBase):
    """Wrap content between two templates"""
    head = Attribute(b'head template')
    tail = Attribute(b'tail template')
    _from = Attribute(b'Application', type=b'application', required=False, default=None)

    def logic(self, context):
        params = self.get_parameters(context)
        td = self.get_let_map(context)
        content = context[b'.content']
        app = self.get_app(context)
        head_template = app.resolve_template(params.head)
        tail_template = app.resolve_template(params.tail)
        content.add_template(b'head', head_template, td)
        yield logic.DeferNodeContents(self)
        content.add_template(b'tail', tail_template, td)


class DefaultMarkup(RenderBase):
    """Use default markup if a value is None or missing"""

    class Help:
        synopsis = b'use default markup for missing values'

    value = Attribute(b'Value', required=True, type=b'expression')
    default = Attribute(b'Default', required=False, default=b'&ndash;')

    def logic(self, context):
        value = self.value(context)
        if is_missing(value) or value is None:
            context[b'.content'].add_renderable(self._tag_name, HTML(self.default(context)))
        else:
            yield logic.DeferNodeContents(self)
        return


class JS(RenderBase):
    """Insert Javascript content.

    Here's an example:

    [code xml]
    <!-- must be inside a content definition -->
    <js>alert("Ready for takeoff!);</js>
    [/code]

    This would render the following:

    [code moyatemplate]
    <script type="text/javascript">
        alert("Ready for takeoff!);
    </script>
    [/code]

    """

    class Help:
        synopsis = b'insert Javascript content'

    class Meta:
        translate = False

    section = Attribute(b'Section to add script to', required=False, default=b'js')

    def logic(self, context):
        section = self.section(context)
        js = context.sub(self.text)
        html = (b'<script type="text/javascript">{}</script>\n').format(js)
        context[b'.content'].get_section(section).add_renderable(self._tag_name, HTML(html))


class CSS(RenderBase):
    """
    This content tag creates a [c]<style>[/c] element in html, with the enclosed text.

    It is generally preferable to use [tag]include-css[/tag], but this tag can be useful to insert dynamically generated CSS.

    """
    section = Attribute(b'Section to add CSS tag to', required=False, default=b'css')

    class Help:
        synopsis = b'add a CSS to content'
        example = b'\n        <css>\n            .character.rygel\n            {\n                font-weight:bold\n            }\n        </css>\n        '

    class Meta:
        translate = False

    def logic(self, context):
        section = self.section(context)
        css = context.sub(self.text)
        html = b'<style type="text/css">\n%s\n</style>\n' % css.strip()
        context[b'.content'].get_section(section).add_renderable(self._tag_name, HTML(html))


class Text(RenderBase):
    _ignore_skip = True

    def logic(self, context):
        text = self.lib.translate(context, self.text)
        text = escape(context.sub(text))
        html = HTML(text or b' ')
        context[b'.content'].add_renderable(self._tag_name, html)


class ConsoleRender(RenderBase):
    """Render an object as terminal output. Useful as a debugging aid to quickly render an object."""
    obj = Attribute(b'Object to render', type=b'expression', required=True)

    def logic(self, context):
        obj = self.obj(context)
        c = Console(nocolors=False, text=False, width=120, html=True, unicode_borders=False)
        text = c.obj(context, obj).get_text()
        html = (b'<div class="moya-console">{}</div>').format(text)
        context[b'.content'].add_renderable(repr(obj), HTML(html))
        self.include_css(context, b'media', b'moya.debug', b'css/debug.css')