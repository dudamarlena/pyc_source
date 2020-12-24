# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/format/text/serializer.py
# Compiled at: 2010-06-12 17:55:55
from ...core import Package, Structure, Comment, EntityList, Entity
from ...diff import StructureDiff, EntityListDiff, BlobDiff
import os

class TextSerializer:

    @classmethod
    def serialize(cls, element, fallback=None):
        if isinstance(element, Package):
            return cls.dump_package(element)
        else:
            return cls.dump_structure(element)

    @classmethod
    def dump_entity(cls, entity, indent=0):
        string = '    ' * indent + 'Entity(id:' + entity.id + ', value:"' + entity.value + '")\n'
        return string

    @classmethod
    def dump_comment(cls, comment, indent=0):
        string = '    ' * indent + 'Comment(\n'
        for element in comment:
            string += cls.dump_element(element, indent + 1)

        string += '    ' * indent + ')\n'
        return string

    @classmethod
    def dump_string(cls, unicode, indent=0):
        return '    ' * indent + 'String("' + unicode.replace('\n', '\\n') + '")\n'

    @classmethod
    def dump_element(cls, element, indent=0):
        if isinstance(element, Entity):
            return cls.dump_entity(element, indent)
        elif isinstance(element, Comment):
            return cls.dump_comment(element, indent)
        elif isinstance(element, unicode) or isinstance(element, str):
            return cls.dump_string(element, indent)
        else:
            return element

    @classmethod
    def dump_structure(cls, l10nobject, indent=0, content=True):
        string = '    ' * indent + '== L10nObject: ' + unicode(l10nobject.id) + ' ==\n'
        if content == True:
            for element in l10nobject:
                string += cls.dump_element(element, indent + 1)

        return string

    @classmethod
    def dump_entitylist(cls, elist, indent=0, content=True):
        string = '    ' * indent + '== EntityList: ' + unicode(elist.id) + ' ==\n'
        if content == True:
            for entity in elist.values():
                string += cls.dump_entity(entity, indent + 1)

        return string

    @classmethod
    def dump_blob(cls, blob, indent=0):
        string = '    ' * indent + 'Blob: ' + blob.id + '\n'
        return string

    @classmethod
    def dump_package(cls, l10npack, indent=0, content=True):
        string = ''
        string += '    ' * indent + '=== L10nPackage: ' + l10npack.id + ' ===\n'
        for (key, package) in l10npack.packages.items():
            string += cls.dump_package(package, indent + 1, content)

        for (key, object) in l10npack.objects.items():
            if isinstance(object, Structure):
                string += cls.dump_structure(object, indent + 1, content)
            elif isinstance(object, EntityList):
                string += cls.dump_entitylist(object, indent + 1, content)
            else:
                string += cls.dump_blob(object, indent + 1)

        return string

    @classmethod
    def dump_blobdiff(cls, objectdiff, indent=0):
        string = ''
        if objectdiff.diff:
            string += '     ' * indent + 'object modified\n'
        else:
            string += '     ' * indent + 'object not modified\n'
        return string

    @classmethod
    def dump_entitylistdiff(cls, entitylistdiff, indent=0):
        string = ''
        added = entitylistdiff.entities('added')
        if len(added):
            string += '     ' * indent + 'added entites:\n'
            for entity in added.values():
                string += '     ' * (indent + 1) + entity.id + '\n'

        removed = entitylistdiff.entities('removed')
        if len(removed):
            string += '     ' * indent + 'removed entities:\n'
            for entity in removed.values():
                string += '     ' * (indent + 1) + entity.id + '\n'

        modified = entitylistdiff.entities('modified')
        if len(modified):
            string += '     ' * indent + 'modified entities:\n'
            for entitydiff in modified.values():
                string += '     ' * (indent + 1) + entitydiff.id + "(value '" + entitydiff.value()[0] + "' -> '" + entitydiff.value()[1] + "')\n"

        return string

    @classmethod
    def dump_structurediff(cls, l10nobjectdiff, indent=0):
        return cls.dump_entitylistdiff(l10nobjectdiff.entitylistdiff(), indent=indent)

    @classmethod
    def dump_packagediff(cls, l10npackagediff, indent=0):
        string = ''
        added = l10npackagediff.structures('added')
        if len(added):
            string += '     ' * indent + '\x1b[1mnew in the latter package:\x1b[0m\n'
            for object in added:
                string += '     ' * (indent + 1) + os.path.join('.', object.id) + '\n'

        removed = l10npackagediff.structures('removed')
        if len(removed):
            string += '     ' * indent + '\x1b[1mremoved in the latter package:\x1b[0m\n'
            for object in removed:
                string += '     ' * (indent + 1) + os.path.join('.', object.id) + '\n'

        modified = l10npackagediff.structures('modified')
        if len(modified):
            string += '     ' * indent + '\x1b[1mmodified in the latter package:\x1b[0m\n'
            for object in modified:
                string += '     ' * (indent + 1) + os.path.join('.', object.id) + '\n'
                if isinstance(object, StructureDiff):
                    string += cls.dump_structurediff(l10npackagediff._structures[object.id]['struct'], indent + 2)
                elif isinstance(object, EntityListDiff):
                    string += cls.dump_entitylistdiff(l10npackagediff._structures[object.id]['struct'], indent + 2)
                elif isinstance(object, BlobDiff):
                    string += cls.dump_blobdiff(l10npackagediff._structures[object.id]['struct'], indent + 2)

        added = l10npackagediff.packages('added')
        if len(added):
            string += '     ' * indent + '\x1b[1mnew in the latter package:\x1b[0m\n'
            for package in added:
                string += '     ' * (indent + 1) + os.path.join('.', package.id) + '\n'

        removed = l10npackagediff.packages('removed')
        if len(removed):
            string += '     ' * indent + '\x1b[1mremoved from latter package:\x1b[0m\n'
            for package in removed:
                string += '     ' * (indent + 1) + os.path.join('.', package.id) + '\n'

        modified = l10npackagediff.packages('modified')
        if len(modified):
            string += '     ' * indent + '\x1b[1mmodified in the latter package:\x1b[0m\n'
            for package in modified:
                string += '     ' * (indent + 1) + os.path.join('.', package.id) + '\n'
                string += cls.dump_packagediff(l10npackagediff._packages[package.id]['package'], indent + 2)

        if not len(string):
            string += '\nThe packages are identical'
        return string