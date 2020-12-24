# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sysadmin/src/malt/malt/ext/malt_tags.py
# Compiled at: 2017-05-12 18:32:12
# Size of source mod 2**32: 3469 bytes
import malt
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


@malt.hooks.register('init_record')
def register_tags(record):
    tagstr, record['tags'] = record.get('tags', ''), []
    for tag in (t.strip() for t in tagstr.split(',')):
        if tag:
            register_tag(record['type'], tag, record['src'])
            record['tags'].append(Tag(tag, url(record['type'], tag)))


@malt.hooks.register('exit_build')
def build_tag_indexes():
    for rectype, recmap in tags.items():
        typedata = malt.site.typedata(rectype)
        for slug, filelist in recmap.items():
            reclist = []
            for filepath in filelist:
                record = malt.records.record(filepath)
                if typedata['order_by'] in record:
                    reclist.append(record)

            index = malt.pages.Index(rectype, slugs(rectype, slug), reclist, typedata['per_tag_index'])
            index['tag'] = names[rectype][slug]
            index['is_tag_index'] = True
            index.render()


@malt.hooks.register('page_classes')
def add_tag_classes(classes, page):
    if page.get('is_tag_index'):
        classes.append('tag-index')
        classes.append('tag-index-%s' % malt.utils.slugify(page['tag']))
    return classes


@malt.hooks.register('page_templates')
def add_tag_templates(templates, page):
    if page.get('is_tag_index'):
        templates = ['%s-tag-index' % page['type']['name'],
         'tag-index',
         'index']
    return templates


def register_tag(rectype, tag, filepath):
    slug = malt.utils.slugify(tag)
    tags.setdefault(rectype, {}).setdefault(slug, []).append(filepath)
    names.setdefault(rectype, {}).setdefault(slug, tag)


def url(rectype, tag):
    return malt.site.url(slugs(rectype, tag, 'index'))


def slugs(rectype, tag, *append):
    slugs = malt.site.slugs(rectype)
    slugs.append(malt.site.typedata(rectype, 'tag_slug'))
    slugs.append(malt.utils.slugify(tag))
    slugs.extend(append)
    return slugs