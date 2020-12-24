"""
Setup to build a python package including FFI file to make use of
the whitenoise-core RUST binaries
"""
from setuptools import setup, find_namespace_packages
import os

# -------------------------------
# Set environment variables
# -------------------------------

# turn on backtraces in rust (for build.rs)
os.environ['RUST_BACKTRACE'] = 'full'  # '1'
os.environ['RUSTFLAGS'] = ""

# set the environment variable to increase compiler optimization
WN_RELEASE = os.environ.get("WN_RELEASE", "false") != "false"

# set the environment variable to use precompiled external libraries
WN_USE_SYSTEM_LIBS = os.environ.get("WN_USE_SYSTEM_LIBS", "false") != "false"

# -------------------------------
# Set directory paths
# -------------------------------

# project path
root_dir = os.path.dirname(os.path.abspath(__file__))

# whitenoise-core repo as a submodule. (https://github.com/opendifferentialprivacy/whitenoise-core)
rust_dir = os.path.join(root_dir, 'whitenoise-core')

# whitenoise-core prototypes + prototype components
prototypes_dir = os.path.join(rust_dir, "validator-rust", "prototypes")
components_dir = os.path.join(prototypes_dir, "components")

# Rust build path
rust_build_path = os.path.join('target', 'release' if WN_RELEASE else 'debug')

# -------------------------------
# Create commands
# -------------------------------
rust_build_cmd = 'cargo build'
if WN_RELEASE:
    rust_build_cmd += ' --release'

validator_build_cmd = [
    'bash', '-c',
    rust_build_cmd + " --manifest-path=validator-rust/Cargo.toml"
]

runtime_build_cmd = [
    'bash', '-c',
    rust_build_cmd + (' --features use-system-libs' if WN_USE_SYSTEM_LIBS else '') + " --manifest-path=runtime-rust/Cargo.toml"
]


def build_native(spec):
    """

    """
    build_validator = spec.add_external_build(
        cmd=validator_build_cmd,
        path=os.path.join(rust_dir)
    )

    spec.add_cffi_module(
        module_path='opendp._native_validator',
        dylib=lambda: build_validator.find_dylib('whitenoise_validator', in_path=rust_build_path),
        header_filename=lambda: build_validator.find_header('api.h', in_path='validator-rust'),
        rtld_flags=['NOW', 'NODELETE']
    )

    build_runtime = spec.add_external_build(
        cmd=runtime_build_cmd,
        path=os.path.join(rust_dir)
    )

    spec.add_cffi_module(
        module_path='opendp._native_runtime',
        dylib=lambda: build_runtime.find_dylib('whitenoise_runtime', in_path=rust_build_path),
        header_filename=lambda: build_runtime.find_header('api.h', in_path='runtime-rust'),
        rtld_flags=['NOW', 'NODELETE']
    )


def build_python(spec):
    spec.add_external_build(
        cmd=['bash', '-c', 'python3 scripts/code_generation.py'],
        path="."
    )


setup(
    packages=find_namespace_packages(include=["opendp.*"]),
    extras_require={
        "plotting": [
            "networkx",
            "matplotlib"
        ],
        "test": [
            "pytest>=4.4.2"
        ]
    },
    milksnake_tasks=[
        build_native,
        build_python
    ]
)
