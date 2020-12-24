# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limiter/event_processors.py
# Compiled at: 2019-12-30 13:03:03
# Size of source mod 2**32: 11629 bytes
import logging, functools
from boto3.dynamodb.conditions import Key
from limiter.utils import validate_table_env_fallback
from limiter.clients import dynamodb
from limiter.managers import RESOURCE_COORDINATE, RESOURCE_ID, RESERVATION_ID
logger = logging.getLogger()

class ProcessorPredicate:
    __doc__ = "\n    Determines if an event matches a specific criteria.\n\n    Instances of this class are used to determine if an event value, at the specified\n    path, evaluates to True by the given function. Instances may also be composed of additional\n    predicates. The additional predicates are either conjunctive (and) or disjunctive (or).\n\n    Args:\n        key (str): Location of the value to evalute with the given function.\n        pred_func (callable): Function which accepts a single argument, the value, and returns True or False\n        and_preds (list:ProcessorPredicate): List of conjunctive ProcessorPredicates. Defaults to an empty list.\n        or_preds (list:ProcessorPredicate): List of disjunctive ProcessorPredicates. Defaults to an empty list.\n\n    Note:\n        If an instance is composed of both conjunctive and disjunctive predicates, only the conjunctive\n        list will be evaluated.\n\n    Examples:\n        >>> event = {'source': 'aws.emr', 'detail': {'clusterId': 'j-1YONHTCP3YZKC', 'state': 'COMPLETED'}}\n        >>> predicate = ProcessorPredicate('detail.state', lambda state: state == 'COMPLETED')\n        >>> predicate.test(event)\n        True\n    "

    def __init__(self, key, pred_func, and_preds=None, or_preds=None):
        self.key = key
        self.pred_func = pred_func
        self.and_preds = and_preds if and_preds else []
        self.or_preds = or_preds if or_preds else []

    def with_and(self, add_pred):
        """
        Add a predicate to the conjunctive list.

        Args:
            add_pred (ProcessorPredicate): The predicate to add.

        Returns:
            This instance.
        """
        self.and_preds.append(add_pred)
        return self

    def with_or(self, add_pred):
        """
        Add a predicate to the disjunctive list.

        Args:
            add_pred (ProcessorPredicate): The predicate to add.

        Returns:
            This instance.
        """
        self.or_preds.append(add_pred)
        return self

    def test(self, event):
        """
        Evaluate an event.

        Args:
            event (dict): The event to evaluate.

        Returns:
            bool: True if the event satisfies the predicate's conditions, False otherwise.
        """
        test_value = _reduce_to_path(event, self.key)
        result = self.pred_func(test_value) if test_value else False
        if self.and_preds:
            if result:
                for pred in self.and_preds:
                    result &= pred.test(event)
                    if not result:
                        break

        if self.or_preds:
            if not result:
                for pred in self.or_preds:
                    result |= pred.test(event)
                    if result:
                        break

        return result


class EventProcessor:
    __doc__ = "\n    Validates and extracts the resource id from events.\n\n    Instances of this class will extract the value at the given id path, if the its predicate evaluates to True\n    from the event. If an instance does not have a predicate the id will be returned without testing. If either the\n    predicate fails or the id path is invalid None will be returned.\n\n    Args:\n        source (str): The origination this processor supports events for, e.g. aws.emr\n        id_path (str): Dot delineated path to the resource id value.\n        predicate (ProcessorPredicate): Predicate to test the event against before extracting the id. Defaults to None.\n        type (str): Event detail-type of the event this porcessor supports. Defaults to None.\n\n    Examples:\n        >>> event = {'source': 'aws.emr', 'detail': {'clusterId': 'j-1YONHTCP3YZKC', 'state': 'COMPLETED'}}\n        >>> predicate = ProcessorPredicate('detail.state', lambda state: state == 'COMPLETED')\n        >>> processor = EventProcessor('aws.emr', 'detail.clusterId', predicate=predicate)\n        >>> processor.test_and_get_id(event)\n        j-1YONHTCP3YZKC\n    "

    def __init__(self, source, id_path, predicate=None, type=None):
        self.source = source
        self.id_path = id_path
        self.predicate = predicate
        self.type = type

    def test_and_get_id(self, event):
        """
        Test the event and extract its resource id.

        If the id path is invalid or the predicate fails None will be returned.

        Args:
            event (dict): Event to test and extract the resource id of.

        Returns:
            str: Id of the resource the event was triggered.
        """
        if self.predicate:
            if not self.predicate.test(event):
                return
        return _reduce_to_path(event, self.id_path)


class EventProcessorManager:
    __doc__ = "\n    Removes non-fungible tokens from DynamoDB represented by termination events.\n\n    Instances of this class are composed of multiple EventProcessors. Each processor is mapped to\n    a single event source, e.g. aws.emr. The processor associated with the event source will verify\n    the event is represented by a token and extract the resource id from the event. The resource id\n    will then be used to determine the resource coordinate and delete the token.\n\n    Args:\n        table_name (str): Name of the DynamoDB non-fungible token table.\n                          Can be set via environment variable `NON_FUNGIBLE_TABLE`\n                          or synthesized using the `LIMITER_TABLES_BASE_NAME` environment variable.\n        index_name (str): Name of the index to query for the resource coordinate using the resource id.\n                          Can be set via environment variable `NON_FUNGIBLE_RES_INDEX`\n                          or synthesized using the `LIMITER_TABLES_BASE_NAME` environment variable.\n        processors (list:EventProcessor): List of event processors. Defaults to None.\n\n    Examples:\n        >>> event = {'source': 'aws.emr', 'detail': {'clusterId': 'j-1YONHTCP3YZKC', 'state': 'COMPLETED'}}\n        >>> predicate = ProcessorPredicate('detail.state', lambda state: state == 'COMPLETED')\n        >>> processor = EventProcessor('aws.emr', 'detail.clusterId', predicate=predicate)\n        >>> manager = EventProcessorManager(table_name='table', index_name='idx', processors=[processor])\n        >>> manager.process_event(event)\n    "

    def __init__(self, table_name=None, index_name=None, processors=None):
        self.processors = {_build_processor_key(x.source, x.type):x for x in processors} if processors else {}
        self.table_name = validate_table_env_fallback(table_name, 'NON_FUNGIBLE_TABLE', 'non-fungible-tokens')
        self.index_name = validate_table_env_fallback(index_name, 'NON_FUNGIBLE_RES_INDEX', 'resource-index')
        self.cache = []
        self._client = None
        self._table = None

    @property
    def client(self):
        """ DynamoDB client """
        if not self._client:
            self._client = dynamodb()
        return self._client

    @property
    def table(self):
        """ DynamoDB Table containing token row """
        if not self._table:
            self._table = self.client.Table(self.table_name)
        return self._table

    def add_processor(self, processor):
        """
        Add a processor to this manager.

        If a processor already exists for the event source, it will be replaced.

        Args:
            processor (EventProcessor): Processor to include when handling events.
        """
        self.processors[processor.source] = processor

    def process_event(self, event):
        """
        Remove the token which represents the resource contained in the event.

        First, the EventProcessor will be selected according to the event source.
        If no processor is found a ValueError will be raised.

        Next, the processor will test the event and extract the resource id.
        If the event is malformed or does not satisfy the processor's testing criteria nothing will be deleted.

        Finally, the resource id is used to find the resource coordinate. The resource coordinate and id form
        the key needed to delete the token.

        Args:
            event (dict): Event containing the resource to remove the token of.

        Raises:
            ValueError: If the event does not contain 'source' if this manager has no processor for the source.
        """
        processor = self._get_processor(event)
        resource_id = processor.test_and_get_id(event)
        if resource_id:
            if resource_id not in self.cache:
                token = self._get_resource_token(resource_id)
                if token:
                    logger.info('Removing %s token %s from %s', processor.source, resource_id, self.table_name)
                    self.table.delete_item(Key={RESOURCE_COORDINATE: token[RESOURCE_COORDINATE], 
                     RESERVATION_ID: token[RESERVATION_ID]})
                else:
                    logger.warning('Could not find a token for resoure %s', resource_id)
                self.cache.append(resource_id)

    def _get_processor(self, event):
        """
        Get the appropriate processor for this event.

        Args:
            event (dict): Event to processor is being retrieved for.

        Returns:
            EventProcessor: Processor for the event's source.

        Raises:
            ValueError: If the event does not contain 'source' if this manager has no processor for the source.
        """
        if 'source' not in event:
            raise ValueError('Cannot process event, source is a required field. Event: ' + str(event))
        else:
            source = event['source']
            type = event.get('detail-type', None)
            source_type_key = _build_processor_key(source, type)
            processor = self.processors.get(source_type_key, None)
            if not processor:
                processor = self.processors.get(source, None)
            raise processor or ValueError('No processor for event source: ' + source)
        return processor

    def _get_resource_token(self, resource_id):
        """
        Get the token representing the specified resouce.

        Args:
            resource_id (str): Resource id to get the resource token of.

        Returns:
            (dict): The token representing the specpfied resource.
        """
        response = self.table.query(IndexName=(self.index_name),
          KeyConditionExpression=(Key(RESOURCE_ID).eq(resource_id)))
        if response['Count'] == 0:
            return
        else:
            return response['Items'][0]


def _reduce_to_path(obj, path):
    """
    Traverses the given object down the specified "." delineated, returning the
    value named by the last path segment.

    Args:
        obj (dict): Dictionary containing the value to extract.
        path (str): Location of the value to extract.

    Examples:
        >>> obj = {'foo': {'bar': {'bat': 'SomethingImportant'}}}
        >>> path = 'foo.bar.bat'
        >>> _reduce_to_path(obj, path)
        SomethingImportant

    Returns:
        str: If the path is valid, otherwise None.
    """
    try:
        if isinstance(path, str):
            path = path.split('.')
        return functools.reduce(lambda x, y: x[y], path, obj)
    except Exception:
        pass


def _build_processor_key(source, type=None):
    if type:
        return source + ':' + type.replace(' ', '').lower()
    else:
        return source