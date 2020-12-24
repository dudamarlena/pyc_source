# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/josh/Documents/python/pymanifold/build/lib/tests/../src/pymanifold.py
# Compiled at: 2018-06-07 16:45:14
# Size of source mod 2**32: 45274 bytes
from pprint import pprint
import math, networkx as nx
from pysmt.shortcuts import Symbol, Plus, Times, Div, Pow, Equals, Real
from pysmt.shortcuts import Minus, GE, GT, LE, LT, And, get_model, is_sat
from pysmt.typing import REAL
from pysmt.logics import QF_NRA

class Schematic:
    """Schematic"""

    def __init__(self, dim):
        """Store the connections as a dictionary to form a graph where each
        value is a list of all nodes/ports that a node flows out to, store
        information about each of the channels in a separate dictionary

        :param list dim: dimensions of the chip, [X_min, Y_min, X_max, X_min] (m)
        """
        self.exprs = []
        self.dim = dim
        self.translation_strats = {'input':self.translate_input, 
         'output':self.translate_output, 
         't-junction':self.translate_tjunc, 
         'rectangle':self.translate_channel}
        self.dg = nx.DiGraph()

    def channel(self, port_from, port_to, min_length=False, min_width=False, min_height=False, kind='rectangle', phase='None'):
        """Create new connection between two nodes/ports with attributes
        consisting of the dimensions of the channel to be used to create the
        SMT equations to calculate solvability of the circuit
        Units are in brackets

        :param str port_from: Port where fluid comes into the channel from
        :param str port_to: Port at the end of the channel where fluid exits
        :param float min_length: Constrain channel to be this long (m)
        :param float width: Constrain channel to be this wide (m)
        :param float height: Constrain channel to be this wide (m)
        :param str kind: Kind of cross section of the channel (rectangle)
        :param str phase: For channels connecting to a T-junction this must be
            either continuous, dispersed or output
        :returns: None -- no issues with creating this channel
        :raises: TypeError if an input parameter is wrong type
                 ValueError if an input parameter has an invalid value
        """
        valid_kinds = 'rectangle'
        if kind not in valid_kinds:
            raise ValueError('Valid channel kinds are: %s' % valid_kinds)
        if port_from not in self.dg.nodes:
            raise ValueError("port_from node doesn't exist")
        else:
            if port_to not in self.dg.nodes():
                raise ValueError("port_to node doesn't exist")
        attributes = {'kind':kind, 
         'length':Symbol('_'.join([port_from, port_to, 'length']), REAL), 
         'min_length':min_length, 
         'width':Symbol('_'.join([port_from, port_to, 'width']), REAL), 
         'min_width':min_width, 
         'height':Symbol('_'.join([port_from, port_to, 'height']), REAL), 
         'min_height':min_height, 
         'flow_rate':Symbol('_'.join([port_from, port_to, 'flow_rate']), REAL), 
         'droplet_volume':Symbol('_'.join([port_from, port_to, 'Dvol']), REAL), 
         'viscosity':Symbol('_'.join([port_from, port_to, 'viscosity']), REAL), 
         'resistance':Symbol('_'.join([port_from, port_to, 'res']), REAL), 
         'phase':phase.lower(), 
         'port_from':port_from, 
         'port_to':port_to}
        not_neg = [
         'min_length', 'min_width', 'min_height']
        for param in not_neg:
            try:
                if attributes[param] is False:
                    continue
                else:
                    if attributes[param] < 0:
                        raise ValueError("channel '%s' parameter '%s' must be >= 0" % param)
            except TypeError as e:
                raise TypeError('channel %s parameter must be int' % param)
            except ValueError as e:
                raise ValueError(e)

        if (port_from, port_to) in self.dg.edges:
            raise ValueError('Channel already exists between these nodes')
        self.dg.add_edge(port_from, port_to)
        for key, attr in attributes.items():
            self.dg.edges[(port_from, port_to)][key] = attr

    def port(self, name, kind, min_pressure=False, min_flow_rate=False, x=False, y=False, density=False, min_viscosity=False):
        """Create new port where fluids can enter or exit the circuit, any
        optional tag left empty will be converted to a variable for the SMT
        solver to solve for a give a value, units in brackets

        :param str name: The name of the port to use when defining channels
        :param str kind: Define if this is an 'input' or 'output' port
        :param float density: Density of fluid (kg/m^3)
        :param float min_viscosity: Viscosity of the fluid (Pa*s)
        :param float min_pressure: Pressure of the input fluid, (Pa)
        :param float min_flow_rate - flow rate of input fluid, (m^3/s)
        :param float X: x-position of port on chip schematic (m)
        :param float Y: y-position of port on chip schematic (m)
        :returns: None -- no issues with creating this port
        :raises: TypeError if an input parameter is wrong type
                 ValueError if an input parameter has an invalid value
        """
        if not isinstance(name, str) or not isinstance(kind, str):
            raise TypeError('name and kind must be strings')
        else:
            if name in self.dg.nodes:
                raise ValueError('Must provide a unique name')
            if kind.lower() not in self.translation_strats.keys():
                raise ValueError('kind must be %s' % self.translation_strats.keys())
        attributes = {'kind':kind.lower(), 
         'viscosity':Symbol(name + '_viscosity', REAL), 
         'min_viscosity':min_viscosity, 
         'pressure':Symbol(name + '_pressure', REAL), 
         'min_pressure':min_pressure, 
         'flow_rate':Symbol(name + '_flow_rate', REAL), 
         'min_flow_rate':min_flow_rate, 
         'density':Symbol(name + '_density', REAL), 
         'min_density':density, 
         'x':Symbol(name + '_X', REAL), 
         'y':Symbol(name + '_Y', REAL), 
         'min_x':x, 
         'min_y':y}
        not_neg = [
         'min_x', 'min_y', 'min_pressure', 'min_flow_rate',
         'min_viscosity', 'min_density']
        for param in not_neg:
            try:
                if attributes[param] is False:
                    continue
                else:
                    if attributes[param] < 0:
                        raise ValueError("port '%s' parameter '%s' must be >= 0" % (
                         name, param))
            except TypeError as e:
                raise TypeError("port '%s' parameter '%s' must be int" % (
                 name, param))
            except ValueError as e:
                raise ValueError(e)

        self.dg.add_node(name)
        for key, attr in attributes.items():
            self.dg.nodes[name][key] = attr

    def node(self, name, x=False, y=False, kind='node'):
        """Create new node where fluids merge or split, kind of node (T-junction,
        Y-junction, cross, etc.) can be specified if not then a basic node
        connecting multiple channels will be created, units in brackets

        :param str name: Name of the node to use when connecting to a channel
        :param float x:  Set the X position of this node (m)
        :param float y:  Set the Y position of this node (m)
        :param str kind: The type of node this is, default is node, other
            option is t-junction
        :returns: None -- no issues with creating this node
        :raises: TypeError if an input parameter is wrong type
                 ValueError if an input parameter has an invalid value
        """
        if not isinstance(name, str) or not isinstance(kind, str):
            raise TypeError('name and kind must be strings')
        else:
            if name in self.dg.nodes:
                raise ValueError('Must provide a unique name')
            if kind.lower() not in self.translation_strats.keys():
                raise ValueError('kind must be %s' % self.translation_strats.keys())
        attributes = {'kind':kind.lower(), 
         'pressure':Symbol(name + '_pressure', REAL), 
         'min_pressure':None, 
         'flow_rate':Symbol(name + '_flow_rate', REAL), 
         'min_flow_rate':None, 
         'viscosity':Symbol(name + '_viscosity', REAL), 
         'min_viscosity':None, 
         'density':Symbol(name + '_density', REAL), 
         'min_density':None, 
         'x':Symbol(name + '_X', REAL), 
         'y':Symbol(name + '_Y', REAL), 
         'min_x':x, 
         'min_y':y}
        not_neg = [
         'min_x', 'min_y']
        for param in not_neg:
            try:
                if attributes[param] < 0:
                    raise ValueError("port '%s' parameter '%s' must be >= 0" % (
                     name, param))
            except TypeError as e:
                raise TypeError("Port '%s' parameter '%s' must be int" % (
                 name, param))
            except ValueError as e:
                raise ValueError(e)

        self.dg.add_node(name)
        for key, attr in attributes.items():
            self.dg.nodes[name][key] = attr

    def translate_chip(self, name):
        """Create SMT expressions for bounding the nodes to be within constraints
        of the overall chip such as its area provided

        :param name: Name of the node to be constrained
        :returns: None -- no issues with translating the chip constraints
        """
        named_node = self.dg.nodes[name]
        self.exprs.append(GE(named_node['x'], Real(self.dim[0])))
        self.exprs.append(GE(named_node['y'], Real(self.dim[1])))
        self.exprs.append(LE(named_node['x'], Real(self.dim[2])))
        self.exprs.append(LE(named_node['y'], Real(self.dim[3])))

    def translate_node(self, name):
        """Create SMT expressions for bounding the parameters of an node
        to be within the constraints defined by the user

        :param name: Name of the node to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """
        named_node = self.dg.nodes[name]
        output_pressures = []
        for node_name in self.dg.pred[name]:
            output_pressures.append(self.channel_output_pressure((node_name, name)))

        if len(self.dg.pred[name]) == 1:
            self.exprs.append(Equals(named_node['pressure'], output_pressures[0]))
        else:
            if len(self.dg.pred[name]) > 1:
                self.exprs.append(Equals(named_node['pressure'], Plus(output_pressures)))
            else:
                if named_node['min_pressure']:
                    self.exprs.append(Equals(named_node['pressure'], Real(named_node['min_pressure'])))
                else:
                    self.exprs.append(GT(named_node['pressure'], Real(0)))
                if named_node['min_x']:
                    self.exprs.append(Equals(named_node['x'], Real(named_node['min_x'])))
                    self.exprs.append(Equals(named_node['y'], Real(named_node['min_y'])))
                else:
                    self.exprs.append(GE(named_node['x'], Real(0)))
                    self.exprs.append(GE(named_node['y'], Real(0)))
                if named_node['min_flow_rate']:
                    self.exprs.append(Equals(named_node['flow_rate'], Real(named_node['min_flow_rate'])))
                else:
                    self.exprs.append(GT(named_node['flow_rate'], Real(0)))
                if named_node['min_viscosity']:
                    self.exprs.append(Equals(named_node['viscosity'], Real(named_node['min_viscosity'])))
                else:
                    self.exprs.append(GT(named_node['viscosity'], Real(0)))
            if named_node['min_density']:
                self.exprs.append(Equals(named_node['density'], Real(named_node['min_density'])))
            else:
                self.exprs.append(GT(named_node['density'], Real(0)))

    def translate_input(self, name):
        """Create SMT expressions for bounding the parameters of an input port
        to be within the constraints defined by the user

        :param name: Name of the port to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """
        if self.dg.size(name) <= 0:
            raise ValueError('Port %s must have 1 or more connections' % name)
        else:
            if len(list(self.dg.predecessors(name))) != 0:
                raise ValueError('Cannot have channels into input port %s' % name)
            self.translate_node(name)
            named_node = self.dg.nodes[name]
            if not named_node['min_flow_rate']:
                flow_rate = self.calculate_port_flow_rate(name)
                self.exprs.append(Equals(named_node['flow_rate'], flow_rate))
        for node_out in self.dg.succ[name]:
            self.translation_strats[self.dg.edges[(name, node_out)]['kind']]((
             name, node_out))

    def translate_output(self, name):
        """Create SMT expressions for bounding the parameters of an output port
        to be within the constraints defined by the user

        :param str name: Name of the port to be constrained
        :returns: None -- no issues with translating the port parameters to SMT
        """
        if self.dg.size(name) <= 0:
            raise ValueError('Port %s must have 1 or more connections' % name)
        elif len(list(self.dg.succ[name])) != 0:
            raise ValueError('Cannot have channels out of output port %s' % name)
        else:
            self.translate_node(name)
            named_node = self.dg.nodes[name]
            total_flow_in = named_node['min_flow_rate'] or []
            for channel_in in self.dg.pred[name]:
                total_flow_in.append(self.dg.edges[(channel_in, name)]['flow_rate'])

            if len(total_flow_in) == 1:
                self.exprs.append(Equals(named_node['flow_rate'], total_flow_in[0]))
            else:
                self.exprs.append(Equals(named_node['flow_rate'], Plus(total_flow_in)))

    def translate_channel(self, name):
        """Create SMT expressions for a given channel (edges in NetworkX naming)
        currently only works for channels with a rectangular shape, but should
        be expanded to include circular and parabolic

        :param str name: The name of the channel to generate SMT equations for
        :returns: None -- no issues with translating channel parameters to SMT
        :raises: KeyError, if channel is not found in the list of defined edges
        """
        try:
            named_channel = self.dg.edges[name]
        except KeyError:
            raise KeyError('Channel with ports %s was not defined' % name)

        port_in_name = named_channel['port_from']
        port_out_name = named_channel['port_to']
        port_in = self.dg.nodes[port_in_name]
        port_out = self.dg.nodes[port_out_name]
        self.exprs.append(self.pythagorean_length(name))
        if named_channel['min_length']:
            self.exprs.append(Equals(named_channel['length'], Real(named_channel['min_length'])))
        else:
            self.exprs.append(GT(named_channel['length'], Real(0)))
        if named_channel['min_width']:
            self.exprs.append(Equals(named_channel['width'], Real(named_channel['min_width'])))
        else:
            self.exprs.append(GT(named_channel['width'], Real(0)))
        if named_channel['min_height']:
            self.exprs.append(Equals(named_channel['height'], Real(named_channel['min_height'])))
        else:
            self.exprs.append(GT(named_channel['height'], Real(0)))
        self.exprs.append(Equals(named_channel['viscosity'], port_in['viscosity']))
        self.exprs.append(Equals(port_out['viscosity'], port_in['viscosity']))
        resistance_list = self.calculate_channel_resistance(name)
        self.exprs.append(resistance_list[0])
        resistance = resistance_list[1]
        self.exprs.append(Equals(named_channel['resistance'], resistance))
        self.exprs.append(GT(named_channel['resistance'], Real(0)))
        self.exprs.append(Equals(named_channel['flow_rate'], port_in['flow_rate']))
        self.translation_strats[port_out['kind']](port_out_name)

    def translate_tjunc(self, name, crit_crossing_angle=0.5):
        """Create SMT expressions for a t-junction node that generates droplets
        Must have 2 input channels (continuous and dispersed phases) and one
        output channel where the droplets leave the node. Continuous is usually
        oil and dispersed is usually water

        :param str name: The name of the channel to generate SMT equations for
        :param crit_crossing_angle: The angle of the dispersed channel to
            the continuous must be great than this to have droplet generation
        :returns: None -- no issues with translating channel parameters to SMT
        :raises: KeyError, if channel is not found in the list of defined edges
        """
        if self.dg.size(name) != 3:
            raise ValueError('T-junction %s must have 3 connections' % name)
        self.translate_node(name)
        try:
            output_node_name = list(dict(self.dg.succ[name]).keys())[0]
            output_node = self.dg.nodes[output_node_name]
            output_channel = self.dg[name][output_node_name]
        except KeyError as e:
            raise KeyError('T-junction must have only one output')

        junction_node_name = name
        junction_node = self.dg.nodes[name]
        continuous_node = ''
        continuous_node_name = ''
        continuous_channel = ''
        dispersed_node = ''
        dispersed_node_name = ''
        dispersed_channel = ''
        phases = nx.get_edge_attributes(self.dg, 'phase')
        for pred_node, phase in phases.items():
            if phase == 'continuous':
                continuous_node_name = pred_node[0]
                continuous_node = self.dg.nodes[continuous_node_name]
                continuous_channel = self.dg[continuous_node_name][junction_node_name]
                self.exprs.append(Equals(continuous_channel['width'], output_channel['width']))
                self.exprs.append(Equals(continuous_channel['height'], output_channel['height']))
            else:
                if phase == 'dispersed':
                    dispersed_node_name = pred_node[0]
                    dispersed_node = self.dg.nodes[dispersed_node_name]
                    dispersed_channel = self.dg[dispersed_node_name][junction_node_name]
                    self.exprs.append(Equals(dispersed_channel['height'], output_channel['height']))
                else:
                    if phase == 'output':
                        continue
                    else:
                        raise ValueError('Invalid phase for T-junction: %s' % name)

        epsilon = Symbol('epsilon', REAL)
        self.exprs.append(GE(epsilon, Real(0)))
        self.exprs.append(Equals(continuous_node['viscosity'], output_node['viscosity']))
        self.exprs.append(Equals(Plus(continuous_channel['flow_rate'], dispersed_channel['flow_rate']), output_channel['flow_rate']))
        self.exprs.append(self.channels_in_straight_line(continuous_node_name, junction_node_name, output_node_name))
        v_output = output_channel['droplet_volume']
        self.exprs.append(Equals(v_output, self.calculate_droplet_volume(output_channel['height'], output_channel['width'], dispersed_channel['width'], epsilon, dispersed_node['flow_rate'], continuous_node['flow_rate'])))
        cosine_squared_theta_crit = Real(math.cos(math.radians(crit_crossing_angle)) ** 2)
        self.exprs.append(LE(cosine_squared_theta_crit, self.cosine_law_crit_angle(continuous_node_name, junction_node_name, dispersed_node_name)))
        self.exprs.append(LE(cosine_squared_theta_crit, self.cosine_law_crit_angle(continuous_node_name, junction_node_name, output_node_name)))
        self.exprs.append(LE(cosine_squared_theta_crit, self.cosine_law_crit_angle(output_node_name, junction_node_name, dispersed_node_name)))
        self.translation_strats[output_node['kind']](output_node_name)

    def channels_in_straight_line(self, node1_name, node2_name, node3_name):
        """Create expressions to assert that 2 channels are in a straight
        line with each other by asserting that a triangle between the 2
        end nodes and the middle node has zero area

        :channel_name1: Name of one of the channels
        :channel_name2: Name of the other channel
        :returns: Expression asserting area of triangle formed between all
            three nodes to be 0
        """
        try:
            self.dg[node1_name][node2_name]
            self.dg[node2_name][node3_name]
        except TypeError as e:
            raise TypeError("Tried asserting that 2 channels are in a straight                line but they aren't connected")

        node1_named = self.dg.nodes[node1_name]
        node2_named = self.dg.nodes[node2_name]
        node3_named = self.dg.nodes[node3_name]
        return Equals(Real(0), Div(Plus(Times(node1_named['x'], Minus(node3_named['y'], node2_named['y'])), Plus(Times(node3_named['x'], Minus(node2_named['y'], node1_named['y'])), Times(node2_named['x'], Minus(node1_named['y'], node3_named['y'])))), Real(2)))

    def simple_pressure_flow(self, channel_name):
        """Assert difference in pressure at the two end nodes for a channel
        equals the flow rate in the channel times the channel resistance
        More complicated calculation available through
        analytical_pressure_flow method (TBD)

        :param str channel_name: Name of the channel
        :returns: SMT expression of equality between delta(P) and Q*R
        """
        channel = self.dg.edges[channel_name]
        port_from_name = channel['port_from']
        port_from = self.dg.nodes[port_from_name]
        port_to_name = channel['port_to']
        port_to = self.dg.nodes[port_to_name]
        p1 = port_from['pressure']
        p2 = port_to['pressure']
        Q = channel['flow_rate']
        R = channel['resistance']
        return Equals(Minus(p1, p2), Times(Q, R))

    def channel_output_pressure(self, channel_name):
        """Calculate the pressure at the output of a channel using
        P_out = R * Q - P_in
        Unit for pressure is Pascals - kg/(m*s^2)

        :param str channel_name: Name of the channel
        :returns: SMT expression of the difference between pressure
            into the channel and R*Q
        """
        channel = self.dg.edges[channel_name]
        P_in = self.dg.nodes[channel_name[0]]['pressure']
        R = channel['resistance']
        Q = channel['flow_rate']
        return Minus(P_in, Times(R, Q))

    def calculate_channel_resistance(self, channel_name):
        """Calculate the droplet resistance in a channel using:
        R = (12 * mu * L) / (w * h^3 * (1 - 0.630 (h/w)) )
        This formula assumes that channel height < width, so
        the first term returned is the assertion for that
        Unit for resistance is kg/(m^4*s)

        :param str channel_name: Name of the channel
        :returns: list -- two SMT expressions, first asserts
            that channel height is less than width, second
            is the above expression in SMT form
        """
        channel = self.dg.edges[channel_name]
        w = channel['width']
        h = channel['height']
        mu = channel['viscosity']
        chL = channel['length']
        return (
         LT(h, w),
         Div(Times(Real(12), Times(mu, chL)), Times(w, Times(Pow(h, Real(3)), Minus(Real(1), Times(Real(0.63), Div(h, w)))))))

    def pythagorean_length(self, channel_name):
        """Use Pythagorean theorem to assert that the channel length
        (hypoteneuse) squared is equal to the legs squared so channel
        length is solved for

        :param str channel_name: Name of the channel
        :returns: SMT expression of the equality of the side lengths squared
            and the channel length squared
        """
        channel = self.dg.edges[channel_name]
        port_from = self.dg.nodes[channel_name[0]]
        port_to = self.dg.nodes[channel_name[1]]
        side_a = Minus(port_from['x'], port_to['x'])
        side_b = Minus(port_from['y'], port_to['y'])
        a_squared = Pow(side_a, Real(2))
        b_squared = Pow(side_b, Real(2))
        a_squared_plus_b_squared = Plus(a_squared, b_squared)
        c_squared = Pow(channel['length'], Real(2))
        return Equals(a_squared_plus_b_squared, c_squared)

    def cosine_law_crit_angle(self, node1_name, node2_name, node3_name):
        """Use cosine law to find cos^2(theta) between three points
        node1---node2---node3 to assert that it is less than cos^2(thetaC)
        where thetaC is the critical crossing angle

        :param node1: Outside node
        :param node2: Middle connecting node
        :param node3: Outside node
        :returns: cos^2 as calculated using cosine law (a_dot_b^2/a^2*b^2)
        """
        node1 = self.dg.nodes[node1_name]
        node2 = self.dg.nodes[node2_name]
        node3 = self.dg.nodes[node3_name]
        aX = Minus(node1['x'], node2['x'])
        aY = Minus(node1['y'], node2['y'])
        bX = Minus(node3['x'], node2['x'])
        bY = Minus(node3['y'], node2['y'])
        a_dot_b_squared = Pow(Plus(Times(aX, bX), Times(aY, bY)), Real(2))
        a_squared_b_squared = Times(Plus(Times(aX, aX), Times(aY, aY)), Plus(Times(bX, bX), Times(bY, bY)))
        return Div(a_dot_b_squared, a_squared_b_squared)

    def calculate_droplet_volume(self, h, w, wIn, epsilon, qD, qC):
        """From paper DOI:10.1039/c002625e.
        Calculating the droplet volume created in a T-junction
        Unit is volume in m^3

        :param Symbol h: Height of channel
        :param Symbol w: Width of continuous/output channel
        :param Symbol wIn: Width of dispersed_channel
        :param Symbol epsilon: Equals 0.414*radius of rounded edge where
                               channels join
        :param Symbol qD: Flow rate in dispersed_channel
        :param Symbol qC: Flow rate in continuous_channel
        """
        q_gutter = Real(0.1)
        v_fill_simple = Minus(Times(Real((3, 8)), Real(math.pi)), Times(Times(Div(Real(math.pi), Real(2)), Minus(Real(1), Div(Real(math.pi), Real(4)))), Div(h, w)))
        hw_parallel = Div(Times(h, w), Plus(h, w))
        r_pinch = Plus(w, Plus(Minus(wIn, Minus(hw_parallel, epsilon)), Pow(Times(Real(2), Times(Minus(wIn, hw_parallel), Minus(w, hw_parallel))), Real(0.5))))
        r_fill = w
        alpha = Times(Minus(Real(1), Div(Real(math.pi), Real(4))), Times(Pow(Minus(Real(1), q_gutter), Real(-1)), Plus(Minus(Pow(Div(r_pinch, w), Real(2)), Pow(Div(r_fill, w), Real(2))), Times(Div(Real(math.pi), Real(4)), Times(Minus(Div(r_pinch, w), Div(r_fill, w)), Div(h, w))))))
        return Times(Times(h, Times(w, w)), Plus(v_fill_simple, Times(alpha, Div(qD, qC))))

    def calculate_port_flow_rate(self, port_name):
        """Calculate the flow rate into a port based on the cross sectional
        area of the channel it flows into, the pressure and the density
        eqn from https://en.wikipedia.org/wiki/Hagen-Poiseuille_equation
        flow_rate = area * sqrt(2*pressure/density)
        Unit for flow rate is m^3/s

        :param str port_name: Name of the port
        :returns: Flow rate determined from port pressure and area of
                  connected channels
        """
        areas = []
        port_named = self.dg.nodes[port_name]
        for port_out in self.dg.succ[port_name]:
            areas.append(Times(self.dg[port_name][port_out]['length'], self.dg[port_name][port_out]['width']))

        total_area = Plus(areas)
        return Times(total_area, Pow(Div(Times(Real(2), port_named['pressure']), port_named['density']), Real(0.5)))

    def translate_schematic(self):
        """Validates that each node has the correct input and output
        conditions met then translates it into pysmt syntax
        Generates SMT formulas to simulate specialized nodes like T-junctions
        and stores them in self.exprs
        """
        has_input = False
        for name in self.dg.nodes:
            kind = self.dg.nodes[name]['kind']
            if kind == 'input':
                has_input = True
                has_output = False
                for x, y in self.dg.nodes(data=True):
                    if y['kind'] == 'output':
                        has_output = True
                        self.translation_strats[kind](name)

                if not has_output:
                    raise ValueError('Schematic input %s has no output' % name)

        if not has_input:
            raise ValueError('Schematic has no input')
        for name in self.dg.nodes:
            self.translate_chip(name)

    def invoke_backend(self, _show):
        """Combine all of the SMT expressions into one expression to sent to Z3
        solver to determine solvability

        :param bool show: If true then the full SMT formula that was created is
                          printed
        :returns: pySMT model showing the values for each of the parameters
        """
        formula = And(self.exprs)
        if _show:
            pprint(formula.serialize())
        model = get_model(formula, solver_name='z3', logic=QF_NRA)
        if model:
            return model
        else:
            return 'No solution found'

    def solve(self, show=False):
        """Create the SMT2 equation for this schematic outlining the design
        of a microfluidic circuit and use Z3 to solve it using pysmt

        :param bool show: If true then the full SMT formula that was created is
                          printed
        :returns: pySMT model showing the values for each of the parameters
        """
        self.translate_schematic()
        return self.invoke_backend(show)