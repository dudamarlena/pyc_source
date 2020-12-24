# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/backend.py
# Compiled at: 2018-02-20 08:15:54
# Size of source mod 2**32: 26578 bytes
import koji, os, threading, shutil, six, productmd.compose, productmd.common
from datetime import datetime
from odcs.server import log, conf, app, db
from odcs.server.models import Compose, COMPOSE_STATES, COMPOSE_FLAGS
from odcs.server.pungi import Pungi, PungiConfig, PungiSourceType
from odcs.server.pulp import Pulp
from concurrent.futures import ThreadPoolExecutor
import glob, odcs.server.utils, odcs.server.pdc, defusedxml.ElementTree

class BackendThread(object):
    __doc__ = '\n    Base BackendThread class.\n\n    The `BackendThread.do_work(...)` is called repeatedly after `timeout`\n    seconds.\n    '

    def __init__(self, timeout=1):
        """
        Creates new BackendThread instance.

        :param int timeout: Timeout in seconds after which do_work is called.
        """
        self.thread = None
        self.exit = False
        self.exit_cond = threading.Condition()
        self.timeout = timeout

    def do_work(self):
        """
        Reimplement this method in your own BackendThread subclass.
        This method is called every `timeout` seconds.
        """
        raise NotImplemented('do_work() method not implemented')

    def _run(self):
        """
        Main "run" method of a thread. Calls `do_work()` after `self.timeout`
        seconds. Stops then `stop()` is called.
        """
        while not self.exit:
            try:
                self.do_work()
            except Exception:
                log.exception('Exception in backend thread')
                try:
                    db.session.rollback()
                except Exception:
                    log.exception('Cannot rollback DB session')

            if self.exit:
                break
            self.exit_cond.acquire()
            self.exit_cond.wait(float(self.timeout))
            self.exit_cond.release()

    def join(self):
        """
        Waits until the thread terminates.
        """
        self.thread.join()

    def stop(self):
        """
        Stops the thread.
        """
        self.exit = True
        self.exit_cond.acquire()
        self.exit_cond.notify()
        self.exit_cond.release()

    def start(self):
        """
        Starts the thread.
        """
        self.thread = threading.Thread(target=(self._run))
        self.thread.setDaemon(True)
        self.thread.start()


class RemoveExpiredComposesThread(BackendThread):
    __doc__ = '\n    Thread used to remove old expired composes.\n    '

    def __init__(self):
        super(RemoveExpiredComposesThread, self).__init__(10)

    def _remove_compose_dir(self, toplevel_dir):
        """
        Removes the compose toplevel_dir symlink together with the real
        path it points to.
        """
        if not os.path.exists(toplevel_dir):
            log.warn('Cannot remove directory %s, it does not exist', toplevel_dir)
            return
        else:
            if os.path.realpath(toplevel_dir) != toplevel_dir:
                targetpath = os.path.realpath(toplevel_dir)
                os.unlink(toplevel_dir)
                if os.path.exists(targetpath):
                    shutil.rmtree(targetpath)
            else:
                shutil.rmtree(toplevel_dir)

    def _get_compose_id_from_path(self, path):
        """
        Returns the ID of compose from directory path in conf.target_dir.
        """
        parts = os.path.basename(path).split('-')
        while parts and parts[0] != 'odcs':
            del parts[0]

        if not parts or len(parts) < 2 or not parts[1].isdigit():
            log.error('Directory %s is not valid compose directory', path)
            return
        else:
            return int(parts[1])

    def do_work(self):
        """
        Checks for the expired composes and removes them.
        """
        log.info('Checking for expired composes')
        composes = Compose.composes_to_expire()
        for compose in composes:
            log.info('%r: Removing compose', compose)
            compose.state = COMPOSE_STATES['removed']
            compose.state_reason = 'Compose is expired'
            compose.time_removed = datetime.utcnow()
            db.session.commit()
            if not compose.reused_id:
                self._remove_compose_dir(compose.toplevel_dir)

        odcs_paths = []
        for dirname in ('latest-odcs-*', 'odcs-*'):
            path = os.path.join(conf.target_dir, dirname)
            odcs_paths += glob.glob(path)

        for path in odcs_paths:
            if not os.path.isdir(path):
                pass
            else:
                compose_id = self._get_compose_id_from_path(path)
                if not compose_id:
                    pass
                else:
                    composes = Compose.query.filter(Compose.id == compose_id).all()
            if not composes:
                log.info('Removing data of compose %d - it is not in database: %s', compose_id, path)
                self._remove_compose_dir(path)
            else:
                compose = composes[0]
                if compose.state == COMPOSE_STATES['removed']:
                    log.info('%r: Removing data of compose - it has already expired some time ago: %s', compose_id, path)
                    self._remove_compose_dir(path)
                    continue


def create_koji_session():
    """
    Creates and returns new koji_session based on the `conf.koji_profile`.
    """
    koji_module = koji.get_profile_module(conf.koji_profile)
    session_opts = {}
    for key in ('krbservice', 'timeout', 'keepalive', 'max_retries', 'retry_interval',
                'anon_retry', 'offline_retry', 'offline_retry_interval', 'debug',
                'debug_xmlrpc', 'krb_rdns', 'use_fast_upload'):
        value = getattr(koji_module.config, key, None)
        if value is not None:
            session_opts[key] = value

    koji_session = koji.ClientSession(koji_module.config.server, session_opts)
    return koji_session


def koji_get_inherited_tags(koji_session, tag, tags=None):
    """
    Returns list of ids of all tags the tag `tag` inherits from.
    """
    info = koji_session.getTag(tag)
    ids = [info['id']]
    seen_tags = tags or set()
    inheritance_data = koji_session.getInheritanceData(tag)
    inheritance_data = [data for data in inheritance_data if data['parent_id'] not in seen_tags]
    for inherited in inheritance_data:
        parent_tag_id = inherited['parent_id']
        seen_tags.add(parent_tag_id)
        info = koji_session.getTag(parent_tag_id)
        if info is None:
            log.error('Cannot get info about Koji tag %s', parent_tag_id)
            return []
        ids += koji_get_inherited_tags(koji_session, info['name'], seen_tags)

    return ids


def resolve_compose(compose):
    """
    Resolves various general compose values to the real ones. For example:
    - Sets the koji_event based on the current Koji event, so it can be used
      to generate the compose and we can find out if we can reuse that compose
      later
    - For MODULE PungiSourceType, resolves the modules without the "release"
      field to latest module release using PDC.
    """
    if compose.source_type == PungiSourceType.REPO:
        repomd = os.path.join(compose.source, 'repodata', 'repomd.xml')
        e = defusedxml.ElementTree.parse(repomd).getroot()
        revision = e.find('{http://linux.duke.edu/metadata/repo}revision').text
        compose.koji_event = int(revision)
    else:
        if compose.source_type == PungiSourceType.KOJI_TAG:
            if not compose.koji_event:
                koji_session = create_koji_session()
                compose.koji_event = int(koji_session.getLastEvent()['id'])
        elif compose.source_type == PungiSourceType.MODULE:
            pdc = odcs.server.pdc.PDC(conf)
            modules = compose.source.split(' ')
            specified_modules = []
            for module in modules:
                variant_dict = pdc.variant_dict_from_str(module)
                specified_modules.append((pdc.get_latest_module)(**variant_dict))

            expand = not compose.flags & COMPOSE_FLAGS['no_deps']
            new_modules = pdc.validate_module_list(specified_modules, expand=expand)
            uids = sorted(('{variant_id}:{variant_version}:{variant_release}'.format)(**m) for m in new_modules)
            compose.source = ' '.join(uids)


def get_reusable_compose(compose):
    """
    Returns the compose in the "done" state which contains the same artifacts
    and results as the compose `compose` and therefore could be reused instead
    of generating new one.
    """
    if compose.source_type == PungiSourceType.RAW_CONFIG:
        return
    composes = db.session.query(Compose).filter(Compose.state == COMPOSE_STATES['done'], Compose.source_type == compose.source_type).all()
    for old_compose in composes:
        if old_compose.reused_id:
            pass
        else:
            packages = set(compose.packages.split(' ')) if compose.packages else set()
            old_packages = set(old_compose.packages.split(' ')) if old_compose.packages else set()
        if packages != old_packages:
            log.debug('%r: Cannot reuse %r - packages not same', compose, old_compose)
        else:
            source = set(compose.source.split(' '))
            old_source = set(old_compose.source.split(' '))
            if source != old_source:
                log.debug('%r: Cannot reuse %r - sources not same', compose, old_compose)
            elif compose.flags != old_compose.flags:
                log.debug('%r: Cannot reuse %r - flags not same, %d != %d', compose, old_compose, compose.flags, old_compose.flags)
            elif compose.results != old_compose.results:
                log.debug('%r: Cannot reuse %r - results not same, %d != %d', compose, old_compose, compose.results, old_compose.results)
            else:
                sigkeys = set(compose.sigkeys.split(' ')) if compose.sigkeys else set()
                old_sigkeys = set(old_compose.sigkeys.split(' ')) if old_compose.sigkeys else set()
                if sigkeys != old_sigkeys:
                    log.debug('%r: Cannot reuse %r - sigkeys not same', compose, old_compose)
                else:
                    arches = set(compose.arches.split(' ')) if compose.arches else set()
                    old_arches = set(old_compose.arches.split(' ')) if old_compose.arches else set()
                    if arches != old_arches:
                        log.debug('%r: Cannot reuse %r - arches not same', compose, old_compose)
                    else:
                        if compose.source_type == PungiSourceType.KOJI_TAG:
                            koji_session = create_koji_session()
                            tags = koji_get_inherited_tags(koji_session, compose.source)
                            if not tags:
                                continue
                            changed = koji_session.tagChangedSinceEvent(old_compose.koji_event, tags)
                            if changed:
                                log.debug('%r: Cannot reuse %r - one of the tags changed since previous compose: %r', compose, old_compose, tags)
                                continue
                        else:
                            if compose.koji_event != old_compose.koji_event:
                                log.debug('%r: Cannot reuse %r - koji_events not same, %d != %d', compose, old_compose, compose.koji_event, old_compose.koji_event)
                                continue
                        return old_compose


def reuse_compose(compose, compose_to_reuse):
    """
    Changes the attribute of `compose` in a way it reuses
    the `compose_to_reuse`.
    """
    compose.reused_id = compose_to_reuse.id
    compose.time_to_expire = max(compose.time_to_expire, compose_to_reuse.time_to_expire)
    compose_to_reuse.time_to_expire = compose.time_to_expire


def _write_repo_file(compose, data=None):
    """
    Writes main repo file for a resulting compose containing the `data`.
    If `data` is not provided, the default one pointing to pungi compose
    will be generated.
    """
    if not data:
        baseurl = os.path.join(compose.result_repo_url, '$basearch', 'os')
        data = '[%s]\nname=ODCS repository for compose %s\nbaseurl=%s\ntype=rpm-md\nskip_if_unavailable=False\ngpgcheck=0\nrepo_gpgcheck=0\nenabled=1\nenabled_metadata=1\n' % (compose.name, compose.name, baseurl)
    dirname = os.path.dirname(compose.result_repofile_path)
    odcs.server.utils.makedirs(dirname)
    with open(compose.result_repofile_path, 'w') as (f):
        f.write(data)


def generate_pulp_compose(compose):
    """
    Generates the compose of PULP type - this basically means only
    repo file pointing to data in pulp.
    """
    content_sets = compose.source.split(' ')
    pulp = Pulp(server_url=(conf.pulp_server_url), username=(conf.pulp_username),
      password=(conf.pulp_password))
    repofile = ''
    for arch in compose.arches.split(' '):
        repos = pulp.get_repo_urls_from_content_sets(content_sets, arch)
        if len(repos) != len(content_sets):
            err = 'Failed to find all the content_sets %r in the Pulp, found only %r' % (
             content_sets, repos.keys())
            log.error(err)
            raise ValueError(err)
        for name in sorted(repos.keys()):
            url = repos[name]
            r = '\n[%s]\nname=%s\nbaseurl=%s\nenabled=1\ngpgcheck=0\n' % (name, name, url)
            repofile += r

    _write_repo_file(compose, repofile)
    compose.state = COMPOSE_STATES['done']
    compose.state_reason = 'Compose is generated successfully'
    log.info('%r: Compose done', compose)
    compose.time_done = datetime.utcnow()
    db.session.add(compose)
    db.session.commit()


def generate_pungi_compose(compose):
    """
    Generates the compose of KOJI, TAG, or REPO type using the Pungi tool.
    """
    packages = compose.packages
    if packages:
        packages = packages.split(' ')
    resolve_compose(compose)
    compose_to_reuse = get_reusable_compose(compose)
    if compose_to_reuse:
        log.info('%r: Reusing compose %r', compose, compose_to_reuse)
        reuse_compose(compose, compose_to_reuse)
    else:
        if compose.source_type == PungiSourceType.RAW_CONFIG:
            source_name, source_hash = compose.source.split('#')
            url_template = conf.raw_config_urls[source_name]
            pungi_cfg = str(url_template % source_hash)
        else:
            pungi_cfg = PungiConfig((compose.name), '1', (compose.source_type), (compose.source),
              packages=packages, sigkeys=(compose.sigkeys),
              results=(compose.results),
              arches=(compose.arches.split(' ')))
            if compose.flags & COMPOSE_FLAGS['no_deps']:
                pungi_cfg.gather_method = 'nodeps'
            if compose.flags & COMPOSE_FLAGS['no_inheritance']:
                pungi_cfg.pkgset_koji_inherit = False
            koji_event = None
            if compose.source_type == PungiSourceType.KOJI_TAG:
                koji_event = compose.koji_event
            pungi = Pungi(pungi_cfg, koji_event)
            pungi.run(compose)
            _write_repo_file(compose)
    compose.state = COMPOSE_STATES['done']
    compose.state_reason = 'Compose is generated successfully'
    log.info('%r: Compose done', compose)
    compose.time_done = datetime.utcnow()
    db.session.add(compose)
    db.session.commit()


def validate_pungi_compose(compose):
    """
    Validate the compose is generated by pungi as expected.
    """
    if compose.packages:
        packages = compose.packages.split()
        pungi_compose = productmd.compose.Compose(compose.toplevel_dir)
        rm = pungi_compose.rpms.rpms
        rpm_nevras = []
        for variant in rm:
            for arch in rm[variant]:
                for srpm_nevra, data in six.iteritems(rm[variant][arch]):
                    for rpm_nevra, data in six.iteritems(rm[variant][arch][srpm_nevra]):
                        if data['category'] == 'source':
                            pass
                        else:
                            rpm_nevras.append(rpm_nevra)

        rpms = set([productmd.common.parse_nvra(n)['name'] for n in rpm_nevras])
        not_found = []
        for pkg in packages:
            if pkg not in rpms:
                not_found.append(pkg)

        if not_found:
            msg = 'The following requested packages are not present in the generated compose: %s.' % ' '.join(not_found)
            log.error(msg)
            raise RuntimeError(msg)


def generate_compose(compose_id, lost_compose=False):
    """
    Generates the compose defined by its `compose_id`. It is run by
    ThreadPoolExecutor from the ComposerThread.
    """
    compose = None
    with app.app_context():
        try:
            compose = Compose.query.filter(Compose.id == compose_id).one()
            log.info('%r: Starting compose generation', compose)
            if compose.source_type == PungiSourceType.PULP:
                generate_pulp_compose(compose)
            else:
                generate_pungi_compose(compose)
                validate_pungi_compose(compose)
        except Exception as e:
            if compose:
                log.exception('%r: Error while generating compose', compose)
            else:
                log.exception('Error while generating compose %d', compose_id)
            compose.state = COMPOSE_STATES['failed']
            compose.state_reason = 'Error while generating compose: %s' % str(e)
            compose.time_done = datetime.utcnow()
            db.session.add(compose)
            db.session.commit()

        compose = Compose.query.filter(Compose.id == compose_id).one()
        if compose:
            if compose.reused_id is None:
                if compose.source_type != PungiSourceType.PULP:
                    try:
                        log.info('Running hardlink to consolidate duplicate files in compose target dir')
                        odcs.server.utils.hardlink(conf.target_dir)
                    except Exception as ex:
                        log.warn(('Error while running hardlink on system: %s' % ex.message), exc_info=True)


class ComposerThread(BackendThread):
    __doc__ = '\n    Thread used to query the database for composes in "wait" state and\n    generating the composes using Pungi.\n    '

    def __init__(self):
        super(ComposerThread, self).__init__(1)
        self.executor = ThreadPoolExecutor(conf.num_concurrent_pungi)
        self.currently_generating = []

    def _generate_new_compose(self, compose):
        """
        Adds the compose to queue of composes to generate, so
        the ThreadPoolExecutor can start working on it.
        """
        compose.state = COMPOSE_STATES['generating']
        compose.state_reason = 'Compose thread started'
        db.session.add(compose)
        db.session.commit()
        self.currently_generating.append(compose.id)
        self.executor.submit(generate_compose, compose.id)

    def generate_new_composes(self):
        """
        Gets all the composes in "wait" state. Generates them using Pungi
        by calling `generate_compose(...)` in ThreadPoolExecutor.
        """
        composes = Compose.query.filter(Compose.state == COMPOSE_STATES['wait']).all()
        for compose in composes:
            log.info('%r: Going to start compose generation.', compose)
            self._generate_new_compose(compose)

    def generate_lost_composes(self):
        """
        Gets all the composes in "generating" state and continues with
        the generation process.

        This method is here to handle situation where the ODCS is restarted
        in the middle of compose generation.
        """
        composes = Compose.query.filter(Compose.state == COMPOSE_STATES['generating']).all()
        for compose in composes:
            if compose.id in self.currently_generating:
                pass
            else:
                log.info('%r: Going to regenerate lost compose.', compose)
                self._generate_new_compose(compose)

    def refresh_currently_generating(self):
        """
        Checks the status of all composes in self.currently_generating
        and removes those which have been already done from this list.
        """
        new_currently_generating_list = []
        for compose_id in self.currently_generating:
            compose = Compose.query.filter(Compose.id == compose_id).one()
            if compose.state != COMPOSE_STATES['generating']:
                pass
            else:
                new_currently_generating_list.append(compose_id)

        self.currently_generating = new_currently_generating_list

    def do_work(self):
        """
        Gets all the composes in "wait" state. Generates them using Pungi
        by calling `generate_compose(...)` in ThreadPoolExecutor.
        """
        self.generate_lost_composes()
        self.generate_new_composes()
        self.refresh_currently_generating()


def run_backend():
    """
    Runs the backend.
    """
    while True:
        remove_expired_composes_thread = RemoveExpiredComposesThread()
        composer_thread = ComposerThread()
        try:
            remove_expired_composes_thread.start()
            composer_thread.start()
            remove_expired_composes_thread.join()
            composer_thread.join()
        except KeyboardInterrupt:
            remove_expired_composes_thread.stop()
            composer_thread.stop()
            remove_expired_composes_thread.join()
            composer_thread.join()
            return 0
        except Exception:
            log.exception('Exception in backend')
            remove_expired_composes_thread.stop()
            composer_thread.stop()
            remove_expired_composes_thread.join()
            composer_thread.join()

    return 0