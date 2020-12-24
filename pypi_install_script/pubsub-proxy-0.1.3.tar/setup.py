import subprocess
import setuptools
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools import setup, Extension, Command, find_packages


class BuildProtoCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from grpc_tools import command
        command.build_package_protos("./pubsub_proxy/proto", strict_mode=True)
        subprocess.call("./fix.sh", cwd="./pubsub_proxy/proto")


class DevelopCommand(develop):
    def run(self):
        self.run_command("build_proto")
        develop.run(self)


class BuildPyCommand(build_py):
    def run(self):
        self.run_command("build_proto")
        build_py.run(self)


setuptools.setup(
    name="pubsub-proxy",
    version="0.1.3",
    description="A Libra pub/sub proxy",
    python_requires="~=3.7",
    packages=setuptools.find_packages(),
    setup_requires=["grpcio-tools"],
    include_package_data=False,
    zip_safe=True,
    install_requires=["grpcio-tools", "grpcio>=1.23.0", "protobuf==3.9.1"],
    entry_points={"console_scripts": ["pubsub-proxy = pubsub_proxy.daemon:main"]},
    cmdclass={
        "build_proto": BuildProtoCommand,
        "build_py": BuildPyCommand,
        "develop": DevelopCommand,
    },
    url="https://github.com/calibra/pubsub_proxy",
)
