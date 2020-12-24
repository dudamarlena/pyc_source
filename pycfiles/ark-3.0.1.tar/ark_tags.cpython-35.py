# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_tags.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 3455 bytes
import ark
tags = {}
names = {}

class Tag:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return 'Tag(name=%s, url=%s)' % (repr(self.name), repr(self.url))

    def __str__(self):
        return '<a href="%s">%s</a>' % (self.url, self.name)


@ark.hooks.register('init_record')
def register_tags(record):
    tagstr, record['tags'] = record.get('tags', ''), []
    for tag in (t.strip() for t in tagstr.split(',')):
        if tag:
            register_tag(record['type'], tag, record['src'])
            record['tags'].append(Tag(tag, url(record['type'], tag)))


@ark.hooks.register('exit_build')
def build_tag_indexes():
    for rectype, recmap in tags.items():
        typedata = ark.site.typedata(rectype)
        for slug, filelist in recmap.items():
            reclist = []
            for filepath in filelist:
                record = ark.records.record(filepath)
                if typedata['order_by'] in record:
                    reclist.append(record)

            index = ark.pages.Index(rectype, slugs(rectype, slug), reclist, typedata['per_tag_index'])
            index['tag'] = names[rectype][slug]
            index['is_tag_index'] = True
            index.render()


@ark.hooks.register('page_classes')
def add_tag_classes(classes, page):
    if page.get('is_tag_index'):
        classes.append('tag-index')
        classes.append('tag-index-%s' % ark.utils.slugify(page['tag']))
    return classes


@ark.hooks.register('page_templates')
def add_tag_templates(templates, page):
    if page.get('is_tag_index'):
        templates = ['%s-tag-index' % page['type']['name'],
         'tag-index',
         'index']
    return templates


def register_tag(rectype, tag, filepath):
    slug = ark.utils.slugify(tag)
    tags.setdefault(rectype, {}).setdefault(slug, []).append(filepath)
    names.setdefault(rectype, {}).setdefault(slug, tag)


def url(rectype, tag):
    return ark.site.url(slugs(rectype, tag, 'index'))


def slugs(rectype, tag, *append):
    slugs = ark.site.slugs(rectype)
    slugs.append(ark.site.typedata(rectype, 'tag_slug'))
    slugs.append(ark.utils.slugify(tag))
    slugs.extend(append)
    return slugs