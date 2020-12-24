# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ari/model.py
# Compiled at: 2016-11-21 07:31:46
# Size of source mod 2**32: 11652 bytes
__doc__ = "Model for mapping ARI Swagger resources and operations into objects.\n\nThe API is modeled into the Repository pattern, as you would find in Domain\nDriven Design.\n\nEach Swagger Resource (a.k.a. API declaration) is mapped into a Repository\nobject, which has the non-instance specific operations (just like what you\nwould find in a repository object).\n\nResponses from operations are mapped into first-class objects, which themselves\nhave methods which map to instance specific operations (just like what you\nwould find in a domain object).\n\nThe first-class objects also have 'on_event' methods, which can subscribe to\nStasis events relating to that object.\n"
import re, requests, logging
log = logging.getLogger(__name__)

class Repository(object):
    """Repository"""

    def __init__(self, client, name, resource):
        self.client = client
        self.name = name
        self.api = resource

    def __repr__(self):
        return 'Repository(%s)' % self.name

    def __getattr__(self, item):
        """Maps resource operations to methods on this object.

        :param item: Item name.
        """
        oper = getattr(self.api, item, None)
        if not (hasattr(oper, '__call__') and hasattr(oper, 'json')):
            raise AttributeError("'%r' object has no attribute '%s'" % (self, item))
        return lambda **kwargs: promote(self.client, oper(**kwargs), oper.json)


class ObjectIdGenerator(object):
    """ObjectIdGenerator"""

    def get_params(self, obj_json):
        """Gets the paramater values for specifying this object in a query.

        :param obj_json: Instance data.
        :type  obj_json: dict
        :return: Dictionary with paramater names and values
        :rtype:  dict of str, str
        """
        raise NotImplementedError('Not implemented')

    def id_as_str(self, obj_json):
        """Gets a single string identifying an object.

        :param obj_json: Instance data.
        :type  obj_json: dict
        :return: Id string.
        :rtype:  str
        """
        raise NotImplementedError('Not implemented')


class DefaultObjectIdGenerator(ObjectIdGenerator):
    """DefaultObjectIdGenerator"""

    def __init__(self, param_name, id_field='id'):
        self.param_name = param_name
        self.id_field = id_field

    def get_params(self, obj_json):
        return {self.param_name: obj_json[self.id_field]}

    def id_as_str(self, obj_json):
        return obj_json[self.id_field]


class BaseObject(object):
    """BaseObject"""
    id_generator = ObjectIdGenerator()

    def __init__(self, client, resource, as_json, event_reg):
        self.client = client
        self.api = resource
        self.json = as_json
        self.id = self.id_generator.id_as_str(as_json)
        self.event_reg = event_reg

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.id)

    def __getattr__(self, item):
        """Promote resource operations related to a single resource to methods
        on this class.

        :param item:
        """
        oper = getattr(self.api, item, None)
        if not (hasattr(oper, '__call__') and hasattr(oper, 'json')):
            raise AttributeError("'%r' object has no attribute '%r'" % (self, item))

        def enrich_operation(**kwargs):
            """Enriches an operation by specifying parameters specifying this
            object's id (i.e., channelId=self.id), and promotes HTTP response
            to a first-class object.

            :param kwargs: Operation parameters
            :return: First class object mapped from HTTP response.
            """
            kwargs.update(self.id_generator.get_params(self.json))
            return promote(self.client, oper(**kwargs), oper.json)

        return enrich_operation

    def on_event(self, event_type, fn, *args, **kwargs):
        """Register event callbacks for this specific domain object.

        :param event_type: Type of event to register for.
        :type  event_type: str
        :param fn:  Callback function for events.
        :type  fn:  (object, dict) -> None
        :param args: Arguments to pass to fn
        :param kwargs: Keyword arguments to pass to fn
        """

        def fn_filter(objects, event, *args, **kwargs):
            """Filter received events for this object.

            :param objects: Objects found in this event.
            :param event: Event.
            """
            if isinstance(objects, dict):
                if self.id in [c.id for c in list(objects.values())]:
                    fn(objects, event, *args, **kwargs)
            elif self.id == objects.id:
                fn(objects, event, *args, **kwargs)

        if not self.event_reg:
            msg = 'Event callback registration called on object with no events'
            raise RuntimeError(msg)
        return self.event_reg(event_type, fn_filter, *args, **kwargs)


class Channel(BaseObject):
    """Channel"""
    id_generator = DefaultObjectIdGenerator('channelId')

    def __init__(self, client, channel_json):
        super(Channel, self).__init__(client, client.swagger.channels, channel_json, client.on_channel_event)


class Bridge(BaseObject):
    """Bridge"""
    id_generator = DefaultObjectIdGenerator('bridgeId')

    def __init__(self, client, bridge_json):
        super(Bridge, self).__init__(client, client.swagger.bridges, bridge_json, client.on_bridge_event)


class Playback(BaseObject):
    """Playback"""
    id_generator = DefaultObjectIdGenerator('playbackId')

    def __init__(self, client, playback_json):
        super(Playback, self).__init__(client, client.swagger.playbacks, playback_json, client.on_playback_event)


class LiveRecording(BaseObject):
    """LiveRecording"""
    id_generator = DefaultObjectIdGenerator('recordingName', id_field='name')

    def __init__(self, client, recording_json):
        super(LiveRecording, self).__init__(client, client.swagger.recordings, recording_json, client.on_live_recording_event)


class StoredRecording(BaseObject):
    """StoredRecording"""
    id_generator = DefaultObjectIdGenerator('recordingName', id_field='name')

    def __init__(self, client, recording_json):
        super(StoredRecording, self).__init__(client, client.swagger.recordings, recording_json, client.on_stored_recording_event)


class EndpointIdGenerator(ObjectIdGenerator):
    """EndpointIdGenerator"""

    def get_params(self, obj_json):
        return {'tech': obj_json['technology'], 
         'resource': obj_json['resource']}

    def id_as_str(self, obj_json):
        return '%(tech)s/%(resource)s' % self.get_params(obj_json)


class Endpoint(BaseObject):
    """Endpoint"""
    id_generator = EndpointIdGenerator()

    def __init__(self, client, endpoint_json):
        super(Endpoint, self).__init__(client, client.swagger.endpoints, endpoint_json, client.on_endpoint_event)


class DeviceState(BaseObject):
    """DeviceState"""
    id_generator = DefaultObjectIdGenerator('deviceName', id_field='name')

    def __init__(self, client, device_state_json):
        super(DeviceState, self).__init__(client, client.swagger.deviceStates, device_state_json, client.on_device_state_event)


class Sound(BaseObject):
    """Sound"""
    id_generator = DefaultObjectIdGenerator('soundId')

    def __init__(self, client, sound_json):
        super(Sound, self).__init__(client, client.swagger.sounds, sound_json, client.on_sound_event)


class Mailbox(BaseObject):
    """Mailbox"""
    id_generator = DefaultObjectIdGenerator('mailboxName', id_field='name')

    def __init__(self, client, mailbox_json):
        super(Mailbox, self).__init__(client, client.swagger.mailboxes, mailbox_json, None)


def promote(client, resp, operation_json):
    """Promote a response from the request's HTTP response to a first class
     object.

    :param client:  ARI client.
    :type  client:  client.Client
    :param resp:    HTTP resonse.
    :type  resp:    requests.Response
    :param operation_json: JSON model from Swagger API.
    :type  operation_json: dict
    :return:
    """
    resp.raise_for_status()
    response_class = operation_json['responseClass']
    is_list = False
    m = re.match('List\\[(.*)\\]', response_class)
    if m:
        response_class = m.group(1)
        is_list = True
    factory = CLASS_MAP.get(response_class)
    if factory:
        resp_json = resp.json()
        if is_list:
            return [factory(client, obj) for obj in resp_json]
        return factory(client, resp_json)
    if resp.status_code == requests.codes.no_content:
        return
    log.info('No mapping for %s; returning JSON' % response_class)
    return resp.json()


CLASS_MAP = {'Bridge': Bridge, 
 'Channel': Channel, 
 'Endpoint': Endpoint, 
 'Playback': Playback, 
 'LiveRecording': LiveRecording, 
 'StoredRecording': StoredRecording, 
 'Mailbox': Mailbox, 
 'DeviceState': DeviceState}