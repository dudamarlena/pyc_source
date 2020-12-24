# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/metadata_xml.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 16675 bytes
import os
from difflib import SequenceMatcher
from lxml import etree
from pkgcore import const as pkgcore_const
from pkgcore.ebuild.atom import MalformedAtom, atom
from snakeoil.osutils import pjoin
from snakeoil.strings import pluralism
from .. import base, results, sources
from . import Check

class _MissingXml(results.Error):
    __doc__ = 'Required XML file is missing.'

    def __init__(self, filename, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename

    @property
    def desc(self):
        return f"{self._attr} is missing {self.filename}"


class _BadlyFormedXml(results.Warning):
    __doc__ = "XML isn't well formed."

    def __init__(self, filename, error, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.error = error

    @property
    def desc(self):
        return f"{self._attr} {self.filename} is not well formed xml: {self.error}"


class _InvalidXml(results.Error):
    __doc__ = 'XML fails XML Schema validation.'

    def __init__(self, filename, message, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.message = message

    @property
    def desc(self):
        return f"{self._attr} {self.filename} violates metadata.xsd:\n{self.message}"


class _MetadataXmlInvalidPkgRef(results.Error):
    __doc__ = 'metadata.xml <pkg/> references unknown/invalid package.'

    def __init__(self, filename, pkgtext, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.pkgtext = pkgtext

    @property
    def desc(self):
        return f"{self._attr} {self.filename} <pkg/> references unknown/invalid package: {self.pkgtext!r}"


class _MetadataXmlInvalidCatRef(results.Error):
    __doc__ = 'metadata.xml <cat/> references unknown/invalid category.'

    def __init__(self, filename, cattext, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.cattext = cattext

    @property
    def desc(self):
        return f"{self._attr} {self.filename} <cat/> references unknown/invalid category: {self.cattext!r}"


class EmptyMaintainer(results.PackageResult, results.Warning):
    __doc__ = 'Package with neither a maintainer or maintainer-needed comment in metadata.xml.'

    def __init__(self, filename, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename

    @property
    def desc(self):
        return 'no package maintainer or maintainer-needed comment specified'


class MaintainerWithoutProxy(results.PackageResult, results.Warning):
    __doc__ = "Package has a proxied maintainer without a proxy.\n\n    All package maintainers have non-@gentoo.org e-mail addresses. Most likely,\n    this means that the package is maintained by a proxied maintainer but there\n    is no explicit proxy (developer or project) listed. This means no Gentoo\n    developer will be CC-ed on bug reports, and most likely no developer\n    oversees the proxied maintainer's activity.\n    "

    def __init__(self, filename, maintainers, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.maintainers = tuple(maintainers)

    @property
    def desc(self):
        s = pluralism(self.maintainers)
        maintainers = ', '.join(self.maintainers)
        return f"proxied maintainer{s} missing proxy dev/project: {maintainers}"


class StaleProxyMaintProject(results.PackageResult, results.Warning):
    __doc__ = 'Package lists proxy-maint project but has no proxied maintainers.\n\n    The package explicitly lists proxy-maint@g.o as the only maintainer.\n    Most likely, this means that the proxied maintainer has been removed\n    but proxy-maint was left over.\n    '

    def __init__(self, filename, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename

    @property
    def desc(self):
        return 'proxy-maint maintainer with no proxies'


class NonexistentProjectMaintainer(results.PackageResult, results.Warning):
    __doc__ = 'Package specifying nonexistent project as a maintainer.'

    def __init__(self, filename, emails, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.emails = tuple(emails)

    @property
    def desc(self):
        s = pluralism(self.emails)
        emails = ', '.join(self.emails)
        return f"nonexistent project maintainer{s}: {emails}"


class WrongMaintainerType(results.PackageResult, results.Warning):
    __doc__ = 'A person-type maintainer matches an existing project.'

    def __init__(self, filename, emails, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.emails = tuple(emails)

    @property
    def desc(self):
        s = pluralism(self.emails)
        emails = ', '.join(self.emails)
        return f'project maintainer{s} with type="person": {emails}'


class PkgMissingMetadataXml(_MissingXml, results.PackageResult):
    __doc__ = 'Package is missing metadata.xml.'


class CatMissingMetadataXml(_MissingXml, results.CategoryResult):
    __doc__ = 'Category is missing metadata.xml.'


class PkgInvalidXml(_InvalidXml, results.PackageResult):
    __doc__ = 'Invalid package metadata.xml.'


class CatInvalidXml(_InvalidXml, results.CategoryResult):
    __doc__ = 'Invalid category metadata.xml.'


class PkgBadlyFormedXml(_BadlyFormedXml, results.PackageResult):
    __doc__ = 'Badly formed package metadata.xml.'


class CatBadlyFormedXml(_BadlyFormedXml, results.CategoryResult):
    __doc__ = 'Badly formed category metadata.xml.'


class PkgMetadataXmlInvalidPkgRef(_MetadataXmlInvalidPkgRef, results.PackageResult):
    __doc__ = 'Invalid package reference in package metadata.xml.'


class CatMetadataXmlInvalidPkgRef(_MetadataXmlInvalidPkgRef, results.CategoryResult):
    __doc__ = 'Invalid package reference in category metadata.xml.'


class PkgMetadataXmlInvalidCatRef(_MetadataXmlInvalidCatRef, results.PackageResult):
    __doc__ = 'Invalid category reference in package metadata.xml.'


class CatMetadataXmlInvalidCatRef(_MetadataXmlInvalidCatRef, results.CategoryResult):
    __doc__ = 'Invalid category reference in category metadata.xml.'


class _MetadataXmlIndentation(results.Warning):
    __doc__ = 'Inconsistent indentation in metadata.xml file.\n\n    Either all tabs or all spaces should be used, not a mixture of both.\n    '

    def __init__(self, filename, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.lines = tuple(lines)

    @property
    def desc(self):
        s = pluralism(self.lines)
        lines = ', '.join(self.lines)
        return f"metadata.xml has inconsistent indentation on line{s}: {lines}"


class CatMetadataXmlIndentation(_MetadataXmlIndentation, results.CategoryResult):
    __doc__ = 'Inconsistent indentation in category metadata.xml file.\n\n    Either all tabs or all spaces should be used, not a mixture of both.\n    '


class PkgMetadataXmlIndentation(_MetadataXmlIndentation, results.PackageResult):
    __doc__ = 'Inconsistent indentation in package metadata.xml file.\n\n    Either all tabs or all spaces should be used, not a mixture of both.\n    '


class _MetadataXmlEmptyElement(results.Warning):
    __doc__ = 'Empty element in metadata.xml file.'

    def __init__(self, filename, element, line, **kwargs):
        (super().__init__)(**kwargs)
        self.filename = filename
        self.element = element
        self.line = line

    @property
    def desc(self):
        return f"metadata.xml has empty element {self.element!r} on line {self.line}"


class CatMetadataXmlEmptyElement(_MetadataXmlEmptyElement, results.CategoryResult):
    __doc__ = 'Empty element in category metadata.xml file.'


class PkgMetadataXmlEmptyElement(_MetadataXmlEmptyElement, results.PackageResult):
    __doc__ = 'Empty element in package metadata.xml file.'


class RedundantLongDescription(results.PackageResult, results.Warning):
    __doc__ = "Package's longdescription element in metadata.xml and DESCRIPTION are interchangeable.\n\n    The longdescription element is for providing extended information that\n    doesn't fit in DESCRIPTION.\n    "

    def __init__(self, msg, **kwargs):
        (super().__init__)(**kwargs)
        self.msg = msg

    @property
    def desc(self):
        return self.msg


class _XmlBaseCheck(Check):
    __doc__ = 'Base class for metadata.xml scans.'
    schema = None
    misformed_error = None
    invalid_error = None
    missing_error = None

    def __init__(self, *args):
        (super().__init__)(*args)
        self.repo_base = self.options.target_repo.location
        self.pkgref_cache = {}
        self._checks = tuple(getattr(self, x) for x in dir(self) if x.startswith('_check_'))
        metadata_xsd = pjoin(self.repo_base, 'metadata', 'xml-schema', 'metadata.xsd')
        if not os.path.isfile(metadata_xsd):
            metadata_xsd = pjoin(pkgcore_const.DATA_PATH, 'xml-schema', 'metadata.xsd')
        self.schema = etree.XMLSchema(etree.parse(metadata_xsd))

    def _check_doc(self, pkg, loc, doc):
        """Perform additional document structure checks."""
        for el in doc.getroot().iterdescendants():
            if not el.getchildren() and (el.text is None or not el.text.strip()) and not el.tag == 'stabilize-allarches':
                yield self.empty_element(loc, (el.tag), (el.sourceline), pkg=pkg)

        for el in doc.findall('.//cat'):
            c = el.text.strip()
            if c not in self.options.search_repo.categories:
                yield self.catref_error((os.path.basename(loc)), c, pkg=pkg)

        for el in doc.findall('.//pkg'):
            p = el.text.strip()
            if p not in self.pkgref_cache:
                try:
                    a = atom(p)
                    found = self.options.search_repo.has_match(a)
                except MalformedAtom:
                    found = False

                self.pkgref_cache[p] = found
            if not self.pkgref_cache[p]:
                yield self.pkgref_error((os.path.basename(loc)), p, pkg=pkg)

    def _check_whitespace(self, pkg, loc, doc):
        """Check for indentation consistency."""
        orig_indent = None
        indents = set()
        with open(loc) as (f):
            for lineno, line in enumerate(f, 1):
                for i in line[:-len(line.lstrip())]:
                    if i != orig_indent:
                        if orig_indent is None:
                            orig_indent = i
                        else:
                            indents.add(lineno)

        if indents:
            yield self.indent_error(loc, (map(str, sorted(indents))), pkg=pkg)

    @staticmethod
    def _format_lxml_errors(error_log):
        for l in error_log:
            yield f"line {l.line}, col {l.column}: ({l.type_name}) {l.message}"

    def _parse_xml(self, pkg, loc):
        try:
            doc = etree.parse(loc)
        except (IOError, OSError):
            if self.options.gentoo_repo:
                yield self.missing_error((os.path.basename(loc)), pkg=pkg)
            return
        except etree.XMLSyntaxError as e:
            yield self.misformed_error((os.path.basename(loc)), (str(e)), pkg=pkg)
            return

        if self.schema is not None:
            if not self.schema.validate(doc):
                message = '\n'.join(self._format_lxml_errors(self.schema.error_log))
                yield self.invalid_error((os.path.basename(loc)), message, pkg=pkg)
                return
        for check in self._checks:
            yield from check(pkg, loc, doc)

    def feed(self, pkgs):
        if not pkgs:
            return
        pkg = pkgs[(-1)]
        loc = self._get_xml_location(pkg)
        yield from self._parse_xml(pkg, loc)
        if False:
            yield None


class PackageMetadataXmlCheck(_XmlBaseCheck):
    __doc__ = 'Package level metadata.xml scans.'
    scope = base.package_scope
    _source = sources.PackageRepoSource
    misformed_error = PkgBadlyFormedXml
    invalid_error = PkgInvalidXml
    missing_error = PkgMissingMetadataXml
    catref_error = PkgMetadataXmlInvalidCatRef
    pkgref_error = PkgMetadataXmlInvalidPkgRef
    indent_error = PkgMetadataXmlIndentation
    empty_element = PkgMetadataXmlEmptyElement
    known_results = frozenset([
     PkgBadlyFormedXml, PkgInvalidXml, PkgMissingMetadataXml,
     PkgMetadataXmlInvalidPkgRef, PkgMetadataXmlInvalidCatRef,
     PkgMetadataXmlIndentation, PkgMetadataXmlEmptyElement, EmptyMaintainer,
     MaintainerWithoutProxy, StaleProxyMaintProject, RedundantLongDescription,
     NonexistentProjectMaintainer, WrongMaintainerType])

    def _check_maintainers(self, pkg, loc, doc):
        """Validate maintainers in package metadata for the gentoo repo."""
        if self.options.gentoo_repo:
            if pkg.maintainers:
                maintainers = any(m.email.endswith('@gentoo.org') for m in pkg.maintainers) or sorted(map(str, pkg.maintainers))
                yield MaintainerWithoutProxy((os.path.basename(loc)),
                  maintainers, pkg=pkg)
            elif len(pkg.maintainers) == 1:
                if any(m.email == 'proxy-maint@gentoo.org' for m in pkg.maintainers):
                    yield StaleProxyMaintProject((os.path.basename(loc)), pkg=pkg)
        elif not any(c.text.strip() == 'maintainer-needed' for c in doc.xpath('//comment()')):
            yield EmptyMaintainer((os.path.basename(loc)), pkg=pkg)
        projects = frozenset(pkg.repo.projects_xml.projects)
        if projects:
            nonexistent = []
            wrong_maintainers = []
            for m in pkg.maintainers:
                if m.maint_type == 'project' and m.email not in projects:
                    nonexistent.append(m.email)
                else:
                    if m.maint_type == 'person' and m.email in projects:
                        wrong_maintainers.append(m.email)

            if nonexistent:
                yield NonexistentProjectMaintainer((os.path.basename(loc)),
                  (sorted(nonexistent)), pkg=pkg)
            if wrong_maintainers:
                yield WrongMaintainerType((os.path.basename(loc)),
                  (sorted(wrong_maintainers)), pkg=pkg)

    def _check_longdescription(self, pkg, loc, doc):
        if pkg.longdescription is not None:
            match_ratio = SequenceMatcher(None, pkg.description, pkg.longdescription).ratio()
            if match_ratio > 0.75:
                msg = 'metadata.xml longdescription closely matches DESCRIPTION'
                yield RedundantLongDescription(msg, pkg=pkg)
            elif len(pkg.longdescription) < 100:
                msg = 'metadata.xml longdescription is too short'
                yield RedundantLongDescription(msg, pkg=pkg)

    def _get_xml_location(self, pkg):
        """Return the metadata.xml location for a given package."""
        return pjoin(os.path.dirname(pkg.ebuild.path), 'metadata.xml')


class CategoryMetadataXmlCheck(_XmlBaseCheck):
    __doc__ = 'Category level metadata.xml scans.'
    scope = base.category_scope
    _source = (sources.CategoryRepoSource, (), (('source', sources.RawRepoSource),))
    misformed_error = CatBadlyFormedXml
    invalid_error = CatInvalidXml
    missing_error = CatMissingMetadataXml
    catref_error = CatMetadataXmlInvalidCatRef
    pkgref_error = CatMetadataXmlInvalidPkgRef
    indent_error = CatMetadataXmlIndentation
    empty_element = CatMetadataXmlEmptyElement
    known_results = frozenset([
     CatBadlyFormedXml, CatInvalidXml, CatMissingMetadataXml,
     CatMetadataXmlInvalidPkgRef, CatMetadataXmlInvalidCatRef,
     CatMetadataXmlIndentation, CatMetadataXmlEmptyElement])

    def _get_xml_location(self, pkg):
        """Return the metadata.xml location for a given package's category."""
        return pjoin(self.repo_base, pkg.category, 'metadata.xml')