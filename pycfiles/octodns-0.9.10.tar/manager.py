# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/octodns/manager.py
# Compiled at: 2020-02-18 18:19:36
from __future__ import absolute_import, division, print_function, unicode_literals
from concurrent.futures import ThreadPoolExecutor
from importlib import import_module
from os import environ
import logging
from .provider.base import BaseProvider
from .provider.plan import Plan
from .provider.yaml import SplitYamlProvider, YamlProvider
from .record import Record
from .yaml import safe_load
from .zone import Zone

class _AggregateTarget(object):
    id = b'aggregate'

    def __init__(self, targets):
        self.targets = targets

    def supports(self, record):
        for target in self.targets:
            if not target.supports(record):
                return False

        return True

    @property
    def SUPPORTS_GEO(self):
        for target in self.targets:
            if not target.SUPPORTS_GEO:
                return False

        return True

    @property
    def SUPPORTS_DYNAMIC(self):
        for target in self.targets:
            if not target.SUPPORTS_DYNAMIC:
                return False

        return True


class MakeThreadFuture(object):

    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def result(self):
        return self.func(*self.args, **self.kwargs)


class MainThreadExecutor(object):
    """
    Dummy executor that runs things on the main thread during the invocation
    of submit, but still returns a future object with the result. This allows
    code to be written to handle async, even in the case where we don't want to
    use multiple threads/workers and would prefer that things flow as if
    traditionally written.
    """

    def submit(self, func, *args, **kwargs):
        return MakeThreadFuture(func, args, kwargs)


class ManagerException(Exception):
    pass


class Manager(object):
    log = logging.getLogger(b'Manager')

    @classmethod
    def _plan_keyer(cls, p):
        plan = p[1]
        if plan.changes:
            return len(plan.changes[0].record.zone.name)
        return 0

    def __init__(self, config_file, max_workers=None, include_meta=False):
        self.log.info(b'__init__: config_file=%s', config_file)
        with open(config_file, b'r') as (fh):
            self.config = safe_load(fh, enforce_order=False)
        manager_config = self.config.get(b'manager', {})
        max_workers = manager_config.get(b'max_workers', 1) if max_workers is None else max_workers
        self.log.info(b'__init__:   max_workers=%d', max_workers)
        if max_workers > 1:
            self._executor = ThreadPoolExecutor(max_workers=max_workers)
        else:
            self._executor = MainThreadExecutor()
        self.include_meta = include_meta or manager_config.get(b'include_meta', False)
        self.log.info(b'__init__:   include_meta=%s', self.include_meta)
        self.log.debug(b'__init__:   configuring providers')
        self.providers = {}
        for provider_name, provider_config in self.config[b'providers'].items():
            try:
                _class = provider_config.pop(b'class')
            except KeyError:
                self.log.exception(b'Invalid provider class')
                raise ManagerException((b'Provider {} is missing class').format(provider_name))

            _class = self._get_named_class(b'provider', _class)
            kwargs = self._build_kwargs(provider_config)
            try:
                self.providers[provider_name] = _class(provider_name, **kwargs)
            except TypeError:
                self.log.exception(b'Invalid provider config')
                raise ManagerException((b'Incorrect provider config for {}').format(provider_name))

        zone_tree = {}
        for name in sorted(self.config[b'zones'].keys(), key=lambda s: s[::-1]):
            pieces = name[:-1].split(b'.')[::-1]
            where = zone_tree
            for piece in pieces:
                try:
                    where = where[piece]
                except KeyError:
                    where[piece] = {}
                    where = where[piece]

        self.zone_tree = zone_tree
        self.plan_outputs = {}
        plan_outputs = manager_config.get(b'plan_outputs', {b'logger': {b'class': b'octodns.provider.plan.PlanLogger', 
                       b'level': b'info'}})
        for plan_output_name, plan_output_config in plan_outputs.items():
            try:
                _class = plan_output_config.pop(b'class')
            except KeyError:
                self.log.exception(b'Invalid plan_output class')
                raise ManagerException((b'plan_output {} is missing class').format(plan_output_name))

            _class = self._get_named_class(b'plan_output', _class)
            kwargs = self._build_kwargs(plan_output_config)
            try:
                self.plan_outputs[plan_output_name] = _class(plan_output_name, **kwargs)
            except TypeError:
                self.log.exception(b'Invalid plan_output config')
                raise ManagerException((b'Incorrect plan_output config for {}').format(plan_output_name))

        return

    def _get_named_class(self, _type, _class):
        try:
            module_name, class_name = _class.rsplit(b'.', 1)
            module = import_module(module_name)
        except (ImportError, ValueError):
            self.log.exception(b'_get_{}_class: Unable to import module %s', _class)
            raise ManagerException((b'Unknown {} class: {}').format(_type, _class))

        try:
            return getattr(module, class_name)
        except AttributeError:
            self.log.exception(b'_get_{}_class: Unable to get class %s from module %s', class_name, module)
            raise ManagerException((b'Unknown {} class: {}').format(_type, _class))

    def _build_kwargs(self, source):
        kwargs = {}
        for k, v in source.items():
            try:
                if v.startswith(b'env/'):
                    try:
                        env_var = v[4:]
                        v = environ[env_var]
                    except KeyError:
                        self.log.exception(b'Invalid provider config')
                        raise ManagerException((b'Incorrect provider config, missing env var {}').format(env_var))

            except AttributeError:
                pass

            kwargs[k] = v

        return kwargs

    def configured_sub_zones(self, zone_name):
        pieces = zone_name[:-1].split(b'.')[::-1]
        where = self.zone_tree
        try:
            while pieces:
                where = where[pieces.pop(0)]

        except KeyError:
            self.log.debug(b'configured_sub_zones: unknown zone, %s, no subs', zone_name)
            return set()

        sub_zone_names = where.keys()
        self.log.debug(b'configured_sub_zones: subs=%s', sub_zone_names)
        return set(sub_zone_names)

    def _populate_and_plan(self, zone_name, sources, targets):
        self.log.debug(b'sync:   populating, zone=%s', zone_name)
        zone = Zone(zone_name, sub_zones=self.configured_sub_zones(zone_name))
        for source in sources:
            source.populate(zone)

        self.log.debug(b'sync:   planning, zone=%s', zone_name)
        plans = []
        for target in targets:
            if self.include_meta:
                meta = Record.new(zone, b'octodns-meta', {b'type': b'TXT', 
                   b'ttl': 60, 
                   b'value': (b'provider={}').format(target.id)})
                zone.add_record(meta, replace=True)
            plan = target.plan(zone)
            if plan:
                plans.append((target, plan))

        return plans

    def sync(self, eligible_zones=[], eligible_targets=[], dry_run=True, force=False):
        self.log.info(b'sync: eligible_zones=%s, eligible_targets=%s, dry_run=%s, force=%s', eligible_zones, eligible_targets, dry_run, force)
        zones = self.config[b'zones'].items()
        if eligible_zones:
            zones = [ z for z in zones if z[0] in eligible_zones ]
        futures = []
        for zone_name, config in zones:
            self.log.info(b'sync:   zone=%s', zone_name)
            try:
                sources = config[b'sources']
            except KeyError:
                raise ManagerException((b'Zone {} is missing sources').format(zone_name))

            try:
                targets = config[b'targets']
            except KeyError:
                raise ManagerException((b'Zone {} is missing targets').format(zone_name))

            if eligible_targets:
                targets = [ t for t in targets if t in eligible_targets ]
            if not targets:
                self.log.info(b'sync:   no eligible targets, skipping')
                continue
            self.log.info(b'sync:   sources=%s -> targets=%s', sources, targets)
            try:
                collected = []
                for source in sources:
                    collected.append(self.providers[source])

                sources = collected
            except KeyError:
                raise ManagerException((b'Zone {}, unknown source: {}').format(zone_name, source))

            try:
                trgs = []
                for target in targets:
                    trg = self.providers[target]
                    if not isinstance(trg, BaseProvider):
                        raise ManagerException((b'{} - "{}" does not support targeting').format(trg, target))
                    trgs.append(trg)

                targets = trgs
            except KeyError:
                raise ManagerException((b'Zone {}, unknown target: {}').format(zone_name, target))

            futures.append(self._executor.submit(self._populate_and_plan, zone_name, sources, targets))

        plans = [ p for f in futures for p in f.result() ]
        plans.sort(key=self._plan_keyer, reverse=True)
        for output in self.plan_outputs.values():
            output.run(plans=plans, log=self.log)

        if not force:
            self.log.debug(b'sync:   checking safety')
            for target, plan in plans:
                plan.raise_if_unsafe()

        if dry_run:
            return 0
        total_changes = 0
        self.log.debug(b'sync:   applying')
        zones = self.config[b'zones']
        for target, plan in plans:
            zone_name = plan.existing.name
            if zones[zone_name].get(b'always-dry-run', False):
                self.log.info(b'sync: zone=%s skipping always-dry-run', zone_name)
                continue
            total_changes += target.apply(plan)

        self.log.info(b'sync:   %d total changes', total_changes)
        return total_changes

    def compare(self, a, b, zone):
        """
        Compare zone data between 2 sources.

        Note: only things supported by both sources will be considered
        """
        self.log.info(b'compare: a=%s, b=%s, zone=%s', a, b, zone)
        try:
            a = [ self.providers[source] for source in a ]
            b = [ self.providers[source] for source in b ]
        except KeyError as e:
            raise ManagerException((b'Unknown source: {}').format(e.args[0]))

        sub_zones = self.configured_sub_zones(zone)
        za = Zone(zone, sub_zones)
        for source in a:
            source.populate(za)

        zb = Zone(zone, sub_zones)
        for source in b:
            source.populate(zb)

        return zb.changes(za, _AggregateTarget(a + b))

    def dump(self, zone, output_dir, lenient, split, source, *sources):
        """
        Dump zone data from the specified source
        """
        self.log.info(b'dump: zone=%s, sources=%s', zone, sources)
        sources = [
         source] + list(sources)
        try:
            sources = [ self.providers[s] for s in sources ]
        except KeyError as e:
            raise ManagerException((b'Unknown source: {}').format(e.args[0]))

        clz = YamlProvider
        if split:
            clz = SplitYamlProvider
        target = clz(b'dump', output_dir)
        zone = Zone(zone, self.configured_sub_zones(zone))
        for source in sources:
            source.populate(zone, lenient=lenient)

        plan = target.plan(zone)
        if plan is None:
            plan = Plan(zone, zone, [], False)
        target.apply(plan)
        return

    def validate_configs(self):
        for zone_name, config in self.config[b'zones'].items():
            zone = Zone(zone_name, self.configured_sub_zones(zone_name))
            try:
                sources = config[b'sources']
            except KeyError:
                raise ManagerException((b'Zone {} is missing sources').format(zone_name))

            try:
                collected = []
                for source in sources:
                    collected.append(self.providers[source])

                sources = collected
            except KeyError:
                raise ManagerException((b'Zone {}, unknown source: {}').format(zone_name, source))

            for source in sources:
                if isinstance(source, YamlProvider):
                    source.populate(zone)