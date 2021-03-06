# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylons_sandbox/egg.py
# Compiled at: 2007-09-30 10:37:19
from zc.buildout.easy_install import *
from zc.buildout.easy_install import _script
from zc.recipe.egg.egg import *
import logging, os, re, zipfile
py_script_template = '#!%(python)s\nimport sys, os\n    \nsys.path[0:0] = [\n  %(path)s,\n  os.getcwd(),\n  ]\n\n_interactive = True\nif len(sys.argv) > 1:\n    import getopt\n    _options, _args = getopt.getopt(sys.argv[1:], \'ic:\')\n    _interactive = False\n    for (_opt, _val) in _options:\n        if _opt == \'-i\':\n            _interactive = True\n        elif _opt == \'-c\':\n            exec _val\n            \n    if _args:\n        sys.argv[:] = _args\n        execfile(sys.argv[0])\n\nif _interactive:\n    import code\n    code.interact(banner="", local=globals())\n'

def _pyscript(path, dest, executable, launcher):
    generated = []
    script = dest
    if sys.platform == 'win32':
        script += '-script'
    if launcher:
        dest += '.buildout'
    contents = py_script_template % dict(python=executable, path=path)
    changed = not (os.path.exists(dest) and open(dest).read() == contents)
    if sys.platform == 'win32':
        exe = script + '.exe'
        open(exe, 'wb').write(pkg_resources.resource_string('setuptools', 'cli.exe'))
        generated.append(exe)
    elif launcher:
        exe = script
        open(exe, 'wb').write(open(launcher, 'rb').read())
        generated.append(exe)
        try:
            os.chmod(exe, 493)
        except (AttributeError, os.error):
            pass
        else:
            logger.info('Generated launcher %r.', exe)
    if changed:
        open(dest, 'w').write(contents)
        try:
            os.chmod(dest, 493)
        except (AttributeError, os.error):
            pass
        else:
            logger.info('Generated interpreter %r.', script)
    generated.append(dest)
    return generated


def scripts__(reqs, working_set, executable, dest, scripts=None, extra_paths=(), arguments='', interpreter=None, initialization='', launcher=None, dependent_scripts=False):
    path = [ dist.location for dist in working_set ]
    path.extend(extra_paths)
    path = repr(path)[1:-1].replace(', ', ',\n  ')
    generated = []
    if isinstance(reqs, str):
        raise TypeError('Expected iterable of requirements or entry points, got string.')
    if initialization:
        initialization = '\n' + initialization + '\n'
    entry_points = []
    if dependent_scripts:
        requirements = [ x[1][0] for x in working_set.entry_keys.items() ]
    else:
        requirements = []
    for req in reqs:
        if req not in requirements:
            requirements.append(req)

    for req in requirements:
        if isinstance(req, str):
            req = pkg_resources.Requirement.parse(req)
            dist = working_set.find(req)
            for name in pkg_resources.get_entry_map(dist, 'console_scripts'):
                entry_point = dist.get_entry_info('console_scripts', name)
                entry_points.append((name, entry_point.module_name, ('.').join(entry_point.attrs)))

        else:
            entry_points.append(req)

    for (name, module_name, attrs) in entry_points:
        if name.startswith('easy_install'):
            continue
        if scripts is not None:
            sname = scripts.get(name)
            if sname is None:
                continue
        else:
            sname = name
        sname = os.path.join(dest, sname)
        generated.extend(_script(module_name, attrs, path, sname, executable, arguments, initialization))

    if interpreter:
        sname = os.path.join(dest, interpreter)
        generated.extend(_pyscript(path, sname, executable, launcher))
    return generated


class Scripts(Eggs):
    __module__ = __name__

    def __init__(self, buildout, name, options):
        super(Scripts, self).__init__(buildout, name, options)
        options['bin-directory'] = buildout['buildout']['bin-directory']
        options['_b'] = options['bin-directory']
        self.extra_paths = [ os.path.join(buildout['buildout']['directory'], p.strip()) for p in options.get('extra-paths', '').split('\n') if p.strip() ]
        if self.extra_paths:
            options['extra-paths'] = ('\n').join(self.extra_paths)

    parse_entry_point = re.compile('([^=]+)=(\\w+(?:[.]\\w+)*):(\\w+(?:[.]\\w+)*)$').match

    def install(self):
        (reqs, ws) = self.working_set()
        options = self.options
        scripts = options.get('scripts')
        if scripts or scripts is None:
            if scripts is not None:
                scripts = scripts.split()
                scripts = dict([ '=' in s and s.split('=', 1) or (s, s) for s in scripts ])
            for s in options.get('entry-points', '').split():
                parsed = self.parse_entry_point(s)
                if not parsed:
                    logging.getLogger(self.name).error('Cannot parse the entry point %s.', s)
                    raise zc.buildout.UserError('Invalid entry point')
                reqs.append(parsed.groups())

            def asbool(value):
                value = str(value)
                if value.strip().lower() in ['1', 'true']:
                    return True
                elif value.strip().lower() in ['0', 'false']:
                    return False
                else:
                    raise Exception('Unrecognised option %s for bool' % val)

            return scripts__(reqs, ws, options['executable'], options['bin-directory'], scripts=scripts, extra_paths=self.extra_paths, interpreter=options.get('interpreter'), initialization=options.get('initialization', ''), arguments=options.get('arguments', ''), launcher=options.get('launcher', None), dependent_scripts=asbool(options.get('dependent_scripts', False)))
        return ()

    update = install


Egg = Scripts