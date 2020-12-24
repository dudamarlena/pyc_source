# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/arya/arya.py
# Compiled at: 2015-10-21 13:49:54
"""
APIC Rest Python Adapter (arya)

Paul Lesiak - palesiak@cisco.com

Copyright (C) 2014 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Converts blocks of APIC XML/JSON into the equivalent cobra code to construct
the objects.
"""
import os, sys, xml.etree.cElementTree as ETree, json, keyword, StringIO
from argparse import ArgumentParser
from string import Template
from collections import OrderedDict

def convert_dn_to_cobra(dn):
    from cobra.mit.naming import Dn
    imports = []
    cobra_dn = Dn.fromString(dn)
    parentMoOrDn = "''"
    dn_dict = OrderedDict()
    for rn in cobra_dn.rns:
        rn_str = str(rn)
        dn_dict[rn_str] = {}
        dn_dict[rn_str]['namingVals'] = tuple(rn.namingVals)
        dn_dict[rn_str]['moClassName'] = rn.meta.moClassName
        dn_dict[rn_str]['className'] = rn.meta.className
        dn_dict[rn_str]['parentMoOrDn'] = parentMoOrDn
        parentMoOrDn = rn.meta.moClassName

    code = []
    dn_dict.popitem()
    for arn in dn_dict.items():
        if len(arn[1]['namingVals']) > 0:
            nvals_str = ', ' + (', ').join(map(lambda x: ("'{0}'").format(str(x)), arn[1]['namingVals']))
        else:
            nvals_str = ''
        code.append(('{0} = {1}({2}{3})').format(arn[1]['moClassName'], arn[1]['className'], arn[1]['parentMoOrDn'], nvals_str))
        package = ('.').join(arn[1]['className'].split('.')[0:-1])
        imports.append(package)

    return (
     arn[1]['moClassName'], imports, ('\n').join(code))


class arya(object):
    EXCLUDEATTR = [
     'configIssues', 'stateQual', 'replTs', 'modTs', 'lcC',
     'childAction', 'monPolDn', 'state', 'lcOwn', 'rn',
     'triggerSt', 'configSt', 'status', 'scope', 'uid',
     'dn']
    APICPACKAGES = []
    try:
        import cobra.model, pkgutil
        APICPACKAGES = sorted([ modname for importer, modname, ispkg in pkgutil.iter_modules(cobra.model.__path__) if not ispkg
                              ], key=lambda l: 100 / len(l))
    except ImportError:
        APICPACKAGES = sorted([
         'testinfralab', 'policer', 'rtpfx', 'task', 'file', 'geo',
         'eqptcapacity', 'monitor', 'rtmap', 'span', 'eqpt', 'fsm',
         'traceroutep', 'lldptlv', 'rtflt', 'snmp', 'draw', 'epm',
         'traceroute', 'isistlv', 'rtcom', 'satm', 'dhcp', 'dns',
         'lldptlvpol', 'eqptcap', 'pcons', 'rule', 'copp', 'dbg',
         'imginstall', 'dhcptlv', 'mcast', 'rmon', 'coop', 'ctx',
         'dhcptlvpol', 'uribv4', 'maint', 'repl', 'comp', 'cnw',
         'synthetic', 'tunnel', 'leqpt', 'reln', 'comm', 'cdp',
         'statstore', 'sysmgr', 'l3ext', 'rbqm', 'vpc', 'cap',
         'igmpsnoop', 'syslog', 'l3cap', 'qosp', 'vns', 'bgp',
         'eqptdiagp', 'rtleak', 'l2ext', 'qosm', 'vmm', 'arp',
         'condition', 'rtctrl', 'l2cap', 'proc', 'top', 'aib',
         'stormctrl', 'opflex', 'l1cap', 'pres', 'tlv', 'aaa',
         'topoctrl', 'naming', 'infra', 'pool', 'tag', 'vz',
         'sysdebug', 'memory', 'ident', 'ping', 'svi', 'pc',
         'rtregcom', 'icmpv6', 'glean', 'phys', 'sts', 'os',
         'rtextcom', 'icmpv4', 'fault', 'ospf', 'stp', 'nw',
         'observer', 'health', 'extnw', 'mock', 'rpm', 'nd',
         'firmware', 'fvtopo', 'event', 'mgmt', 'rib', 'mo',
         'eqptdiag', 'fmcast', 'ethpm', 'lldp', 'res', 'l4',
         'datetime', 'frmwrk', 'eptrk', 'lacp', 'qos', 'l3',
         'callhome', 'fabric', 'dbgac', 'l3vm', 'psu', 'l2',
         'actrlcap', 'dbgexp', 'ctrlr', 'isis', 'pol', 'l1',
         'vlanmgr', 'config', 'adcom', 'ipv6', 'pki', 'ip',
         'sysmgrp', 'compat', 'actrl', 'ipv4', 'oam', 'im',
         'syshist', 'action', 'vsvc', 'igmp', 'mon', 'ha',
         'sysfile', 'vxlan', 'vlan', 'icmp', 'mcp', 'fv',
         'svccore', 'stats', 'trig', 'fvns', 'lbp', 'ac',
         'regress', 'rtsum', 'test', 'vtap', 'hvs'], key=lambda l: 100 / len(l))

    POLUNICONTAINED = ['configBackupStatusCont', 'dbgDebugP',
     'vnsScriptHandlerState', 'aaaUserEp',
     'rbqmUseCaseGroup', 'l3extDomP',
     'tagAliasDef', 'l2extDomP',
     'faultCounts', 'fvTenant',
     'infraInfra', 'physDomP',
     'fabricInst', 'fvCtxDef',
     'healthInst', 'vmmProvP',
     'aaaRbacEp', 'fvBDDef',
     'fvEpPCont', 'vnsVDev',
     'ctrlrInst', 'tagDef']

    def __init__(self):
        """
        Class constructor
        Define some of the python modules we will always be importing
        """
        self.objectcounter = 0
        self.importlist = [
         'cobra.mit.access', 'cobra.mit.session', 'cobra.mit.request']
        self.varnames = OrderedDict()

    def resolvemoname(self, moname):
        """
        This method does a longest prefix match on the name of an mo, e.g.,
        fvTenant and then finds the APIC package name that this class belongs
        to. If it's unable to find a matching package name, it means something
        in the input XML/JSON is screwy and that we should raise an exception
        returns: packageName, className, e.g., fv, Tenant
        """
        for c in self.APICPACKAGES:
            if moname.startswith(c):
                package = c
                name = moname[len(c):len(moname)]
                break
        else:
            raise LookupError('Unable to find class %s in package list' % moname)

        return (
         package, name)

    def getvarname(self, objname):
        """
        This method helps track variable names that are in use so in case of
        nested and/or duplicate variable names the code has to auto generate
        we can easily differentiate between them. it's simply an occurence
        counter, that returns the name of the object with its occurence count
        appended to the end
        """
        if objname in self.varnames:
            self.varnames[objname] += 1
            return '%s%d' % (objname, self.varnames[objname])
        else:
            self.varnames[objname] = 1
            return ('{0}').format(objname)

    def buildattributestring(self, attr):
        """
        Builds the attribute string for the object creation

        attr is a dict containing name value pairs of the attribute and value
        """
        if not isinstance(attr, dict):
            attr = dict()
        parmlist = []
        for k, v in attr.items():
            if k not in self.EXCLUDEATTR:
                if keyword.iskeyword(k):
                    k += '_'
                v = repr(v)
                parmlist.append('%s=%s' % (k, v))

        attribstr = (', ').join(parmlist)
        return attribstr

    def buildcommand(self, mofullname, moparent, attr):
        """
        This is the build ol' chunk of code that accepts the mo, it's parent
        and attributes and then creates the equivalent cobra calls
        This method should be pretty meta format agnostic -- I was able to use
        this same method for both JSON and XML with no changes

        mofullname - complete MO name, extracted from the JSON key/XML tag name
        moparent - parent object variable name
        attr - dict (key/value pair) containing attributes for this MO
        """
        cmd = ''
        objectvarname = None
        mopackagename, moclassname = self.resolvemoname(mofullname)
        if moclassname.startswith('Rt'):
            pass
        else:
            attribstr = self.buildattributestring(attr)
            cobrapackagename = 'cobra.model.%s' % mopackagename
            if cobrapackagename not in self.importlist:
                self.importlist.append(cobrapackagename)
            objectvarname = self.getvarname(mofullname)
            if mofullname == 'polUni':
                return ('', moparent)
            parms = [moparent]
            if attribstr != '':
                parms.append(attribstr)
            cmd += '%s = cobra.model.%s.%s(%s)\n' % (
             objectvarname, mopackagename, moclassname, (', ').join(parms))
            if attr.get('status', '') == 'deleted':
                cmd += '%s.delete()\n' % objectvarname
            self.objectcounter += 1
        return (
         cmd, objectvarname)

    def recursexmltree(self, elem, parentname):
        pycode, objectname = self.buildcommand(elem.tag, parentname, elem.attrib)
        for e in elem:
            pycode += self.recursexmltree(e, objectname)

        return pycode

    def recursejsondict(self, jsondict, parentname):
        pycode, objectname = self.buildcommand(jsondict.keys()[0], parentname, jsondict[jsondict.keys()[0]].get('attributes', {}))
        if 'children' in jsondict[jsondict.keys()[0]]:
            for j in jsondict[jsondict.keys()[0]]['children']:
                pycode += self.recursejsondict(j, objectname)

        return pycode

    def getpython(self, xmlstr=None, jsonstr=None, apicip='1.1.1.1', apicpassword='password', apicuser='admin', nocommit=False, brief=False):
        if brief:
            pycodetemplate = Template('$lookupCode\n$objStructureCode\n$commitCode')
        else:
            pycodetemplate = Template("#!/usr/bin/env python\n'''\nAutogenerated code using $myFileName\nOriginal Object Document Input: \n$sourceDoc\n'''\n$raisecheckwarning\n\n# list of packages that should be imported for this code to work\n$imports\nfrom cobra.internal.codec.xmlcodec import toXMLStr\n\n# log into an APIC and create a directory object\nls = cobra.mit.session.LoginSession('https://$apicHost', '$apicUser', '$apicPassword')\nmd = cobra.mit.access.MoDirectory(ls)\nmd.login()\n\n# the top level object on which operations will be made\n$lookupCode\n\n# build the request using cobra syntax\n$objStructureCode\n\n# commit the generated code to APIC\nprint toXMLStr($topMo)\n$commitCode")
        vals = {}
        topobjectvar = 'topMo'
        topdn = None
        if nocommit:
            vals['raisecheckwarning'] = ''
        else:
            vals['raisecheckwarning'] = "raise RuntimeError('Please review the auto generated code before ' +\n                    'executing the output. Some placeholders will ' +\n                    'need to be changed')"
        if xmlstr and jsonstr:
            raise ValueError('Both xmlfile and jsonfile provided. Which one ' + 'do I listen to? I am so confused!')
        if xmlstr:
            tree = ETree.ElementTree(ETree.fromstring(xmlstr))
            root = tree.getroot()
            toptag = root.tag
            if toptag == 'imdata':
                root = list(root)[0]
            topdn = root.attrib.get('dn', None)
        elif jsonstr:
            j = json.loads(jsonstr)
            toptag = j.keys()[0]
            if toptag == 'imdata':
                j = j['imdata'][0]
            topdn = j[j.keys()[0]].get('attributes', {}).get('dn', None)
        else:
            toptag = None
        if toptag in self.POLUNICONTAINED:
            self.importlist.append('cobra.model.pol')
            lookupcodestr = "topMo = cobra.model.pol.Uni('')\n"
            vals['lookupCode'] = lookupcodestr
        elif toptag == 'polUni':
            self.importlist.append('cobra.model.pol')
            vals['lookupCode'] = ("{0} = cobra.model.pol.Uni('')").format(topobjectvar)
        else:
            if topdn:
                try:
                    topobjectvar, imports, lookupcodestr = convert_dn_to_cobra(topdn)
                    self.importlist.extend(imports)
                except ImportError:
                    self.importlist.append('cobra.mit.naming')
                    lookupcodestr = '# Confirm the dn below is for your top dn\n'
                    lookupcodestr += 'topDn = cobra.mit.naming.'
                    lookupcodestr += ("Dn.fromString('{0}')\n").format(topdn)
                    lookupcodestr += 'topParentDn = topDn.getParent()\n'
                    lookupcodestr += ('{0} = md.lookupByDn(topParentDn)').format(topobjectvar)

            else:
                lookupcodestr = '# Replace the text below with the dn of your '
                lookupcodestr += 'top object\n'
                lookupcodestr += ("{0} = md.lookupByDn('REPLACEME')").format(topobjectvar)
            vals['lookupCode'] = lookupcodestr
        if xmlstr:
            vals['objStructureCode'] = self.recursexmltree(root, topobjectvar)
        elif jsonstr:
            vals['objStructureCode'] = self.recursejsondict(j, topobjectvar)
        vals['apicHost'] = apicip
        vals['apicUser'] = apicuser
        vals['apicPassword'] = apicpassword
        vals['sourceDoc'] = xmlstr or jsonstr
        vals['myFileName'] = os.path.basename(str(sys.argv[0]))
        vals['imports'] = ('\n').join([ 'import %s' % i for i in sorted(set(self.importlist)) ])
        vals['topMo'] = topobjectvar
        commitcodestr = 'c = cobra.mit.request.ConfigRequest()\n'
        commitcodestr += ('c.addMo({0})\n').format(topobjectvar)
        if not nocommit:
            commitcodestr += 'md.commit(c)\n'
        vals['commitCode'] = commitcodestr
        return pycodetemplate.substitute(vals)


def isxmlorjson(s):
    try:
        json.loads(s)
        isjson = True
    except ValueError:
        isjson = False

    try:
        ETree.ElementTree(ETree.fromstring(s))
        isxml = True
    except ETree.ParseError:
        isxml = False

    if isjson and isxml:
        raise ValueError('This file appears to be both XML and JSON. I am ' + 'confused. Goodbye')
    if isjson:
        return 'json'
    else:
        if isxml:
            return 'xml'
        else:
            return

        return


def runfromcli(args):

    def processinputstr(inputstr, args):
        format = isxmlorjson(inputstr)
        if format == 'xml':
            return arya().getpython(xmlstr=inputstr, apicip=args.ip, apicpassword=args.password, apicuser=args.username, nocommit=args.nocommit, brief=args.brief)
        if format == 'json':
            return arya().getpython(jsonstr=inputstr, apicip=args.ip, apicpassword=args.password, apicuser=args.username, nocommit=args.nocommit, brief=args.brief)
        raise IOError('Unsupported format passed as input. Please check ' + 'that input is formatted correctly in JSON or XML syntax')

    if args.filein or args.stdin:
        if args.stdin:
            inputstr = sys.stdin.read()
        elif args.filein:
            with file(args.filein, 'r') as (inputfilehandle):
                inputstr = inputfilehandle.read()
        print processinputstr(inputstr, args)
    elif args.sourcedir:
        sourcedir = os.path.realpath(args.sourcedir)
        if args.targetdir:
            targetdir = os.path.realpath(args.targetdir)
        else:
            targetdir = sourcedir
        print 'Reading from %s and writing to %s' % (sourcedir, targetdir)
        os.chdir(args.sourcedir)
        for files in os.listdir('.'):
            if files.lower().endswith('.xml') or files.lower().endswith('.json'):
                outfilename = os.path.join(targetdir, os.path.basename(files).split('.')[(-2)] + '.py')
                if os.path.isfile(outfilename):
                    raise IOError('Output file: %s already exists' % outfilename)
                print '%s -> %s' % (files, outfilename)
                p = None
                try:
                    with file(files, 'r') as (f):
                        p = processinputstr(f.read(), args)
                except ETree.ParseError:
                    print 'XML parser error %s' % files
                else:
                    with open(outfilename, 'w') as (f):
                        f.write(p)

    return True


def main():
    parser = ArgumentParser('Code generator for APIC cobra SDK')
    parser.add_argument('-f', '--filein', help='Document containing post to be sent to ' + 'REST API', required=False)
    parser.add_argument('-s', '--stdin', help='Parse input from stdin, for use as a filter, ' + ('e.g., cat doc.xml | {0} -s').format(os.path.basename(sys.argv[0])), action='store_true', default=False, required=False)
    parser.add_argument('-d', '--sourcedir', help='Specify a source directory containing ' + 'ACI object files you want to convert to python. ', required=False)
    parser.add_argument('-t', '--targetdir', help='Where to write the .py files that come ' + 'from the -d directory. If none is ' + 'specified, it will default to SOURCEDIR', required=False)
    parser.add_argument('-i', '--ip', help='IP address of APIC to be ' + ' pre-populated', required=False, default='1.1.1.1')
    parser.add_argument('-u', '--username', help='Username for APIC account ' + 'to be pre-populated in generated code', required=False, default='admin')
    parser.add_argument('-p', '--password', help='Password for APIC account ' + ' to be pre-populated in generated code', required=False, default='password')
    parser.add_argument('-nc', '--nocommit', help='Generate code without final commit to changes', required=False, default=False, action='store_true')
    parser.add_argument('-b', '--brief', help='Generate brief code (without headers, comments, etc)', required=False, default=False, action='store_true')
    args = parser.parse_args()
    if not args.filein and not args.sourcedir and not args.stdin:
        print 'ERROR: You must specify at least -d, -f, or -s '
        print ''
        parser.print_help()
        sys.exit(1)
    runfromcli(args)


if __name__ == '__main__':
    main()