# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/stream.py
# Compiled at: 2020-04-14 15:37:55
# Size of source mod 2**32: 7833 bytes
from typing import List, Union, Optional
from datalogue.models.datastore import Datastore, DatastoreDef, _datastore_def_from_payload
from datalogue.models.transformations import Transformation, _transformation_from_payload
from datalogue.models.transformations.commons import DataType
from datalogue.utils import _parse_list
from datalogue.errors import DtlError, _property_not_found

class Definition:
    __doc__ = '\n    A Pipeline is a series of transformations that will output its results to a target\n    and can contain Child(ren ?) Pipelines. cf diagram below.\n\n        Parent Pipelines -> Transformations -+-> Target\n                                             |\n                                             +-> Children Pipelines\n    '

    def __init__(self, transformations: List[Transformation], pipelines: List['Definition'], target: Union[(Datastore, DatastoreDef)]):
        if isinstance(target, Datastore):
            target = target.definition
        self.transformations = transformations
        self.pipelines = pipelines
        self.target = target

    def __repr__(self):
        return f"Pipeline(type: {self.transformations!r}, pipelines: {self.pipelines!r}, target: {self.target!r})"

    def __eq__(self, other: 'Definition'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self) -> Union[(DtlError, dict)]:
        if self.target.datastore_id is None:
            return DtlError('Cannot serialize a pipeline with a target that was not saved to the database (id missing)')
        else:
            return {'transformations':list(map(lambda s: s._as_payload(), self.transformations)), 
             'pipelines':list(map(lambda s: s._as_payload(), self.pipelines)), 
             'target':self.target._as_payload()}

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'Definition')]:
        """
        Builds a pipeline object from a dictionary,

        :param json: dictionary parsed from json
        :return:
        """
        transformations = json.get('transformations')
        if transformations is not None:
            transformations = _parse_list(_transformation_from_payload)(transformations)
            if isinstance(transformations, DtlError):
                return transformations
            else:
                transformations = list()
        else:
            pipelines = json.get('pipelines')
            if pipelines is not None:
                pipelines = _parse_list(Definition._from_payload)(pipelines)
                if isinstance(pipelines, DtlError):
                    return pipelines
            else:
                pipelines = list()
        target = json.get('target')
        if target is None:
            return DtlError("Cannot have a pipeline without a 'target' property")
        else:
            target = _datastore_def_from_payload(target)
            if isinstance(target, DtlError):
                return target
            return Definition(transformations, pipelines, target)


class EnvVariable:
    __doc__ = '\n    Object that represents an environment variable.\n\n    An environment variable can be either a literal or an expression that returns a value.\n\n    Right now you can input as a value:\n        - a string: "a"\n        - an int: 3\n        - a float: 4.3\n        - a boolean: false\n        - a script to index a source of data: `Source(<source_json_object>).index(n => n.label == "some_label")`. This\n           will cache the data into a `Map` with the key being the value of the label you specified and value being\n           the whole adg.\n\n    The environment variables are injected as arguments into the lambda functions defined inside transformations.\n\n        EX: MapFunction transformation\n\n    ALPHA FEATURE\n    '

    def __init__(self, data_type: DataType, value: str, key: str):
        """
        Builds an environment variable to be evaluated before execution of a stream

        :param data_type: type of the variable
        :param value: string to be evaluated
        :param key: key to be used to retrieve the value inside a lambda function
        """
        self.type = data_type
        self.value = value
        self.key = key

    def __eq__(self, other: 'EnvVariable'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"EnvVariable(type: {self.type.value}, value: {self.value!r}, key: {self.key!r})"

    def _as_payload(self):
        return {'type':self.type.value, 
         'value':self.value, 
         'key':self.key}

    @staticmethod
    def _from_payload(json: dict) -> Union[('EnvVariable', DtlError)]:
        data_type = json.get('type')
        if data_type is None:
            return _property_not_found('type', json)
        data_type = DataType.from_str(data_type)
        if isinstance(data_type, DtlError):
            return data_type
        value = json.get('value')
        if value is None:
            return _property_not_found('value', json)
        else:
            key = json.get('key')
            if key is None:
                return _property_not_found('key', json)
            return EnvVariable(data_type, value, key)


class Stream:
    __doc__ = '\n    Describes a stream of data flowing from a source to one or several destinations with transformations\n\n        Source -+-> Pipeline 0\n                |\n                +-> Pipeline 1\n\n               ...\n    '

    def __init__(self, source: Union[(DatastoreDef, Datastore)], pipelines: List[Definition], env: Optional[List[EnvVariable]]=None):
        """
        Creates a stream from a source flowing into different pipelines

        :param source: source of the streaming data
        :param pipelines: pipelines containing the transformations and targets for the data
        :param env: list of environment variables to be evaluated before beginning streaming the data
        """
        if isinstance(source, Datastore):
            source = source.definition
        self.source = source
        self.pipelines = pipelines
        self.env = env

    def __repr__(self):
        return f"Stream(type: {self.source!r}, pipelines: {self.pipelines!r}, env: {self.env!r})"

    def __eq__(self, other: 'Stream'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self):
        base = {'source':self.source._as_payload(), 
         'pipelines':list(map(lambda s: s._as_payload(), self.pipelines))}
        if self.env is not None:
            base['env'] = list(map(lambda s: s._as_payload(), self.env))
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'Stream')]:
        """
        Builds a Stream instance from a json object

        :param json:
        :return: if fails returns a string with the error message
        """
        source = json.get('source')
        if source is None:
            return DtlError('stream needs a source of data')
        source = _datastore_def_from_payload(source)
        if isinstance(source, DtlError):
            return source
        pipelines = json.get('pipelines')
        if pipelines is None:
            return DtlError("streams needs a 'pipelines' property")
        pipelines = _parse_list(Definition._from_payload)(pipelines)
        if isinstance(pipelines, DtlError):
            return pipelines
        else:
            env = json.get('env')
            if env is not None:
                env = _parse_list(EnvVariable._from_payload)(env)
                if isinstance(env, DtlError):
                    return env
            return Stream(source, pipelines, env)