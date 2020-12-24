# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breilly/git/fm-orchestrator/module_build_service/mmd_resolver.py
# Compiled at: 2019-12-13 10:33:05
import collections, itertools, solv
from module_build_service import log, conf
from module_build_service.models import ModuleBuild

class MMDResolver(object):
    """
    Resolves dependencies between Module metadata objects.
    """

    def module_dep(self, name, stream=None, version=None, version_op=None):
        """Create a libsolv Dependency

        Dependency could be in following forms:

        module(name)
        module(name:stream)
        module(name:stream) op version

        :param str name: module name.
        :param str stream: optional module stream. If specified, dependency
            will be the 2nd form above.
        :param str version: optional module version.
        :param version_op: optional libsolv relational flag constant. If
            specified, dependency will be the 3rd form above. Defaults to
            ``solv.REL_EQ``.
        :return: a libsolv Dependency object
        """
        if name and stream:
            dep = self.pool.Dep(('module({}:{})').format(name, stream))
        else:
            dep = self.pool.Dep(('module({})').format(name))
        if version:
            dep = dep.Rel(version_op or solv.REL_EQ, self.pool.Dep(version))
        return dep

    def solvable_provides(self, solvable, name, stream=None, version=None, version_op=None):
        """Add a Provides: dependency to a solvable

        This is parallel to RPM-world ``Provides: perl(foo)`` or ``Requires: perl(foo)``.

        Please refer to :meth:`module_dep` for detailed information of
        arguments name, stream, version and version_op.

        :param solvable: a solvable object the Provides dependency will be
            added to.
        """
        dep = self.module_dep(name, stream, version, version_op)
        solvable.add_deparray(solv.SOLVABLE_PROVIDES, dep)

    def __init__(self):
        self.pool = solv.Pool()
        self.pool.setarch('x86_64')
        self.build_repo = self.pool.add_repo('build')
        self.available_repo = self.pool.add_repo('available')
        self.solvables = {}

    def _deps2reqs(self, deps, base_module_stream_overrides=None, exact_versions=True):
        """
        Helper method converting dependencies from MMD to solv.Dep instance expressing
        the dependencies in a way libsolv accepts as input.

        So for example for following input:
            deps = [{'gtk': ['1'], 'foo': ['1']}]
        The resulting solv.Dep expression will be:
            ((module(gtk) with module(gtk:1)) and (module(foo) with module(foo:1)))

        Base modules are handled in a special way in case when the stream of base module
        contains version in the "x.y.z" format. For example "el8.0.0" or "el7.6.0".
        In this case, the resulting solv.Dep expression for such base module will contain version
        string computed using ModuleBuild.get_stream_version() method:
        For example:
            module(platform) with module(platform:el8) = 080200

        The stream used to compute the version can be also overridden using the
        `base_module_stream_overrides` dict which has base module name as a key and
        the stream which will be used to compute the version as a value.
        This is needed for cases when module requires just "platform:el8", but was
        in fact built against particular platform stream, for example platform:el8.1.0.
        In this case, such module should still require platform:el8, but in particular
        version which is passed to this method using the `base_module_stream_overrides`.

        When `exact_versions` is set to False, the base module dependency will contain
        ">=" operator instead of "=".

        The "with" syntax is here to allow depending on "module(gtk)" meaning "any gtk".
        This can happen in case {'gtk': []} is used as an input.

        See the inline comments for more information.

        :param list deps: List of dicts with dependency name as key and list of
            streams as value.
        :param dict base_module_stream_overrides: The key is base module name, value
            is the stream string which will be used to compute `version` part of the
            base module solv.Dep expression.
        :param bool exact_versions: When set to False, the base module dependency
            will contain ">=" operator instead of "=".
        :rtype: solv.Dep
        :return: solv.Dep instance with dependencies in form libsolv accepts.
        """
        rel_or_dep = lambda dep, op, rel: dep.Rel(op, rel) if dep is not None else rel
        reqs = None
        for dep_dicts in deps:
            require = None
            for name, streams in dep_dicts.items():
                is_base_module = name in conf.base_module_names
                req_pos = None
                for stream in streams:
                    if is_base_module:
                        if base_module_stream_overrides and name in base_module_stream_overrides:
                            stream_for_version = base_module_stream_overrides[name]
                        else:
                            stream_for_version = stream
                        stream_version_str = str(ModuleBuild.get_stream_version(stream_for_version, right_pad=False))
                        if len(stream_version_str) < 5:
                            req_pos = rel_or_dep(req_pos, solv.REL_OR, self.module_dep(name, stream))
                        else:
                            op = solv.REL_EQ
                            if not exact_versions:
                                op |= solv.REL_GT
                            version = ModuleBuild.get_stream_version(stream_for_version, right_pad=False)
                            req_pos = rel_or_dep(req_pos, solv.REL_OR, self.module_dep(name, stream, str(version), op))
                    else:
                        req_pos = rel_or_dep(req_pos, solv.REL_OR, self.module_dep(name, stream))

                req = self.module_dep(name)
                if req_pos is not None:
                    req = req.Rel(solv.REL_WITH, req_pos)
                require = rel_or_dep(require, solv.REL_AND, req)

            reqs = rel_or_dep(reqs, solv.REL_OR, require)

        return reqs

    def _add_base_module_provides(self, solvable, mmd):
        """
        Adds the "stream version" and the "virtual_streams" from XMD section of `mmd` to `solvable`.

        Base modules like "platform" can contain virtual streams which need to be considered
        when resolving dependencies. For example module "platform:el8.1.0" can provide virtual
        stream "el8". In this case the solvable will have following additional Provides:

        - module(platform:el8.1.0) = 80100 - Modules can require specific platform stream.
        - module(platform:el8) = 80100 - Module can also require just platform:el8.
        """
        if mmd.get_module_name() not in conf.base_module_names:
            return
        stream_version = ModuleBuild.get_stream_version(mmd.get_stream_name(), right_pad=False)
        if stream_version:
            self.solvable_provides(solvable, mmd.get_module_name(), mmd.get_stream_name(), str(stream_version))
        xmd = mmd.get_xmd()
        if not xmd.get('mbs', {}).get('virtual_streams'):
            return
        version = stream_version or mmd.get_version()
        for stream in xmd['mbs']['virtual_streams']:
            self.solvable_provides(solvable, mmd.get_module_name(), stream, str(version))

    def _get_base_module_stream_overrides(self, mmd):
        """
        Checks the xmd["mbs"]["buildrequires"] and returns the dict containing
        base module name as a key and stream of base module against which this
        module was built. This is later used to override base module streams
        in the _deps2reqs method.

        :param Modulemd mmd: Metadata of module for which the stream overrides are returned.
        :rtype: dict
        :return: Dict with module name as a key and new stream as a value.
        """
        overrides = {}
        xmd = mmd.get_xmd()
        if 'buildrequires' in xmd.get('mbs', {}):
            for base_module_name in conf.base_module_names:
                if base_module_name not in xmd['mbs']['buildrequires']:
                    continue
                if 'stream' not in xmd['mbs']['buildrequires'][base_module_name]:
                    continue
                stream = xmd['mbs']['buildrequires'][base_module_name]['stream']
                overrides[base_module_name] = stream

        return overrides

    def add_modules(self, mmd):
        """
        Adds module represented by `mmd` metadata to MMDResolver. Modules added by this
        method will be considered as possible dependencies while resolving the dependencies
        using the `solve(...)` method only if their "context" is None. Otherwise they are
        treated like input modules we want to resolve dependencies for.

        :param Modulemd mmd: Metadata of module to add.
        :rtype: list
        :return: list of solv.Solvable instances representing the module in libsolv world.
        """
        n, s, v, c = (
         mmd.get_module_name(), mmd.get_stream_name(), mmd.get_version(), mmd.get_context())
        stream_version = ModuleBuild.get_stream_version(s, right_pad=False)
        normdeps = lambda mmd, dep_type: [ {name:getattr(dep, ('get_{}_streams').format(dep_type))(name) for name in getattr(dep, ('get_{}_modules').format(dep_type))()}
         for dep in mmd.get_dependencies()
        ]
        solvables = []
        if c is not None:
            solvable = self.available_repo.add_solvable()
            solvable.name = '%s:%s:%d:%s' % (n, s, v, c)
            solvable.evr = str(v)
            solvable.arch = 'x86_64'
            self.solvable_provides(solvable, n)
            if not stream_version:
                self.solvable_provides(solvable, n, s, str(v))
            self._add_base_module_provides(solvable, mmd)
            base_module_stream_overrides = self._get_base_module_stream_overrides(mmd)
            requires = self._deps2reqs(normdeps(mmd, 'runtime'), base_module_stream_overrides, False)
            log.debug('Adding module %s with requires: %r', solvable.name, requires)
            solvable.add_deparray(solv.SOLVABLE_REQUIRES, requires)
            solvable.add_deparray(solv.SOLVABLE_CONFLICTS, self.module_dep(n))
            solvables.append(solvable)
            ns = (':').join([n, s])
            if ns not in self.solvables:
                self.solvables[ns] = []
            self.solvables[ns].append(solvable)
        else:
            normalized_deps = normdeps(mmd, 'buildtime')
            for c, deps in enumerate(mmd.get_dependencies()):
                solvable = self.build_repo.add_solvable()
                solvable.name = '%s:%s:%d:%d' % (n, s, v, c)
                solvable.evr = str(v)
                solvable.arch = 'src'
                requires = self._deps2reqs([normalized_deps[c]])
                log.debug('Adding module %s with requires: %r', solvable.name, requires)
                solvable.add_deparray(solv.SOLVABLE_REQUIRES, requires)
                solvables.append(solvable)
                ns = (':').join([n, s])
                if ns not in self.solvables:
                    self.solvables[ns] = []
                self.solvables[ns].append(solvable)

        return solvables

    def solve(self, mmd):
        """
        Solves dependencies of module defined by `mmd` object. Returns set
        containing frozensets with all the possible combinations which
        satisfied dependencies.

        ``solve`` uses a policy called "First" to resolve the dependencies.
        That is, only single combination of buildrequires will be returned with
        "gtk:1" and "platform:f28", because the input buildrequires section did
        not mention any platform stream and therefore "first one" is used.

        :param mmd: Input modulemd which should have the `context` set to None.
        :type mmd: Modulemd.ModuleStream
        :return: set of frozensets of n:s:v:c of modules which satisfied the
            dependency solving.
        """
        solvables = self.add_modules(mmd)
        if not solvables:
            raise ValueError('No module(s) found for resolving')
        self.pool.createwhatprovides()
        s2nsvca = lambda s: '%s:%s' % (s.name, s.arch)
        s2ns = lambda s: (':').join(s.name.split(':', 2)[:2])
        for ns, unordered_solvables in self.solvables.items():
            unordered_solvables.sort(key=lambda s: int(s.name.split(':')[2]), reverse=True)

        solver = self.pool.Solver()
        alternatives = collections.OrderedDict()
        for src in solvables:
            job = self.pool.Job(solv.Job.SOLVER_INSTALL | solv.Job.SOLVER_SOLVABLE, src.id)
            requires = src.lookup_deparray(solv.SOLVABLE_REQUIRES)
            if len(requires) > 1:
                raise SystemError('At max one element should be in Requires: %s' % requires)
            elif len(requires) == 0:
                return {
                 frozenset([s2nsvca(src)])}
            requires = requires[0]
            src_alternatives = alternatives[src] = collections.OrderedDict()
            if src.arch != 'src':
                raise NotImplementedError
            deps = str(requires).split(' and ')
            if len(deps) > 1:
                deps[0] = deps[0][1:]
                deps[-1] = deps[(-1)][:-1]
            deps = [ self.pool.parserpmrichdep(dep) if dep.startswith('(') else self.pool.Dep(dep) for dep in deps
                   ]
            for opt in itertools.product(*[ self.pool.whatprovides(dep) for dep in deps ]):
                log.debug('Testing %s with combination: %s', src, opt)
                key = tuple(s2ns(s) for s in opt)
                jobs = [ self.pool.Job(solv.Job.SOLVER_FAVOR | solv.Job.SOLVER_SOLVABLE, s.id) for s in opt
                       ] + [
                 job]
                log.debug('Jobs:')
                for j in jobs:
                    log.debug('  - %s', j)

                problems = solver.solve(jobs)
                if problems:
                    problem_str = self._detect_transitive_stream_collision(problems)
                    if problem_str:
                        err_msg = problem_str
                    else:
                        err_msg = (', ').join(str(p) for p in problems)
                    raise RuntimeError(('Problems were found during module dependency resolution: {}').format(err_msg))
                newsolvables = solver.transaction().newsolvables()
                log.debug('Transaction:')
                for s in newsolvables:
                    log.debug('  - %s', s)

                all_solvables_found = True
                for s in opt:
                    if s not in newsolvables:
                        all_solvables_found = False
                        break

                if all_solvables_found:
                    alternative = src_alternatives.setdefault(key, [])
                    alternative.append(newsolvables)
                else:
                    log.debug('  - ^ Not all favored solvables found in the result, skipping.')

        for transactions in alternatives.values():
            for ns, trans in transactions.items():
                sorted_trans = []
                for i, t in enumerate(trans):
                    idx = []
                    for s in t:
                        name_stream = s2ns(s)
                        if name_stream not in self.solvables:
                            continue
                        index = self.solvables[name_stream].index(s)
                        idx.append(index)

                    sorted_trans.append([i, idx])

                sorted_trans.sort(key=lambda i: sum(i[1]))
                if sorted_trans:
                    transactions[ns] = [
                     trans[sorted_trans[0][0]]]

        return set(frozenset(s2nsvca(s) for s in transactions[0]) for src_alternatives in alternatives.values() for transactions in src_alternatives.values())

    @staticmethod
    def _detect_transitive_stream_collision(problems):
        """Return problem description if transitive stream collision happens

        Transitive stream collision could happen if different buildrequired
        modules requires same module but with different streams. For example,

        app:1 --br--> gtk:1 --req--> baz:1* -------- req --------> platform:f29
             |                                                     ^
             +--br--> foo:1 --req--> bar:1 --req--> baz:2* --req---|

        as a result, ``baz:1`` will conflicts with ``baz:2``.

        :param problems: list of problems returned from ``solv.Solver.solve``.
        :return: a string of problem description if transitive stream collision
            is detected. The description is provided by libsolv without
            changed. If no such collision, None is returned.
        :rtype: str or None
        """

        def find_conflicts_pairs():
            for problem in problems:
                for rule in problem.findallproblemrules():
                    info = rule.info()
                    if info.type == solv.Solver.SOLVER_RULE_PKG_CONFLICTS:
                        pair = [
                         info.solvable.name, info.othersolvable.name]
                        pair.sort()
                        yield pair

        formatted_conflicts_pairs = (', ').join(('{} and {}').format(*item) for item in find_conflicts_pairs())
        if formatted_conflicts_pairs:
            return ('The module has conflicting buildrequires of: {}').format(formatted_conflicts_pairs)