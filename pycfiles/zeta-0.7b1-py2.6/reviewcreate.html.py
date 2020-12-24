# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratap/mybzr/pratap/dev/zeta/defenv/data/templates/derived/projects/reviewcreate.html.py
# Compiled at: 2010-07-12 03:41:08
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1278920468.838961
_template_filename = '/home/pratap/mybzr/pratap/dev/zeta/zeta/templates-dojo/derived/projects/reviewcreate.html'
_template_uri = '/derived/projects/reviewcreate.html'
_template_cache = cache.Cache(__name__, _modified_time)
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['create_review', 'hd_script', 'bd_body', 'hd_links', 'bd_script']
page_tooltips = [
 [
  'Help',
  'Review - documents, code and wiki pages. Every review created, has an\n<em>author</em>, a <em>moderator</em> and <em>participants</em>.\n'],
 [
  'Author',
  "<em>Author</em> can add comments, comment's nature and also\nreponsible for taking actions on all review comments."],
 [
  'Moderator',
  "<em>Moderator</em> can add comments, comment's nature and is responsible\nfor approving actions taken on review comments. Once all the comments are\napprove, the moderator can close the review."],
 [
  'Participant',
  '<em>Participants</em> can comment and reply to other paticipants\ncomment.'],
 [
  'Review-set',
  'Collection of reviews. Especially useful to create review entries for every\nmodified / added file in repository changeset\n'],
 [
  'Timeline',
  'Timeline of all updates done to Review(s).']]

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]


def _mako_generate_namespaces(context):
    ns = runtime.Namespace('forms', context._clean_inheritance_tokens(), templateuri='/component/forms.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'forms')] = ns
    ns = runtime.Namespace('elements', context._clean_inheritance_tokens(), templateuri='/component/elements.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'elements')] = ns
    return


def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '/base/basic1.html', _template_uri)


def render_body(context, **pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n')
        __M_writer('\n\n\n')
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_create_review(context):
    context.caller_stack._push_frame()
    try:
        forms = _mako_get_namespace(context, 'forms')
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    <div id="prjrevwcreate" class="floatl">\n        ')
        __M_writer(escape(forms.form_createrev(c.authuser, c.project, c.rsets, h.suburl_createrev, c.projusers, c.usernames, c.forsrc, c.forversion)))
        __M_writer('\n    </div>\n    <div id="prjrsetcreate" class="floatl ml10"\n         style="border-left : 2px solid gray;">\n        ')
        __M_writer(escape(forms.form_createrset(c.authuser, c.project, h.suburl_createrset, request.url)))
        __M_writer('\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_script()))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_body(context):
    context.caller_stack._push_frame()
    try:
        capture = context.get('capture', UNDEFINED)
        c = context.get('c', UNDEFINED)
        elements = _mako_get_namespace(context, 'elements')
        h = context.get('h', UNDEFINED)
        forms = _mako_get_namespace(context, 'forms')

        def create_review():
            return render_create_review(context)

        __M_writer = context.writer()
        __M_writer('\n    ')
        sel_revw = capture(forms.form_selectrevw, c.authuser, c.revwlist, c.review and c.review.resource_url or '')
        sel_rset = capture(forms.form_selectrset, c.authuser, c.rsetlist, c.reviewset and c.reviewset.name or '')
        revwsets = '<span class="ml10 fwnormal fntsmall">                     <a href="%s" title="List of reviews sets">                     Reviewsets</a></span>' % h.url_reviewsets
        charts = capture(elements.iconlink, h.url_revwcharts, 'barchart', title='Review analytics')
        tline = capture(elements.iconlink, h.url_revwtimeline, 'timeline', title='Timeline')
        __M_writer('\n    ')
        __M_writer(escape(elements.mainnav()))
        __M_writer('\n    ')
        __M_writer(escape(elements.contextnav([sel_revw, sel_rset, revwsets], rspans=[
         charts, tline], tooltips=page_tooltips)))
        __M_writer('\n\n    <div id="bdy" class="w100">\n')
        if c.authusername == 'anonymous' or not c.userpanes:
            __M_writer('        <div class="fullpanel1">\n')
        else:
            __M_writer('        <div class="panel1">\n')
        __M_writer('            <div>\n                ')
        __M_writer(escape(create_review()))
        __M_writer('\n            </div>\n        </div> \n')
        if c.authusername != 'anonymous' and c.userpanes:
            __M_writer('        <div class="panel2">')
            __M_writer(escape(elements.user_panes(c.userpanes)))
            __M_writer('</div>\n')
        __M_writer('    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_hd_links(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.hd_links()))
        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_bd_script(context):
    context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n    ')
        __M_writer(escape(parent.bd_script()))
        __M_writer('\n\n    <script type="text/javascript">\n        dojo.addOnLoad( function() {\n            var n_select = dojo.query( \'#selectrevw\' )[0];\n            n_select ? select_goto( n_select ) : null;\n        });\n        dojo.addOnLoad( initform_createrev );\n        dojo.addOnLoad( initform_createrset );\n\n        dojo.addOnLoad( setup_userpanes );\n        dojo.addOnLoad( adjust_upheight );\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()