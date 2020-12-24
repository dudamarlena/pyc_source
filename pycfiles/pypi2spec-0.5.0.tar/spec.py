# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierrey/repos/gitrepo/pypi2spec/pypi2spec/spec.py
# Compiled at: 2014-08-26 01:56:59
"""
Spec class, handles the read/write of the spec file
"""
import datetime, os, re, sys, textwrap
from jinja2 import Template
try:
    from pypi2spec import get_logger, get_rpm_tag, Pypi2specError
except ImportError:
    from __init__ import get_logger, get_rpm_tag, Pypi2specError

def format_description(description):
    """ Format the description as required by rpm """
    if not description:
        return ''
    if not any([ len(line) > 75 for line in description.split('\n') ]):
        return description
    wrapper = textwrap.TextWrapper(width=75)
    cleaned = ('\n').join([ l.strip() for l in description.split('\n') ])
    return ('\n\n').join([ wrapper.fill(p) for p in cleaned.split('\n\n') ])


def format_dependencies(dependencies):
    """ Format the dependencies cleanning them as much as possible for rpm.
    """
    ignorelist = [
     'python']
    versionmotif = re.compile('\\d\\.\\d\\.?\\d?')
    char = {'\r': '', 
       '(': ' ', 
       ')': ' ', 
       ',': ' ', 
       '  ': ' '}
    for key in char.keys():
        dependencies = dependencies.replace(key, char[key])

    dep_list = []
    for dep in dependencies.split(' '):
        if dep.strip():
            if '>' not in dep and '<' not in dep and '=' not in dep and len(versionmotif.findall(dep)) == 0 and dep.strip() not in ignorelist:
                dep = dep.strip()
                dep_list.append(dep)

    return (' ').join(dep_list).strip()


class Spec:
    """
    Spec Class
        Write the spec file.
    """

    def __init__(self, settings, package=None, python3=False):
        """ Constructor.
        """
        self.package = package
        self.settings = settings
        self.__dict = {}
        self.log = get_logger()
        self.spec = None
        self.python3 = python3
        return

    def fill_spec_info(self):
        """ Fills the different variable required for the spec file. """
        self.log.info('Filling spec variable from info collected')
        self.__dict['modname'] = self.package.name
        self.__dict['barename'] = self.package.name.replace('.', '-')
        if self.package.name.startswith('python-'):
            self.__dict['name'] = self.__dict['barename']
        else:
            self.__dict['name'] = 'python-%s' % self.__dict['barename']
        self.__dict['arch'] = self.package.arch
        self.__dict['version'] = self.package.version
        self.__dict['summary'] = self.package.summary
        self.__dict['license'] = self.package.license
        self.__dict['description'] = format_description(self.package.description)
        self.__dict['URL'] = self.package.url
        self.__dict['source0'] = self.package.source0
        self.__dict['_source0'] = self.package.source0.replace(self.package.name, '%{modname}').replace(self.package.version, '%{version}')
        self.__dict['packager'] = self.settings.get('packager')
        self.__dict['email'] = self.settings.get('email')
        self.__dict['date'] = datetime.datetime.now().strftime('%a %b %d %Y')
        self.__dict['python3'] = self.python3

    def get_specfile(self):
        """ Return the path to the spec file.
        """
        specdir = get_rpm_tag('_specdir')
        if self.package.name.startswith('python-'):
            specname = '%s.spec' % self.__dict['barename'].lower()
        else:
            specname = 'python-%s.spec' % self.__dict['barename'].lower()
        return '%s/%s' % (specdir, specname)

    def read_specfile(self):
        """ Read the specfile present in the spec directory.
        """
        specfile = self.get_specfile()
        if os.path.exists(specfile) and os.path.isfile(specfile):
            self.log.info('Reading file %s' % specfile)
            try:
                stream = open(specfile, 'r')
                self.spec = stream.read()
                stream.close()
            except IOError as err:
                self.log.info('Cannot read the file %s' % specfile)
                self.log.debug('ERROR: %s' % err)

    def get_template(self):
        """ Read the empty template and fills it with the information
        retrieved.
        """
        template = '%s/specfile.tpl' % os.path.dirname(__file__)
        self.log.info('Filling spec template')
        try:
            stream = open(template, 'r')
            tplfile = stream.read()
            stream.close()
            mytemplate = Template(tplfile)
            self.spec = mytemplate.render(self.__dict)
        except IOError as err:
            self.log.debug('ERROR: %s' % err)
            raise Pypi2specError('Cannot read the file %s' % template)

    def write_spec(self, verbose=False):
        """ Write down the spec to the spec directory as returned by rpm.
        """
        specfile = self.get_specfile()
        self.log.info('Writing file %s' % specfile)
        try:
            stream = open(specfile, 'w')
            stream.write(self.spec.encode('utf-8'))
            stream.close()
            self.log.debug('Spec file writen: %s' % specfile)
            print 'Spec file writen: %s' % specfile
        except IOError as err:
            print 'Cannot write the file %s' % specfile
            self.log.debug('ERROR: %s' % err)