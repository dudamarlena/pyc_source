# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/model/component.py
# Compiled at: 2020-01-28 14:35:58
"""
Parameter, ComponentType and Component class definitions.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""
from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError, ParseError
from lems.model.dynamics import Dynamics
from lems.model.structure import Structure
from lems.model.simulation import Simulation
from lems.parser.expr import ExprParser

class Parameter(LEMSBase):
    """
    Stores a parameter declaration.
    """

    def __init__(self, name, dimension, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.dimension = dimension
        self.fixed = False
        self.fixed_value = None
        self.value = None
        self.numeric_value = None
        self.description = description
        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<{0} name="{1}" dimension="{2}"').format('Fixed' if self.fixed else 'Parameter', self.name, self.dimension) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'

    def __str__(self):
        return ('{0}: name="{1}" dimension="{2}"').format('Fixed' if self.fixed else 'Parameter', self.name, self.dimension) + ((' description = "{0}"').format(self.description) if self.description else '')

    def __repr__(self):
        return self.__str__()


class Fixed(Parameter):
    """
    Stores a fixed parameter specification.
    """

    def __init__(self, parameter, value, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        Parameter.__init__(self, parameter, '__dimension_inherited__', description)
        self.fixed = True
        self.fixed_value = value

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Fixed parameter="{0}"').format(self.name) + (' value="{0}"').format(self.fixed_value) + '/>'


class Property(LEMSBase):
    """ 
    Store the specification of a property. 
    """

    def __init__(self, name, dimension=None, default_value=None, description=''):
        """
        Constructor.
        """
        self.name = name
        self.dimension = dimension
        self.description = description
        self.default_value = default_value

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Property name="{0}"').format(self.name) + ((' dimension="{0}"').format(self.dimension) if self.dimension else 'none') + ((' defaultValue = "{0}"').format(self.default_value) if self.default_value else '') + '/>'


class IndexParameter(LEMSBase):
    """
    Stores a parameter which is an index (integer > 0).
    """

    def __init__(self, name, description=''):
        """
        Constructor.
        """
        self.name = name
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<IndexParameter name="{0}"').format(self.name) + '' + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class DerivedParameter(LEMSBase):
    """ 
    Store the specification of a derived parameter. 
    """

    def __init__(self, name, value, dimension=None, description=''):
        """
        Constructor.

        See instance variable documentation for more info on derived parameters.
        """
        self.name = name
        self.dimension = dimension
        self.value = value
        self.description = description
        try:
            ep = ExprParser(self.value)
            self.expression_tree = ep.parse()
        except:
            raise ParseError("Parse error when parsing value expression '{0}' for derived parameter {1}", self.value, self.name)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<DerivedParameter name="{0}"').format(self.name) + ((' dimension="{0}"').format(self.dimension) if self.dimension else '') + ((' value="{0}"').format(self.value) if self.value else '') + '/>'


class Constant(LEMSBase):
    """
    Stores a constant specification.
    """

    def __init__(self, name, value, dimension=None, symbol=None, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.symbol = symbol
        self.value = value
        self.dimension = dimension
        self.description = description
        self.numeric_value = None
        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return '<Constant' + ((' name = "{0}"').format(self.name) if self.name else '') + ((' symbol = "{0}"').format(self.symbol) if self.symbol else '') + ((' value = "{0}"').format(self.value) if self.value else '') + ((' dimension = "{0}"').format(self.dimension) if self.dimension else '') + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class Exposure(LEMSBase):
    """
    Stores a exposure specification.
    """

    def __init__(self, name, dimension, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.dimension = dimension
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Exposure name="{0}" dimension="{1}"').format(self.name, self.dimension) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class Requirement(LEMSBase):
    """
    Stores a requirement specification.
    """

    def __init__(self, name, dimension, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.dimension = dimension
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Requirement name="{0}" dimension="{1}"').format(self.name, self.dimension) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class ComponentRequirement(LEMSBase):
    """
    Specifies a component that is required
    """

    def __init__(self, name, description=''):
        """
        Constructor.
        """
        self.name = name
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<ComponentRequirement name="{0}"').format(self.name) + '' + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class InstanceRequirement(LEMSBase):
    """
    Stores an instance requirement specification.
    """

    def __init__(self, name, type, description=''):
        """
        Constructor.
        """
        self.name = name
        self.type = type
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<InstanceRequirement name="{0}" type="{1}"').format(self.name, self.type) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class Children(LEMSBase):
    """
    Stores children specification.
    """

    def __init__(self, name, type_, multiple=False):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.type = type_
        self.multiple = multiple

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<{2} name="{0}" type="{1}"/>').format(self.name, self.type, 'Children' if self.multiple else 'Child')


class Text(LEMSBase):
    """
    Stores a text entry specification.
    """

    def __init__(self, name, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.description = description
        self.value = None
        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Text name="{0}"').format(self.name) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'

    def __str__(self):
        return ('Text, name: {0}').format(self.name) + ((', description = "{0}"').format(self.description) if self.description else '') + ((', value = "{0}"').format(self.value) if self.value else '')

    def __repr__(self):
        return self.__str__()


class Link(LEMSBase):
    """
    Stores a link specification.
    """

    def __init__(self, name, type_, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.type = type_
        self.description = description
        self.value = None
        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Link name="{0}" type="{1}"').format(self.name, self.type) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class Path(LEMSBase):
    """
    Stores a path entry specification.
    """

    def __init__(self, name, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.description = description
        self.value = None
        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Path name="{0}"').format(self.name) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class EventPort(LEMSBase):
    """
    Stores an event port specification.
    """

    def __init__(self, name, direction, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        d = direction.lower()
        if d != 'in' and d != 'out':
            raise ModelError(("Invalid direction '{0}' in event port '{1}'").format(direction, name))
        self.direction = direction
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<EventPort name="{0}" direction="{1}"').format(self.name, self.direction) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class ComponentReference(LEMSBase):
    """
    Stores a component reference.
    """

    def __init__(self, name, type_, local=None):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.type = type_
        self.local = local
        self.referenced_component = None
        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<ComponentReference name="{0}" type="{1}"').format(self.name, self.type) + ((' local = "{0}"').format(self.local) if self.local else '') + '/>'


class Attachments(LEMSBase):
    """
    Stores an attachment type specification.
    """

    def __init__(self, name, type_, description=''):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.type = type_
        self.description = description

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Attachments name="{0}" type="{1}"').format(self.name, self.type) + ((' description = "{0}"').format(self.description) if self.description else '') + '/>'


class Fat(LEMSBase):
    """
    Stores common elements for a component type / fat component.
    """

    def __init__(self):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.parameters = Map()
        self.properties = Map()
        self.derived_parameters = Map()
        self.index_parameters = Map()
        self.constants = Map()
        self.exposures = Map()
        self.requirements = Map()
        self.component_requirements = Map()
        self.instance_requirements = Map()
        self.children = Map()
        self.texts = Map()
        self.links = Map()
        self.paths = Map()
        self.event_ports = Map()
        self.component_references = Map()
        self.attachments = Map()
        self.dynamics = Dynamics()
        self.structure = Structure()
        self.simulation = Simulation()
        self.types = set()

    def add_parameter(self, parameter):
        """
        Adds a paramter to this component type.

        @param parameter: Parameter to be added.
        @type parameter: lems.model.component.Parameter
        """
        self.parameters[parameter.name] = parameter

    def add_property(self, property):
        """
        Adds a property to this component type.

        @param property: Property to be added.
        @type property: lems.model.component.Property
        """
        self.properties[property.name] = property

    def add_derived_parameter(self, derived_parameter):
        """
        Adds a derived_parameter to this component type.

        @param derived_parameter: Derived Parameter to be added.
        @type derived_parameter: lems.model.component.DerivedParameter
        """
        self.derived_parameters[derived_parameter.name] = derived_parameter

    def add_index_parameter(self, index_parameter):
        """
        Adds an index_parameter to this component type.

        @param index_parameter: Index Parameter to be added.
        @type index_parameter: lems.model.component.IndexParameter
        """
        self.index_parameters[index_parameter.name] = index_parameter

    def add_constant(self, constant):
        """
        Adds a paramter to this component type.

        @param constant: Constant to be added.
        @type constant: lems.model.component.Constant
        """
        self.constants[constant.name] = constant

    def add_exposure(self, exposure):
        """
        Adds a exposure to this component type.

        @param exposure: Exposure to be added.
        @type exposure: lems.model.component.Exposure
        """
        self.exposures[exposure.name] = exposure

    def add_requirement(self, requirement):
        """
        Adds a requirement to this component type.

        @param requirement: Requirement to be added.
        @type requirement: lems.model.component.Requirement
        """
        self.requirements[requirement.name] = requirement

    def add_component_requirement(self, component_requirement):
        """
        Adds a component requirement to this component type.

        @param component_requirement: ComponentRequirement to be added.
        @type component_requirement: lems.model.component.ComponentRequirement
        """
        self.component_requirements[component_requirement.name] = component_requirement

    def add_instance_requirement(self, instance_requirement):
        """
        Adds an instance requirement to this component type.

        @param instance_requirement: InstanceRequirement to be added.
        @type instance_requirement: lems.model.component.InstanceRequirement
        """
        self.instance_requirements[instance_requirement.name] = instance_requirement

    def add_children(self, children):
        """
        Adds children to this component type.

        @param children: Children to be added.
        @type children: lems.model.component.Children
        """
        self.children[children.name] = children

    def add_text(self, text):
        """
        Adds a text to this component type.

        @param text: Text to be added.
        @type text: lems.model.component.Text
        """
        self.texts[text.name] = text

    def add_link(self, link):
        """
        Adds a link to this component type.

        @param link: Link to be added.
        @type link: lems.model.component.Link
        """
        self.links[link.name] = link

    def add_path(self, path):
        """
        Adds a path to this component type.

        @param path: Path to be added.
        @type path: lems.model.component.Path
        """
        self.paths[path.name] = path

    def add_event_port(self, event_port):
        """
        Adds a event port to this component type.

        @param event_port: Event port to be added.
        @type event_port: lems.model.component.EventPort
        """
        self.event_ports[event_port.name] = event_port

    def add_component_reference(self, component_reference):
        """
        Adds a component reference to this component type.

        @param component_reference: Component reference to be added.
        @type component_reference: lems.model.component.ComponentReference
        """
        self.component_references[component_reference.name] = component_reference

    def add_attachments(self, attachments):
        """
        Adds an attachments type specification to this component type.

        @param attachments: Attachments specification to be added.
        @type attachments: lems.model.component.Attachments
        """
        self.attachments[attachments.name] = attachments

    def add(self, child):
        """
        Adds a typed child object to the component type.

        @param child: Child object to be added.
        """
        if isinstance(child, Parameter):
            self.add_parameter(child)
        elif isinstance(child, Property):
            self.add_property(child)
        elif isinstance(child, DerivedParameter):
            self.add_derived_parameter(child)
        elif isinstance(child, IndexParameter):
            self.add_index_parameter(child)
        elif isinstance(child, Constant):
            self.add_constant(child)
        elif isinstance(child, Exposure):
            self.add_exposure(child)
        elif isinstance(child, Requirement):
            self.add_requirement(child)
        elif isinstance(child, ComponentRequirement):
            self.add_component_requirement(child)
        elif isinstance(child, InstanceRequirement):
            self.add_instance_requirement(child)
        elif isinstance(child, Children):
            self.add_children(child)
        elif isinstance(child, Text):
            self.add_text(child)
        elif isinstance(child, Link):
            self.add_link(child)
        elif isinstance(child, Path):
            self.add_path(child)
        elif isinstance(child, EventPort):
            self.add_event_port(child)
        elif isinstance(child, ComponentReference):
            self.add_component_reference(child)
        elif isinstance(child, Attachments):
            self.add_attachments(child)
        else:
            raise ModelError('Unsupported child element')


class ComponentType(Fat):
    """
    Stores a component type declaration.
    """

    def __init__(self, name, description='', extends=None):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        Fat.__init__(self)
        self.name = name
        self.extends = extends
        self.description = description
        self.types.add(name)

    def __str__(self):
        return ('ComponentType, name: {0}').format(self.name)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = ('<ComponentType name="{0}"').format(self.name) + ((' extends="{0}"').format(self.extends) if self.extends else '') + ((' description="{0}"').format(self.description) if self.description else '')
        chxmlstr = ''
        for property in self.properties:
            chxmlstr += property.toxml()

        for parameter in self.parameters:
            chxmlstr += parameter.toxml()

        for derived_parameter in self.derived_parameters:
            chxmlstr += derived_parameter.toxml()

        for index_parameter in self.index_parameters:
            chxmlstr += index_parameter.toxml()

        for constant in self.constants:
            chxmlstr += constant.toxml()

        childxml = ''
        childrenxml = ''
        for children in self.children:
            if children.multiple:
                childrenxml += children.toxml()
            else:
                childxml += children.toxml()

        chxmlstr += childxml
        chxmlstr += childrenxml
        for link in self.links:
            chxmlstr += link.toxml()

        for component_reference in self.component_references:
            chxmlstr += component_reference.toxml()

        for attachment in self.attachments:
            chxmlstr += attachment.toxml()

        for event_port in self.event_ports:
            chxmlstr += event_port.toxml()

        for exposure in self.exposures:
            chxmlstr += exposure.toxml()

        for requirement in self.requirements:
            chxmlstr += requirement.toxml()

        for component_requirement in self.component_requirements:
            chxmlstr += component_requirement.toxml()

        for instance_requirement in self.instance_requirements:
            chxmlstr += instance_requirement.toxml()

        for path in self.paths:
            chxmlstr += path.toxml()

        for text in self.texts:
            chxmlstr += text.toxml()

        chxmlstr += self.dynamics.toxml()
        chxmlstr += self.structure.toxml()
        chxmlstr += self.simulation.toxml()
        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</ComponentType>'
        else:
            xmlstr += '/>'
        return xmlstr


class Component(LEMSBase):
    """
    Stores a component instantiation.
    """

    def __init__(self, id_, type_, **params):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        self.id = id_
        self.type = type_
        self.parameters = dict()
        for key in params.keys():
            self.parameters[key] = params[key]

        self.children = list()
        self.parent_id = None
        return

    def __str__(self):
        return ('Component, id: {0}, type: {1},\n   parameters: {2}\n   parent: {3}\n').format(self.id, self.type, self.parameters, self.parent_id)

    def __repr__(self):
        return self.__str__()

    def set_parameter(self, parameter, value):
        """
        Set a parameter.

        @param parameter: Parameter to be set.
        @type parameter: str

        @param value: Value to be set to.
        @type value: str
        """
        self.parameters[parameter] = value

    def add_child(self, child):
        """
        Adds a child component.

        @param child: Child component to be added.
        @type child: lems.model.component.Component
        """
        self.children.append(child)

    def add(self, child):
        """
        Adds a typed child object to the component.

        @param child: Child object to be added.
        """
        if isinstance(child, Component):
            self.add_child(child)
        else:
            raise ModelError('Unsupported child element')

    def set_parent_id(self, parent_id):
        """
        Sets the id of the parent Component
        
        @param parent_id: id of the parent Component
        @type parent_id: str
        """
        self.parent_id = parent_id

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = ('<Component id="{0}" type="{1}"').format(self.id, self.type)
        for k, v in self.parameters.items():
            xmlstr += (' {0}="{1}"').format(k, v)

        if self.children:
            xmlstr += '>'
            for child in self.children:
                xmlstr += child.toxml()

            xmlstr += '</Component>'
        else:
            xmlstr += '/>'
        return xmlstr


class FatComponent(Fat):
    """
    Stores a resolved component.
    """

    def __init__(self, id_, type_):
        """
        Constructor.

        See instance variable documentation for more details on parameters.
        """
        Fat.__init__(self)
        self.id = id_
        self.type = type_
        self.child_components = list()
        self.parent_id = None
        return

    def __str__(self):
        return ('FatComponent, id: {0}, type: {1}, parent:{2}').format(self.id, self.type, self.parent_id) + ((', num children: {0}').format(len(self.child_components)) if len(self.child_components) > 0 else '')

    def add_child_component(self, child_component):
        """
        Adds a child component to this fat component.

        @param child_component: Child component to be added.
        @type child_component: lems.model.component.FatComponent
        """
        self.child_components.append(child_component)

    def add(self, child):
        """
        Adds a typed child object to the component type.

        @param child: Child object to be added.
        """
        if isinstance(child, FatComponent):
            self.add_child_component(child)
        else:
            Fat.add(self, child)

    def set_parent_id(self, parent_id):
        """
        Sets the id of the parent Component
        
        @param parent_id: id of the parent Component
        @type parent_id: str
        """
        self.parent_id = parent_id