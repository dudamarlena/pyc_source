# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/colin/checks/deprecated_labels.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 4512 bytes
from colin.core.checks.labels import DeprecatedLabelAbstractCheck

class ArchitectureLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'architecture_label_capital_deprecated'

    def __init__(self):
        super(ArchitectureLabelCapitalDeprecatedCheck, self).__init__(message="Label 'Architecture' is deprecated.",
          description="Replace with 'architecture'.",
          reference_url='?????',
          tags=[
         'architecture', 'label', 'capital', 'deprecated'],
          old_label='Architecture',
          new_label='architecture')


class BZComponentDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'bzcomponent_deprecated'

    def __init__(self):
        super(BZComponentDeprecatedCheck, self).__init__(message="Label 'BZComponent' is deprecated.",
          description="Replace with 'com.redhat.component'.",
          reference_url='?????',
          tags=[
         'com.redhat.component', 'bzcomponent', 'label', 'deprecated'],
          old_label='BZComponent',
          new_label='com.redhat.component')


class InstallLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'install_label_capital_deprecated'

    def __init__(self):
        super(InstallLabelCapitalDeprecatedCheck, self).__init__(message="Label 'INSTALL' is deprecated.",
          description="Replace with 'install'.",
          reference_url='?????',
          tags=[
         'install', 'label', 'capital', 'deprecated'],
          old_label='INSTALL',
          new_label='install')


class NameLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'name_label_capital_deprecated'

    def __init__(self):
        super(NameLabelCapitalDeprecatedCheck, self).__init__(message="Label 'Name' is deprecated.",
          description="Replace with 'name'.",
          reference_url='?????',
          tags=[
         'name', 'label', 'capital', 'deprecated'],
          old_label='Name',
          new_label='name')


class ReleaseLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'release_label_capital_deprecated'

    def __init__(self):
        super(ReleaseLabelCapitalDeprecatedCheck, self).__init__(message="Label 'Release' is deprecated.",
          description="Replace with 'release'.",
          reference_url='?????',
          tags=[
         'release', 'label', 'capital', 'deprecated'],
          old_label='Release',
          new_label='release')


class UninstallLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'uninstall_label_capital_deprecated'

    def __init__(self):
        super(UninstallLabelCapitalDeprecatedCheck, self).__init__(message="Label 'UNINSTALL' is deprecated.",
          description="Replace with 'uninstall'.",
          reference_url='?????',
          tags=[
         'uninstall', 'label', 'capital', 'deprecated'],
          old_label='UNINSTALL',
          new_label='uninstall')


class VersionLabelCapitalDeprecatedCheck(DeprecatedLabelAbstractCheck):
    name = 'version_label_capital_deprecated'

    def __init__(self):
        super(VersionLabelCapitalDeprecatedCheck, self).__init__(message="Label 'Version' is deprecated.",
          description="Replace with 'version'.",
          reference_url='?????',
          tags=[
         'version', 'label', 'capital', 'deprecated'],
          old_label='Version',
          new_label='version')