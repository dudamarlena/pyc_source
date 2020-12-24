# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/models.py
# Compiled at: 2020-04-24 19:15:49
# Size of source mod 2**32: 63686 bytes
"""Define Dallinger's core models."""
from datetime import datetime
import inspect
from sqlalchemy import ForeignKey, or_, and_
from sqlalchemy import Column, String, Text, Enum, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import relationship, validates
from .db import Base
DATETIME_FMT = '%Y-%m-%dT%H:%M:%S.%f'

def timenow():
    """A string representing the current date and time."""
    return datetime.now()


class SharedMixin(object):
    __doc__ = 'Create shared columns.'
    id = Column(Integer, primary_key=True, index=True)
    creation_time = Column(DateTime, nullable=False, default=timenow, index=True)
    property1 = Column(Text, nullable=True, default=None)
    property2 = Column(Text, nullable=True, default=None)
    property3 = Column(Text, nullable=True, default=None)
    property4 = Column(Text, nullable=True, default=None)
    property5 = Column(Text, nullable=True, default=None)
    failed = Column(Boolean, nullable=False, default=False, index=True)
    time_of_death = Column(DateTime, default=None)
    details = Column(JSONB, nullable=False, server_default='{}', default=(lambda : {}))

    def json_data(self):
        return {}

    def __json__(self):
        """Return json description of a participant."""
        model_data = {'id':self.id, 
         'creation_time':self.creation_time, 
         'failed':self.failed, 
         'time_of_death':self.time_of_death, 
         'property1':self.property1, 
         'property2':self.property2, 
         'property3':self.property3, 
         'property4':self.property4, 
         'property5':self.property5, 
         'details':self.details}
        model_data.update(self.json_data())
        return model_data


class Participant(Base, SharedMixin):
    __doc__ = 'An ex silico participant.'
    __tablename__ = 'participant'
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_on':type,  'polymorphic_identity':'participant'}
    fingerprint_hash = Column((String(50)), nullable=True)
    recruiter_id = Column((String(50)), nullable=True)
    worker_id = Column((String(50)), nullable=False)
    assignment_id = Column((String(50)), nullable=False, index=True)
    unique_id = Column((String(75)), nullable=False, index=True)
    hit_id = Column((String(50)), nullable=False)
    mode = Column((String(50)), nullable=False)
    end_time = Column(DateTime)
    base_pay = Column(Float)
    bonus = Column(Float)
    status = Column(Enum('working',
      'overrecruited',
      'submitted',
      'approved',
      'rejected',
      'returned',
      'abandoned',
      'did_not_attend',
      'bad_data',
      'missing_notification',
      'replaced',
      name='participant_status'),
      nullable=False,
      default='working',
      index=True)

    def __init__(self, recruiter_id, worker_id, assignment_id, hit_id, mode, fingerprint_hash=None):
        """Create a participant."""
        self.recruiter_id = recruiter_id
        self.worker_id = worker_id
        self.assignment_id = assignment_id
        self.hit_id = hit_id
        self.unique_id = worker_id + ':' + assignment_id
        self.mode = mode
        self.fingerprint_hash = fingerprint_hash

    def json_data(self):
        """Return json description of a participant."""
        return {'type':self.type, 
         'recruiter':self.recruiter_id, 
         'assignment_id':self.assignment_id, 
         'hit_id':self.hit_id, 
         'mode':self.mode, 
         'end_time':self.end_time, 
         'base_pay':self.base_pay, 
         'bonus':self.bonus, 
         'status':self.status}

    def nodes(self, type=None, failed=False):
        """Get nodes associated with this participant.

        Return a list of nodes associated with the participant. If specified,
        ``type`` filters by class. By default failed nodes are excluded, to
        include only failed nodes use ``failed=True``, for all nodes use
        ``failed=all``.

        """
        if type is None:
            type = Node
        else:
            if not issubclass(type, Node):
                raise TypeError('{} is not a valid node type.'.format(type))
            if failed not in ('all', False, True):
                raise ValueError('{} is not a valid node failed'.format(failed))
        if failed == 'all':
            return type.query.filter_by(participant_id=(self.id)).all()
        else:
            return type.query.filter_by(failed=failed, participant_id=(self.id)).all()

    def questions(self, type=None):
        """Get questions associated with this participant.

        Return a list of questions associated with the participant. If
        specified, ``type`` filters by class.

        """
        if type is None:
            type = Question
        if not issubclass(type, Question):
            raise TypeError('{} is not a valid question type.'.format(type))
        return type.query.filter_by(participant_id=(self.id)).all()

    def infos(self, type=None, failed=False):
        """Get all infos created by the participants nodes.

        Return a list of infos produced by nodes associated with the
        participant. If specified, ``type`` filters by class. By default, failed
        infos are excluded, to include only failed nodes use ``failed=True``,
        for all nodes use ``failed=all``. Note that failed filters the infos,
        not the nodes - infos from all nodes (whether failed or not) can be
        returned.

        """
        nodes = self.nodes(failed='all')
        infos = []
        for n in nodes:
            infos.extend(n.infos(type=type, failed=failed))

        return infos

    def fail(self):
        """Fail a participant.

        Set :attr:`~dallinger.models.SharedMixin.failed` to ``True`` and
        :attr:`~dallinger.models.SharedMixin.time_of_death` to now. Instruct all
        not-failed nodes associated with the participant to fail.

        """
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()
            for n in self.nodes():
                n.fail()

            for q in self.questions():
                q.fail()

    @property
    def recruiter(self):
        from dallinger import recruiters
        recruiter_name = self.recruiter_id or 'hotair'
        if recruiter_name.startswith('bots:'):
            recruiter_name = 'bots'
        return recruiters.by_name(recruiter_name)


class Question(Base, SharedMixin):
    __doc__ = 'Responses of a participant to debriefing questions.'
    __tablename__ = 'question'
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_on':type,  'polymorphic_identity':'question'}
    participant_id = Column(Integer, ForeignKey('participant.id'))
    participant = relationship(Participant, backref='all_questions')
    number = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

    def __init__(self, participant, question, response, number):
        """Create a question."""
        if participant.failed:
            raise ValueError('{} cannot create a question as it has failed'.format(participant))
        self.participant = participant
        self.participant_id = participant.id
        self.number = number
        self.question = question
        self.response = response

    def fail(self):
        """Fail a question.

        Set :attr:`~dallinger.models.SharedMixin.failed` to True and
        :attr:`~dallinger.models.SharedMixin.time_of_death` to now.

        """
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()

    def json_data(self):
        """Return json description of a question."""
        return {'number':self.number, 
         'type':self.type, 
         'participant_id':self.participant_id, 
         'question':self.question, 
         'response':self.response}


class Network(Base, SharedMixin):
    __doc__ = 'Contains and manages a set of Nodes and Vectors etc.'
    __tablename__ = 'network'
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_on':type, 
     'polymorphic_identity':'network'}
    max_size = Column(Integer, nullable=False, default=1000000.0)
    full = Column(Boolean, nullable=False, default=False, index=True)
    role = Column((String(26)), nullable=False, default='default', index=True)

    def __repr__(self):
        """The string representation of a network."""
        return '<Network-{}-{} with {} nodes, {} vectors, {} infos, {} transmissions and {} transformations>'.format(self.id, self.type, len(self.nodes()), len(self.vectors()), len(self.infos()), len(self.transmissions()), len(self.transformations()))

    def json_data(self):
        """Return json description of a participant."""
        return {'type':self.type, 
         'max_size':self.max_size, 
         'full':self.full, 
         'role':self.role}

    def nodes(self, type=None, failed=False, participant_id=None):
        """Get nodes in the network.

        type specifies the type of Node. Failed can be "all", False
        (default) or True. If a participant_id is passed only
        nodes with that participant_id will be returned.
        """
        if type is None:
            type = Node
        else:
            if not issubclass(type, Node):
                raise TypeError('{} is not a valid node type.'.format(type))
            if failed not in ('all', False, True):
                raise ValueError('{} is not a valid node failed'.format(failed))
            if participant_id is not None:
                if failed == 'all':
                    return type.query.filter_by(network_id=(self.id),
                      participant_id=participant_id).all()
                else:
                    return type.query.filter_by(network_id=(self.id),
                      participant_id=participant_id,
                      failed=failed).all()
            else:
                if failed == 'all':
                    return type.query.filter_by(network_id=(self.id)).all()
                else:
                    return type.query.filter_by(failed=failed, network_id=(self.id)).all()

    def size(self, type=None, failed=False):
        """How many nodes in a network.

        type specifies the class of node, failed
        can be True/False/all.
        """
        return len(self.nodes(type=type, failed=failed))

    def infos(self, type=None, failed=False):
        """
        Get infos in the network.

        type specifies the type of info (defaults to Info). failed { False,
        True, "all" } specifies the failed state of the infos. To get infos
        from a specific node, see the infos() method in class
        :class:`~dallinger.models.Node`.

        """
        if type is None:
            type = Info
        if failed not in ('all', False, True):
            raise ValueError('{} is not a valid failed'.format(failed))
        if failed == 'all':
            return type.query.filter_by(network_id=(self.id)).all()
        else:
            return type.query.filter_by(network_id=(self.id), failed=failed).all()

    def transmissions(self, status='all', failed=False):
        """Get transmissions in the network.

        status { "all", "received", "pending" }
        failed { False, True, "all" }
        To get transmissions from a specific vector, see the
        transmissions() method in class Vector.
        """
        if status not in ('all', 'pending', 'received'):
            raise ValueError('You cannot get transmission of status {}.'.format(status) + 'Status can only be pending, received or all')
        else:
            if failed not in ('all', False, True):
                raise ValueError('{} is not a valid failed'.format(failed))
            if status == 'all':
                if failed == 'all':
                    return Transmission.query.filter_by(network_id=(self.id)).all()
                else:
                    return Transmission.query.filter_by(network_id=(self.id),
                      failed=failed).all()
            else:
                if failed == 'all':
                    return Transmission.query.filter_by(network_id=(self.id),
                      status=status).all()
                else:
                    return Transmission.query.filter_by(network_id=(self.id),
                      status=status,
                      failed=failed).all()

    def transformations(self, type=None, failed=False):
        """Get transformations in the network.

        type specifies the type of transformation (default = Transformation).
        failed = { False, True, "all" }

        To get transformations from a specific node,
        see Node.transformations().
        """
        if type is None:
            type = Transformation
        if failed not in ('all', True, False):
            raise ValueError('{} is not a valid failed'.format(failed))
        if failed == 'all':
            return type.query.filter_by(network_id=(self.id)).all()
        else:
            return type.query.filter_by(network_id=(self.id), failed=failed).all()

    def latest_transmission_recipient(self):
        """Get the node that most recently received a transmission."""
        from operator import attrgetter
        ts = Transmission.query.filter_by(status='received',
          network_id=(self.id),
          failed=False).all()
        if ts:
            t = max(ts, key=(attrgetter('receive_time')))
            return t.destination
        else:
            return

    def vectors(self, failed=False):
        """
        Get vectors in the network.

        failed = { False, True, "all" }
        To get the vectors to/from to a specific node, see Node.vectors().
        """
        if failed not in ('all', False, True):
            raise ValueError('{} is not a valid vector failed'.format(failed))
        if failed == 'all':
            return Vector.query.filter_by(network_id=(self.id)).all()
        else:
            return Vector.query.filter_by(network_id=(self.id), failed=failed).all()

    def add_node(self, node):
        """Add the node to the network."""
        raise NotImplementedError

    def fail(self):
        """Fail an entire network."""
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()
            for n in self.nodes():
                n.fail()

    def calculate_full(self):
        """Set whether the network is full."""
        self.full = len(self.nodes()) >= (self.max_size or 0)

    def print_verbose(self):
        """Print a verbose representation of a network."""
        print('Nodes: ')
        for a in self.nodes(failed='all'):
            print(a)

        print('\nVectors: ')
        for v in self.vectors(failed='all'):
            print(v)

        print('\nInfos: ')
        for i in self.infos(failed='all'):
            print(i)

        print('\nTransmissions: ')
        for t in self.transmissions(failed='all'):
            print(t)

        print('\nTransformations: ')
        for t in self.transformations(failed='all'):
            print(t)


class Node(Base, SharedMixin):
    __doc__ = 'A point in a network.'
    __tablename__ = 'node'
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_on':type,  'polymorphic_identity':'node'}
    network_id = Column(Integer, (ForeignKey('network.id')), index=True)
    network = relationship(Network, backref='all_nodes')
    participant_id = Column(Integer, (ForeignKey('participant.id')), index=True)
    participant = relationship(Participant, backref='all_nodes')

    def __init__(self, network, participant=None):
        """Create a node."""
        if network.failed:
            raise ValueError('Cannot create node in {} as it has failed'.format(network))
        else:
            if participant is not None:
                if participant.failed:
                    raise ValueError('{} cannot create a node as it has failed'.format(participant))
            if participant is not None:
                if participant.status != 'working':
                    raise ValueError('{} cannot create a node as they are not working'.format(participant))
            self.network = network
            self.network_id = network.id
            network.calculate_full()
            if participant is not None:
                self.participant = participant
                self.participant_id = participant.id

    def __repr__(self):
        """The string representation of a node."""
        return 'Node-{}-{}'.format(self.id, self.type)

    def json_data(self):
        """The json of a node."""
        return {'type':self.type, 
         'network_id':self.network_id, 
         'participant_id':self.participant_id}

    def vectors(self, direction='all', failed=False):
        """Get vectors that connect at this node.

        Direction can be "incoming", "outgoing" or "all" (default).
        Failed can be True, False or all
        """
        if direction not in ('all', 'incoming', 'outgoing'):
            raise ValueError('{} is not a valid vector direction. Must be all, incoming or outgoing.'.format(direction))
        elif failed not in ('all', False, True):
            raise ValueError('{} is not a valid vector failed'.format(failed))
        else:
            if failed == 'all':
                if direction == 'all':
                    return Vector.query.filter(or_(Vector.destination_id == self.id, Vector.origin_id == self.id)).all()
                else:
                    if direction == 'incoming':
                        return Vector.query.filter_by(destination_id=(self.id)).all()
                    if direction == 'outgoing':
                        return Vector.query.filter_by(origin_id=(self.id)).all()
            else:
                if direction == 'all':
                    return Vector.query.filter(and_(Vector.failed == failed, or_(Vector.destination_id == self.id, Vector.origin_id == self.id))).all()
                if direction == 'incoming':
                    return Vector.query.filter_by(destination_id=(self.id),
                      failed=failed).all()
                if direction == 'outgoing':
                    return Vector.query.filter_by(origin_id=(self.id), failed=failed).all()

    def neighbors(self, type=None, direction='to', failed=None):
        """Get a node's neighbors - nodes that are directly connected to it.

        Type specifies the class of neighbour and must be a subclass of
        Node (default is Node).
        Connection is the direction of the connections and can be "to"
        (default), "from", "either", or "both".
        """
        if type is None:
            type = Node
        else:
            if not issubclass(type, Node):
                raise ValueError('{} is not a valid neighbor type,needs to be a subclass of Node.'.format(type))
            else:
                if direction not in ('both', 'either', 'from', 'to'):
                    raise ValueError('{} not a valid neighbor connection.Should be both, either, to or from.'.format(direction))
                elif failed is not None:
                    raise ValueError('You should not pass a failed argument to neighbors(). Neighbors is unusual in that a failed argument cannot be passed. This is because there is inherent uncertainty in what it means for a neighbor to be failed. The neighbors function will only ever return not-failed nodes connected to you via not-failed vectors. If you want to do more elaborate queries, for example, getting not-failed nodes connected to you via failed vectors, you should do so via sql queries.')
                else:
                    neighbors = []
                    if direction == 'to':
                        outgoing_vectors = Vector.query.with_entities(Vector.destination_id).filter_by(origin_id=(self.id),
                          failed=False).all()
                        neighbor_ids = [v.destination_id for v in outgoing_vectors]
                        if neighbor_ids:
                            neighbors = Node.query.filter(Node.id.in_(neighbor_ids)).all()
                            neighbors = [n for n in neighbors if isinstance(n, type)]
                    if direction == 'from':
                        incoming_vectors = Vector.query.with_entities(Vector.origin_id).filter_by(destination_id=(self.id),
                          failed=False).all()
                        neighbor_ids = [v.origin_id for v in incoming_vectors]
                        if neighbor_ids:
                            neighbors = Node.query.filter(Node.id.in_(neighbor_ids)).all()
                            neighbors = [n for n in neighbors if isinstance(n, type)]
                if direction == 'either':
                    neighbors = list(set(self.neighbors(type=type, direction='to') + self.neighbors(type=type, direction='from')))
            if direction == 'both':
                neighbors = list(set(self.neighbors(type=type, direction='to')) & set(self.neighbors(type=type, direction='from')))
        return neighbors

    def is_connected(self, whom, direction='to', failed=None):
        """Check whether this node is connected [to/from] whom.

        whom can be a list of nodes or a single node.
        direction can be "to" (default), "from", "both" or "either".

        If whom is a single node this method returns a boolean,
        otherwise it returns a list of booleans
        """
        if failed is not None:
            raise ValueError('You should not pass a failed argument to is_connected.is_connected is unusual in that a failed argument cannot be passed. This is because there is inherent uncertainty in what it means for a connection to be failed. The is_connected function will only ever check along not-failed vectors. If you want to check along failed vectors you should do so via sql queries.')
        else:
            if isinstance(whom, list):
                is_list = True
            else:
                whom = [
                 whom]
                is_list = False
            whom_ids = [n.id for n in whom]
            for node in whom:
                if not isinstance(node, Node):
                    raise TypeError('is_connected cannot parse objects of type {}.'.format(type(node)))

            if direction not in ('to', 'from', 'either', 'both'):
                raise ValueError('{} is not a valid direction for is_connected'.format(direction))
            connected = []
            if direction == 'to':
                vectors = Vector.query.with_entities(Vector.destination_id).filter_by(origin_id=(self.id),
                  failed=False).all()
                destinations = set([v.destination_id for v in vectors])
                for w in whom_ids:
                    connected.append(w in destinations)

            else:
                if direction == 'from':
                    vectors = Vector.query.with_entities(Vector.origin_id).filter_by(destination_id=(self.id),
                      failed=False).all()
                    origins = set([v.origin_id for v in vectors])
                    for w in whom_ids:
                        connected.append(w in origins)

                elif direction in ('either', 'both'):
                    vectors = Vector.query.with_entities(Vector.origin_id, Vector.destination_id).filter(and_(Vector.failed == false(), or_(Vector.destination_id == self.id, Vector.origin_id == self.id))).all()
                    destinations = set([v.destination_id for v in vectors])
                    origins = set([v.origin_id for v in vectors])
                    if direction == 'either':
                        origins_destinations = destinations.union(origins)
                    else:
                        if direction == 'both':
                            origins_destinations = destinations.intersection(origins)
                        for w in whom_ids:
                            connected.append(w in origins_destinations)

        if is_list:
            return connected
        else:
            return connected[0]

    def infos(self, type=None, failed=False):
        """Get infos that originate from this node.

        Type must be a subclass of :class:`~dallinger.models.Info`, the default is
        ``Info``. Failed can be True, False or "all".

        """
        if type is None:
            type = Info
        else:
            if not issubclass(type, Info):
                raise TypeError('Cannot get infos of type {} as it is not a valid type.'.format(type))
            if failed not in ('all', False, True):
                raise ValueError('{} is not a valid vector failed'.format(failed))
        if failed == 'all':
            return type.query.filter_by(origin_id=(self.id)).all()
        else:
            return type.query.filter_by(origin_id=(self.id), failed=failed).all()

    def received_infos(self, type=None, failed=None):
        """Get infos that have been sent to this node.

        Type must be a subclass of info, the default is Info.
        """
        if failed is not None:
            raise ValueError('You should not pass a failed argument to received_infos. received_infos is unusual in that a failed argument cannot be passed. This is because there is inherent uncertainty in what it means for a received info to be failed. The received_infos function will only ever check not-failed transmissions. If you want to check failed transmissions you should do so via sql queries.')
        else:
            if type is None:
                type = Info
            raise issubclass(type, Info) or TypeError('Cannot get infos of type {} as it is not a valid type.'.format(type))
        transmissions = Transmission.query.with_entities(Transmission.info_id).filter_by(destination_id=(self.id),
          status='received',
          failed=False).all()
        info_ids = [t.info_id for t in transmissions]
        if info_ids:
            return type.query.filter(type.id.in_(info_ids)).all()
        else:
            return []

    def transmissions(self, direction='outgoing', status='all', failed=False):
        """Get transmissions sent to or from this node.

        Direction can be "all", "incoming" or "outgoing" (default).
        Status can be "all" (default), "pending", or "received".
        failed can be True, False or "all"
        """
        if direction not in ('incoming', 'outgoing', 'all'):
            raise ValueError('You cannot get transmissions of direction {}.'.format(direction) + 'Type can only be incoming, outgoing or all.')
        else:
            if status not in ('all', 'pending', 'received'):
                raise ValueError('You cannot get transmission of status {}.'.format(status) + 'Status can only be pending, received or all')
            else:
                if failed not in ('all', False, True):
                    raise ValueError('{} is not a valid transmission failed'.format(failed))
                if direction == 'all':
                    if status == 'all':
                        return Transmission.query.filter(and_(Transmission.failed == false(), or_(Transmission.destination_id == self.id, Transmission.origin_id == self.id))).order_by('creation_time').all()
                    else:
                        return Transmission.query.filter(and_(Transmission.failed == false(), Transmission.status == status, or_(Transmission.destination_id == self.id, Transmission.origin_id == self.id))).order_by('creation_time').all()
                if direction == 'incoming':
                    if status == 'all':
                        return Transmission.query.filter_by(failed=False, destination_id=(self.id)).order_by('creation_time').all()
                    else:
                        return Transmission.query.filter(and_(Transmission.failed == false(), Transmission.destination_id == self.id, Transmission.status == status)).order_by('creation_time').all()
            if direction == 'outgoing':
                if status == 'all':
                    return Transmission.query.filter_by(failed=False, origin_id=(self.id)).order_by('creation_time').all()
                else:
                    return Transmission.query.filter(and_(Transmission.failed == false(), Transmission.origin_id == self.id, Transmission.status == status)).order_by('creation_time').all()

    def transformations(self, type=None, failed=False):
        """
        Get Transformations done by this Node.

        type must be a type of Transformation (defaults to Transformation)
        Failed can be True, False or "all"
        """
        if failed not in ('all', False, True):
            raise ValueError('{} is not a valid transmission failed'.format(failed))
        if type is None:
            type = Transformation
        if failed == 'all':
            return type.query.filter_by(node_id=(self.id)).all()
        else:
            return type.query.filter_by(node_id=(self.id), failed=failed).all()

    def fail(self):
        """
        Fail a node, setting its status to "failed".

        Also fails all vectors that connect to or from the node.
        You cannot fail a node that has already failed, but you
        can fail a dead node.

        Set node.failed to True and :attr:`~dallinger.models.Node.time_of_death`
        to now. Instruct all not-failed vectors connected to this node, infos
        made by this node, transmissions to or from this node and
        transformations made by this node to fail.

        """
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()
            self.network.calculate_full()
            for v in self.vectors():
                v.fail()

            for i in self.infos():
                i.fail()

            for t in self.transmissions(direction='all'):
                t.fail()

            for t in self.transformations():
                t.fail()

    def connect(self, whom, direction='to'):
        """Create a vector from self to/from whom.

        Return a list of newly created vector between the node and whom.
        ``whom`` can be a specific node or a (nested) list of nodes. Nodes can
        only connect with nodes in the same network. In addition nodes cannot
        connect with themselves or with Sources. ``direction`` specifies the
        direction of the connection it can be "to" (node -> whom), "from" (whom
        -> node) or both (node <-> whom). The default is "to".

        Whom may be a (nested) list of nodes.

        Will raise an error if:
            1. whom is not a node or list of nodes
            2. whom is/contains a source if direction is to or both
            3. whom is/contains self
            4. whom is/contains a node in a different network

        If self is already connected to/from whom a Warning
        is raised and nothing happens.

        This method returns a list of the vectors created
        (even if there is only one).

        """
        if direction not in ('to', 'from', 'both'):
            raise ValueError('{} is not a valid direction for connect()'.format(direction))
        else:
            whom = self.flatten([whom])
            new_vectors = []
            if direction in ('to', 'both'):
                already_connected_to = self.flatten([
                 self.is_connected(direction='to', whom=whom)])
                for node, connected in zip(whom, already_connected_to):
                    if connected:
                        print('Warning! {} already connected to {}, instruction to connect will be ignored.'.format(self, node))
                    else:
                        new_vectors.append(Vector(origin=self, destination=node))

            if direction in ('from', 'both'):
                already_connected_from = self.flatten([
                 self.is_connected(direction='from', whom=whom)])
                for node, connected in zip(whom, already_connected_from):
                    if connected:
                        print('Warning! {} already connected from {}, instruction to connect will be ignored.'.format(self, node))
                    else:
                        new_vectors.append(Vector(origin=node, destination=self))

        return new_vectors

    def flatten(self, lst):
        """Turn a list of lists into a list."""
        if lst == []:
            return lst
        else:
            if isinstance(lst[0], list):
                return self.flatten(lst[0]) + self.flatten(lst[1:])
            return lst[:1] + self.flatten(lst[1:])

    def transmit(self, what=None, to_whom=None):
        """Transmit one or more infos from one node to another.

        "what" dictates which infos are sent, it can be:
            (1) None (in which case the node's _what method is called).
            (2) an Info (in which case the node transmits the info)
            (3) a subclass of Info (in which case the node transmits all
                its infos of that type)
            (4) a list of any combination of the above
        "to_whom" dictates which node(s) the infos are sent to, it can be:
            (1) None (in which case the node's _to_whom method is called)
            (2) a Node (in which case the node transmits to that node)
            (3) a subclass of Node (in which case the node transmits to all
                nodes of that type it is connected to)
            (4) a list of any combination of the above
        Will additionally raise an error if:
            (1) _what() or _to_whom() returns None or a list containing None.
            (2) what is/contains an info that does not originate from the
                transmitting node
            (3) to_whom is/contains a node that the transmitting node does not
                have a not-failed connection with.
        """
        whats = set()
        for what in self.flatten([what]):
            if what is None:
                what = self._what()
            if inspect.isclass(what) and issubclass(what, Info):
                whats.update(self.infos(type=what))
            else:
                whats.add(what)

        to_whoms = set()
        for to_whom in self.flatten([to_whom]):
            if to_whom is None:
                to_whom = self._to_whom()
            if inspect.isclass(to_whom) and issubclass(to_whom, Node):
                to_whoms.update(self.neighbors(direction='to', type=to_whom))
            else:
                to_whoms.add(to_whom)

        transmissions = []
        vectors = self.vectors(direction='outgoing')
        for what in whats:
            for to_whom in to_whoms:
                try:
                    vector = [v for v in vectors if v.destination_id == to_whom.id][0]
                except IndexError:
                    raise ValueError('{} cannot transmit to {} as it does not have a connection to them'.format(self, to_whom))

                t = Transmission(info=what, vector=vector)
                transmissions.append(t)

        return transmissions

    def _what(self):
        """What to transmit if what is not specified.

        Return the default value of ``what`` for
        :func:`~dallinger.models.Node.transmit`. Should not return None or a list
        containing None.

        """
        return Info

    def _to_whom(self):
        """To whom to transmit if to_whom is not specified.

        Return the default value of ``to_whom`` for
        :func:`~dallinger.models.Node.transmit`. Should not return None or a list
        containing None.

        """
        return Node

    def receive(self, what=None):
        """Receive some transmissions.

        Received transmissions are marked as received, then their infos are
        passed to update().

        "what" can be:

            1. None (the default) in which case all pending transmissions are
               received.
            2. a specific transmission.

        Will raise an error if the node is told to receive a transmission it has
        not been sent.

        """
        if self.failed:
            raise ValueError('{} cannot receive as it has failed.'.format(self))
        else:
            received_transmissions = []
            if what is None:
                pending_transmissions = self.transmissions(direction='incoming',
                  status='pending')
                for transmission in pending_transmissions:
                    transmission.status = 'received'
                    transmission.receive_time = timenow()
                    received_transmissions.append(transmission)

            else:
                if isinstance(what, Transmission):
                    if what in self.transmissions(direction='incoming', status='pending'):
                        transmission.status = 'received'
                        what.receive_time = timenow()
                        received_transmissions.append(what)
                    else:
                        raise ValueError('{} cannot receive {} as it is not in its pending_transmissions'.format(self, what))
                else:
                    raise ValueError('Nodes cannot receive {}'.format(what))
        self.update([t.info for t in received_transmissions])

    def update(self, infos):
        """Process received infos.

        Update controls the default behavior of a node when it receives infos.
        By default it does nothing.
        """
        if self.failed:
            raise ValueError('{} cannot update as it has failed.'.format(self))

    def replicate(self, info_in):
        """Replicate an info."""
        if self.failed:
            raise ValueError('{} cannot replicate as it has failed.'.format(self))
        from .transformations import Replication
        info_out = type(info_in)(origin=self, contents=(info_in.contents))
        Replication(info_in=info_in, info_out=info_out)

    def mutate(self, info_in):
        """Replicate an info + mutation.

        To mutate an info, that info must have a method called
        ``_mutated_contents``.

        """
        if self.failed:
            raise ValueError('{} cannot mutate as it has failed.'.format(self))
        from .transformations import Mutation
        info_out = type(info_in)(origin=self, contents=(info_in._mutated_contents()))
        Mutation(info_in=info_in, info_out=info_out)


class Vector(Base, SharedMixin):
    __doc__ = 'A directed path that links two Nodes.\n\n    Nodes can only send each other information if they are linked by a Vector.\n    '
    __tablename__ = 'vector'
    origin_id = Column(Integer, (ForeignKey('node.id')), index=True)
    origin = relationship(Node,
      foreign_keys=[origin_id], backref='all_outgoing_vectors')
    destination_id = Column(Integer, (ForeignKey('node.id')), index=True)
    destination = relationship(Node,
      foreign_keys=[destination_id], backref='all_incoming_vectors')
    network_id = Column(Integer, (ForeignKey('network.id')), index=True)
    network = relationship(Network, backref='all_vectors')

    def __init__(self, origin, destination):
        """Create a vector."""
        if origin.network_id != destination.network_id:
            raise ValueError('{}, in network {}, cannot connect with {} as it is in network {}'.format(origin, origin.network_id, destination, destination.network_id))
        else:
            if origin.failed:
                raise ValueError('{} cannot connect to {} as {} has failed'.format(origin, destination, origin))
            else:
                if destination.failed:
                    raise ValueError('{} cannot connect to {} as {} has failed'.format(origin, destination, destination))
                from dallinger.nodes import Source
                if isinstance(destination, Source):
                    raise TypeError('Cannot connect to {} as it is a Source.'.format(destination))
            if origin == destination:
                raise ValueError('{} cannot connect to itself.'.format(origin))
        self.origin = origin
        self.origin_id = origin.id
        self.destination = destination
        self.destination_id = destination.id
        self.network = origin.network
        self.network_id = origin.network_id

    def __repr__(self):
        """The string representation of a vector."""
        return 'Vector-{}-{}'.format(self.origin_id, self.destination_id)

    def json_data(self):
        """The json representation of a vector."""
        return {'origin_id':self.origin_id, 
         'destination_id':self.destination_id, 
         'network_id':self.network_id}

    def transmissions(self, status='all'):
        """Get transmissions sent along this Vector.

        Status can be "all" (the default), "pending", or "received".
        """
        if status not in ('all', 'pending', 'received'):
            raise ValueError('You cannot get {} transmissions.'.format(status) + 'Status can only be pending, received or all')
        if status == 'all':
            return Transmission.query.filter_by(vector_id=(self.id), failed=False).all()
        else:
            return Transmission.query.filter_by(vector_id=(self.id),
              status=status,
              failed=False).all()

    def fail(self):
        """Fail a vector."""
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()
            for t in self.transmissions():
                t.fail()


class Info(Base, SharedMixin):
    __doc__ = 'A unit of information.'
    __tablename__ = 'info'
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_on':type,  'polymorphic_identity':'info'}
    origin_id = Column(Integer, (ForeignKey('node.id')), index=True)
    origin = relationship(Node, backref='all_infos')
    network_id = Column(Integer, (ForeignKey('network.id')), index=True)
    network = relationship(Network, backref='all_infos')
    contents = Column((Text()), default=None)

    def __init__(self, origin, contents=None, details=None, failed=False):
        """Create an info."""
        if origin.failed:
            if not failed:
                raise ValueError('Only failed Infos can be added to {}, as it has failed'.format(origin))
        else:
            self.origin = origin
            self.origin_id = origin.id
            self.contents = contents
            self.network_id = origin.network_id
            self.network = origin.network
            if details:
                self.details = details
            if failed is not None:
                self.failed = failed

    @validates('contents')
    def _write_once(self, key, value):
        existing = getattr(self, key)
        if existing is not None:
            raise ValueError('The contents of an info is write-once.')
        return value

    def __repr__(self):
        """The string representation of an info."""
        return 'Info-{}-{}'.format(self.id, self.type)

    def json_data(self):
        """The json representation of an info."""
        return {'type':self.type, 
         'origin_id':self.origin_id, 
         'network_id':self.network_id, 
         'contents':self.contents}

    def fail(self):
        """Fail an info.

        Set info.failed to True and :attr:`~dallinger.models.Info.time_of_death`
        to now. Instruct all transmissions and transformations involving this
        info to fail.
        """
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()
            for t in self.transmissions():
                t.fail()

            for t in self.transformations():
                t.fail()

    def transmissions(self, status='all'):
        """Get all the transmissions of this info.

        status can be all/pending/received.
        """
        if status not in ('all', 'pending', 'received'):
            raise ValueError('You cannot get transmission of status {}.'.format(status) + 'Status can only be pending, received or all')
        if status == 'all':
            return Transmission.query.filter_by(info_id=(self.id), failed=False).all()
        else:
            return Transmission.query.filterby(info_id=(self.id),
              status=status,
              failed=False).all()

    def transformations(self, relationship='all'):
        """Get all the transformations of this info.

        Return a list of transformations involving this info. ``relationship``
        can be "parent" (in which case only transformations where the info is
        the ``info_in`` are returned), "child" (in which case only
        transformations where the info is the ``info_out`` are returned) or
        ``all`` (in which case any transformations where the info is the
        ``info_out`` or the ``info_in`` are returned). The default is ``all``

        """
        if relationship not in ('all', 'parent', 'child'):
            raise ValueError('You cannot get transformations of relationship {}'.format(relationship) + 'Relationship can only be parent, child or all.')
        else:
            if relationship == 'all':
                return Transformation.query.filter(and_(Transformation.failed == false(), or_(Transformation.info_in == self, Transformation.info_out == self))).all()
            if relationship == 'parent':
                return Transformation.query.filter_by(info_in_id=(self.id),
                  failed=False).all()
            if relationship == 'child':
                return Transformation.query.filter_by(info_out_id=(self.id),
                  failed=False).all()

    def _mutated_contents(self):
        """The mutated contents of an info.

        When an info is asked to mutate, this method will be executed
        in order to determine the contents of the new info created.

        The base class function raises an error and so must be overwritten
        to be used.
        """
        raise NotImplementedError('_mutated_contents needs to be overwritten in class {}'.format(type(self)))


class Transmission(Base, SharedMixin):
    __doc__ = 'An instance of an Info being sent along a Vector.'
    __tablename__ = 'transmission'
    vector_id = Column(Integer, (ForeignKey('vector.id')), index=True)
    vector = relationship(Vector, backref='all_transmissions')
    info_id = Column(Integer, (ForeignKey('info.id')), index=True)
    info = relationship(Info, backref='all_transmissions')
    origin_id = Column(Integer, (ForeignKey('node.id')), index=True)
    origin = relationship(Node,
      foreign_keys=[origin_id], backref='all_outgoing_transmissions')
    destination_id = Column(Integer, (ForeignKey('node.id')), index=True)
    destination = relationship(Node,
      foreign_keys=[destination_id], backref='all_incoming_transmissions')
    network_id = Column(Integer, (ForeignKey('network.id')), index=True)
    network = relationship(Network, backref='networks_transmissions')
    receive_time = Column(DateTime, default=None)
    status = Column(Enum('pending', 'received', name='transmission_status'),
      nullable=False,
      default='pending',
      index=True)

    def __init__(self, vector, info):
        """Create a transmission."""
        if vector.failed:
            raise ValueError('Cannot transmit along {} as it has failed.'.format(vector))
        else:
            if info.failed:
                raise ValueError('Cannot transmit {} as it has failed.'.format(info))
            if info.origin_id != vector.origin_id:
                raise ValueError('Cannot transmit {} along {} as they do not have the same origin'.format(info, vector))
        self.vector_id = vector.id
        self.vector = vector
        self.info_id = info
        self.info = info
        self.origin_id = vector.origin_id
        self.origin = vector.origin
        self.destination_id = vector.destination_id
        self.destination = vector.destination
        self.network_id = vector.network_id
        self.network = vector.network

    def mark_received(self):
        """Mark a transmission as having been received."""
        self.receive_time = timenow()
        self.status = 'received'

    def __repr__(self):
        """The string representation of a transmission."""
        return 'Transmission-{}'.format(self.id)

    def json_data(self):
        """The json representation of a transmissions."""
        return {'vector_id':self.vector_id, 
         'origin_id':self.origin_id, 
         'destination_id':self.destination_id, 
         'info_id':self.info_id, 
         'network_id':self.network_id, 
         'receive_time':self.receive_time, 
         'status':self.status}

    def fail(self):
        """Fail a transmission."""
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()


class Transformation(Base, SharedMixin):
    __doc__ = 'An instance of one info being transformed into another.'
    __tablename__ = 'transformation'
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_on':type,  'polymorphic_identity':'transformation'}
    info_in_id = Column(Integer, (ForeignKey('info.id')), index=True)
    info_in = relationship(Info,
      foreign_keys=[info_in_id], backref='transformation_applied_to')
    info_out_id = Column(Integer, (ForeignKey('info.id')), index=True)
    info_out = relationship(Info,
      foreign_keys=[info_out_id], backref='transformation_whence')
    node_id = Column(Integer, (ForeignKey('node.id')), index=True)
    node = relationship(Node, backref='transformations_here')
    network_id = Column(Integer, (ForeignKey('network.id')), index=True)
    network = relationship(Network, backref='networks_transformations')

    def __repr__(self):
        """The string representation of a transformation."""
        return 'Transformation-{}'.format(self.id)

    def __init__(self, info_in, info_out):
        """Create a transformation."""
        if info_in.origin_id != info_out.origin_id:
            if info_in.id not in [t.info_id for t in info_out.origin.transmissions(direction='incoming',
              status='received')]:
                raise ValueError('Cannot transform {} into {} as they are not at the same node.'.format(info_in, info_out))
        for i in [info_in, info_out]:
            if i.failed:
                raise ValueError('Cannot transform {} as it has failed'.format(i))

        self.info_in = info_in
        self.info_out = info_out
        self.node = info_out.origin
        self.network = info_out.network
        self.info_in_id = info_in.id
        self.info_out_id = info_out.id
        self.node_id = info_out.origin_id
        self.network_id = info_out.network_id

    def json_data(self):
        """The json representation of a transformation."""
        return {'info_in_id':self.info_in_id, 
         'info_out_id':self.info_out_id, 
         'node_id':self.node_id, 
         'network_id':self.network_id}

    def fail(self):
        """Fail a transformation."""
        if self.failed is True:
            raise AttributeError('Cannot fail {} - it has already failed.'.format(self))
        else:
            self.failed = True
            self.time_of_death = timenow()


class Notification(Base, SharedMixin):
    __doc__ = 'A notification from AWS.'
    __tablename__ = 'notification'
    assignment_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)


class Recruitment(Base, SharedMixin):
    __doc__ = 'A record of a request to recruit a participant.'
    __tablename__ = 'recruitment'
    recruiter_id = Column((String(50)), nullable=True)