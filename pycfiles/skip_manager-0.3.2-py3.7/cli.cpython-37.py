# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/cli.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 3157 bytes
from typing import Dict, Set, Type
import click
from click import Context
from skip.managers.apt import Apt
from skip.managers.apt_get import AptGet
from skip.managers.brew import Brew
from skip.managers.brew_cask import BrewCask
from skip.managers.choco import Choco
from skip.managers.flatpak import Flatpak
from skip.managers.gem import Gem
from skip.managers.linux_brew import LinuxBrew
from skip.managers.macos_brew import MacOSBrew
from skip.managers.manager import PackageManager
from skip.managers.mas import Mas
from skip.managers.npm import Npm
from skip.managers.pip import Pip
from skip.managers.snap import Snap

def managers() -> Set[Type[PackageManager]]:
    return {Brew, Npm, Apt, AptGet, Gem, Choco, Pip, Snap, LinuxBrew, BrewCask,
     MacOSBrew, Mas, Flatpak}


@click.group()
def skip():
    pass


@skip.command(help='Performs a full upgrade and cleanup for all package managers')
@click.pass_context
def autopilot(context: Context) -> bool:
    context.invoke(update)
    context.invoke(upgrade)
    context.invoke(clean)
    return True


@skip.command(help='Setup all package managers')
def setup() -> bool:
    for manager in managers():
        if manager.check():
            print('Start: ' + manager.canonical_name() + '.setup()')
            manager.setup()
            print('Finish: ' + manager.canonical_name() + '.setup()')

    return True


@skip.command(help='Updates all package managers')
def update() -> bool:
    for manager in managers():
        if manager.check():
            print('Start: ' + manager.canonical_name() + '.update()')
            manager.update()
            print('Finish: ' + manager.canonical_name() + '.update()')

    return True


@skip.command(help='Upgrades all package managers')
def upgrade() -> bool:
    for manager in managers():
        if manager.check():
            print('Start: ' + manager.canonical_name() + '.upgrade()')
            manager.upgrade()
            print('Finish: ' + manager.canonical_name() + '.upgrade()')

    return True


@skip.command(help='Cleans all package managers')
def clean() -> bool:
    for manager in managers():
        if manager.check():
            print('Start: ' + manager.canonical_name() + '.clean()')
            manager.clean()
            print('Finish: ' + manager.canonical_name() + '.clean()')

    return True


@skip.command(help='Installs all packages in Skipfile.toml for all package managers')
def install() -> bool:
    with open('Skipfile.toml', 'r') as (file):
        from toml import loads
        skipfile = loads(file.read())
        for manager in managers():
            if manager.check():
                print('Start: ' + manager.canonical_name() + '.install()')
                packages = skipfile['package_manager'][manager.canonical_name()]
                for package in packages:
                    if packages[package] is str:
                        packages[package] = packages[package].strip().split()

                manager.install(packages)
                print('Finish: ' + manager.canonical_name() + '.install()')

    return True