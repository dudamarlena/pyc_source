# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfischer/code/repo2docker/repo2docker/buildpacks/base.py
# Compiled at: 2019-09-18 03:20:22
# Size of source mod 2**32: 26995 bytes
import textwrap, jinja2, tarfile, io, os, re, logging, string, sys, hashlib, escapism
import xml.etree.ElementTree as ET
from traitlets import Dict
TEMPLATE = '\nFROM buildpack-deps:bionic\n\n# avoid prompts from apt\nENV DEBIAN_FRONTEND=noninteractive\n\n# Set up locales properly\nRUN apt-get -qq update && \\\n    apt-get -qq install --yes --no-install-recommends locales > /dev/null && \\\n    apt-get -qq purge && \\\n    apt-get -qq clean && \\\n    rm -rf /var/lib/apt/lists/*\n\nRUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \\\n    locale-gen\n\nENV LC_ALL en_US.UTF-8\nENV LANG en_US.UTF-8\nENV LANGUAGE en_US.UTF-8\n\n# Use bash as default shell, rather than sh\nENV SHELL /bin/bash\n\n# Set up user\nARG NB_USER\nARG NB_UID\nENV USER ${NB_USER}\nENV HOME /home/${NB_USER}\n\nRUN adduser --disabled-password \\\n    --gecos "Default user" \\\n    --uid ${NB_UID} \\\n    ${NB_USER}\n\nRUN wget --quiet -O - https://deb.nodesource.com/gpgkey/nodesource.gpg.key |  apt-key add - && \\\n    DISTRO="bionic" && \\\n    echo "deb https://deb.nodesource.com/node_10.x $DISTRO main" >> /etc/apt/sources.list.d/nodesource.list && \\\n    echo "deb-src https://deb.nodesource.com/node_10.x $DISTRO main" >> /etc/apt/sources.list.d/nodesource.list\n\n# Base package installs are not super interesting to users, so hide their outputs\n# If install fails for some reason, errors will still be printed\nRUN apt-get -qq update && \\\n    apt-get -qq install --yes --no-install-recommends \\\n       {% for package in base_packages -%}\n       {{ package }} \\\n       {% endfor -%}\n    > /dev/null && \\\n    apt-get -qq purge && \\\n    apt-get -qq clean && \\\n    rm -rf /var/lib/apt/lists/*\n\n{% if packages -%}\nRUN apt-get -qq update && \\\n    apt-get -qq install --yes \\\n       {% for package in packages -%}\n       {{ package }} \\\n       {% endfor -%}\n    > /dev/null && \\\n    apt-get -qq purge && \\\n    apt-get -qq clean && \\\n    rm -rf /var/lib/apt/lists/*\n{% endif -%}\n\nEXPOSE 8888\n\n{% if build_env -%}\n# Environment variables required for build\n{% for item in build_env -%}\nENV {{item[0]}} {{item[1]}}\n{% endfor -%}\n{% endif -%}\n\n{% if path -%}\n# Special case PATH\nENV PATH {{ \':\'.join(path) }}:${PATH}\n{% endif -%}\n\n{% if build_script_files -%}\n# If scripts required during build are present, copy them\n{% for src, dst in build_script_files|dictsort %}\nCOPY {{ src }} {{ dst }}\n{% endfor -%}\n{% endif -%}\n\n{% for sd in build_script_directives -%}\n{{sd}}\n{% endfor %}\n\n# Allow target path repo is cloned to be configurable\nARG REPO_DIR=${HOME}\nENV REPO_DIR ${REPO_DIR}\nWORKDIR ${REPO_DIR}\n\n# We want to allow two things:\n#   1. If there\'s a .local/bin directory in the repo, things there\n#      should automatically be in path\n#   2. postBuild and users should be able to install things into ~/.local/bin\n#      and have them be automatically in path\n#\n# The XDG standard suggests ~/.local/bin as the path for local user-specific\n# installs. See https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html\nENV PATH ${HOME}/.local/bin:${REPO_DIR}/.local/bin:${PATH}\n\n{% if env -%}\n# The rest of the environment\n{% for item in env -%}\nENV {{item[0]}} {{item[1]}}\n{% endfor -%}\n{% endif -%}\n\n# Run pre-assemble scripts! These are instructions that depend on the content\n# of the repository but don\'t access any files in the repository. By executing\n# them before copying the repository itself we can cache these steps. For\n# example installing APT packages.\n{% if preassemble_script_files -%}\n# If scripts required during build are present, copy them\n{% for src, dst in preassemble_script_files|dictsort %}\nCOPY src/{{ src }} ${REPO_DIR}/{{ dst }}\n{% endfor -%}\n{% endif -%}\n\n{% if preassemble_script_directives -%}\nUSER root\nRUN chown -R ${NB_USER}:${NB_USER} ${REPO_DIR}\n{% endif -%}\n\n{% for sd in preassemble_script_directives -%}\n{{ sd }}\n{% endfor %}\n\n# Copy and chown stuff. This doubles the size of the repo, because\n# you can\'t actually copy as USER, only as root! Thanks, Docker!\nUSER root\nCOPY src/ ${REPO_DIR}\nRUN chown -R ${NB_USER}:${NB_USER} ${REPO_DIR}\n\n# Run assemble scripts! These will actually turn the specification\n# in the repository into an image.\n{% for sd in assemble_script_directives -%}\n{{ sd }}\n{% endfor %}\n\n# Container image Labels!\n# Put these at the end, since we don\'t want to rebuild everything\n# when these change! Did I mention I hate Dockerfile cache semantics?\n{% for k, v in labels|dictsort %}\nLABEL {{k}}="{{v}}"\n{%- endfor %}\n\n# We always want containers to run as non-root\nUSER ${NB_USER}\n\n{% if post_build_scripts -%}\n# Make sure that postBuild scripts are marked executable before executing them\n{% for s in post_build_scripts -%}\nRUN chmod +x {{ s }}\nRUN ./{{ s }}\n{% endfor %}\n{% endif -%}\n\n# Add start script\n{% if start_script is not none -%}\nRUN chmod +x "{{ start_script }}"\nENV R2D_ENTRYPOINT "{{ start_script }}"\n{% endif -%}\n\n# Add entrypoint\nCOPY /repo2docker-entrypoint /usr/local/bin/repo2docker-entrypoint\nENTRYPOINT ["/usr/local/bin/repo2docker-entrypoint"]\n\n# Specify the default command to run\nCMD ["jupyter", "notebook", "--ip", "0.0.0.0"]\n\n{% if appendix -%}\n# Appendix:\n{{ appendix }}\n{% endif %}\n'
ENTRYPOINT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo2docker-entrypoint')

class BuildPack:
    __doc__ = '\n    A composable BuildPack.\n\n    Specifically used for creating Dockerfiles for use with repo2docker only.\n\n    Things that are kept constant:\n     - base image\n     - some environment variables (such as locale)\n     - user creation & ownership of home directory\n     - working directory\n\n    Everything that is configurable is additive & deduplicative,\n    and there are *some* general guarantees of ordering.\n\n    '

    def __init__(self):
        self.log = logging.getLogger('repo2docker')
        self.appendix = ''
        self.labels = {}
        if sys.platform.startswith('win'):
            self.log.warning('Windows environment detected. Note that Windows support is experimental in repo2docker.')

    def get_packages(self):
        """
        List of packages that are installed in this BuildPack.

        Versions are not specified, and ordering is not guaranteed. These
        are usually installed as apt packages.
        """
        return set()

    def get_base_packages(self):
        """
        Base set of apt packages that are installed for all images.

        These contain useful images that are commonly used by a lot of images,
        where it would be useful to share a base docker image layer that
        contains them.

        These would be installed with a --no-install-recommends option.
        """
        return {
         'less',
         'nodejs',
         'unzip'}

    def get_build_env(self):
        """
        Ordered list of environment variables to be set for this image.

        Ordered so that environment variables can use other environment
        variables in their values.

        Expects tuples, with the first item being the environment variable
        name and the second item being the value.

        These environment variables will be set prior to build.
        Use .get_env() to set environment variables after build.
        """
        return []

    def get_env(self):
        """
        Ordered list of environment variables to be set for this image.

        Ordered so that environment variables can use other environment
        variables in their values.

        Expects tuples, with the first item being the environment variable
        name and the second item being the value.

        These variables will not be available to build.
        """
        return []

    def get_path(self):
        """
        Ordered list of file system paths to look for executables in.

        Just sets the PATH environment variable. Separated out since
        it is very commonly set by various buildpacks.
        """
        return []

    def get_labels(self):
        """
        Docker labels to set on the built image.
        """
        return self.labels

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.
        """
        return {}

    @property
    def stencila_manifest_dir(self):
        """Find the stencila manifest dir if it exists"""
        if hasattr(self, '_stencila_manifest_dir'):
            return self._stencila_manifest_dir
        self._stencila_manifest_dir = None
        for root, dirs, files in os.walk('.'):
            if 'manifest.xml' in files:
                self.log.debug('Found a manifest.xml at %s', root)
                self._stencila_manifest_dir = root.split(os.path.sep, 1)[1]
                self.log.info('Using stencila manifest.xml in %s', self._stencila_manifest_dir)
                break

        return self._stencila_manifest_dir

    @property
    def stencila_contexts(self):
        """Find the stencila manifest contexts from file path in manifest"""
        if hasattr(self, '_stencila_contexts'):
            return self._stencila_contexts
        self._stencila_contexts = set()
        files = []
        if self.stencila_manifest_dir:
            manifest = ET.parse(os.path.join(self.stencila_manifest_dir, 'manifest.xml'))
            documents = manifest.findall('./documents/document')
            files = [os.path.join(self.stencila_manifest_dir, x.get('path')) for x in documents]
        else:
            return self._stencila_contexts
            for filename in files:
                self.log.debug('Extracting contexts from %s', filename)
                document = ET.parse(filename)
                code_chunks = document.findall('.//code[@specific-use="source"]')
                languages = [x.get('language') for x in code_chunks]
                self._stencila_contexts.update(languages)
                self.log.info('Added executions contexts, now have %s', self._stencila_contexts)
                break

            return self._stencila_contexts

    def get_build_scripts(self):
        """
        Ordered list of shell script snippets to build the base image.

        A list of tuples, where the first item is a username & the
        second is a single logical line of a bash script that should
        be RUN as that user.

        These are run before the source of the repository is copied
        into the container image, and hence can not reference stuff
        from the repository. When the build scripts are done, the
        container image should be in a state where it is generically
        re-useable for building various other repositories with
        similar environments.

        You can use environment variable substitutions in both the
        username and the execution script.
        """
        return []

    def get_preassemble_script_files(self):
        """
        Dict of files to be copied to the container image for use in preassembly.

        This is copied before the `build_scripts`, `preassemble_scripts` and
        `assemble_scripts` are run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the
        repository and the value is the destination file path inside the
        repository in the container.
        """
        return {}

    def get_preassemble_scripts(self):
        """
        Ordered list of shell snippets to build an image for this repository.

        A list of tuples, where the first item is a username & the
        second is a single logical line of a bash script that should
        be RUN as that user.

        These are run before the source of the repository is copied into
        the container image. These should be the scripts that depend on the
        repository but do not need access to the contents.

        For example the list of APT packages to install.
        """
        return []

    def get_assemble_scripts(self):
        """
        Ordered list of shell script snippets to build the repo into the image.

        A list of tuples, where the first item is a username & the
        second is a single logical line of a bash script that should
        be RUN as that user.

        These are run after the source of the repository is copied into
        the container image (into the current directory). These should be
        the scripts that actually build the repository into the container
        image.

        If this needs to be dynamically determined (based on the presence
        or absence of certain files, for example), you can create any
        method and decorate it with `traitlets.default('assemble_scripts)`
        and the return value of this method is used as the value of
        assemble_scripts. You can expect that the script is running in
        the current directory of the repository being built when doing
        dynamic detection.

        You can use environment variable substitutions in both the
        username and the execution script.
        """
        return []

    def get_post_build_scripts(self):
        """
        An ordered list of executable scripts to execute after build.

        Is run as a non-root user, and must be executable. Used for performing
        build time steps that can not be performed with standard tools.

        The scripts should be as deterministic as possible - running it twice
        should not produce different results!
        """
        return []

    def get_start_script(self):
        """
        The path to a script to be executed at container start up.

        This script is added as the `ENTRYPOINT` to the container.

        It is run as a non-root user, and must be executable. Used for
        performing run time steps that can not be performed with standard
        tools. For example setting environment variables for your repository.

        The script should be as deterministic as possible - running it twice
        should not produce different results.
        """
        pass

    @property
    def binder_dir(self):
        has_binder = os.path.isdir('binder')
        has_dotbinder = os.path.isdir('.binder')
        if has_binder:
            if has_dotbinder:
                raise RuntimeError("The repository contains both a 'binder' and a '.binder' directory. However they are exclusive.")
        if has_dotbinder:
            return '.binder'
        if has_binder:
            return 'binder'
        return ''

    def binder_path(self, path):
        """Locate a file"""
        return os.path.join(self.binder_dir, path)

    def detect(self):
        return True

    def render(self):
        """
        Render BuildPack into Dockerfile
        """
        t = jinja2.Template(TEMPLATE)
        build_script_directives = []
        last_user = 'root'
        for user, script in self.get_build_scripts():
            if last_user != user:
                build_script_directives.append('USER {}'.format(user))
                last_user = user
            build_script_directives.append('RUN {}'.format(textwrap.dedent(script.strip('\n'))))

        assemble_script_directives = []
        last_user = 'root'
        for user, script in self.get_assemble_scripts():
            if last_user != user:
                assemble_script_directives.append('USER {}'.format(user))
                last_user = user
            assemble_script_directives.append('RUN {}'.format(textwrap.dedent(script.strip('\n'))))

        preassemble_script_directives = []
        last_user = 'root'
        for user, script in self.get_preassemble_scripts():
            if last_user != user:
                preassemble_script_directives.append('USER {}'.format(user))
                last_user = user
            preassemble_script_directives.append('RUN {}'.format(textwrap.dedent(script.strip('\n'))))

        build_script_files = {self.generate_build_context_filename(k)[0]:v for k, v in self.get_build_script_files().items()}
        return t.render(packages=(sorted(self.get_packages())),
          path=(self.get_path()),
          build_env=(self.get_build_env()),
          env=(self.get_env()),
          labels=(self.get_labels()),
          build_script_directives=build_script_directives,
          preassemble_script_files=(self.get_preassemble_script_files()),
          preassemble_script_directives=preassemble_script_directives,
          assemble_script_directives=assemble_script_directives,
          build_script_files=build_script_files,
          base_packages=(sorted(self.get_base_packages())),
          post_build_scripts=(self.get_post_build_scripts()),
          start_script=(self.get_start_script()),
          appendix=(self.appendix))

    @staticmethod
    def generate_build_context_filename(src_path, hash_length=6):
        """
        Generate a filename for a file injected into the Docker build context.

        In case the src_path is relative, it's assumed it's relative to directory of
        this __file__. Returns the resulting filename and an absolute path to the source
        file on host.
        """
        if not os.path.isabs(src_path):
            src_parts = src_path.split('/')
            src_path = (os.path.join)(os.path.dirname(__file__), *src_parts)
        src_path_hash = hashlib.sha256(src_path.encode('utf-8')).hexdigest()
        safe_chars = set(string.ascii_letters + string.digits)

        def escape(s):
            return escapism.escape(s, safe=safe_chars, escape_char='-')

        src_path_slug = escape(src_path)
        filename = 'build_script_files/{name}-{hash}'
        return (
         filename.format(name=(src_path_slug[:255 - hash_length - 20]),
           hash=(src_path_hash[:hash_length])).lower(),
         src_path)

    def build(self, client, image_spec, memory_limit, build_args, cache_from, extra_build_kwargs):
        tarf = io.BytesIO()
        tar = tarfile.open(fileobj=tarf, mode='w')
        dockerfile_tarinfo = tarfile.TarInfo('Dockerfile')
        dockerfile = self.render().encode('utf-8')
        dockerfile_tarinfo.size = len(dockerfile)
        tar.addfile(dockerfile_tarinfo, io.BytesIO(dockerfile))

        def _filter_tar(tar):
            tar.uname = ''
            tar.gname = ''
            tar.uid = int(build_args.get('NB_UID', 1000))
            tar.gid = int(build_args.get('NB_UID', 1000))
            return tar

        for src in sorted(self.get_build_script_files()):
            dest_path, src_path = self.generate_build_context_filename(src)
            tar.add(src_path, dest_path, filter=_filter_tar)

        tar.add(ENTRYPOINT_FILE, 'repo2docker-entrypoint', filter=_filter_tar)
        tar.add('.', 'src/', filter=_filter_tar)
        tar.close()
        tarf.seek(0)
        if not isinstance(memory_limit, int):
            raise ValueError("The memory limit has to be specified as aninteger but is '{}'".format(type(memory_limit)))
        limits = {}
        if memory_limit:
            limits = {'memory':memory_limit, 
             'memswap':memory_limit}
        build_kwargs = dict(fileobj=tarf,
          tag=image_spec,
          custom_context=True,
          buildargs=build_args,
          decode=True,
          forcerm=True,
          rm=True,
          container_limits=limits,
          cache_from=cache_from)
        build_kwargs.update(extra_build_kwargs)
        for line in (client.build)(**build_kwargs):
            yield line


class BaseImage(BuildPack):

    def get_build_env(self):
        """Return env directives required for build"""
        return [
         ('APP_BASE', '/srv'),
         ('NPM_DIR', '${APP_BASE}/npm'),
         ('NPM_CONFIG_GLOBALCONFIG', '${NPM_DIR}/npmrc')]

    def get_path(self):
        return super().get_path() + ['${NPM_DIR}/bin']

    def get_build_scripts(self):
        scripts = [
         ('root', '\n                mkdir -p ${NPM_DIR} && \\\n                chown -R ${NB_USER}:${NB_USER} ${NPM_DIR}\n                '),
         ('${NB_USER}', '\n                npm config --global set prefix ${NPM_DIR}\n                ')]
        return super().get_build_scripts() + scripts

    def get_env(self):
        """Return env directives to be set after build"""
        env = []
        if self.stencila_manifest_dir:
            archive_dir, archive = os.path.split(self.stencila_manifest_dir)
            env.extend([
             (
              'STENCILA_ARCHIVE_DIR', '${REPO_DIR}/' + archive_dir),
             (
              'STENCILA_ARCHIVE', archive)])
        return env

    def detect(self):
        return True

    def get_preassemble_scripts(self):
        scripts = []
        try:
            with open(self.binder_path('apt.txt')) as (f):
                extra_apt_packages = []
                for l in f:
                    package = l.partition('#')[0].strip()
                    if not package:
                        continue
                    if not re.match('^[a-z0-9.+-]+', package):
                        raise ValueError('Found invalid package name {} in apt.txt'.format(package))
                    extra_apt_packages.append(package)

            scripts.append((
             'root',
             '\n                apt-get -qq update && \\\n                apt-get install --yes --no-install-recommends {} && \\\n                apt-get -qq purge && \\\n                apt-get -qq clean && \\\n                rm -rf /var/lib/apt/lists/*\n                '.format(' '.join(sorted(extra_apt_packages)))))
        except FileNotFoundError:
            pass

        if 'py' in self.stencila_contexts:
            scripts.extend([
             ('${NB_USER}', '\n                        ${KERNEL_PYTHON_PREFIX}/bin/pip install --no-cache https://github.com/stencila/py/archive/f1260796.tar.gz && \\\n                        ${KERNEL_PYTHON_PREFIX}/bin/python -m stencila register\n                        ')])
        if self.stencila_manifest_dir:
            scripts.extend([
             ('${NB_USER}', '\n                        ${NB_PYTHON_PREFIX}/bin/pip install --no-cache nbstencilaproxy==0.1.1 && \\\n                        jupyter serverextension enable --sys-prefix --py nbstencilaproxy && \\\n                        jupyter nbextension install    --sys-prefix --py nbstencilaproxy && \\\n                        jupyter nbextension enable     --sys-prefix --py nbstencilaproxy\n                        ')])
        return scripts

    def get_assemble_scripts(self):
        """Return directives to run after the entire repository has been added to the image"""
        return []

    def get_post_build_scripts(self):
        post_build = self.binder_path('postBuild')
        if os.path.exists(post_build):
            return [
             post_build]
        return []

    def get_start_script(self):
        start = self.binder_path('start')
        if os.path.exists(start):
            return os.path.join('${REPO_DIR}', start)