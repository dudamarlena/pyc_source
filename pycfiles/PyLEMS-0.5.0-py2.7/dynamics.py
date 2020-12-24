# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/model/dynamics.py
# Compiled at: 2015-11-16 08:17:20
"""
Behavioral dynamics of component types.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""
from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError, ParseError
from lems.parser.expr import ExprParser

class StateVariable(LEMSBase):
    """
    Store the specification of a state variable.
    """

    def __init__(self, name, dimension, exposure=None):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """
        self.name = name
        self.dimension = dimension
        self.exposure = exposure

    def __str__(self):
        return ('StateVariable name="{0}" dimension="{1}"').format(self.name, self.dimension) + ((' exposure="{0}"').format(self.exposure) if self.exposure else '')

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<StateVariable name="{0}" dimension="{1}"').format(self.name, self.dimension) + ((' exposure="{0}"').format(self.exposure) if self.exposure else '') + '/>'


class DerivedVariable(LEMSBase):
    """
    Store the specification of a derived variable.
    """

    def __init__(self, name, **params):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """
        self.name = name
        self.dimension = params['dimension'] if 'dimension' in params else None
        self.exposure = params['exposure'] if 'exposure' in params else None
        self.select = params['select'] if 'select' in params else None
        self.value = params['value'] if 'value' in params else None
        self.reduce = params['reduce'] if 'reduce' in params else None
        self.required = params['required'] if 'required' in params else None
        self.expression_tree = None
        if self.value != None:
            try:
                self.expression_tree = ExprParser(self.value).parse()
            except:
                raise ParseError("Parse error when parsing value expression '{0}' for derived variable {1}", self.value, self.name)

        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<DerivedVariable name="{0}"').format(self.name) + ((' dimension="{0}"').format(self.dimension) if self.dimension else '') + ((' exposure="{0}"').format(self.exposure) if self.exposure else '') + ((' select="{0}"').format(self.select) if self.select else '') + ((' value="{0}"').format(self.value) if self.value else '') + ((' reduce="{0}"').format(self.reduce) if self.reduce else '') + ((' required="{0}"').format(self.required) if self.required else '') + '/>'


class Case(LEMSBase):
    """
    Store the specification of a case for a Conditional Derived Variable.
    """

    def __init__(self, condition, value):
        """
        Constructor.
        """
        self.condition = condition
        self.value = value
        self.condition_expression_tree = None
        self.value_expression_tree = None
        try:
            self.value_expression_tree = ExprParser(self.value).parse()
            if not self.condition:
                self.condition_expression_tree = None
            else:
                self.condition_expression_tree = ExprParser(self.condition).parse()
        except:
            raise ParseError("Parse error when parsing case with condition '{0}' and value {1}", self.condition, self.value)

        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Case condition="{0}" value="{1}"').format(self.condition, self.value) + '/>'


class ConditionalDerivedVariable(LEMSBase):
    """
    Store the specification of a conditional derived variable.
    """

    def __init__(self, name, dimension, exposure=None):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """
        self.name = name
        self.dimension = dimension
        self.exposure = exposure
        self.cases = list()

    def add_case(self, case):
        """
        Adds a case to this conditional derived variable.

        @param case: Case to be added.
        @type case: lems.model.dynamics.Case
        """
        self.cases.append(case)

    def add(self, child):
        """
        Adds a typed child object to the conditional derived variable.

        @param child: Child object to be added.
        """
        if isinstance(child, Case):
            self.add_case(child)
        else:
            raise ModelError('Unsupported child element')

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = ('<ConditionalDerivedVariable name="{0}"').format(self.name) + ((' dimension="{0}"').format(self.dimension) if self.dimension else '') + ((' exposure="{0}"').format(self.exposure) if self.exposure else '')
        chxmlstr = ''
        for case in self.cases:
            chxmlstr += case.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</ConditionalDerivedVariable>'
        else:
            xmlstr += '/>'
        return xmlstr


class TimeDerivative(LEMSBase):
    """
    Store the specification of a time derivative specifcation.
    """

    def __init__(self, variable, value):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """
        self.variable = variable
        self.value = value
        self.expression_tree = None
        try:
            self.expression_tree = ExprParser(value).parse()
        except:
            raise ParseError("Parse error when parsing value expression '{0}' for state variable {1}", self.value, self.variable)

        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<TimeDerivative variable="{0}" value="{1}"/>').format(self.variable, self.value)


class Action(LEMSBase):
    """
    Base class for event handler actions.
    """
    pass


class StateAssignment(Action):
    """
    State assignment specification.
    """

    def __init__(self, variable, value):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """
        Action.__init__(self)
        self.variable = variable
        self.value = value
        self.expression_tree = None
        try:
            self.expression_tree = ExprParser(value).parse()
        except:
            raise ParseError("Parse error when parsing state assignment value expression '{0}' for state variable {1}", self.value, self.variable)

        return

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<StateAssignment variable="{0}" value="{1}"/>').format(self.variable, self.value)


class EventOut(Action):
    """
    Event transmission specification.
    """

    def __init__(self, port):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        Action.__init__(self)
        self.port = port

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<EventOut port="{0}"/>').format(self.port)


class Transition(Action):
    """
    Regime transition specification.
    """

    def __init__(self, regime):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        Action.__init__(self)
        self.regime = regime

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Transition regime="{0}"/>').format(self.regime)


class EventHandler(LEMSBase):
    """
    Base class for event handlers.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.actions = list()

    def __str__(self):
        istr = 'EventHandler...'
        return istr

    def add_action(self, action):
        """
        Adds an action to this event handler.

        @param action: Action to be added.
        @type action: lems.model.dynamics.Action
        """
        self.actions.append(action)

    def add(self, child):
        """
        Adds a typed child object to the event handler.

        @param child: Child object to be added.
        """
        if isinstance(child, Action):
            self.add_action(child)
        else:
            raise ModelError('Unsupported child element')


class OnStart(EventHandler):
    """
    Specification for event handler called upon initialization of the component.
    """

    def __init__(self):
        """
        Constructor.
        """
        EventHandler.__init__(self)

    def __str__(self):
        istr = 'OnStart: ['
        for action in self.actions:
            istr += str(action)

        istr += ']'
        return str(istr)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = '<OnStart'
        chxmlstr = ''
        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnStart>'
        else:
            xmlstr += '/>'
        return xmlstr


class OnCondition(EventHandler):
    """
    Specification for event handler called upon satisfying a given condition.
    """

    def __init__(self, test):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        EventHandler.__init__(self)
        self.test = test
        try:
            self.expression_tree = ExprParser(test).parse()
        except:
            raise ParseError("Parse error when parsing OnCondition test '{0}'", test)

    def __str__(self):
        istr = 'OnCondition...'
        return istr

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = ('<OnCondition test="{0}"').format(self.test)
        chxmlstr = ''
        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnCondition>'
        else:
            xmlstr += '/>'
        return xmlstr


class OnEvent(EventHandler):
    """
    Specification for event handler called upon receiving en event sent by another component.
    """

    def __init__(self, port):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        EventHandler.__init__(self)
        self.port = port

    def __str__(self):
        istr = 'OnEvent, port: %s' % self.port
        return istr

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = ('<OnEvent port="{0}"').format(self.port)
        chxmlstr = ''
        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnEvent>'
        else:
            xmlstr += '/>'
        return xmlstr


class OnEntry(EventHandler):
    """
    Specification for event handler called upon entry into a new behavior regime.
    """

    def __init__(self):
        """
        Constructor.
        """
        EventHandler.__init__(self)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        xmlstr = '<OnEntry'
        chxmlstr = ''
        for action in self.actions:
            chxmlstr += action.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</OnEntry>'
        else:
            xmlstr += '/>'
        return xmlstr


class KineticScheme(LEMSBase):
    """
    Kinetic scheme specifications.
    """

    def __init__(self, name, nodes, state_variable, edges, edge_source, edge_target, forward_rate, reverse_rate):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        self.name = name
        self.nodes = nodes
        self.state_variable = state_variable
        self.edges = edges
        self.edge_source = edge_source
        self.edge_target = edge_target
        self.forward_rate = forward_rate
        self.reverse_rate = reverse_rate

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<KineticScheme name="{0}" nodes="{1}" edges="{2}" stateVariable="{3}" edgeSource="{4}" edgeTarget="{5}" forwardRate="{6}" reverseRate="{7}"/>').format(self.name, self.nodes, self.edges, self.state_variable, self.edge_source, self.edge_target, self.forward_rate, self.reverse_rate)


class Behavioral(LEMSBase):
    """
    Store dynamic behavioral attributes.
    """

    def __init__(self):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        self.parent_behavioral = None
        self.state_variables = Map()
        self.derived_variables = Map()
        self.conditional_derived_variables = Map()
        self.time_derivatives = Map()
        self.event_handlers = list()
        self.kinetic_schemes = Map()
        return

    def has_content(self):
        if len(self.state_variables) == 0 and len(self.derived_variables) == 0 and len(self.conditional_derived_variables) == 0 and len(self.time_derivatives) == 0 and len(self.event_handlers) == 0 and len(self.kinetic_schemes) == 0:
            return False
        else:
            return True

    def clear(self):
        """
        Clear behavioral entities.
        """
        self.time_derivatives = Map()

    def add_state_variable(self, sv):
        """
        Adds a state variable to this behavior regime.

        @param sv: State variable.
        @type sv: lems.model.dynamics.StateVariable
        """
        self.state_variables[sv.name] = sv

    def add_derived_variable(self, dv):
        """
        Adds a derived variable to this behavior regime.

        @param dv: Derived variable.
        @type dv: lems.model.dynamics.DerivedVariable
        """
        self.derived_variables[dv.name] = dv

    def add_conditional_derived_variable(self, cdv):
        """
        Adds a conditional derived variable to this behavior regime.

        @param cdv: Conditional Derived variable.
        @type cdv: lems.model.dynamics.ConditionalDerivedVariable
        """
        self.conditional_derived_variables[cdv.name] = cdv

    def add_time_derivative(self, td):
        """
        Adds a time derivative to this behavior regime.

        @param td: Time derivative.
        @type td: lems.model.dynamics.TimeDerivative
        """
        self.time_derivatives[td.variable] = td

    def add_event_handler(self, eh):
        """
        Adds an event handler to this behavior regime.

        @param eh: Event handler.
        @type eh: lems.model.dynamics.EventHandler
        """
        self.event_handlers.append(eh)

    def add_kinetic_scheme(self, ks):
        """
        Adds a kinetic scheme to this behavior regime.

        @param ks: Kinetic scheme.
        @type ks: lems.model.dynamics.KineticScheme
        """
        self.kinetic_schemes[ks.name] = ks

    def add(self, child):
        """
        Adds a typed child object to the behavioral object.

        @param child: Child object to be added.
        """
        if isinstance(child, StateVariable):
            self.add_state_variable(child)
        elif isinstance(child, DerivedVariable):
            self.add_derived_variable(child)
        elif isinstance(child, ConditionalDerivedVariable):
            self.add_conditional_derived_variable(child)
        elif isinstance(child, TimeDerivative):
            self.add_time_derivative(child)
        elif isinstance(child, EventHandler):
            self.add_event_handler(child)
        elif isinstance(child, KineticScheme):
            self.add_kinetic_scheme(child)
        else:
            raise ModelError('Unsupported child element')

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        chxmlstr = ''
        for state_variable in self.state_variables:
            chxmlstr += state_variable.toxml()

        for derived_variable in self.derived_variables:
            chxmlstr += derived_variable.toxml()

        for conditional_derived_variable in self.conditional_derived_variables:
            chxmlstr += conditional_derived_variable.toxml()

        for time_derivative in self.time_derivatives:
            chxmlstr += time_derivative.toxml()

        for event_handler in self.event_handlers:
            chxmlstr += event_handler.toxml()

        for kinetic_scheme in self.kinetic_schemes:
            chxmlstr += kinetic_scheme.toxml()

        if isinstance(self, Dynamics):
            for regime in self.regimes:
                chxmlstr += regime.toxml()

        if isinstance(self, Dynamics):
            xmlprefix = 'Dynamics'
            xmlsuffix = 'Dynamics'
            xmlempty = ''
        else:
            xmlprefix = ('Regime name="{0}"').format(self.name) + (' initial="true"' if self.initial else '')
            xmlsuffix = 'Regime'
            xmlempty = ('<{0}/>', format(xmlprefix))
        if chxmlstr:
            xmlstr = ('<{0}>').format(xmlprefix) + chxmlstr + ('</{0}>').format(xmlsuffix)
        else:
            xmlstr = xmlempty
        return xmlstr


class Regime(Behavioral):
    """
    Stores a single behavioral regime for a component type.
    """

    def __init__(self, name, parent_behavioral, initial=False):
        """
        Constructor.
        
        See instance variable documentation for more details on parameters.
        """
        Behavioral.__init__(self)
        self.name = name
        self.parent_behavioral = parent_behavioral
        self.initial = initial


class Dynamics(Behavioral):
    """
    Stores behavioral dynamics specification for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """
        Behavioral.__init__(self)
        self.regimes = Map()

    def add_regime(self, regime):
        """
        Adds a behavior regime to this dynamics object.

        @param regime: Behavior regime to be added.
        @type regime: lems.model.dynamics.Regime """
        self.regimes[regime.name] = regime

    def add(self, child):
        """
        Adds a typed child object to the dynamics object.

        @param child: Child object to be added.
        """
        if isinstance(child, Regime):
            self.add_regime(child)
        else:
            Behavioral.add(self, child)

    def has_content(self):
        if len(self.regimes) > 0:
            return True
        else:
            return Behavioral.has_content(self)