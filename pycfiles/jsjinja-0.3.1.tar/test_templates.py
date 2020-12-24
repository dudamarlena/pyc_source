# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/syrus/Projects/jsjinja/jsjinja/tests/test_templates.py
# Compiled at: 2013-04-18 14:36:37
import os, jinja2, jsjinja
from nose import with_setup

def setup_func():
    pass


def teardown_func():
    pass


from pyv8 import PyV8
TEMPLATE_FOLDER = 'templates/'
env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_FOLDER))
env.add_extension('jsjinja.ext.JsJinjaExtension')

class Global(PyV8.JSClass):

    def log(self, *args):
        print args


ctx = PyV8.JSContext(Global())
ctx.enter()
ctx.eval(jsjinja.lib())

def test_extension():
    js = env.jsjinja.generate_source(source='{{a}}')
    ex = ctx.eval('(new (%s))' % js).render({'a': 'test'})
    assert ex == 'test'


def test_extensiontag():
    template = '{% jsjinja %}{% macro x(s) %}{{s}}{% endmacro %}{% endjsjinja %}'
    t = env.from_string(template)
    js = str(t.render())
    print js
    ex = ctx.eval('(new (%s))' % js).module().x('test')
    assert ex == 'test'


code = env.jsjinja.generate_all()
ctx.eval(code)
context = {'context': True}

def compare_templates(f):
    jinja_template = env.get_template(f).render(context)
    js_template = ctx.locals.Jinja2.getTemplate(f)
    js_template_rendered = unicode(js_template.render(context), 'utf-8')
    print 'JS TEMPLATE:\n', js_template
    print 'Jinja:\n', jinja_template
    print 'Js:\n', js_template_rendered
    assert jinja_template == js_template_rendered


def test_case_generator():
    templates = env.list_templates()
    for f in templates:
        yield (
         compare_templates, f)


def main():
    """Runs the testsuite as command line application."""
    import nose
    try:
        nose.main(defaultTest='')
    except Exception as e:
        print 'Error: %s' % e


if __name__ == '__main__':
    main()