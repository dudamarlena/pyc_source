# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/docs.py
# Compiled at: 2016-05-20 23:26:47
"""
Utils called from project_root/docs/conf.py when Sphinx
documentation is generated.
"""
from __future__ import division, print_function, unicode_literals
import os.path
from datetime import datetime
from shutil import copyfile, move
from socket import gethostname
from string import letters
from warnings import warn
from django.template.defaultfilters import urlize
from django.utils.datastructures import SortedDict
from future.builtins import map, open, str
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from django.utils.functional import Promise
from shuyucms import __version__
from shuyucms.conf import registry
from shuyucms.utils.importing import import_dotted_path, path_for_import

def deep_force_unicode(value):
    """
    Recursively call force_text on value.
    """
    if isinstance(value, (list, tuple, set)):
        value = type(value)(map(deep_force_unicode, value))
    elif isinstance(value, dict):
        value = type(value)(map(deep_force_unicode, value.items()))
    elif isinstance(value, Promise):
        value = force_text(value)
    return value


def build_settings_docs(docs_path, prefix=None):
    """
    Converts names, descriptions and defaults for settings in
    ``shuyucms.conf.registry`` into RST format for use in docs,
    optionally filtered by setting names with the given prefix.
    """
    dynamic = b'[dynamic]'
    lines = [b'.. THIS DOCUMENT IS AUTO GENERATED VIA conf.py']
    for name in sorted(registry.keys()):
        if prefix and not name.startswith(prefix):
            continue
        setting = registry[name]
        settings_name = b'``%s``' % name
        setting_default = setting[b'default']
        if isinstance(setting_default, str):
            if gethostname() in setting_default or setting_default.startswith(b'/') and os.path.exists(setting_default):
                setting_default = dynamic
        if setting_default != dynamic:
            setting_default = repr(deep_force_unicode(setting_default))
        lines.extend([b'', settings_name, b'-' * len(settings_name)])
        lines.extend([b'',
         urlize(setting[b'description'] or b'').replace(b'<a href="', b'`').replace(b'" rel="nofollow">', b' <').replace(b'</a>', b'>`_')])
        if setting[b'choices']:
            choices = (b', ').join([ b'%s: ``%s``' % (str(v), force_text(k)) for k, v in setting[b'choices']
                                   ])
            lines.extend([b'', b'Choices: %s' % choices, b''])
        lines.extend([b'', b'Default: ``%s``' % setting_default])

    with open(os.path.join(docs_path, b'settings.rst'), b'w') as (f):
        f.write((b'\n').join(lines).replace(b"u'", b"'").replace(b"yo'", b"you'"))


def build_deploy_docs(docs_path):
    try:
        from fabric.main import load_fabfile
    except ImportError:
        warn(b"Couldn't build fabfile.rst, fabric not installed")
        return

    project_template_path = path_for_import(b'shuyucms.project_template')
    commands = load_fabfile(os.path.join(project_template_path, b'fabfile'))[1]
    lines = []
    for name in sorted(commands.keys()):
        doc = commands[name].__doc__.strip().split(b'\n')[0]
        lines.append(b'  * ``fab %s`` - %s' % (name, doc))

    with open(os.path.join(docs_path, b'fabfile.rst'), b'w') as (f):
        f.write((b'\n').join(lines))


_changeset_date = lambda cs: datetime.fromtimestamp(cs.date()[0])

def build_changelog(docs_path, package_name=b'shuyucms'):
    """
    Converts Mercurial commits into a changelog in RST format.
    """
    project_path = os.path.join(docs_path, b'..')
    version_file = os.path.join(package_name, b'__init__.py')
    version_var = b'__version__'
    changelog_filename = b'CHANGELOG'
    changelog_file = os.path.join(project_path, changelog_filename)
    versions = SortedDict()
    repo = None
    ignore = ('AUTHORS', 'formatting', 'typo', 'pep8', 'pep 8', 'whitespace', 'README',
              'trans', 'print debug', 'debugging', 'tabs', 'style', 'sites', 'ignore',
              'tweak', 'cleanup', 'minor', 'for changeset', '.com``', 'oops', 'syntax')
    hotfixes = {b'40cbc47b8d8a': b'1.0.9', 
       b'a25749986abc': b'1.0.10'}
    try:
        from mercurial import ui, hg, error
        from mercurial.commands import tag
    except ImportError:
        pass
    else:
        try:
            ui = ui.ui()
            repo = hg.repository(ui, project_path)
        except error.RepoError:
            return

    if repo is None:
        return
    changesets = [ repo.changectx(changeset) for changeset in repo.changelog ]
    for cs in sorted(changesets, reverse=True, key=_changeset_date):
        files = cs.files()
        new_version = False
        description = cs.description().decode(b'utf-8')
        description = description.rstrip(b'.').replace(b'\n', b'. ')
        while b'  ' in description:
            description = description.replace(b'  ', b' ')

        description = description.replace(b'. . ', b'. ').replace(b'...', b',')
        while b'..' in description:
            description = description.replace(b'..', b'.')

        description = description.replace(b':.', b':').replace(b"n'. t", b"n't")
        words = description.split()
        for i, word in enumerate(words):
            if set(b'._') & set(word[:-1]) and set(letters) & set(word) and b'`' not in word and not word[0].isdigit():
                last = b''
                if word[(-1)] in b',.':
                    last, word = word[(-1)], word[:-1]
                words[i] = b'``%s``%s' % (word, last)

        description = (b' ').join(words)
        if version_file in files:
            for line in cs[version_file].data().split(b'\n'):
                if line.startswith(version_var):
                    exec line
                    if locals()[version_var] == b'0.1.0':
                        locals()[version_var] = b'1.0.0'
                        break
                    versions[locals()[version_var]] = {b'changes': [], b'date': _changeset_date(cs).strftime(b'%b %d, %Y')}
                    new_version = len(files) == 1

        hotfix = hotfixes.get(cs.hex()[:12])
        if hotfix or new_version:
            if hotfix:
                version_tag = hotfix
            else:
                try:
                    version_tag = locals()[version_var]
                except KeyError:
                    version_tag = None

            if version_tag and version_tag not in cs.tags():
                try:
                    tag(ui, repo, version_tag, rev=cs.hex())
                    print(b'Tagging version %s' % version_tag)
                except:
                    pass

        merge = len(cs.parents()) > 1
        branch_closed = len(files) == 0
        changelog_update = changelog_filename in files
        ignored = [ w for w in ignore if w.lower() in description.lower() ]
        one_word = len(description.split()) == 1
        if merge or new_version or branch_closed or changelog_update or ignored or one_word:
            continue
        version = None
        try:
            version = locals()[version_var]
        except KeyError:
            if not hotfix:
                continue

        user = cs.user().decode(b'utf-8').split(b'<')[0].strip()
        entry = b'%s - %s' % (description, user)
        if hotfix or entry not in versions[version][b'changes']:
            if hotfix:
                versions[hotfix] = {b'changes': [entry], b'date': _changeset_date(cs).strftime(b'%b %d, %Y')}
            else:
                versions[version][b'changes'].insert(0, entry)

    with open(changelog_file, b'w') as (f):
        for version, version_info in versions.items():
            header = b'Version %s (%s)' % (version, version_info[b'date'])
            f.write(b'%s\n' % header)
            f.write(b'%s\n' % (b'-' * len(header)))
            f.write(b'\n')
            if version_info[b'changes']:
                for change in version_info[b'changes']:
                    f.write(b'  * %s\n' % change)

            else:
                f.write(b'  * No changes listed.\n')
            f.write(b'\n')

    return


def build_modelgraph(docs_path, package_name=b'shuyucms'):
    """
    Creates a diagram of all the models for shuyucms and the given
    package name, generates a smaller version and add it to the
    docs directory for use in model-graph.rst
    """
    to_path = os.path.join(docs_path, b'img', b'graph.png')
    build_path = os.path.join(docs_path, b'build', b'_images')
    resized_path = os.path.join(os.path.dirname(to_path), b'graph-small.png')
    settings = import_dotted_path(package_name + b'.project_template.settings')
    apps = [ a.rsplit(b'.')[1] for a in settings.INSTALLED_APPS if a.startswith(b'shuyucms.') or a.startswith(package_name + b'.')
           ]
    try:
        from django_extensions.management.commands import graph_models
    except ImportError:
        warn(b"Couldn't build model_graph, django_extensions not installed")
    else:
        options = {b'inheritance': True, b'outputfile': b'graph.png', b'layout': b'dot'}
        try:
            graph_models.Command().execute(*apps, **options)
        except Exception as e:
            warn(b"Couldn't build model_graph, graph_models failed on: %s" % e)
        else:
            try:
                move(b'graph.png', to_path)
            except OSError as e:
                warn(b"Couldn't build model_graph, move failed on: %s" % e)

        try:
            if not os.path.exists(build_path):
                os.makedirs(build_path)
            copyfile(to_path, os.path.join(build_path, b'graph.png'))
        except OSError as e:
            warn(b"Couldn't build model_graph, copy to build failed on: %s" % e)

        try:
            from PIL import Image
            image = Image.open(to_path)
            image.width = 800
            image.height = image.size[1] * 800 // image.size[0]
            image.save(resized_path, b'PNG', quality=100)
        except Exception as e:
            warn(b"Couldn't build model_graph, resize failed on: %s" % e)
            return


def build_requirements(docs_path, package_name=b'shuyucms'):
    """
    Updates the requirements file with shuyucms's version number.
    """
    mezz_string = b'shuyucms=='
    project_path = os.path.join(docs_path, b'..')
    requirements_file = os.path.join(project_path, package_name, b'project_template', b'requirements.txt')
    with open(requirements_file, b'r') as (f):
        requirements = f.readlines()
    with open(requirements_file, b'w') as (f):
        f.write(b'shuyucms==%s\n' % __version__)
        for requirement in requirements:
            if requirement.strip() and not requirement.startswith(mezz_string):
                f.write(requirement)