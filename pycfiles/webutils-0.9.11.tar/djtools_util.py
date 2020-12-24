# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/templatetags/djtools_util.py
# Compiled at: 2016-05-17 14:52:55
from django import template
register = template.Library()

@register.filter
def tabularize(value, cols):
    """
        modifies a list to become a list of lists 
        eg [1,2,3,4] becomes [[1,2], [3,4]] with an argument of 2
        Taken from django user group

        Usage:
          {% for row in object_list|tabularize:"4" %}
            {% for obj in row %}
              ....
            {% endfor %}
          {% endfor %}
    """
    try:
        cols = int(cols)
    except ValueError:
        return [
         value]

    return map(*([None] + [ value[i::cols] for i in range(0, cols) ]))


class MapTranslateNode(template.Node):

    def __init__(self, data, src_variables, variable_name):
        self.data = data
        self.src_variables = src_variables
        self.variable_name = variable_name

    def render(self, context):
        from webutils.helpers import map_translate
        data = template.Variable(self.data).resolve(context)
        src_variables = [ template.Variable(x).resolve(context) for x in self.src_variables ]
        new_data = map_translate(data, *src_variables)
        context[self.variable_name] = new_data
        return ''


@register.tag
def map_translate(parser, token):
    """ Used to templatize custom data strings. See 
        webutils.helpers.map_translate for more details.
        
        Usage:
        
        {% map_translate data_string, source,extra,fields as result_name %}
        
        Will run data_string through map_translate using source (plus extra
        fields) and give the result in the template context as "result_name"
    """
    try:
        name, data, src_variables, as_, variable_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' % token.split_contents()[0])

    return MapTranslateNode(data, src_variables.split(','), variable_name)