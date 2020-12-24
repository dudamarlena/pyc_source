# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\transport_network_analysis\core.py
# Compiled at: 2019-03-21 16:05:34
# Size of source mod 2**32: 38477 bytes
"""Main module."""
import json, logging, uuid, simpy, networkx as nx, pyproj, shapely.geometry, datetime, time
logger = logging.getLogger(__name__)

class SimpyObject:
    __doc__ = 'General object which can be extended by any class requiring a simpy environment\n\n    env: a simpy Environment\n    '

    def __init__(self, env, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.env = env


class Identifiable:
    __doc__ = 'Something that has a name and id\n\n    name: a name\n    id: a unique id generated with uuid'

    def __init__(self, name, id=None, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.name = name
        self.id = id if id else str(uuid.uuid1())


class Locatable:
    __doc__ = 'Something with a geometry (geojson format)\n\n    geometry: can be a point as well as a polygon'

    def __init__(self, geometry, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.geometry = geometry


class Neighbours:
    __doc__ = 'Can be added to a locatable object (list)\n    \n    travel_to: list of locatables to which can be travelled'

    def ___init(self, travel_to, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.neighbours = travel_to


class HasContainer(SimpyObject):
    __doc__ = 'Container class\n\n    capacity: amount the container can hold\n    level: amount the container holds initially\n    container: a simpy object that can hold stuff'

    def __init__(self, capacity, level=0, total_requested=0, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.container = simpy.Container((self.env), capacity, init=level)
        self.total_requested = total_requested

    @property
    def is_loaded(self):
        if self.container.level > 0:
            return True
        return False

    @property
    def filling_degree(self):
        return self.container.level / self.container.capacity


class VesselProperties:
    __doc__ = '\n    Add information on possible restrictions to the vessels.\n    Height, width, etc.\n    '

    def __init__(self, vessel_type, installed_power, width, length, height_empty, height_full, draught_empty, draught_full, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.vessel_type = vessel_type
        self.installed_power = installed_power
        self.width = width
        self.length = length
        self.height_empty = height_empty
        self.height_full = height_full
        self.draught_empty = draught_empty
        self.draught_full = draught_full

    @property
    def current_height(self):
        """ Calculate current height based on filling degree """
        return self.filling_degree * (self.height_full - self.height_empty) + self.height_empty

    @property
    def current_draught(self):
        """ Calculate current draught based on filling degree """
        return self.filling_degree * (self.draught_full - self.draught_empty) + self.draught_empty


class HasEnergy:
    __doc__ = '\n    Add information on energy use and effects on energy use.\n    '

    def __init__(self, emissionfactor, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.emissionfactor = emissionfactor
        self.energy_use = {'total':0,  'stationary':0}
        self.co2_footprint = {'total_footprint':0,  'stationary':0}
        self.mki_footprint = {'total_footprint':0,  'stationary':0}

    @property
    def power(self):
        return 2 * (self.current_speed * self.resistance * 0.001)

    def calculate_energy_consumption(self):
        """Calculation of energy consumption based on total time in system and properties"""
        stationary_phase_indicator = [
         'Doors closing stop', 'Converting chamber stop', 'Doors opening stop', 'aiting to pass lock stop']
        times = self.log['Timestamp']
        messages = self.log['Message']
        for i in range(len(times) - 1):
            delta_t = times[(i + 1)] - times[i]
            if messages[(i + 1)] in stationary_phase_indicator:
                energy_delta = self.power * delta_t / 3600
                self.energy_use['total_energy'] += energy_delta * 0.15
                self.energy_use['stationary'] += energy_delta * 0.15
            else:
                self.energy_use['total_energy'] += self.power * delta_t / 3600


class Routeable:
    __doc__ = 'Something with a route (networkx format)\n    route: a networkx path'

    def __init__(self, route, complete_path=None, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.route = route
        self.complete_path = complete_path


class IsLock:
    __doc__ = '\n    Create a lock object\n    '

    def __init__(self, nodes, neighbour_lock, lock_length, lock_width, doors_open, doors_close, operating_time, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.nodes = nodes
        self.neighbour_lock = neighbour_lock
        self.lock_length = lock_length
        self.lock_width = lock_width
        self.doors_open = doors_open
        self.doors_close = doors_close
        self.operating_time = operating_time


class Movable(SimpyObject, Locatable, Routeable):
    __doc__ = 'Movable class\n\n    Used for object that can move with a fixed speed\n    geometry: point used to track its current location\n    v: speed'

    def __init__(self, v=1, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.v = v
        self.wgs84 = pyproj.Geod(ellps='WGS84')

    def move(self):
        """determine distance between origin and destination, and
        yield the time it takes to travel it
        
        Assumption is that self.path is in the right order - vessel moves from route[0] to route[-1].
        """
        self.distance = 0
        if self.geometry != nx.get_node_attributes(self.env.FG, 'geometry')[self.route[0]]:
            orig = self.geometry
            dest = nx.get_node_attributes(self.env.FG, 'geometry')[self.route[0]]
            print('Origin', orig)
            print('Destination', dest)
            self.distance += self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]
            yield self.env.timeout(self.distance / self.current_speed)
            self.log_entry('Sailing to start', self.env.now, self.distance, dest)
        for node in enumerate(self.route):
            origin = self.route[node[0]]
            destination = self.route[(node[0] + 1)]
            edge = self.env.FG.edges[(origin, destination)]
            if 'Object' in edge.keys():
                if edge['Object'] == 'Lock':
                    yield from self.pass_lock(origin, destination)
                else:
                    if edge['Object'] == 'Waiting Area':
                        yield from self.pass_waiting_area(origin, destination, self.route[(node[0] + 2)])
                    else:
                        yield from self.pass_edge(origin, destination)
            else:
                yield from self.pass_edge(origin, destination)
            if node[0] + 2 == len(self.route):
                break

        self.geometry = nx.get_node_attributes(self.env.FG, 'geometry')[destination]
        logger.debug('  distance: ' + '%4.2f' % self.distance + ' m')
        logger.debug('  sailing:  ' + '%4.2f' % self.current_speed + ' m/s')
        logger.debug('  duration: ' + '%4.2f' % (self.distance / self.current_speed / 3600) + ' hrs')

    def pass_edge(self, origin, destination):
        edge = self.env.FG.edges[(origin, destination)]
        orig = nx.get_node_attributes(self.env.FG, 'geometry')[origin]
        dest = nx.get_node_attributes(self.env.FG, 'geometry')[destination]
        distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]
        self.distance += distance
        arrival = self.env.now
        if 'Resources' in edge.keys():
            with self.env.FG.edges[(origin, destination)]['Resources'].request() as (request):
                yield request
                if arrival != self.env.now:
                    self.log_entry('Waiting to pass edge {} - {} start'.format(origin, destination), arrival, 0, orig)
                    self.log_entry('Waiting to pass edge {} - {} stop'.format(origin, destination), self.env.now, 0, orig)
                self.log_entry('Sailing from node {} to node {} start'.format(origin, destination), self.env.now, 0, orig)
                yield self.env.timeout(distance / self.current_speed)
                self.log_entry('Sailing from node {} to node {} stop'.format(origin, destination), self.env.now, 0, dest)
        else:
            self.log_entry('Sailing from node {} to node {} start'.format(origin, destination), self.env.now, 0, orig)
            yield self.env.timeout(distance / self.current_speed)
            self.log_entry('Sailing from node {} to node {} start'.format(origin, destination), self.env.now, 0, dest)

    def pass_lock(self, origin, destination):
        edge = self.env.FG.edges[(origin, destination)]
        edge_opposite = self.env.FG.edges[(destination, origin)]
        orig = nx.get_node_attributes(self.env.FG, 'geometry')[origin]
        dest = nx.get_node_attributes(self.env.FG, 'geometry')[destination]
        water_level = origin
        distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]
        self.distance += distance
        arrival = self.env.now
        if 'Water level' in edge.keys():
            if edge['Water level'] == water_level:
                priority = 0
            else:
                priority = 1
        else:
            priority = 0
        with self.env.FG.edges[(origin, destination)]['Resources'].request(priority=priority) as (request):
            yield request
            if arrival != self.env.now:
                self.log_entry('Waiting to pass lock start'.format(origin, destination), arrival, 0, orig)
                self.log_entry('Waiting to pass lock stop'.format(origin, destination), self.env.now, 0, orig)
            if 'Water level' in edge.keys():
                if water_level != edge['Water level']:
                    self.log_entry('Doors closing start', self.env.now, 0, orig)
                    yield self.env.timeout(600)
                    self.log_entry('Doors closing stop', self.env.now, 0, orig)
                    self.log_entry('Converting chamber start', self.env.now, 0, orig)
                    yield self.env.timeout(1200)
                    self.log_entry('Converting chamber stop', self.env.now, 0, orig)
                    self.log_entry('Doors opening start', self.env.now, 0, orig)
                    yield self.env.timeout(600)
                    self.log_entry('Doors opening start', self.env.now, 0, orig)
                    self.env.FG.edges[(origin, destination)]['Water level'] = water_level
            if 'Water level' not in edge.keys() or edge['Water level'] == water_level:
                chamber = shapely.geometry.Point((orig.x + dest.x) / 2, (orig.y + dest.y) / 2)
                self.log_entry('Sailing into lock start', self.env.now, 0, orig)
                yield self.env.timeout(300)
                self.log_entry('Sailing into lock stop', self.env.now, 0, chamber)
                self.log_entry('Doors closing start', self.env.now, 0, chamber)
                yield self.env.timeout(600)
                self.log_entry('Doors closing stop', self.env.now, 0, chamber)
                chamber = shapely.geometry.Point((orig.x + dest.x) / 2, (orig.y + dest.y) / 2)
                self.log_entry('Converting chamber start', self.env.now, 0, chamber)
                yield self.env.timeout(1200)
                self.log_entry('Converting chamber stop', self.env.now, 0, chamber)
                self.log_entry('Doors opening start', self.env.now, 0, chamber)
                yield self.env.timeout(600)
                self.log_entry('Doors opening stop', self.env.now, 0, chamber)
                self.log_entry('Sailing out of lock start', self.env.now, 0, chamber)
                yield self.env.timeout(300)
                self.log_entry('Sailing out of lock stop', self.env.now, 0, dest)
                self.env.FG.edges[(origin, destination)]['Water level'] = destination
            self.env.FG.edges[(origin, destination)]['Water level'] = destination

    def pass_waiting_area(self, origin, destination, lock):
        edge = self.env.FG.edges[(origin, destination)]
        edge_lock = self.env.FG.edges[(destination, lock)]
        orig = nx.get_node_attributes(self.env.FG, 'geometry')[origin]
        dest = nx.get_node_attributes(self.env.FG, 'geometry')[destination]
        water_level = destination
        distance = self.wgs84.inv(shapely.geometry.asShape(orig).x, shapely.geometry.asShape(orig).y, shapely.geometry.asShape(dest).x, shapely.geometry.asShape(dest).y)[2]
        self.distance += distance
        arrival = self.env.now
        if 'Resources' in edge.keys():
            with self.env.FG.edges[(origin, destination)]['Resources'].request() as (request):
                yield request
                if arrival != self.env.now:
                    self.log_entry('Waiting to pass edge {} - {} start'.format(origin, destination), arrival, 0, orig)
                    self.log_entry('Waiting to pass edge {} - {} stop'.format(origin, destination), self.env.now, 0, orig)
                elif 'Water level' in edge_lock.keys():
                    if edge_lock['Water level'] != water_level:
                        self.log_entry('Waiting to pass lock start'.format(origin, destination), self.env.now, 0, orig)
                        while edge_lock['Water level'] != water_level:
                            yield self.env.timeout(60)

                        self.log_entry('Waiting to pass lock stop'.format(origin, destination), self.env.now, 0, dest)
                    else:
                        self.log_entry('Sailing from node {} to node {}'.format(origin, destination), self.env.now, 0, dest)
                        yield self.env.timeout(distance / self.current_speed)
                        self.log_entry('Sailing from node {} to node {}'.format(origin, destination), self.env.now, 0, dest)
                else:
                    self.log_entry('Sailing from node {} to node {}'.format(origin, destination), self.env.now, 0, dest)
                    yield self.env.timeout(distance / self.current_speed)
                    self.log_entry('Sailing from node {} to node {}'.format(origin, destination), self.env.now, 0, dest)
        else:
            yield self.env.timeout(distance / self.current_speed)
            self.log_entry('Sailing from node {} to node {}'.format(origin, destination), self.env.now, 0, dest)

    def is_at(self, locatable, tolerance=100):
        current_location = shapely.geometry.asShape(self.geometry)
        other_location = shapely.geometry.asShape(locatable.geometry)
        _, _, distance = self.wgs84.inv(current_location.x, current_location.y, other_location.x, other_location.y)
        return distance < tolerance

    @property
    def current_speed(self):
        return self.v


class ContainerDependentMovable(Movable, HasContainer):
    __doc__ = 'ContainerDependentMovable class\n\n    Used for objects that move with a speed dependent on the container level\n    compute_v: a function, given the fraction the container is filled (in [0,1]), returns the current speed'

    def __init__(self, compute_v, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.compute_v = compute_v
        self.wgs84 = pyproj.Geod(ellps='WGS84')

    @property
    def current_speed(self):
        return self.compute_v(self.container.level / self.container.capacity)


class HasResource(SimpyObject):
    __doc__ = 'HasProcessingLimit class\n\n    Adds a limited Simpy resource which should be requested before the object is used for processing.'

    def __init__(self, nr_resources=1, priority=False, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.resource = simpy.PriorityResource((self.env), capacity=nr_resources) if priority else simpy.Resource((self.env), capacity=nr_resources)


class Log(SimpyObject):
    __doc__ = "Log class\n\n    log: log message [format: 'start activity' or 'stop activity']\n    t: timestamp\n    value: a value can be logged as well\n    geometry: value from locatable (lat, lon)"

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.log = {'Message':[],  'Timestamp':[],  'Value':[],  'Geometry':[]}

    def log_entry(self, log, t, value, geometry_log):
        """Log"""
        self.log['Message'].append(log)
        self.log['Timestamp'].append(datetime.datetime.fromtimestamp(t))
        self.log['Value'].append(value)
        self.log['Geometry'].append(geometry_log)

    def get_log_as_json(self):
        json = []
        for msg, t, value, geometry_log in zip(self.log['Message'], self.log['Timestamp'], self.log['Value'], self.log['Geometry']):
            json.append(dict(message=msg, time=t, value=value, geometry_log=geometry_log))

        return json


class Processor(SimpyObject):
    __doc__ = 'Processor class\n\n    rate: rate with which quantity can be processed [amount/s]'

    def __init__(self, rate, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.rate = rate

    def process(self, origin, destination, amount, origin_resource_request=None, destination_resource_request=None):
        """get amount from origin container, put amount in destination container,
        and yield the time it takes to process it"""
        if isinstance(origin, HasContainer):
            raise isinstance(destination, HasContainer) or AssertionError
        else:
            if not (isinstance(origin, HasResource) and isinstance(destination, HasResource)):
                raise AssertionError
            raise isinstance(origin, Log) and isinstance(destination, Log) or AssertionError
        assert origin.container.level >= amount
        assert destination.container.capacity - destination.container.level >= amount
        my_origin_turn = origin_resource_request
        if my_origin_turn is None:
            my_origin_turn = origin.resource.request()
        my_dest_turn = destination_resource_request
        if my_dest_turn is None:
            my_dest_turn = destination.resource.request()
        yield my_origin_turn
        yield my_dest_turn
        origin.log_entry('unloading start', self.env.now, origin.container.level)
        destination.log_entry('loading start', self.env.now, destination.container.level)
        origin.container.get(amount)
        destination.container.put(amount)
        yield self.env.timeout(amount / self.rate)
        origin.log_entry('unloading stop', self.env.now, origin.container.level)
        destination.log_entry('loading stop', self.env.now, destination.container.level)
        logger.debug('  process:        ' + '%4.2f' % (amount / self.rate / 3600) + ' hrs')
        if origin_resource_request is None:
            origin.resource.release(my_origin_turn)
        if destination_resource_request is None:
            destination.resource.release(my_dest_turn)


class DictEncoder(json.JSONEncoder):
    __doc__ = 'serialize a simpy digital_twin object to json'

    def default(self, o):
        result = {}
        for key, val in o.__dict__.items():
            if isinstance(val, simpy.Environment):
                continue
            if isinstance(val, simpy.Container):
                result['capacity'] = val.capacity
                result['level'] = val.level
            elif isinstance(val, simpy.Resource):
                result['nr_resources'] = val.capacity
            else:
                result[key] = val

        return result


def serialize(obj):
    return json.dumps(obj, cls=DictEncoder)