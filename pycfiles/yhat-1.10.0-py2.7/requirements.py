# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yhat/requirements.py
# Compiled at: 2017-04-26 17:15:42
from pip._vendor.pkg_resources import Requirement, RequirementParseError
try:
    from pip.utils import get_installed_distributions
except ImportError:
    from pip.util import get_installed_distributions

from warnings import warn
import types

def _get_package_name(obj):
    """Returns the package name (e.g. "sklearn") for a Python object"""
    try:
        if isinstance(obj, types.ModuleType):
            return obj.__package__.split('.')[0]
        else:
            if isinstance(obj, type):
                return obj.__module__.split('.')[0]
            if isinstance(obj, object):
                return obj.__class__.__module__.split('.')[0]
            return

    except:
        return

    return


def parseUserRequirementsList(reqList):
    PACKAGE_LIMIT = 25
    pkgCount = 0
    userReqsRaw = []
    userReqs = []
    for r in reqList:
        r = r.strip().strip('\n')
        if r[-4:] == '.txt':
            pkgList = []
            f = open(r, 'r')
            for line in f:
                line = line.strip('\n').strip()
                if line[0] != '#':
                    pkgList.append(line)

            f.close()
            reqList.extend(pkgList)
        else:
            try:
                if r[:4] != 'yhat':
                    userReqsRaw.append(Requirement.parse(r))
                    pkgCount += 1
            except RequirementParseError:
                if r[:3] == 'git':
                    userReqsRaw.append(r)
                    pkgCount += 1
                else:
                    print 'Package ' + r + ' was not recognized as a valid package.'
            except:
                print (
                 'Unexpected error:', sys.exc_info()[0])
                raise

    if pkgCount > PACKAGE_LIMIT:
        warn('\nYou have tried to add %s requirmements, which exceeds the maximum amount you can add during a deployment.\nIf possible, please consider explicily adding fewer requirements and try to re-deploy.\nOr if you require this many packages, contact Yhat to upgrade your base image.\n' % str(pkgCount))
        sys.exit()
    else:
        for pkg in userReqsRaw:
            if pkg not in userReqs:
                userReqs.append(pkg)

    return userReqs


def initializeRequirements(model):
    requirements = {'modelSpecified': [], 'required': [], 'autodetected': []}
    userReqs = getattr(model, 'REQUIREMENTS', '')
    if isinstance(userReqs, str):
        userReqs = [ r for r in userReqs.splitlines() if r ]
    if userReqs:
        userReqs = parseUserRequirementsList(userReqs)
        requirements['modelSpecified'] = userReqs
    import yhat
    yhatReq = Requirement.parse('yhat==%s' % yhat.__version__)
    requirements['required'].append(yhatReq)
    return requirements


def getImplicitRequirements(model, session):
    requirements = initializeRequirements(model)
    requirements = implicit(session, requirements)
    return bundleRequirments(requirements)


def getExplicitRequirements(model, session):
    requirements = initializeRequirements(model)
    return bundleRequirments(requirements)


def printRequirements(requirements):
    for cat, reqList in list(requirements.items()):
        if reqList:
            if cat == 'required':
                print 'required packages'
            else:
                if cat == 'modelSpecified':
                    print 'model specified requirements'
                elif cat == 'autodetected':
                    print 'autodetected packages'
                for r in reqList:
                    if '==' not in str(r) and str(r)[:3] != 'git':
                        r = str(r) + ' (latest)'
                    print ' [+] ' + str(r)


def bundleRequirments(requirements):
    reqList = []
    mergedReqs = merge(requirements)
    for reqs in mergedReqs.values():
        if reqs:
            for r in reqs:
                reqList.append(r)

    bundleString = ('\n').join(str(r) for r in reqList)
    printRequirements(requirements)
    return bundleString


def implicit(session, requirements):
    """
    Returns a list of Requirement instances for all the library dependencies
    of a given session. These are matched using the contents of "top_level.txt"
    metadata for all package names in the session.
    """
    package_names = [ _get_package_name(g) for g in list(session.values()) ]
    package_names = set([ _f for _f in package_names if _f ])
    reqs = {}
    for d in get_installed_distributions():
        for top_level in d._get_metadata('top_level.txt'):
            if top_level in package_names and top_level != 'yhat':
                if d.project_name in reqs:
                    reqs[d.project_name] = max(reqs[d.project_name], d.version)
                else:
                    reqs[d.project_name] = d.version

    requirements['autodetected'] = [ Requirement.parse('%s==%s' % r) for r in list(reqs.items()) ]
    return requirements


def merge(requirements):
    """
    Merges autodetected and explicit requirements together. Autodetected
    requirements are pulled out the user's session (i.e. globals()).
    Explicit requirements are provided directly by the user. This
    function reconciles them and merges them into one set of requirements.
    Warnings are given to the user in case of version mismatch.
    Because we want to move away from implicitly getting requirements, we warn
    the user if there are implicitly detecdet but not explicitly stated
    requirements.
    """
    implicit_dict = {}
    for r in requirements['autodetected']:
        implicit_dict[r.project_name] = r

    explicit_dict = {}
    for r in requirements['modelSpecified']:
        if type(r) != str:
            explicit_dict[r.project_name] = r

    for project_name, exp_req in list(explicit_dict.items()):
        if project_name in implicit_dict:
            imp_req = implicit_dict[project_name]
            if exp_req == imp_req:
                requirements['autodetected'].remove(Requirement.parse(str(imp_req)))
            elif project_name == 'yhat':
                warn('The yhat package can be removed from REQUIREMENTS. It is required and added for you.')
                try:
                    requirements['autodetected'].remove(Requirement.parse(str(imp_req)))
                    requirements['modelSpecified'].remove(Requirement.parse(str(exp_req)))
                except:
                    pass

            else:
                warn('You have explicitly %s as a requirement, which differs from %s, which is was implicitly found to be installed locally\nDeploying with explicitly defined package: %s ' % (
                 exp_req, imp_req, exp_req))
                requirements['autodetected'].remove(Requirement.parse(str(imp_req)))

    for project_name, imp_req in list(implicit_dict.items()):
        if project_name not in explicit_dict:
            warn('Dependency %s was found with autodetection, but we recommend explicitly stating your requirements.' % imp_req)

    return requirements