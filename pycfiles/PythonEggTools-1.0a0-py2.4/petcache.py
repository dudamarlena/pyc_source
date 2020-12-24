# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pet/petcache.py
# Compiled at: 2006-12-22 07:59:52
"""
This module provides an interface to the pet-cache script.
"""
import sys, optparse, pkg_resources, email, fillparagraph, operator
__all__ = [
 'show', 'showpkg', 'pkgnames', 'main']

def showpkg(args):
    return _showcmd(args, print_showpkg_info)


def show(args):
    return _showcmd(args, print_show_info)


def _showcmd(args, printfunc):
    packages = []
    errs = []
    for pkgname in args:
        try:
            packages.append(pkg_resources.get_distribution(pkgname))
        except pkg_resources.DistributionNotFound:
            errs.append('W: Unable to locate package %s' % pkgname)

    if packages:
        for pkg in packages:
            printfunc(pkg)

    for e in errs:
        print >> sys.stderr, e

    if not packages:
        print >> sys.stderr, 'E: No packages found'
        return 100


def pkgnames(args):
    prefix = ''
    if args:
        prefix = args[0]
    getname = operator.attrgetter('project_name')
    pkgnames = map(getname, pkg_resources.working_set)
    if prefix:
        if prefix.islower():
            prefixed = lambda s: s.lower().startswith(prefix)
        else:
            prefixed = lambda s: s.startswith(prefix)
        pkgnames = filter(prefixed, pkgnames)
    for name in pkgnames:
        print >> sys.stdout, name


def print_showpkg_info(pkg, out=sys.stdout):
    """ Prints extended information about a package to the output
        stream defined in `out` (defaults to stdout)
        """
    print >> out, 'Package:', pkg.project_name
    print >> out, 'Version:'
    print >> out, '%s (%s)' % (pkg.version, pkg.location)
    print >> out, 'Reverse Depends:'
    rdepends = get_reverse_dependancies(pkg)
    if rdepends:
        print >> out, (', ').join([ '%s' % d for d in rdepends ])
    print >> out, 'Dependancies:'
    dependancies = get_dependancies(pkg)
    if not dependancies:
        print >> out, 'None'
    deps = (', ').join([ str(d) for d in dependancies ])
    print >> out, deps


def print_show_info(pkg, out=sys.stdout):
    """ Prints extended information about a package to the output
        stream defined in `out` (defaults to stdout)
        """
    pkginfo = get_pkginfo(pkg)
    print >> out, 'Package:', pkg.project_name
    altinfo = pkginfo.copy()
    suppress = [
     'Name', 'Description', 'Platform']
    for x in suppress:
        del altinfo[x]

    items = [ (k, altinfo[k]) for k in sorted(altinfo.keys()) ]
    for (k, v) in items:
        print >> out, '%s: %s' % (k, v)

    print >> out, 'Description:'
    desc = pkginfo['Description']
    desc = fillparagraph.fill_paragraphs(desc, 59)
    desc = ' ' + desc.replace('\n', '\n ')
    print >> out, desc
    deps = (', ').join([ str(d) for d in get_dependancies(pkg) ])
    print >> out, 'Platform:', pkg.platform and pkg.platform or 'Any'
    print >> out, 'Depends:', deps
    print >> out, 'Filename:', pkg.location
    print >> out, ''
    print >> out, ''


def get_reverse_dependancies(pkg):
    """ Return a list of Distribution objects that need this package.
        """
    target_req = pkg.as_requirement()
    dists = pkg_resources.working_set
    rdeps = []
    for dist in dists:
        for req in dist.requires():
            if target_req in req:
                rdeps.append(dist)
                break

    return rdeps


def get_dependancies(pkg):
    """ Return a list of Requirement objects that this package needs.
        """
    return pkg.requires()


def get_pkginfo(dist):
    """ Return a dictionary of package information for the
        Distribution `dist`.
        """
    try:
        return dict(email.message_from_string(dist.get_metadata('PKG-INFO')))
    except email.Errors.MessageError, e:
        err = "E: Failed to parse option '%s' in PKG-INFO file for %s" % (e, dist)
        raise Exception(err)


def get_module_func(fname):
    return globals().get(fname)


def main(args=None):
    if not args:
        args = sys.argv[1:]
    usage = "Usage: \tpet-cache [options] show pkg1 [pkg2 ...]\n        pet-cache [options] pkgnames [prefix]\n\npet-cache is a simple command line interface for querying the Python\npackage file cache.\n\nCommands:\n    show - Show a readable detailed record of a package\n    showpkg - Similar to 'show'\n    pkgnames - Display all packages in the cache, optionally filtered\n        to names that begin with the supplied prefix\n\nOptions:\n    --help (-h) This help text.\n"
    if '--help' in args or '-h' in args or '-?' in args or not args:
        print usage
        return
    commands = ['showpkg', 'show', 'pkgnames']
    command = ''
    for x in args:
        if x in commands:
            command = x
            break
        elif not x.startswith('-'):
            return "E: '%s' is not a valid package command" % x

    if not command:
        return 'E: You must supply a package command'
    args.remove(command)
    fun = get_module_func(command)
    if not fun:
        return "E: '%s' is not a valid package command" % command
    return fun(args)


if __name__ == '__main__':
    main()