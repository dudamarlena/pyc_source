# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/backend.py
# Compiled at: 2019-01-14 10:01:56
# Size of source mod 2**32: 5563 bytes
"""Backend module for llb3d compiler."""
import tempfile, pathlib, shutil, glob, subprocess, sys, os, stat
from llvmlite import ir, binding
SOURCE_DIRECTORY = pathlib.Path(__file__).parent.resolve() / 'bbprogram'
SOURCE_FILENAME = 'bbprogram.s'
EXECUTABLE_FILENAME = 'bbprogram'
SYSTEM_SHARED = pathlib.Path('/usr/lib/x86_64-linux-gnu')
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

def load_shared_library(name):
    """Find and load shared library."""
    if (SOURCE_DIRECTORY / name).exists():
        binding.load_library_permanently(str(SOURCE_DIRECTORY / name))
    else:
        binding.load_library_permanently(str(SYSTEM_SHARED / name))


UCHAR_T = ir.IntType(16)
USTR_T = ir.PointerType(UCHAR_T)
INT32_T = ir.IntType(32)
FLOAT32_T = ir.FloatType()
VOID_T = ir.VoidType()
BBMAIN_SIGNATURE = ir.FunctionType(VOID_T, tuple())
INT32_ZERO = ir.Constant(INT32_T, 0)

class Backend:
    __doc__ = 'Backend class: compile ast to llvm ir.'

    def __init__(self):
        """Init backend."""
        self.debug = False
        self.source_module = ir.Module()
        self.init_runtime()
        bbmain = ir.Function((self.source_module), BBMAIN_SIGNATURE, name='bbmain')
        block = bbmain.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(block)
        self.builder.ret_void()

    def init_runtime(self):
        """Init runtime libraries."""
        self.runtime = {'Print': ir.Function(self.source_module, ir.FunctionType(VOID_T, (USTR_T,)), 'Print')}

    def optimize(self, opt_level=2) -> binding.ModuleRef:
        """Compile and optimize llvm module."""
        llvm_module = binding.parse_assembly(str(self.source_module))
        llvm_module.verify()
        pass_manager = binding.create_module_pass_manager()
        pass_manager_builder = binding.create_pass_manager_builder()
        pass_manager_builder.opt_level = opt_level
        pass_manager_builder.populate(pass_manager)
        pass_manager.run(llvm_module)
        return llvm_module

    @staticmethod
    def get_target_machine():
        """Return current target machine."""
        return binding.Target.from_default_triple().create_target_machine()

    def emit_assembly(self) -> str:
        """Optimize and return target assembler."""
        llvm_module = self.optimize()
        target_machine = self.get_target_machine()
        return target_machine.emit_assembly(llvm_module)

    def emit_llvm(self) -> str:
        """Optimize and return llvm ir."""
        llvm_module = self.optimize()
        return str(llvm_module)

    def emit_executable(self, executable_filename: str):
        """Create executable file."""
        with tempfile.TemporaryDirectory() as (source_dir):
            source_dir = pathlib.Path(source_dir)
            with open(source_dir / SOURCE_FILENAME, 'w') as (output):
                output.write(self.emit_assembly())
            for filename in glob.iglob(str(SOURCE_DIRECTORY / '*')):
                shutil.copy2(filename, str(source_dir))

            build_dir = source_dir / 'build'
            build_dir.mkdir(parents=True, exist_ok=True)
            config = 'Debug' if self.debug else 'Release'
            cmake_args = (
             '-DCMAKE_BUILD_TYPE=' + config,)
            build_args = (
             '--config', config)
            subprocess.run((('cmake', '..') + cmake_args), stdout=(sys.stdout.fileno()),
              stderr=(sys.stderr.fileno()),
              cwd=build_dir,
              check=True)
            subprocess.run((('cmake', '--build', '.') + build_args), stdout=(sys.stdout.fileno()),
              stderr=(sys.stderr.fileno()),
              cwd=build_dir,
              check=True)
            shutil.copy2(build_dir / EXECUTABLE_FILENAME, executable_filename)

    def run(self, *args, check=True, **kwargs) -> subprocess.CompletedProcess:
        """Run program in a subprocess.

        Return completed process.
        All keyword arguments pass to subprocess.run.
        check is set to True by default.
        """
        with tempfile.NamedTemporaryFile() as (executable_file):
            executable_filename = executable_file.name
            executable_file.close()
            self.emit_executable(executable_filename)
            os.chmod(executable_filename, stat.S_IXUSR)
            return (subprocess.run)(args=(executable_filename,) + args, check=check, **kwargs)