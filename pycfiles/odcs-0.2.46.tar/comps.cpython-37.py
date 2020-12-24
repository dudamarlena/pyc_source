# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/comps.py
# Compiled at: 2019-07-25 06:36:19
# Size of source mod 2**32: 4692 bytes
COMPS_TEMPLATE = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE comps PUBLIC "-//Red Hat, Inc.//DTD Comps info//EN" "comps.dtd">\n<comps>\n  {%- for group in comps.groups %}\n  <group>\n    <id>{{ group.id }}</id>\n    <name>{{ group.name }}</name>\n    <description>{{ group.description }}</description>\n    <default>{{ group.is_default|lower }}</default>\n    <uservisible>{{ group.is_uservisible|lower }}</uservisible>\n    <packagelist>\n        {%- for package in group.packages %}\n        <packagereq\n        {%- if package.type %} type="{{ package.type }}"{% endif -%}\n        {%- if package.arch %} arch="{{ package.arch }}"{% endif -%}\n        {%- if package.requires %} requires="{{ package.requires }}"{% endif -%}\n        {%- if package.is_basearchonly %} basearchonly="{{ package.is_basearchonly | lower }}"{% endif -%}\n        {%- if false %}{% endif -%}>{{ package.name }}</packagereq>\n        {%- endfor %}\n    </packagelist>\n  </group>\n  {%- endfor %}\n</comps>\n\n'
VARIANTS_TEMPLATE = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE variants PUBLIC "-//Red Hat, Inc.//DTD Variants info//EN" "variants2012.dtd">\n<variants>\n  {%- for variant in product.variants %}\n  <variant id="{{ variant.id }}" name="{{ variant.name }}" type="{{ variant.type }}">\n    <arches>\n      {%- for arch in variant.arches %}\n      <arch>{{ arch.name }}</arch>\n      {%- endfor %}\n    </arches>\n    {%- if variant.groups %}\n    <groups>\n      {%- for group in variant.groups %}\n        <group\n        {%- if group in variant.default_groups %} default="true"{% endif -%}\n        {%- if false %}{% endif %}>{{ group.name }}</group>\n      {%- endfor %}\n    </groups>\n    {%- endif %}\n    {%- if variant.modules %}\n    <modules>\n      {%- for module in variant.modules %}\n      <module>{{ module.name }}</module>\n      {%- endfor %}\n    </modules>\n    {%- endif %}\n  </variant>\n  {%- endfor %}\n</variants>\n\n'

class Arch(object):

    def __init__(self, name):
        self.name = name


class Package(object):

    def __init__(self, name, arch=None, type=None, requires=None, is_basearchonly=False):
        self.name = name
        self.arch = arch
        self.type = type
        self.requires = requires
        self.is_basearchonly = is_basearchonly


class Module(object):

    def __init__(self, name):
        self.name = name


class Group(object):

    def __init__(self, id, name, description, is_default=True, is_uservisible=True):
        self.id = id
        self.name = name
        self.description = description
        self.is_default = is_default
        self.is_uservisible = is_uservisible
        self.packages = []

    def add_package(self, package):
        self.packages.append(package)


class Comps(object):

    def __init__(self):
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)


class Variant(object):

    def __init__(self, id, name, type, source_type):
        self.id = id
        self.name = name
        self.type = type
        self.arches = []
        self.source_type = source_type
        self.groups = []
        self.default_groups = []
        self.modules = []

    def add_arch(self, arch):
        self.arches.append(arch)

    def add_group(self, group, default=True):
        self.groups.append(group)
        if default:
            self.default_groups.append(group)

    def add_module(self, module):
        self.modules.append(module)


class Product(object):

    def __init__(self):
        self.variants = []

    def add_variant(self, variant):
        self.variants.append(variant)