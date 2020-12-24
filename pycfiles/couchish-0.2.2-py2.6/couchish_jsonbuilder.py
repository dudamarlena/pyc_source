# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchish/couchish_jsonbuilder.py
# Compiled at: 2009-05-08 12:08:14
from couchish.create_view import getjs
from couchish.schemaish_jsonbuilder import strip_stars
from string import Template

def buildview(view):
    """
    function (doc) {
        if (doc.model_type == 'book'){
            for (var i1 in doc.metadata) {
            for (var i2 in doc.metadata[i1].authors) {
                emit(doc.metadata[i1].authors[i2]._ref, null);
            }
            }
        }
    }
    """
    main_template = Template('    function (doc) {\n$body\n    }')
    if_template = Template("        if (doc.model_type == '$type'){\n$body\n        }\n")
    for_template = Template('            for (var i$n in doc$attr) {\n$body\n            }')
    emit_template = Template('                emit(doc$attr._ref, null);')
    out = ''
    for (type, attrs) in view.items():
        out_fors = ''
        for attr in attrs:
            templ_if = if_template.substitute({'type': type, 'body': '$body'})
            segments = attr.replace('.*', '*').split('.')
            cleansegments = attr.replace('.*', '').split('.')
            out_attr = ''
            templ_fors = '$body\n'
            for (n, segment) in enumerate(segments):
                if segment.endswith('*'):
                    out_loop_var = out_attr + '.%s' % cleansegments[n]
                    out_attr += '.%s[i%s]' % (cleansegments[n], n)
                    templ_for = for_template.substitute(n=n, attr=out_loop_var, body='$body')
                    templ_fors = Template(templ_fors).substitute(body=templ_for)
                else:
                    out_attr += '.%s' % cleansegments[n]

            out_emit = emit_template.substitute(attr=out_attr)
            out_fors += Template(templ_fors).substitute(body=out_emit)

        out += Template(templ_if).substitute(body=out_fors)

    return (
     main_template.substitute(body=out), None)


def build_refersto_view(uses):
    model_types = set()
    if isinstance(uses, basestring):
        model_type = uses.split('.')[0]
        uses = [uses]
    else:
        for use in uses:
            mt = use.split('.')[0]
            model_types.add(mt)

        if len(model_types) > 1:
            raise ValueError('Can only use one model type in "uses" at the moment')
        model_type = list(model_types)[0]
    viewdef = 'function (doc) {\n'
    viewdef += "    if (doc.model_type == '" + model_type + "'){\n"
    viewdef += '        emit(doc._id, %s )\n' % getjs(uses)
    viewdef += '    }\n'
    viewdef += '}\n'
    return viewdef


def get_view(view, views, views_by_viewname, model_type=None):
    if model_type is None:
        model_type = view.get('model_type')
    if 'designdoc' not in view:
        view['designdoc'] = model_type
    if 'map' in view:
        map = view['map']
        reduce = view.get('reduce')
    elif 'type' in view:
        if 'name' not in view:
            view['name'] = view['type']
        if view['type'] == 'all':
            map, reduce = "function(doc) { if (doc.model_type == '%s') { emit(doc._id, null); } }" % model_type, None
        if view['type'] == 'all_count':
            map, reduce = "function(doc) { if (doc.model_type == '%s') { emit(doc._id, 1); } }" % model_type, 'function(keys, values) { return sum(values); }'
    else:
        map = build_refersto_view(view['uses'])
        reduce = view.get('reduce')
    if 'url' not in view:
        if view['designdoc'] is None:
            raise KeyError('Cannot work out a design doc for view %s' % view.get('name'))
        else:
            view['url'] = '%s/%s' % (view['designdoc'], view['name'])
    views_by_viewname[view['url']] = {'url': view['url'], 'key': view.get('key', '_id'), 'uses': view.get('uses')}
    views_by_viewname[view['url']]['map'] = (
     map, reduce)
    views[view['url']] = (map, reduce)
    return


def get_reference(field):
    if 'attr' not in field:
        return (field.get('refersto', None), field.get('uses', None))
    else:
        return get_reference(field['attr'])


def get_views(models_definition, views_definition):
    views = {}
    views_by_viewname = {}
    views_by_uses = {}
    viewnames_by_attribute = {}
    attributes_by_viewname = {}
    for view in views_definition:
        get_view(view, views, views_by_viewname)

    for (model_type, definition) in models_definition.items():
        for view in definition.get('views', []):
            get_view(view, views, views_by_viewname, model_type=model_type)

    parents = []
    field_to_view = {}
    for (model_type, definition) in models_definition.items():
        for field in definition['fields']:
            field['key'] = strip_stars(field['name'])
            if field.get('type', '').startswith('Sequence'):
                fieldname = '%s.*' % field['name']
            else:
                fieldname = field['name']
            if 'attr' in field:
                (refersto, uses) = get_reference(field['attr'])
                if refersto:
                    view = views_by_viewname[refersto]
                    if not uses:
                        uses = view['uses']
                    if isinstance(uses, basestring):
                        views_by_uses.setdefault(view['url'] + '-rev', {}).setdefault(model_type, []).append(fieldname)
                        viewnames_by_attribute.setdefault(uses, set()).add(refersto)
                        attributes_by_viewname.setdefault(refersto, {}).setdefault(model_type, set()).add(fieldname.replace('.*', '*'))
                    else:
                        views_by_uses.setdefault(view['url'] + '-rev', {}).setdefault(model_type, []).append(fieldname)
                        attributes_by_viewname.setdefault(refersto, {}).setdefault(model_type, set()).add(fieldname.replace('.*', '*'))
                        for use in uses:
                            viewnames_by_attribute.setdefault(use, set()).add(refersto)

            if 'viewby' in field:
                if '*' in fieldname:
                    raise Exception("Can't generate viewby views on attributes in sequences")
                if field['viewby'] == True:
                    url = '%s/by_%s' % (model_type, fieldname)
                else:
                    url = field['viewby']
                views[url] = (
                 "function(doc) { if (doc.model_type=='%s') { emit(doc.%s,  null ); } }" % (model_type, field['name']), None)
                if 'viewby_count' in field:
                    if field['viewby_count'] == True:
                        url = '%s/by_%s_count' % (model_type, fieldname)
                    else:
                        url = field['viewby_count']
                    views[url] = (
                     "function(doc) { if (doc.model_type == '%s') { emit(doc._id, 1); } }" % model_type, 'function(keys, values) { return sum(values); }')

    for (url, view) in views_by_uses.items():
        views[url] = buildview(view)

    out = {'views': views, 'views_by_viewname': views_by_viewname, 'viewnames_by_attribute': viewnames_by_attribute, 'attributes_by_viewname': attributes_by_viewname, 'views_by_uses': views_by_uses}
    return out