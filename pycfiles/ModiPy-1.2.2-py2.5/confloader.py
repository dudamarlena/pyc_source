# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/confloader.py
# Compiled at: 2009-08-25 18:19:45
"""
The ConfigLoader loads in a particular configuration file that
specifies the change definition to be run.
"""
import re, sys, os
from lxml import etree
from namespace import create_namespace
from iterator import create_iterator
from device import Device
from change import ChangeConditionFailure, NoCommands
from provisioner import UserBailout, NoTargetsError
import util
from twisted.internet import defer, reactor
from twisted.python import log as tlog
import logging, debug
log = logging.getLogger('modipy')
xinclude_re = re.compile('.*<xi:include href=[\\\'\\"](?P<uri>.*)[\\\'\\"].*')

class ConfigLoader():
    """
    A ConfigLoader is used to load in a change configuration and
    set up all the objects that define the change.
    """

    def __init__(self):
        self.doc = None
        self.global_namespace = {}
        self.provisioners = {}
        self.devices = {}
        self.change_templates = {}
        self.changes = {}
        self.iterators = {}
        self.pending_changes = []
        self.change_success = []
        self.change_failure = []
        self.backout_success = []
        self.backout_failure = []
        self.change_skipped = []
        log.debug('created ConfigLoader')
        return

    def load_config(self, options, devices=[]):
        self.options = options
        d = defer.succeed(None)
        if options.configfile:
            d.addCallback(self.parse, options.configfile, devices)
        for change in self.changes.values():
            if change.name in options.skip_changes:
                log.info('Skipping change: %s', change.name)
                change.state('skipped')
                self.change_complete(None, change)

        for change in self.changes.values():
            if len(options.only_changes) > 0 and change.name not in options.only_changes:
                log.info('Skipping change: %s', change.name)
                change.state('skipped')
                self.change_complete(None, change)

        return d

    def parse(self, ignored, configfile, devicenames):
        """
        Parse my configuration file.
        """
        try:
            self.tree = etree.parse(configfile)
        except IOError, e:
            log.error('Cannot parse configuration file: %s', e)
            raise

        try:
            self.tree.xinclude()
        except etree.XIncludeError:
            log.error('XInclude of a file failed.')
            log.error('Use external tool such as xmllint to figure out why.')
            log.error("Sorry, but lxml.etree won't tell me exactly what went wrong.")
            raise

        try:
            nsnode = self.tree.xpath('/config/namespace')[0]
            self.add_namespace(None, nsnode)
        except IndexError:
            pass

        d = defer.succeed(None)
        for nodename in [
         'iterator',
         'provisioner',
         'device']:
            self.parse_nodes(d, nodename)

        d.addCallback(self.add_commandline_devices, devicenames)
        for nodename in [
         'changetemplate',
         'change']:
            self.parse_nodes(d, nodename)

        d.addCallback(self.set_prereqs)
        return d

    def parse_nodes(self, d, nodename):
        """
        Parse all nodes with a given name
        @param d: a L{defer.Deferred} to callback when finished
        """
        for node in self.tree.findall(nodename):
            log.debug("Adding a '%s' node", nodename)
            funcname = 'add_%s' % nodename
            func = getattr(self, funcname)
            d.addCallback(func, node)

    def add_commandline_devices(self, ignored, devicenames):
        """
        Add devices specified on the commandline to the active config
        """
        if len(devicenames) != 0:
            for dev in devicenames:
                if dev not in self.devices.keys():
                    log.info("Adding commandline specified device: '%s'" % dev)
                    self.devices[dev] = Device(dev)

            for dev in self.devices.keys():
                if dev not in devicenames:
                    log.info("Not using configured device '%s' (not on commandline)", dev)
                    del self.devices[dev]

    def set_prereqs(self, ignored):
        log.debug('Setting prereqs...')
        prereqs = self.tree.xpath('descendant-or-self::*/prereq')
        log.debug('found prereq nodes: %s', prereqs)
        for node in prereqs:
            prereq_changename = node.text
            try:
                prereq_for_name = node.attrib['for']
            except KeyError:
                try:
                    prereq_for_name = node.xpath('parent::*')[0].attrib['name']
                except KeyError:
                    log.error("prerequisite change '%s' is not defined.", prereq_for_name)

            try:
                prereq_change = self.changes[prereq_changename]
                log.debug('prereq_changename: %s', prereq_changename)
            except KeyError:
                log.error("Cannot find change '%s' as prereq for change '%s'", prereq_changename, prereq_for)
                raise

            try:
                change_for = self.changes[prereq_for_name]
            except KeyError:
                log.error("Cannot find change '%s' with prereq of '%s'", prereq_for_name, prereq_changename)
                raise

            change_for.add_prereq(prereq_change)
            log.debug("Added change '%s' as prereq for change '%s'", prereq_changename, prereq_for_name)

        self.process_dependencies()

    def add_iterator(self, ignored, node):
        """
        Add an iterator, which is a list of namespaces
        that will be iterated over for a particular change step.
        """
        iter = create_iterator(node)
        self.iterators[iter.name] = iter
        log.debug("Added iterator '%s'", iter.name)
        return iter.load_config(None)

    def import_module(self, module_name):
        """
        Custom dynamic import function to import change and provisioner modules.
        """
        try:
            mod = sys.modules[module_name]
            return mod
        except KeyError:
            log.debug("module '%s' not yet imported. Importing...", module_name)
            mod = __import__(module_name)
            components = module_name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)

            return mod

    def add_provisioner(self, ignored, node):
        """
        Add a provisioner to my configuration based on the parsed element.
        """
        prov_klass = node.attrib['type']
        prov_name = node.attrib['name']
        try:
            module_name = node.attrib['module']
        except KeyError:
            module_name = 'modipy.provisioner'

        kwargs = {}
        for key in node.attrib:
            if key not in ('type', 'name', 'module'):
                kwargs[key] = node.attrib[key]

        log.debug("Attempting to create a '%s' provisioner", prov_klass)
        prov_module = self.import_module(module_name)
        log.debug('prov_module is: %s', prov_module)
        klass = getattr(prov_module, prov_klass)
        if self.options.sessionlog is not None:
            sessionlog = open(self.options.sessionlog, 'w')
        else:
            filename = '%s.log' % os.path.splitext(self.options.configfile)[0]
            sessionlog = open(filename, 'w')
        try:
            provisioner = klass(prov_name, authoritarian=self.options.authoritarian, autobackout=self.options.autobackout, sessionlog=sessionlog, **kwargs)
        except TypeError, e:
            log.error("Incorrect parameter supplied for provisioner of type '%s'", prov_klass)
            raise e

        log.debug("created provisioner '%s': %s", prov_name, provisioner)
        nodelist = node.xpath('*')
        taglist = [ x.tag for x in nodelist ]
        for tag in provisioner.get_required_tags():
            if tag not in taglist:
                raise ValueError("Required tag '%s' not found in '%s' definition." % (tag, provisioner.name))

        for subnode in nodelist:
            provisioner.parse_config_node(subnode)

        self.provisioners[prov_name] = provisioner
        return provisioner

    def add_device(self, ignored, node):
        """
        Add a device to my configuration based on the parsed element.
        """
        device_name = node.attrib['name']
        device = Device(device_name)
        for subnode in node.xpath('*'):
            attrib = subnode.tag
            value = subnode.text
            setattr(device, attrib, value)

        log.debug('created device: %s', device)
        self.devices[device_name] = device
        return device

    def add_changetemplate(self, ignored, node):
        """
        Add a change template to my list of available templates.
        A change template is a change object that may not have
        all of its parameters set yet.
        """
        change_tmpl = self.create_change_object(node)
        self.set_change_params(change_tmpl, node)
        self.set_change_namespace(change_tmpl, node)
        self.set_change_provisioner(change_tmpl, node)
        self.set_change_iterator(change_tmpl, node)
        self.set_change_onfail(change_tmpl, node)
        self.change_templates[change_tmpl.name] = change_tmpl
        return change_tmpl

    def add_change(self, ignored, node):
        """
        When adding a change, check for some extra options such as a
        change template, which will cause this change to be based on
        an existing change template.
        """
        log.debug('Adding new change...')
        if node.attrib.has_key('template'):
            tmpl_name = node.attrib['template']
            log.debug("Change is based on a template: '%s'", tmpl_name)
            try:
                template = self.change_templates[tmpl_name]
            except KeyError:
                raise ValueError("Change template '%s' is not defined" % tmpl_name)
            else:
                change = template.copy()
                change.name = node.attrib['name']
                self.set_change_params(change, node)
                self.set_change_namespace(change, node)
                self.set_change_provisioner(change, node)
                self.set_change_iterator(change, node)
                self.set_change_onfail(change, node)
        else:
            change = self.add_changetemplate(None, node)
        if getattr(change, 'provisioner', None) is None:
            for prov in self.provisioners.values():
                log.debug("Checking provisioner: '%s'", prov)
                if change.provisioner_interface.providedBy(prov):
                    log.debug("change '%s' will use provisioner '%s'", change.name, prov.name)
                    change.provisioner = prov
                    break
                else:
                    log.debug("provisioner '%s' does not provide interface %s", prov.name, change.provisioner_interface)

        if change.provisioner is None:
            raise ValueError("No compatible provisioners exist for change '%s'" % change.name)
        self.changes[change.name] = change
        log.debug("Adding change '%s' to pending changes: %s", change.name, self.pending_changes)
        self.pending_changes.append(change)
        return change

    def create_change_object(self, node):
        """
        Create a change object from a node.
        This may be used as a change template, or a regular change.
        """
        try:
            change_name = node.attrib['name']
            log.debug("Creating change object '%s'...", change_name)
        except KeyError:
            log.error('Change definition has no name')
            raise

        if change_name in self.changes:
            raise KeyError("Change '%s' already exists. Duplicate change name defined.", change_name)
        try:
            change_klass = node.attrib['type']
        except KeyError:
            log.error("Change definition for '%s' has no type.", change_name)
            raise

        try:
            module_name = node.attrib['module']
        except KeyError:
            module_name = 'modipy.change_command'

        log.debug("Creating a '%s' change", change_klass)
        change_module = self.import_module(module_name)
        log.debug('Loaded change module: %s', change_module)
        klass = getattr(change_module, change_klass)
        change = klass(change_name, nopause=self.options.nopause)
        log.debug("created change '%s': %s", change_name, change)
        return change

    def set_change_namespace(self, change, node):
        """
        Add a namespace to a change or change template
        """
        log.debug('change namespace: %s', change.namespace)
        if change.namespace == {}:
            log.debug('change has no namespace, using the global one.')
            change.namespace = self.global_namespace

    def set_change_provisioner(self, change, node):
        try:
            provname = node.attrib['provisioner']
        except KeyError:
            return

        provname = util.substituteVariables(provname, change.namespace)
        try:
            prov = self.provisioners[provname]
        except KeyError:
            raise KeyError("Provisioner named '%s' is not defined" % provname)

        if not change.provisioner_interface.providedBy(prov):
            raise ValueError("Provisioner '%s' does not provide interface '%s' required by change '%s'" % (prov.name, change.provisioner_interface, change.name))
        change.provisioner = prov

    def set_change_params(self, change, node):
        """
        Set common change parameters, defined in subnodes.
        """
        for subnode in node.xpath('*'):
            if subnode.tag == 'target':
                targetname = subnode.attrib['name']
                log.debug('-- Found targetname: %s', targetname)
                if targetname == 'ALL_TARGETS':
                    if len(self.devices) == 0:
                        raise ValueError('No devices defined. ALL_TARGETS specifies nothing.')
                    change.devices.extend(self.devices.values())
                    devicenames = (',').join([ '%s' % x for x in self.devices.keys() ])
                    log.debug("added target devices '%s' for change '%s'", devicenames, change)
                else:
                    targetname = util.substituteVariables(targetname, change.namespace)
                    try:
                        dev = self.devices[targetname]
                    except KeyError, e:
                        raise KeyError("Device '%s' not defined" % targetname)
                    else:
                        change.devices.append(dev)
                        log.debug("added target device '%s' for change '%s'", dev, change)
            elif subnode.tag == 'depends':
                changename = subnode.attrib['on']
                try:
                    change.pre_requisites.append(self.changes[changename])
                except KeyError:
                    if changename == change.name:
                        log.error("Change '%s' cannot be a pre-requisite of itself.", changename)
                    else:
                        log.error("Configuration error: Unknown pre-requisite '%s' for change '%s'", changename, change.name)
                    raise
                else:
                    log.debug("added change pre-requisite: '%s' for change '%s'", changename, change)
            else:
                method_name = 'parse_%s' % str(subnode.tag)
                try:
                    method = getattr(change, method_name)
                except AttributeError, e:
                    raise AttributeError("'%s' is not a valid sub-element of %s" % (subnode.tag, change))

                method(subnode)

    def set_change_iterator(self, change, node):
        """
        Set an optional change iterator
        """
        try:
            itername = node.attrib['iterator']
        except KeyError:
            itername = None

        if itername is not None:
            itername = util.substituteVariables(itername, change.namespace)
            try:
                change.iterator = self.iterators[itername]
                log.debug("change '%s' will iterate with iterator '%s'" % (change.name, itername))
            except KeyError:
                log.error("Iterator '%s' is not defined", itername)
                raise

        return

    def set_change_onfail(self, change, node):
        """
        Attempt to add an 'onfail' mode for the change, if defined
        """
        log.debug("Checking for 'onfail' attribute...")
        try:
            onfail = node.attrib['onfail']
            log.debug('onfail attrib found.')
            if onfail == 'continue':
                change.on_fail_continue = True
                log.debug('Processing will continue if this change fails')
            elif onfail == 'retry':
                change.on_fail_retry = True
                log.debug('This change will retry on failure')
                try:
                    max_retries = int(node.attrib['max_retries'])
                    change.max_retries = max_retries
                except KeyError:
                    pass
                else:
                    log.debug('  This change will retry at most %d times', change.max_retries)
                    try:
                        retry_delay = int(node.attrib['retry_delay'])
                        if retry_delay < 0:
                            raise ValueError("Retry delay for change '%s' must be > 0" % change.name)
                        change.retry_delay = retry_delay
                    except KeyError:
                        pass

        except KeyError:
            pass

    def set_change_noop(self, change, node):
        """
        Mark a change as a 'No Op' if it has the noop attribute set.
        If it's not set to anything, this is taken as meaning 'true'.
        If it's absent, then it
        """
        try:
            onfail = node.attrib['noop']
            log.debug('noop attrib found')
            if not (noop.lower().startswith('n') or noop.lower().startswith('f')):
                change.noop = True
        except KeyError:
            pass

    def add_namespace(self, ignored, node, item=None):
        """
        Add a namespace, defined by nsnode, to an item (such as a change)
        This is called within an 'add_' method for the other items,
        such as iterators and changes.
        """
        log.debug('Adding namespace: node')
        ns = create_namespace(node)
        if item is None:
            self.global_namespace = ns
        else:
            log.debug('Adding namespace to item: %s', item)
            ns.parent = self.global_namespace
            item.namespace = ns
        return ns

    def get_available_changes(self):
        """
        This returns a list of pending changes that can be performed,
        either because they have no pre-requsites, or all their
        pre-requisistes have been successfully implemented.
        """
        changelist = []
        log.debug('pending changes: %s', self.pending_changes)
        if self.options.backout:
            log.info('In backout mode. Doing changes in reverse.')
            for change in self.pending_changes:
                if not change.has_children():
                    changelist.append(change)
                    log.debug("change '%s' has no children. Adding to backout change queue.", change)
                    continue
                all_children = True
                for child_change in change.children:
                    if child_change.state() not in ('backout_ok', 'skipped', 'success'):
                        all_children = False
                        break

                if all_children:
                    changelist.append(change)

        else:
            for change in self.pending_changes:
                log.debug('testing change %s', change)
                if len(change.pre_requisites) == 0:
                    changelist.append(change)
                    log.debug("change '%s' has no pre-reqs. Adding to execution queue.", change)
                    continue
                else:
                    all_prereqs = True
                    for prereq in change.pre_requisites:
                        log.debug("change '%s' has a pre-req of '%s'", change, prereq)
                        if prereq not in self.change_success and prereq not in self.change_skipped:
                            if prereq.state() in ('backout_ok', ):
                                continue
                            elif prereq.state() not in ('pending', 'retry') and prereq.on_fail_continue:
                                log.debug('prereq failed, but is marked onfail:continue.')
                                continue
                            log.debug("pre-req '%s' not complete yet.", prereq)
                            all_prereqs = False
                            break

                    if all_prereqs:
                        log.debug("All pre-reqs for '%s' have completed. Adding to execution queue.", change)
                        changelist.append(change)
                    else:
                        log.debug("change '%s' has pending pre-reqs", change)

        log.debug('Returning changelist: %s', changelist)
        return changelist

    def change_complete(self, fail_result, change):
        """
        Move a change from pending to complete.
        """
        log.debug('marking change as complete.')
        if change.state() == 'success':
            self.change_success.append(change)
            self.pending_changes.remove(change)
        elif change.state() == 'skipped':
            log.debug('skipping change. removing from pending queue: %s', self.pending_changes)
            self.change_skipped.append(change)
            self.pending_changes.remove(change)
            log.debug('pending changes are now: %s', self.pending_changes)
        elif change.state() == 'partial_failure':
            self.change_failure.append(change)
            self.pending_changes.remove(change)
        elif change.state() == 'total_failure':
            self.change_failure.append(change)
            self.pending_changes.remove(change)
        elif change.state() == 'backout_ok':
            self.change_failure.append(change)
            self.backout_success.append(change)
            self.pending_changes.remove(change)
        elif change.state() == 'backout_failed':
            self.change_failure.append(change)
            self.backout_failure.append(change)
            self.pending_changes.remove(change)
        elif change.state() == 'retry_pending':
            log.info("Change '%s' will be retried in '%d' seconds", change.name, change.retry_delay)
        elif change.state() == 'retry':
            log.info("Change '%s' will be retried", change.name)
        elif change.state() == 'pending':
            log.info("Change '%s' did not run.", change.name)
            self.pending_changes.remove(change)
        else:
            log.error("Unknown/unhandled change state '%s'", change.state)
            self.pending_changes.remove(change)
            raise ValueError('change_complete() cannot handle change state: %s', change.state)

    def process_dependencies(self):
        """
        Post-process the dependency tree after loading it.
        This sets up the pre-reqs for each change, as specified
        in the dependency tree.
        """
        for node in self.tree.findall('dependencies'):
            log.debug('dependency node: %s', node)


class ChangeController():
    """
    An overall change controller, to control the changes
    """

    def __init__(self, config_loader):
        self.cfgldr = config_loader
        self.current_changelist = []
        self.alldone = None
        return

    def do_changes(self, ignored):
        self.alldone = defer.Deferred()
        self.get_next_changes(None)
        self.alldone.addCallbacks(self.print_stats, self.print_stats)
        return self.alldone

    def get_next_changes(self, results):
        """
        Fetch the next set of changes to run.
        This collects all changes that don't have any
        pre-requisites (on the first pass), or that have had all
        their pre-requisites complete successfully.
        These changes can therefore all be run together, since they
        have no interdependencies on one another.

        When in backout mode, we do sortof the opposite: we find
        all the changes that have nothing that depends on them, or
        that have already been backed out.

        FIXME: This is terribly inefficient. It would be better to
        build a Directed Acyclic Graph at the beginning, and then
        traverse it during execution.
        """
        log.debug('Results in get_next_changes are: %s', results)
        log.debug('Fetching outstanding changes...')
        self.current_changelist = self.cfgldr.get_available_changes()
        if len(self.current_changelist) == 0:
            if len(self.cfgldr.pending_changes) > 0:
                log.info('Pending changes exist that cannot be executed!')
                self.alldone.errback(ValueError('Pending changes cannot be executed'))
            elif self.alldone is not None:
                self.alldone.callback('All changes complete')
        else:
            log.debug('Pending changes to be executed. Scheduling.')
            return self.do_pending_changes(None)
        return

    def do_pending_changes(self, ignored):
        """
        This runs all the pending changes that are currently queued.
        It runs all of them simultaneously, since they have been identified
        as changes that can be run together. If you want to run changes
        sequentially, then they should have sequential dependencies.

        FIXME: Maybe add a flag to allow sequential mode operation?
        """
        log.debug('Running pending changes...')
        dlist = []
        log.debug('changelist is: %s', self.current_changelist)
        for change in self.current_changelist:
            log.debug("adding change '%s' to implementation queue", change.name)
            d = change.provisioner.perform_change(None, change, self.cfgldr.global_namespace, backout=self.cfgldr.options.backout)
            d.addCallback(self.change_complete, change)
            d.addErrback(self.change_failure, change)
            dlist.append(d)

        dl = defer.DeferredList(dlist, fireOnOneErrback=True, consumeErrors=True)
        dl.addCallback(self.get_next_changes)
        dl.addErrback(self.bailout)
        return dl

    def bailout(self, failure):
        """
        Bailout detects the first error from the deferred list,
        and bails out.
        """
        log.debug('Running bailout because of: %s', failure)
        if failure.value.subFailure.type == UserBailout:
            self.alldone.callback('Bailout')
        else:
            log.debug('Unhandled bailout failure: %s', failure)
            self.alldone.errback(failure.value.subFailure)

    def change_complete(self, result, change):
        """
        Move change from pending to complete
        """
        self.cfgldr.change_complete(result, change)

    def change_failure(self, failure, change):
        if failure.type == UserBailout:
            log.debug('Controller detected UserBailout')
            self.change_complete(failure, change)
            return failure
        elif failure.type == ChangeConditionFailure:
            log.debug('Controller detected ChangeConditionFailure')
            self.change_complete(failure, change)
            return failure
        elif failure.type == NoCommands:
            self.change_complete(failure, change)
            return failure
        elif failure.type == NoTargetsError:
            return failure
        else:
            log.error('Major change failure: %s', failure.value)
            tlog.err(failure)
            self.change_complete(failure, change)
            return failure

    def print_stats(self, ignored):
        """
        We've finished all our work, and now we summarise what happened.
        """
        success_count = len(self.cfgldr.change_success)
        failure_count = len(self.cfgldr.change_failure)
        skip_count = len(self.cfgldr.change_skipped)
        backout_success_count = len(self.cfgldr.backout_success)
        backout_failure_count = len(self.cfgldr.backout_failure)
        pending_count = len(self.cfgldr.pending_changes)
        log.info('--- Final results ---')
        if not self.cfgldr.options.backout:
            if not (success_count > 0 or failure_count > 0):
                log.info('no changes succeeded or failed!')
            else:
                log.info('%d ok, %d failed, %d skipped (%d%% success rate)' % (success_count, failure_count, skip_count, 100 * success_count / (success_count + failure_count)))
            if success_count > 0:
                log.info('Successful changes: %s' % (', ').join([ x.name for x in self.cfgldr.change_success ]))
            if failure_count > 0:
                log.info('Failed changes: %s' % (', ').join([ x.name for x in self.cfgldr.change_failure ]))
            if skip_count > 0:
                log.info('Skipped changes: %s' % (', ').join([ x.name for x in self.cfgldr.change_skipped ]))
        if backout_success_count > 0 or backout_failure_count > 0:
            log.info('%d backed out ok, %d failed (%d%% backout success rate)' % (backout_success_count, backout_failure_count, 100 * backout_success_count / (backout_success_count + backout_failure_count)))
        if backout_success_count > 0:
            log.info('Changes backed out ok: %s' % (', ').join([ x.name for x in self.cfgldr.backout_success ]))
        if backout_failure_count > 0:
            log.info('Changes NOT backed out ok: %s' % (', ').join([ x.name for x in self.cfgldr.backout_failure ]))
        if pending_count > 0:
            if pending_count > 1:
                plural = 's'
                waswere = 'were'
            else:
                plural = ''
                waswere = 'was'
            log.info('%d change%s %s not attempted: %s' % (pending_count, plural, waswere, (', ').join([ x.name for x in self.cfgldr.pending_changes ])))
        return (
         success_count, failure_count + pending_count)


if __name__ == '__main__':
    log.setLevel(logging.INFO)
    configfile = 'etc/test_change.conf'
    try:
        cfgldr = ConfigLoader(configfile)
    except:
        log.error('Cannot load configuration. Aborting.')
        sys.exit(1)
    else:
        log.debug('changes to apply: %s', cfgldr.changes)
        log.debug('total devices: %s', cfgldr.devices)
        controller = ChangeController(cfgldr)

        def mystop(ignored):
            log.debug('finished!')
            reactor.stop()


        def errstop(failure):
            log.info('Changes not implemented ok!')
            reactor.stop()


        def go():
            d = controller.do_changes()
            d.addCallbacks(mystop, errstop)


        reactor.callLater(0, go)
        reactor.run()