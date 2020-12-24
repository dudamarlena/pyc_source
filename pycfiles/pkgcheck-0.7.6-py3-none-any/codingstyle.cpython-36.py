# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/codingstyle.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 18931 bytes
"""Various line-based checks."""
import re
from collections import defaultdict
from pkgcore.ebuild.eapi import EAPI
from snakeoil.klass import jit_attr
from snakeoil.mappings import ImmutableDict
from snakeoil.sequences import stable_unique
from snakeoil.strings import pluralism
from .. import results, sources
from . import Check
PREFIX_VARIABLES = ('EROOT', 'ED', 'EPREFIX')
PATH_VARIABLES = ('BROOT', 'ROOT', 'D') + PREFIX_VARIABLES

class _CommandResult(results.LineResult):
    __doc__ = 'Generic command result.'

    def __init__(self, command, **kwargs):
        (super().__init__)(**kwargs)
        self.command = command

    @property
    def usage_desc(self):
        return (f"{self.command!r}")

    @property
    def desc(self):
        s = f"{self.usage_desc}, used on line {self.lineno}"
        if self.line != self.command:
            s += f": {self.line!r}"
        return s


class _EapiCommandResult(_CommandResult):
    __doc__ = 'Generic EAPI command result.'
    _status = None

    def __init__(self, *args, eapi, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.eapi = eapi

    @property
    def usage_desc(self):
        return f"{self.command!r} {self._status} in EAPI {self.eapi}"


class DeprecatedEapiCommand(_EapiCommandResult, results.Warning):
    __doc__ = 'Ebuild uses a deprecated EAPI command.'
    _status = 'deprecated'


class BannedEapiCommand(_EapiCommandResult, results.Error):
    __doc__ = 'Ebuild uses a banned EAPI command.'
    _status = 'banned'


class BadCommandsCheck(Check):
    __doc__ = 'Scan ebuild for various deprecated and banned command usage.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([DeprecatedEapiCommand, BannedEapiCommand])
    CMD_USAGE_REGEX = '^(\\s*|.*[|&{{(]+\\s*)\\b(?P<cmd>{})(?!\\.)\\b'

    def _cmds_regex(self, cmds):
        return re.compile(self.CMD_USAGE_REGEX.format('|'.join(cmds)))

    @jit_attr
    def regexes(self):
        d = {}
        for eapi_str, eapi in EAPI.known_eapis.items():
            regexes = []
            if eapi.bash_cmds_banned:
                regexes.append((
                 self._cmds_regex(eapi.bash_cmds_banned),
                 BannedEapiCommand,
                 {'eapi': eapi_str}))
            if eapi.bash_cmds_deprecated:
                regexes.append((
                 self._cmds_regex(eapi.bash_cmds_deprecated),
                 DeprecatedEapiCommand,
                 {'eapi': eapi_str}))
            d[eapi_str] = tuple(regexes)

        return ImmutableDict(d)

    def feed(self, pkg):
        regexes = self.regexes[str(pkg.eapi)]
        for lineno, line in enumerate(pkg.lines, 1):
            line = line.strip()
            if not line:
                continue
            if line[0] != '#':
                for regex, result_cls, kwargs in regexes:
                    match = regex.match(line)
                    if match is not None:
                        yield result_cls(match.group('cmd'), line=line, lineno=lineno, pkg=pkg, **kwargs)


class MissingSlash(results.VersionResult, results.Error):
    __doc__ = 'Ebuild uses a path variable missing a trailing slash.'

    def __init__(self, match, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.match = match
        self.lines = tuple(lines)

    @property
    def desc(self):
        s = pluralism(self.lines)
        lines = ', '.join(map(str, self.lines))
        return f"{self.match} missing trailing slash on line{s}: {lines}"


class UnnecessarySlashStrip(results.VersionResult, results.Warning):
    __doc__ = 'Ebuild uses a path variable that strips a nonexistent slash.'

    def __init__(self, match, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.match = match
        self.lines = tuple(lines)

    @property
    def desc(self):
        s = pluralism(self.lines)
        lines = ', '.join(map(str, self.lines))
        return f"{self.match} unnecessary slash strip on line{s}: {lines}"


class DoublePrefixInPath(results.VersionResult, results.Error):
    __doc__ = 'Ebuild uses two consecutive paths including EPREFIX.\n\n    Ebuild combines two path variables (or a variable and a getter), both\n    of which include EPREFIX, resulting in double prefixing. This is the case\n    when combining many pkg-config-based or alike getters with ED or EROOT.\n\n    For example, ``${ED}$(python_get_sitedir)`` should be replaced\n    with ``${D}$(python_get_sitedir)``.\n    '

    def __init__(self, match, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.match = match
        self.lines = tuple(lines)

    @property
    def desc(self):
        s = pluralism(self.lines)
        lines = ', '.join(map(str, self.lines))
        return f"{self.match}: concatenates two paths containing EPREFIX on line{s} {lines}"


class PathVariablesCheck(Check):
    __doc__ = 'Scan ebuild for path variables with various issues.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([MissingSlash, UnnecessarySlashStrip, DoublePrefixInPath])
    prefixed_dir_functions = ('insinto', 'exeinto', 'dodir', 'keepdir', 'fowners',
                              'fperms', 'java-pkg_jarinto', 'java-pkg_sointo', 'python_scriptinto',
                              'python_moduleinto')
    prefixed_getters = ('get_bashcompdir', 'get_bashhelpersdir', 'db_includedir', 'get_golibdir_gopath',
                        'get_llvm_prefix', 'python_get_sitedir', 'python_get_includedir',
                        'python_get_library_path', 'python_get_scriptdir', 'qt4_get_bindir',
                        'qt5_get_bindir', 's6_get_servicedir', 'systemd_get_systemunitdir',
                        'systemd_get_userunitdir', 'systemd_get_utildir', 'systemd_get_systemgeneratordir')
    prefixed_rhs_variables = ('EPREFIX', 'PYTHON', 'PYTHON_SITEDIR', 'PYTHON_INCLUDEDIR',
                              'PYTHON_LIBPATH', 'PYTHON_CONFIG', 'PYTHON_SCRIPTDIR')

    def __init__(self, *args):
        (super().__init__)(*args)
        self.missing_regex = re.compile('(\\${(%s)})"?\\w+/' % '|'.join(PATH_VARIABLES))
        self.unnecessary_regex = re.compile('(\\${(%s)%%/})' % '|'.join(PATH_VARIABLES))
        self.double_prefix_regex = re.compile('(\\${(%s)(%%/)?}/?\\$(\\((%s)\\)|{(%s)}))' % (
         '|'.join(PREFIX_VARIABLES),
         '|'.join(self.prefixed_getters),
         '|'.join(self.prefixed_rhs_variables)))
        self.double_prefix_func_regex = re.compile('\\b(%s)\\s[^&|;]*\\$(\\((%s)\\)|{(%s)})' % (
         '|'.join(self.prefixed_dir_functions),
         '|'.join(self.prefixed_getters),
         '|'.join(self.prefixed_rhs_variables)))
        self.double_prefix_func_false_positive_regex = re.compile('.*?[#]["]?\\$(\\((%s)\\)|{(%s)})' % (
         '|'.join(self.prefixed_getters),
         '|'.join(self.prefixed_rhs_variables)))

    def feed(self, pkg):
        missing = defaultdict(list)
        unnecessary = defaultdict(list)
        double_prefix = defaultdict(list)
        for lineno, line in enumerate(pkg.lines, 1):
            line = line.strip()
            if not line:
                continue
            if line[0] != '#':
                match = self.double_prefix_regex.search(line)
                if match is not None:
                    double_prefix[match.group(1)].append(lineno)
                match = self.double_prefix_func_regex.search(line)
                if match is not None:
                    if self.double_prefix_func_false_positive_regex.match(match.group(0)) is None:
                        double_prefix[match.group(0)].append(lineno)
                if pkg.eapi.options.trailing_slash:
                    pass
                else:
                    match = self.missing_regex.search(line)
                    if match is not None:
                        missing[match.group(1)].append(lineno)
                    match = self.unnecessary_regex.search(line)
                    if match is not None:
                        unnecessary[match.group(1)].append(lineno)

        for match, lines in missing.items():
            yield MissingSlash(match, lines, pkg=pkg)

        for match, lines in unnecessary.items():
            yield UnnecessarySlashStrip(match, lines, pkg=pkg)

        for match, lines in double_prefix.items():
            yield DoublePrefixInPath(match, lines, pkg=pkg)


class AbsoluteSymlink(results.LineResult, results.Warning):
    __doc__ = 'Ebuild uses dosym with absolute paths instead of relative.'

    def __init__(self, cmd, **kwargs):
        (super().__init__)(**kwargs)
        self.cmd = cmd

    @property
    def desc(self):
        return f"dosym called with absolute path on line {self.lineno}: {self.cmd}"


class AbsoluteSymlinkCheck(Check):
    __doc__ = 'Scan ebuild for dosym absolute path usage instead of relative.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([AbsoluteSymlink])
    DIRS = ('bin', 'etc', 'lib', 'opt', 'sbin', 'srv', 'usr', 'var')

    def __init__(self, *args):
        (super().__init__)(*args)
        dirs = '|'.join(self.DIRS)
        path_vars = '|'.join(PATH_VARIABLES)
        prefixed_regex = f'"\\${{({path_vars})(%/)?}}(?P<cp>")?(?(cp)\\S*|.*?")'
        non_prefixed_regex = f"""(?P<op>["\\\'])?/({dirs})(?(op).*?(?P=op)|\\S*)"""
        self.regex = re.compile(f"^\\s*(?P<cmd>dosym\\s+({prefixed_regex}|{non_prefixed_regex}))")

    def feed(self, pkg):
        for lineno, line in enumerate(pkg.lines, 1):
            if not line.strip():
                pass
            else:
                matches = self.regex.match(line)
                if matches is not None:
                    yield AbsoluteSymlink((matches.group('cmd')), line=line, lineno=lineno, pkg=pkg)


class DeprecatedInsinto(results.LineResult, results.Warning):
    __doc__ = 'Ebuild uses insinto where more compact commands exist.'

    def __init__(self, cmd, **kwargs):
        (super().__init__)(**kwargs)
        self.cmd = cmd

    @property
    def desc(self):
        return f"deprecated insinto usage (use {self.cmd} instead), line {self.lineno}: {self.line}"


class InsintoCheck(Check):
    __doc__ = 'Scan ebuild for deprecated insinto usage.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([DeprecatedInsinto])
    path_mapping = ImmutableDict({'/etc/conf.d':'doconfd or newconfd', 
     '/etc/env.d':'doenvd or newenvd', 
     '/etc/init.d':'doinitd or newinitd', 
     '/etc/pam.d':'dopamd or newpamd from pam.eclass', 
     '/usr/share/applications':'domenu or newmenu from desktop.eclass'})

    def __init__(self, *args):
        (super().__init__)(*args)
        paths = '|'.join(s.replace('/', '/+') + '/?' for s in self.path_mapping)
        self._insinto_re = re.compile(f"(?P<insinto>insinto[ \\t]+(?P<path>{paths})(?!/\\w+))(?:$|[/ \\t])")
        self._insinto_doc_re = re.compile('(?P<insinto>insinto[ \\t]+/usr/share/doc/(")?\\$\\{PF?\\}(?(2)\\2)(/\\w+)*)(?:$|[/ \\t])')

    def feed(self, pkg):
        for lineno, line in enumerate(pkg.lines, 1):
            if not line.strip():
                pass
            else:
                matches = self._insinto_re.search(line)
            if matches is not None:
                path = re.sub('//+', '/', matches.group('path'))
                cmd = self.path_mapping[path.rstrip('/')]
                yield DeprecatedInsinto(cmd,
                  line=(matches.group('insinto')), lineno=lineno, pkg=pkg)
            else:
                if pkg.eapi.options.dodoc_allow_recursive:
                    matches = self._insinto_doc_re.search(line)
                    if matches is not None:
                        yield DeprecatedInsinto('docinto/dodoc',
                          line=(matches.group('insinto')), lineno=lineno,
                          pkg=pkg)


class ObsoleteUri(results.VersionResult, results.Warning):
    __doc__ = 'URI used is obsolete.\n\n    The URI used to fetch distfile is obsolete and can be replaced\n    by something more modern. Note that the modern replacement usually\n    results in different file contents, so you need to rename it (to\n    avoid mirror collisions with the old file) and update the ebuild\n    (for example, by removing no longer necessary vcs-snapshot.eclass).\n    '

    def __init__(self, line, uri, replacement, **kwargs):
        (super().__init__)(**kwargs)
        self.line = line
        self.uri = uri
        self.replacement = replacement

    @property
    def desc(self):
        return f"obsolete fetch URI: {self.uri} on line {self.line}, should be replaced by: {self.replacement}"


class ObsoleteUriCheck(Check):
    __doc__ = 'Scan ebuild for obsolete URIs.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([ObsoleteUri])
    REGEXPS = (('.*\\b(?P<uri>(?P<prefix>https?://github\\.com/.*?/.*?/)(?:tar|zip)ball(?P<ref>\\S*))', '\\g<prefix>archive\\g<ref>.tar.gz'),
               ('.*\\b(?P<uri>(?P<prefix>https?://gitlab\\.com/.*?/(?P<pkg>.*?)/)repository/archive\\.(?P<format>tar|tar\\.gz|tar\\.bz2|zip)\\?ref=(?P<ref>\\S*))', '\\g<prefix>-/archive/\\g<ref>/\\g<pkg>-\\g<ref>.\\g<format>'))

    def __init__(self, *args):
        (super().__init__)(*args)
        self.regexes = []
        for regexp, repl in self.REGEXPS:
            self.regexes.append((re.compile(regexp), repl))

    def feed(self, pkg):
        for lineno, line in enumerate(pkg.lines, 1):
            if not not line.strip():
                if line.startswith('#'):
                    pass
                else:
                    for regexp, repl in self.regexes:
                        matches = regexp.match(line)
                        if matches is not None:
                            uri = matches.group('uri')
                            yield ObsoleteUri(lineno, uri, (regexp.sub(repl, uri)), pkg=pkg)


class HomepageInSrcUri(results.VersionResult, results.Warning):
    __doc__ = '${HOMEPAGE} is referenced in SRC_URI.\n\n    SRC_URI is built on top of ${HOMEPAGE}. This is discouraged since HOMEPAGE\n    is multi-valued by design, and is subject to potential changes that should\n    not accidentally affect SRC_URI.\n    '

    @property
    def desc(self):
        return '${HOMEPAGE} in SRC_URI'


class StaticSrcUri(results.VersionResult, results.Warning):
    __doc__ = 'SRC_URI contains static value instead of the dynamic equivalent.\n\n    For example, using static text to relate to the package version in SRC_URI\n    instead of ${P} or ${PV} where relevant.\n    '

    def __init__(self, static_str, **kwargs):
        (super().__init__)(**kwargs)
        self.static_str = static_str

    @property
    def desc(self):
        return f"{self.static_str!r} in SRC_URI"


class VariableInHomepage(results.VersionResult, results.Warning):
    __doc__ = 'HOMEPAGE includes a variable.\n\n    The HOMEPAGE ebuild variable entry in the devmanual [#]_ states only raw\n    text should be used.\n\n    .. [#] https://devmanual.gentoo.org/ebuild-writing/variables/#ebuild-defined-variables\n    '

    def __init__(self, variables, **kwargs):
        (super().__init__)(**kwargs)
        self.variables = tuple(variables)

    @property
    def desc(self):
        s = pluralism(self.variables)
        variables = ', '.join(self.variables)
        return f"HOMEPAGE includes variable{s}: {variables}"


class RawEbuildCheck(Check):
    __doc__ = 'Scan raw ebuild content for various issues.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([HomepageInSrcUri, StaticSrcUri, VariableInHomepage])

    def __init__(self, *args):
        (super().__init__)(*args)
        attr_vars = ('HOMEPAGE', 'SRC_URI')
        self.attr_regex = re.compile('|'.join(f'^\\s*(?P<{x.lower()}>{x}="[^"]*")' for x in attr_vars), re.MULTILINE)
        self.var_regex = re.compile('\\${[^}]+}')

    def check_homepage(self, pkg, s):
        matches = self.var_regex.findall(s)
        if matches:
            yield VariableInHomepage((stable_unique(matches)), pkg=pkg)

    def check_src_uri(self, pkg, s):
        if '${HOMEPAGE}' in s:
            yield HomepageInSrcUri(pkg=pkg)
        exts = pkg.eapi.archive_exts_regex_pattern
        P = re.escape(pkg.P)
        PV = re.escape(pkg.PV)
        static_src_uri_re = f'/(?P<static_str>({P}{exts}(?="|\\n)|{PV}(?=/)))'
        for match in re.finditer(static_src_uri_re, s):
            static_str = match.group('static_str')
            yield StaticSrcUri(static_str, pkg=pkg)

    def feed(self, pkg):
        for match in self.attr_regex.finditer(''.join(pkg.lines)):
            attr = match.lastgroup
            func = getattr(self, f"check_{attr}")
            yield from func(pkg, match.group(attr))

        if False:
            yield None


class RedundantDodir(results.LineResult, results.Warning):
    __doc__ = 'Ebuild using a redundant dodir call.'

    def __init__(self, cmd, **kwargs):
        (super().__init__)(**kwargs)
        self.cmd = cmd

    @property
    def desc(self):
        return f"dodir called before {self.cmd}, line {self.lineno}: {self.line}"


class RedundantDodirCheck(Check):
    __doc__ = 'Scan ebuild for redundant dodir usage.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([RedundantDodir])

    def __init__(self, *args):
        (super().__init__)(*args)
        cmds = '|'.join(('insinto', 'exeinto', 'docinto'))
        self.cmds_regex = re.compile(f"^\\s*(?P<cmd>({cmds}))\\s+(?P<path>\\S+)")
        self.dodir_regex = re.compile('^\\s*(?P<call>dodir\\s+(?P<path>\\S+))')

    def feed(self, pkg):
        lines = enumerate(pkg.lines, 1)
        for lineno, line in lines:
            line = line.strip()
            if not line or line[0] == '#':
                pass
            else:
                dodir = self.dodir_regex.match(line)
            if dodir:
                lineno, line = next(lines)
                cmd = self.cmds_regex.match(line)
                if cmd and dodir.group('path') == cmd.group('path'):
                    yield RedundantDodir((cmd.group('cmd')),
                      line=(dodir.group('call')), lineno=(lineno - 1),
                      pkg=pkg)