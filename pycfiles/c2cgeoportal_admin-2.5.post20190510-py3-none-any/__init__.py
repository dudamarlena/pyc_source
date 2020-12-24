# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/c2cgeoportal/scaffolds/__init__.py
# Compiled at: 2019-04-23 07:29:02
import re, subprocess, os, json, requests, yaml
from six import string_types
from simplejson.scanner import JSONDecodeError
from pyramid.scaffolds.template import Template
from pyramid.compat import input_
from c2cgeoportal.lib.bashcolor import colorize, GREEN

class BaseTemplate(Template):
    """
    A class that can be used as a base class for c2cgeoportal scaffolding
    templates.

    Greatly inspired from ``pyramid.scaffolds.template.PyramidTemplate``.
    """

    def pre(self, command, output_dir, vars_):
        """
        Overrides ``pyramid.scaffold.template.Template.pre``, adding
        several variables to the default variables list. Also prevents
        common misnamings (such as naming a package "site" or naming a
        package logger "root").
        """
        self._get_vars(vars_, 'package', 'Get a package name: ')
        self._get_vars(vars_, 'apache_vhost', 'The Apache vhost name: ')
        self._get_vars(vars_, 'srid', 'Spatial Reference System Identifier (e.g. 21781): ', int)
        srid = vars_['srid']
        extent = self._epsg2bbox(srid)
        self._get_vars(vars_, 'extent', ('Extent (minx miny maxx maxy): in EPSG: {srid} projection, default is [{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}]: ').format(srid=srid, bbox=extent) if extent else ('Extent (minx miny maxx maxy): in EPSG: {srid} projection: ').format(srid=srid))
        match = re.match('([\\d.]+)[,; ] *([\\d.]+)[,; ] *([\\d.]+)[,; ] *([\\d.]+)', vars_['extent'])
        if match is not None:
            extent = [ match.group(n + 1) for n in range(4) ]
        vars_['extent'] = (',').join(extent)
        vars_['extent_mapserver'] = (' ').join(extent)
        vars_['extent_viewer'] = json.dumps(extent)
        ret = Template.pre(self, command, output_dir, vars_)
        if vars_['package'] == 'site':
            raise ValueError("Sorry, you may not name your package 'site'. The package name 'site' has a special meaning in Python.  Please name it anything except 'site'.")
        package_logger = vars_['package']
        if package_logger == 'root':
            package_logger = 'app'
        vars_['package_logger'] = package_logger
        return ret

    @staticmethod
    def out(msg):
        print msg

    @staticmethod
    def _get_vars(vars_, name, prompt, type_=None):
        """
        Set an attribute in the vars dict.
        """
        if name.upper() in os.environ:
            value = os.environ[name.upper()]
        else:
            value = vars_.get(name)
        if value is None:
            value = input_(prompt).strip()
        if type_ is not None:
            try:
                type_(value)
            except ValueError:
                print ('The attribute {} is not a {}').format(name, type_)
                exit(1)

        vars_[name] = value
        return

    @staticmethod
    def _epsg2bbox(srid):
        try:
            r = requests.get(('http://epsg.io/?format=json&q={}').format(srid))
            bbox = r.json()['results'][0]['bbox']
            r = requests.get(('http://epsg.io/trans?s_srs=4326&t_srs={srid}&data={bbox[1]},{bbox[0]}').format(srid=srid, bbox=bbox))
            r1 = r.json()[0]
            r = requests.get(('http://epsg.io/trans?s_srs=4326&t_srs={srid}&data={bbox[3]},{bbox[2]}').format(srid=srid, bbox=bbox))
            r2 = r.json()[0]
            return [
             r1['x'], r2['y'], r2['x'], r1['y']]
        except JSONDecodeError:
            print "epsg.io doesn't return a correct json."
            return
        except IndexError:
            print 'Unable to get the bbox'
            return

        return


class TemplateCreate(BaseTemplate):
    _template_dir = 'create'
    summary = 'Template used to create a c2cgeoportal project'

    def post(self, command, output_dir, vars_):
        """
        Overrides the base template class to print the next step.
        """
        if os.name == 'posix':
            for file in ('post-restore-code', 'pre-restore-database.mako'):
                dest = os.path.join(output_dir, 'deploy/hooks', file)
                subprocess.check_call(['chmod', '+x', dest])

        self.out('\nContinue with:')
        self.out(colorize(('.build/venv/bin/pcreate -s c2cgeoportal_update ../{vars[project]} package={vars[package]} srid={vars[srid]} extent={vars[extent]}').format(vars=vars_), GREEN))
        return BaseTemplate.post(self, command, output_dir, vars_)


class TemplateUpdate(BaseTemplate):
    _template_dir = 'update'
    summary = 'Template used to update a c2cgeoportal project'

    def pre(self, command, output_dir, vars_):
        """
        Overrides the base template
        """
        if os.path.exists('project.yaml'):
            with open('project.yaml', 'r') as (f):
                project = yaml.safe_load(f)
                if 'template_vars' in project:
                    for key, value in project['template_vars'].items():
                        vars_[key] = value.encode('utf-8') if isinstance(value, string_types) else value

        return BaseTemplate.pre(self, command, output_dir, vars_)

    def post(self, command, output_dir, vars_):
        """
        Overrides the base template class to print "Welcome to c2cgeoportal!"
        after a successful scaffolding rendering.
        """
        if os.name == 'posix':
            dest = os.path.join(output_dir, '.whiskey/action_hooks/pre-build.mako')
            subprocess.check_call(['chmod', '+x', dest])
        self.out(colorize('\nWelcome to c2cgeoportal!', GREEN))
        return BaseTemplate.post(self, command, output_dir, vars_)