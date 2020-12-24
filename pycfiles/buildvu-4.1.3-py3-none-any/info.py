# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/command/info.py
# Compiled at: 2007-08-08 19:58:56
__doc__ = 'Dump meta information about the current project.'
from distutils.cmd import Command

def name_email(name, email):
    if name and email:
        return '%s <%s>' % (name, email)
    else:
        return name or email


def lax_zip(seq1, seq2):
    len1, len2 = len(seq1), len(seq2)
    if len1 > len2:
        seq2 = seq2 + [(None, None)] * (len1 - len2)
    elif len2 > len1:
        seq1 = seq1 + [(None, None)] * (len2 - len1)
    return zip(seq1, seq2)


def dump(col1, col2=None):
    attr_len = col2 and 12 or 14
    value_len = 20
    rows = []
    if col2:
        for ((n1, v1), (n2, v2)) in lax_zip(col1, col2):
            if n1:
                rows.append(('%s:' % n1).ljust(attr_len))
                rows.append(str(v1).ljust(value_len))
            else:
                rows.append(' ' * (attr_len + value_len))
            if n2:
                rows.append(('%s:' % n2).ljust(attr_len))
                rows.append(str(v2).ljust(value_len))
            rows.append('\n')

    for (n, v) in col1:
        rows.append(('%s:' % n).ljust(attr_len))
        rows.append(str(v).ljust(value_len))
        rows.append('\n')

    print ('').join(rows)


class info(Command):
    __module__ = __name__
    description = 'dump various bits of information about this package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from distutils.command.build_py import build_py
        base = build_py(self.distribution)
        base.initialize_options()
        base.finalize_options()
        self.build_py = base
        self.dump_info()

    def dump_info(self):
        dist = self.distribution
        print '%s - %s\n' % (dist.get_name(), dist.get_description())
        package_info = [('Name', dist.get_name()), ('Version', dist.get_version()), ('License', dist.get_license())]
        if dist.get_platforms() != ['UNKNOWN']:
            platforms = (', ').join(dist.get_platforms())
        else:
            platforms = 'All (not specified)'
        package_info.append(('Platforms', platforms))
        person_info = []
        if dist.get_author() != 'UNKNOWN':
            author = name_email(dist.get_author(), dist.get_author_email())
            person_info.append(('Author', author))
        if dist.get_maintainer() != 'UNKNOWN':
            maintainer = name_email(dist.get_maintainer(), dist.get_maintainer_email())
            person_info.append(('Maintainer', maintainer))
        if dist.get_contact() != 'UNKNOWN' and dist.get_contact() != dist.get_author():
            contact = name_email(dist.get_contact(), dist.get_contact_email())
            person_info.append(('Contact', contact))
        url_info = []
        if dist.get_url():
            url_info.append(('Project URL', '<%s>' % dist.get_url()))
        if dist.get_download_url():
            url_info.append(('Download URL', '<%s>' % dist.get_download_url()))
        dump(package_info, person_info)
        dump(url_info)
        self.dump_trove_cats()
        if dist.get_long_description():
            print 'Description:\n'
            print '    ' + dist.get_long_description().replace('\n', '\n    ')

    def dump_trove_cats(self):
        classifiers = self.distribution.get_classifiers()
        if len(classifiers):
            print 'Trove Classifiers:\n'
            for c in classifiers:
                print '    ' + c

            print