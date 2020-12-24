# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/config/build_config.py
# Compiled at: 2020-02-28 20:45:48
# Size of source mod 2**32: 6340 bytes
from opengen.config.tcp_server_config import TcpServerConfiguration
import random, string

class BuildConfiguration:
    __doc__ = 'Build configuration\n\n    Configuration for the code generator\n\n    '
    DEBUG_MODE = 'debug'
    RELEASE_MODE = 'release'

    def __init__(self, build_dir='.'):
        """
        Construct an instance of BuildConfiguration

        :param build_dir: Target directory, defaults to the current directory

        :return: A new instance of BuildConfiguration

        """
        random_string = ''.join(random.choice(string.ascii_letters) for _i in range(20))
        self._BuildConfiguration__target_system = None
        self._BuildConfiguration__build_mode = BuildConfiguration.RELEASE_MODE
        self._BuildConfiguration__id = random_string
        self._BuildConfiguration__cost_function_name = 'phi_' + random_string
        self._BuildConfiguration__grad_cost_function_name = 'grad_phi_' + random_string
        self._BuildConfiguration__constraint_penalty_function = 'mapping_f2_' + random_string
        self._BuildConfiguration__alm_constraints_mapping_f1 = 'mapping_f1_' + random_string
        self._BuildConfiguration__rebuild = False
        self._BuildConfiguration__build_dir = build_dir
        self._BuildConfiguration__open_version = None
        self._BuildConfiguration__build_c_bindings = False
        self._BuildConfiguration__tcp_interface_config = None
        self._BuildConfiguration__local_path = None

    @property
    def rebuild(self):
        """Whether to re-build the optimizer from scratch"""
        return self._BuildConfiguration__rebuild

    @property
    def id(self):
        """Unique identifier of build configuration"""
        return self._BuildConfiguration__id

    @property
    def cost_function_name(self):
        return self._BuildConfiguration__cost_function_name

    @property
    def grad_function_name(self):
        return self._BuildConfiguration__grad_cost_function_name

    @property
    def constraint_penalty_function_name(self):
        return self._BuildConfiguration__constraint_penalty_function

    @property
    def alm_mapping_f1_function_name(self):
        return self._BuildConfiguration__alm_constraints_mapping_f1

    @property
    def target_system(self):
        """Target system"""
        return self._BuildConfiguration__target_system

    @property
    def build_mode(self):
        """Build mode (release or debug)"""
        return self._BuildConfiguration__build_mode

    @property
    def build_dir(self):
        """Directory in which the auto-generated optimizer will be stored"""
        return self._BuildConfiguration__build_dir

    @property
    def open_version(self):
        """
        OpEn version used with the auto-generated solver

        :return: The method returns either a specific version of OpEn,
        which will be used with the auto-generated optimizer, or `None`,
        in which case, the latest version will be used. You may set your
        preferred version of OpEn with `with_open_version`
        """
        return self._BuildConfiguration__open_version

    @property
    def local_path(self):
        return self._BuildConfiguration__local_path

    @property
    def build_c_bindings(self):
        return self._BuildConfiguration__build_c_bindings

    @property
    def tcp_interface_config(self):
        return self._BuildConfiguration__tcp_interface_config

    def with_rebuild(self, do_rebuild):
        """
        Whether to clean and rebuild the code generator, if it already exists

        :param do_rebuild: if set to True, the target code generator
        will be cleaned and rebuilt from scratch

        :return: current instance of BuildConfiguration
        """
        self._BuildConfiguration__rebuild = do_rebuild
        return self

    def with_target_system(self, target_system):
        """
        Specify the target system

        :param target_system: target system as string (e.g., use
        "arm-unknown-linux-gnueabihf" or "rpi" for Raspberry Pi).
        Note that you must have installed the target using `rustup`
        if you need to cross-compile.

        :return: current instance of BuildConfiguration
        """
        if target_system.lower() == 'rpi':
            self._BuildConfiguration__target_system = 'arm-unknown-linux-gnueabihf'
        else:
            self._BuildConfiguration__target_system = target_system
        return self

    def with_build_mode(self, build_mode):
        """
        Set the build mode (debug/release)

        :param build_mode: Choose either 'debug' or 'release'; the former is
        fast, but suboptimal, while the later may take a while to compile,
        but the generated binary is significantly faster

        :return: current instance of BuildConfiguration

        """
        self._BuildConfiguration__build_mode = build_mode
        return self

    def with_build_directory(self, build_dir):
        """
        Specify the build directory

        :param build_dir: build directory as string

        :return: current instance of BuildConfiguration
        """
        self._BuildConfiguration__build_dir = build_dir
        return self

    def with_open_version(self, open_version='*', local_path=None):
        """
        Specify the version of OpEn to link to

        :param open_version: version of OpEn (in case you want to
        compile with an older version of OpEn; if not, the latest
        version of OpEn will be used)

        :param local_path: you can compile using a local version
        of OpEn. In that case, you need to provide the full absolute
        path to that local OpEn directory.

        :return: current instance of BuildConfiguration
        """
        self._BuildConfiguration__open_version = open_version
        self._BuildConfiguration__local_path = local_path
        return self

    def with_build_c_bindings(self, build_c_bindings=True):
        """
        If activated, OpEn will generate C/C++ bindings for the
        auto-generated solver

        :param build_c_bindings: whether to build C/C++ bindings for
        auto-generated solver; default: `True`, i.e., it suffices
        to call `build_config.with_build_c_bindings()` instead of
        `build_config.with_build_c_bindings(True)`

        :return: current instance of BuildConfiguration
        """
        self._BuildConfiguration__build_c_bindings = build_c_bindings
        return self

    def with_tcp_interface_config(self, tcp_interface_config=TcpServerConfiguration()):
        """
        Specify a TCP server configuration object

        :param tcp_interface_config: Custom TCP server configuration

        :return: current instance of BuildConfiguration
        """
        self._BuildConfiguration__tcp_interface_config = tcp_interface_config
        return self