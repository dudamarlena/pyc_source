# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anybox/buildbot/capability/steps.py
# Compiled at: 2017-10-20 04:47:35
"""Common build steps."""
import random
from buildbot.process.buildstep import LoggingBuildStep
from buildbot.process.buildstep import SUCCESS
from buildbot.process.buildstep import FAILURE
from .constants import CAPABILITY_PROP_FMT
from .version import Version, VersionFilter

class DescriptionBuildStep(LoggingBuildStep):
    """A base buildstep with description class.

    The goal is to factor out processing of description related kwargs in init.
    """

    def __init__(self, description=None, descriptionDone=None, descriptionSuffix=None, **kw):
        LoggingBuildStep.__init__(self, **kw)
        if description:
            self.description = description
        if isinstance(description, basestring):
            self.description = [
             self.description]
        if descriptionDone:
            self.descriptionDone = descriptionDone
        if isinstance(descriptionDone, basestring):
            self.descriptionDone = [
             self.descriptionDone]
        if descriptionSuffix:
            self.descriptionSuffix = descriptionSuffix
        if isinstance(descriptionSuffix, basestring):
            self.descriptionSuffix = [
             self.descriptionSuffix]


class SetCapabilityProperties(DescriptionBuildStep):
    """Set capability related properties.

    Example behaviour::

          capa_name 1.3 port=1234

    will produce a property ``capability_capa_name_port`` with value ``1234``.
    """

    def __init__(self, capability_name, capability_prop='capability', build_requires_prop='build_requires', capability_version_prop=None, **kw):
        """

        capability_prop is the name of the complex worker-level property
        entirely describing the capabilities
        capability_version_prop is the name of the property (builder-level)
        giving the version capability to take into account.
        """
        DescriptionBuildStep.__init__(self, **kw)
        self.capability_name = capability_name
        self.capability_prop = capability_prop
        self.build_requires_prop = build_requires_prop
        self.capability_version_prop = capability_version_prop

    def start(self):
        cap_details = self.getProperty(self.capability_prop)[self.capability_name]
        if not cap_details:
            self.finished(SUCCESS)
            return
        else:
            logs = []
            build_requires = self.getProperty(self.build_requires_prop, {})
            for req in build_requires:
                req = VersionFilter.parse(req)
                if req.cap != self.capability_name:
                    continue
                cap_details = dict((v, o) for v, o in cap_details.items() if req.match(Version.parse(v)))

            options = None
            if self.capability_version_prop:
                cap_version = self.getProperty(self.capability_version_prop)
                if cap_version is not None:
                    options = cap_details[cap_version]
            if options is None:
                choice = random.choice(cap_details.keys())
                logs.append('On worker %r, the following versions of capability %r are applicable for this build: %r, picking %r at random' % (
                 self.getProperty('workername'),
                 self.capability_name,
                 cap_details.keys(),
                 choice))
                options = cap_details[choice]
            for opt, value in options.items():
                prop = CAPABILITY_PROP_FMT % (self.capability_name, opt)
                logs.append('%s: %r' % (prop, value))
                self.setProperty(prop, value, 'Capability')

            self.addCompleteLog('property changes', ('\n').join(logs))
            self.finished(SUCCESS)
            return