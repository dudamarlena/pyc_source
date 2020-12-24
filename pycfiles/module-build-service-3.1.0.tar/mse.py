# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breilly/git/fm-orchestrator/module_build_service/utils/mse.py
# Compiled at: 2019-12-12 15:53:56
from module_build_service import log, models, Modulemd, conf
from module_build_service.errors import StreamAmbigous
from module_build_service.errors import UnprocessableEntity
from module_build_service.mmd_resolver import MMDResolver
from module_build_service.utils.general import deps_to_dict, mmd_to_str
from module_build_service.resolver import GenericResolver

def expand_single_mse_streams(db_session, name, streams, default_streams=None, raise_if_stream_ambigous=False):
    """
    Helper method for `expand_mse_stream()` expanding single name:[streams].
    Returns list of expanded streams.

    :param db_session: SQLAlchemy DB session.
    :param str name: Name of the module which will be expanded.
    :param streams: List of streams to expand.
    :type streams: list[str]
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    """
    default_streams = default_streams or {}
    streams_is_blacklist = all(stream.startswith('-') for stream in streams)
    if streams_is_blacklist or len(streams) == 0:
        if name in default_streams:
            expanded_streams = [
             default_streams[name]]
        elif raise_if_stream_ambigous:
            raise StreamAmbigous('There are multiple streams to choose from for module %s.' % name)
        else:
            builds = models.ModuleBuild.get_last_build_in_all_streams(db_session, name)
            expanded_streams = [ build.stream for build in builds ]
    else:
        expanded_streams = []
    for stream in streams:
        if stream.startswith('-'):
            if streams_is_blacklist and stream[1:] in expanded_streams:
                expanded_streams.remove(stream[1:])
        else:
            expanded_streams.append(stream)

    if len(expanded_streams) > 1:
        if name in default_streams:
            expanded_streams = [
             default_streams[name]]
        elif raise_if_stream_ambigous:
            raise StreamAmbigous('There are multiple streams %r to choose from for module %s.' % (
             expanded_streams, name))
    return expanded_streams


def expand_mse_streams(db_session, mmd, default_streams=None, raise_if_stream_ambigous=False):
    """
    Expands streams in both buildrequires/requires sections of MMD.

    :param db_session: SQLAlchemy DB session.
    :param Modulemd.ModuleStream mmd: Modulemd metadata with original unexpanded module.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    """
    for deps in mmd.get_dependencies():
        new_deps = Modulemd.Dependencies()
        for name in deps.get_runtime_modules():
            streams = deps.get_runtime_streams(name)
            new_streams = expand_single_mse_streams(db_session, name, streams, default_streams, raise_if_stream_ambigous)
            if not new_streams:
                new_deps.set_empty_runtime_dependencies_for_module(name)
            else:
                for stream in new_streams:
                    new_deps.add_runtime_stream(name, stream)

        for name in deps.get_buildtime_modules():
            streams = deps.get_buildtime_streams(name)
            new_streams = expand_single_mse_streams(db_session, name, streams, default_streams, raise_if_stream_ambigous)
            if not new_streams:
                new_deps.set_empty_buildtime_dependencies_for_module(name)
            else:
                for stream in new_streams:
                    new_deps.add_buildtime_stream(name, stream)

        mmd.remove_dependencies(deps)
        mmd.add_dependencies(new_deps)


def _get_mmds_from_requires(db_session, requires, mmds, recursive=False, default_streams=None, raise_if_stream_ambigous=False, base_module_mmds=None):
    """
    Helper method for get_mmds_required_by_module_recursively returning
    the list of module metadata objects defined by `requires` dict.

    :param db_session: SQLAlchemy database session.
    :param dict requires: requires or buildrequires in the form {module: [streams]}
    :param mmds: Dictionary with already handled name:streams as a keys and lists
        of resulting mmds as values.
    :param recursive: If True, the requires are checked recursively.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    :param list base_module_mmds: List of modulemd metadata instances. When set, the
        returned list contains MMDs build against each base module defined in
        `base_module_mmds` list.
    :return: Dict with name:stream as a key and list with mmds as value.
    """
    default_streams = default_streams or {}
    added_mmds = {}
    resolver = GenericResolver.create(db_session, conf)
    for name, streams in requires.items():
        if name in conf.base_module_names:
            continue
        streams_to_try = streams
        if name in default_streams:
            streams_to_try = [
             default_streams[name]]
        else:
            if len(streams_to_try) > 1 and raise_if_stream_ambigous:
                raise StreamAmbigous('There are multiple streams %r to choose from for module %s.' % (
                 streams_to_try, name))
            for stream in streams:
                ns = '%s:%s' % (name, stream)
                if ns not in mmds:
                    mmds[ns] = []
                if ns not in added_mmds:
                    added_mmds[ns] = []
                if base_module_mmds:
                    for base_module_mmd in base_module_mmds:
                        mmds[ns] += resolver.get_buildrequired_modulemds(name, stream, base_module_mmd)

                else:
                    mmds[ns] = resolver.get_module_modulemds(name, stream, strict=True)
                added_mmds[ns] += mmds[ns]

    if recursive:
        for mmd_list in added_mmds.values():
            for mmd in mmd_list:
                for deps in mmd.get_dependencies():
                    deps_dict = deps_to_dict(deps, 'runtime')
                    mmds = _get_mmds_from_requires(db_session, deps_dict, mmds, True, base_module_mmds=base_module_mmds)

    return mmds


def get_compatible_base_module_mmds(resolver, base_mmd, ignore_ns=None):
    """
    Returns dict containing the base modules compatible with `base_mmd` grouped by their state.

    :param GenericResolver resolver: GenericResolver instance.
    :param Modulemd base_mmd: Modulemd instant to return compatible modules for.
    :param set ignore_ns: When set, defines the name:stream of base modules which will be ignored
        by this function and therefore not returned.
    :return dict: Dictionary with module's state name as a key and list of Modulemd objects for
        each compatible base module in that state. For example:
            {
                "ready": [base_mmd_1, base_mmd_2]
                "garbage": [base_mmd_3]
            }
        The input `base_mmd` is always included in the result in "ready" state.
    """
    ret = {'ready': [], 'garbage': []}
    ret['ready'].append(base_mmd)
    ns = (':').join([base_mmd.get_module_name(), base_mmd.get_stream_name()])
    if not ignore_ns:
        seen = set() if 1 else set(ignore_ns)
        seen.add(ns)
        xmd = base_mmd.get_xmd()
        virtual_streams = xmd.get('mbs', {}).get('virtual_streams')
        return virtual_streams or ret
    if conf.allow_only_compatible_base_modules:
        stream_version_lte = True
        states = ['ready']
    else:
        stream_version_lte = False
        states = ['ready', 'garbage']
    for state in states:
        mmds = resolver.get_compatible_base_module_modulemds(base_mmd, stream_version_lte, virtual_streams, [
         models.BUILD_STATES[state]])
        ret_chunk = []
        for mmd_ in mmds:
            mmd_ns = (':').join([mmd_.get_module_name(), mmd_.get_stream_name()])
            if mmd_ns not in seen:
                ret_chunk.append(mmd_)
                seen.add(mmd_ns)

        ret[state] += ret_chunk

    return ret


def get_base_module_mmds(db_session, mmd):
    """
    Returns list of MMDs of base modules buildrequired by `mmd` including the compatible
    old versions of the base module based on the stream version.

    :param Modulemd mmd: Input modulemd metadata.
    :rtype: dict with lists of Modulemd
    :return: Dict with "ready" or "garbage" state name as a key and list of MMDs of base modules
        buildrequired by `mmd` as a value.
    """
    seen = set()
    ret = {'ready': [], 'garbage': []}
    resolver = GenericResolver.create(db_session, conf)
    for deps in mmd.get_dependencies():
        buildrequires = {module:deps.get_buildtime_streams(module) for module in deps.get_buildtime_modules()}
        for name in conf.base_module_names:
            if name not in buildrequires.keys():
                continue
            sorted_desc_streams = sorted(buildrequires[name], reverse=True, key=models.ModuleBuild.get_stream_version)
            for stream in sorted_desc_streams:
                ns = (':').join([name, stream])
                if ns in seen:
                    continue
                mmds = resolver.get_module_modulemds(name, stream)
                if not mmds:
                    continue
                base_mmd = mmds[0]
                new_ret = get_compatible_base_module_mmds(resolver, base_mmd, ignore_ns=seen)
                for state in new_ret.keys():
                    for mmd_ in new_ret[state]:
                        mmd_ns = (':').join([mmd_.get_module_name(), mmd_.get_stream_name()])
                        seen.add(mmd_ns)

                    ret[state] += new_ret[state]

            break

    return ret


def get_mmds_required_by_module_recursively(db_session, mmd, default_streams=None, raise_if_stream_ambigous=False):
    """
    Returns the list of Module metadata objects of all modules required while
    building the module defined by `mmd` module metadata. This presumes the
    module metadata streams are expanded using `expand_mse_streams(...)`
    method.

    This method finds out latest versions of all the build-requires of
    the `mmd` module and then also all contexts of these latest versions.

    For each build-required name:stream:version:context module, it checks
    recursively all the "requires" and finds the latest version of each
    required module and also all contexts of these latest versions.

    :param db_session: SQLAlchemy database session.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    :rtype: list of Modulemd metadata
    :return: List of all modulemd metadata of all modules required to build
        the module `mmd`.
    """
    mmds = {}
    base_module_mmds = get_base_module_mmds(db_session, mmd)
    if not base_module_mmds['ready']:
        base_module_choices = (' or ').join(conf.base_module_names)
        raise UnprocessableEntity(('None of the base module ({}) streams in the buildrequires section could be found').format(base_module_choices))
    for base_module in base_module_mmds['ready']:
        ns = (':').join([base_module.get_module_name(), base_module.get_stream_name()])
        mmds.setdefault(ns, [])
        mmds[ns].append(base_module)

    all_base_module_mmds = base_module_mmds['ready'] + base_module_mmds['garbage']
    for deps in mmd.get_dependencies():
        deps_dict = deps_to_dict(deps, 'buildtime')
        mmds = _get_mmds_from_requires(db_session, deps_dict, mmds, False, default_streams, raise_if_stream_ambigous, all_base_module_mmds)

    for mmd_key in list(mmds.keys()):
        for mmd in mmds[mmd_key]:
            for deps in mmd.get_dependencies():
                deps_dict = deps_to_dict(deps, 'runtime')
                mmds = _get_mmds_from_requires(db_session, deps_dict, mmds, True, default_streams, raise_if_stream_ambigous, all_base_module_mmds)

    res = []
    for ns, mmds_list in mmds.items():
        if len(mmds_list) == 0:
            raise UnprocessableEntity('Cannot find any module builds for %s' % ns)
        res += mmds_list

    return res


def generate_expanded_mmds(db_session, mmd, raise_if_stream_ambigous=False, default_streams=None):
    """
    Returns list with MMDs with buildrequires and requires set according
    to module stream expansion rules. These module metadata can be directly
    built using MBS.

    :param db_session: SQLAlchemy DB session.
    :param Modulemd.ModuleStream mmd: Modulemd metadata with original unexpanded module.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    """
    if not default_streams:
        default_streams = {}
    current_mmd = mmd.copy()
    current_mmd.set_context(None)
    expand_mse_streams(db_session, current_mmd, default_streams, raise_if_stream_ambigous)
    mmd_resolver = MMDResolver()
    mmds_for_resolving = get_mmds_required_by_module_recursively(db_session, current_mmd, default_streams, raise_if_stream_ambigous)
    for m in mmds_for_resolving:
        mmd_resolver.add_modules(m)

    nsvcs_to_solve = [ m.get_nsvc() for m in mmds_for_resolving ]
    log.info('Starting resolving with following input modules: %r', nsvcs_to_solve)
    requires_combinations = mmd_resolver.solve(current_mmd)
    log.info('Resolving done, possible requires: %r', requires_combinations)
    mmds = []
    for requires in requires_combinations:
        mmd_copy = mmd.copy()
        xmd = mmd_copy.get_xmd()
        dependencies_id = None
        self_nsvca = None
        req_name_stream = {}
        for nsvca in requires:
            req_name, req_stream, _, req_context, req_arch = nsvca.split(':')
            if req_arch == 'src':
                assert req_name == current_mmd.get_module_name()
                assert req_stream == current_mmd.get_stream_name()
                assert dependencies_id is None
                assert self_nsvca is None
                dependencies_id = int(req_context)
                self_nsvca = nsvca
                continue
            req_name_stream[req_name] = req_stream

        if dependencies_id is None or self_nsvca is None:
            raise RuntimeError('%s:%s not found in requires %r' % (
             current_mmd.get_module_name(), current_mmd.get_stream_name(), requires))
        new_deps = Modulemd.Dependencies()
        deps = mmd_copy.get_dependencies()[dependencies_id]
        deps_requires = deps_to_dict(deps, 'runtime')
        deps_buildrequires = deps_to_dict(deps, 'buildtime')
        for req_name, req_streams in deps_requires.items():
            if req_name not in deps_buildrequires:
                if not req_streams:
                    new_deps.set_empty_runtime_dependencies_for_module(req_name)
                else:
                    for req_stream in req_streams:
                        new_deps.add_runtime_stream(req_name, req_stream)

            elif set(req_streams) != set(deps_buildrequires[req_name]):
                if not req_streams:
                    new_deps.set_empty_runtime_dependencies_for_module(req_name)
                else:
                    for req_stream in req_streams:
                        new_deps.add_runtime_stream(req_name, req_stream)

                new_deps.add_buildtime_stream(req_name, req_name_stream[req_name])
            else:
                new_deps.add_runtime_stream(req_name, req_name_stream[req_name])
                new_deps.add_buildtime_stream(req_name, req_name_stream[req_name])

        for req_name, req_streams in deps_buildrequires.items():
            if req_name not in deps_requires:
                new_deps.add_buildtime_stream(req_name, req_name_stream[req_name])

        mmd_copy.remove_dependencies(deps)
        mmd_copy.add_dependencies(new_deps)
        br_list = []
        for nsvca in requires:
            if nsvca == self_nsvca:
                continue
            nsvc = (':').join(nsvca.split(':')[:-1])
            br_list.append(nsvc)

        if 'mbs' not in xmd:
            xmd['mbs'] = {}
        resolver = GenericResolver.create(db_session, conf)
        xmd['mbs']['buildrequires'] = resolver.resolve_requires(br_list)
        xmd['mbs']['mse'] = True
        mmd_copy.set_xmd(xmd)
        context = models.ModuleBuild.contexts_from_mmd(mmd_to_str(mmd_copy)).context
        mmd_copy.set_context(context)
        mmds.append(mmd_copy)

    return mmds