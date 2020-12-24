# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bom/bom.py
# Compiled at: 2018-07-16 12:07:24
import json, os, rest
from kicad.kicad_schematic_file import KicadSchematicFile
from helper.exception import print_stack

class BomException(BaseException):

    def __init__(self, error):
        self.error = error


class Bom(object):

    def __init__(self):
        self.filename = None
        self.parts = []
        self.part_components = {}
        self.component_part = {}
        self.schematic = None
        self.saved = True
        return

    def LoadFile(self, filename):
        print 'Load BOM', filename
        self.part_components = {}
        self.component_part = {}
        self.parts = []
        if os.path.isfile(filename) == False:
            raise Exception('Error: %s does not exists' % filename)
        with open(filename, 'r') as (infile):
            content = json.load(infile)
        self.schematic = KicadSchematicFile()
        self.schematic.LoadFile(content['schematic'])
        part_not_found = []
        for part in content['parts']:
            try:
                self.parts.append(rest.api.find_part(part['id']))
                self.part_components[part['id']] = []
            except:
                print_stack()
                print 'Warning: part %d not found on server' % part['id']
                part_not_found.append(part)

        component_not_found = []
        part_id_not_found = []
        for part_id in content['components']:
            part = None
            for p in self.parts:
                if p.id == int(part_id):
                    part = p
                    break

            if part:
                schematic_components = self.schematic.Components()
                for component in content['components'][part_id]:
                    if self.part_components.has_key(int(part_id)):
                        if self.schematic.ExistComponent(component['timestamp']):
                            self.part_components[int(part_id)].append(self.schematic.GetComponent(component['timestamp']))
                            self.component_part[component['timestamp']] = part
                        else:
                            print 'Warning: component %s does not exist in schematic' % component['timestamp']
                            component_not_found.append(component)
                    else:
                        print 'Warning: part %d not found on bom' % part_id
                        part_id_not_found.append(int(part_id))

            else:
                print 'Warning: part %d from BOM does not exist on server' % int(part_id)
                part_id_not_found.append(int(part_id))

        self.filename = filename
        self.saved = True
        return

    def byteify(self, input):
        if isinstance(input, dict):
            return {self.byteify(key):self.byteify(value) for key, value in input.iteritems()}
        else:
            if isinstance(input, list):
                return [ self.byteify(element) for element in input ]
            if isinstance(input, unicode):
                return input.encode('utf-8')
            return input

    def SaveFile(self, filename):
        print 'Save BOM', filename
        with open(filename, 'w') as (outfile):
            parts = []
            for part in self.parts:
                parts.append({'id': part.id, 'name': part.name, 'description': part.description})

            part_components = {}
            for part_name in self.part_components:
                if len(self.part_components[part_name]) > 0:
                    part_components[part_name] = []
                for component in self.part_components[part_name]:
                    part_components[part_name].append({'timestamp': component.timestamp, 'reference': component.reference, 'value': component.value})

            input = {'schematic': self.schematic.filename, 'parts': parts, 'components': part_components}
            json_string = json.dumps(self.byteify(input), ensure_ascii=False, sort_keys=True, indent=4, separators=(',',
                                                                                                                    ': '))
            outfile.write(json_string)
        self.filename = filename
        self.saved = True

    def Save(self):
        self.SaveFile(self.filename)

    def Parts(self):
        return self.parts

    def ExistPart(self, part):
        for p in self.parts:
            if p.id == part.id:
                return True

        return False

    def SetSchematic(self, file):
        self.schematic = KicadSchematicFile()
        self.schematic.LoadFile(file)
        for component in self.schematic.Components():
            if component.kipart_id:
                part = None
                try:
                    part = rest.api.find_part(component.kipart_id)
                    self.AddPart(part)
                    self.AddPartComponent(part, component)
                except Exception as e:
                    print format(e)

        return

    def AddPart(self, part):
        self.parts.append(part)
        self.part_components[part.id] = []
        self.saved = False

    def AddPartComponent(self, part, component):
        self.part_components[part.id].append(component)
        self.component_part[component.timestamp] = part
        self.saved = False

    def RemovePart(self, part):
        self.parts.remove(part)
        for component in self.part_components[part.id]:
            self.component_part.pop(component.timestamp)

        self.part_components.pop(part.id)
        self.saved = False

    def RemovePartComponent(self, component):
        part = self.component_part[component.timestamp]
        self.component_part.pop(component.timestamp)
        for part_component in self.part_components[part.id]:
            if part_component.timestamp == component.timestamp:
                self.part_components[part.id].remove(part_component)

        self.saved = False

    def NumComponents(self, bom_part):
        num_components = 0
        if self.part_components.has_key(bom_part.id):
            num_components = num_components + len(self.part_components[bom_part.id])
        return num_components