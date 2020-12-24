# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/models/table.py
# Compiled at: 2020-04-10 11:06:25
# Size of source mod 2**32: 3992 bytes
from typing import List, Optional
import attr
from amundsen_common.models.user import User
from marshmallow_annotations.ext.attrs import AttrsSchema

@attr.s(auto_attribs=True, kw_only=True)
class Reader:
    user: User
    read_count: int


class ReaderSchema(AttrsSchema):

    class Meta:
        target = Reader
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Tag:
    tag_type: str
    tag_name: str


class TagSchema(AttrsSchema):

    class Meta:
        target = Tag
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Watermark:
    watermark_type = None
    watermark_type: Optional[str]
    partition_key = None
    partition_key: Optional[str]
    partition_value = None
    partition_value: Optional[str]
    create_time = None
    create_time: Optional[str]


class WatermarkSchema(AttrsSchema):

    class Meta:
        target = Watermark
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Statistics:
    stat_type: str
    stat_val = None
    stat_val: Optional[str]
    start_epoch = None
    start_epoch: Optional[int]
    end_epoch = None
    end_epoch: Optional[int]


class StatisticsSchema(AttrsSchema):

    class Meta:
        target = Statistics
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Column:
    name: str
    description = None
    description: Optional[str]
    source_description = None
    source_description: Optional[str]
    col_type: str
    sort_order: int
    stats = []
    stats: List[Statistics]
    tags = []
    tags: List[Tag]
    badges = []
    badges: Optional[List[Tag]]
    user_editable_tags = []
    user_editable_tags: Optional[List[Tag]]
    read_only_tags = []
    read_only_tags: Optional[List[Tag]]
    data_driven_tags = []
    data_driven_tags: Optional[List[Tag]]
    sensitivity_tags = []
    sensitivity_tags: Optional[List[Tag]]
    source_application_tags = []
    source_application_tags: Optional[List[Tag]]


class ColumnSchema(AttrsSchema):

    class Meta:
        target = Column
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Application:
    application_url = None
    application_url: Optional[str]
    description = None
    description: Optional[str]
    id: str
    name = None
    name: Optional[str]
    kind = None
    kind: Optional[str]


class ApplicationSchema(AttrsSchema):

    class Meta:
        target = Application
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Source:
    source_type: str
    source: str


class SourceSchema(AttrsSchema):

    class Meta:
        target = Source
        register_as_scheme = True


def default_if_none(arg: Optional[bool]) -> bool:
    return arg or 


@attr.s(auto_attribs=True, kw_only=True)
class ProgrammaticDescription:
    source: str
    text: str


class ProgrammaticDescriptionSchema(AttrsSchema):

    class Meta:
        target = ProgrammaticDescription
        register_as_scheme = True


@attr.s(auto_attribs=True, kw_only=True)
class Table:
    database: str
    cluster: str
    schema: str
    name: str
    tags = []
    tags: List[Tag]
    badges = []
    badges: Optional[List[Tag]]
    user_editable_tags = []
    user_editable_tags: Optional[List[Tag]]
    read_only_tags = []
    read_only_tags: Optional[List[Tag]]
    data_driven_tags = []
    data_driven_tags: Optional[List[Tag]]
    sensitivity_tags = []
    sensitivity_tags: Optional[List[Tag]]
    source_application_tags = []
    source_application_tags: Optional[List[Tag]]
    table_readers = []
    table_readers: List[Reader]
    description = None
    description: Optional[str]
    source_description = None
    source_description: Optional[str]
    columns: List[Column]
    owners = []
    owners: List[User]
    watermarks = []
    watermarks: List[Watermark]
    table_writer = None
    table_writer: Optional[Application]
    last_updated_timestamp = None
    last_updated_timestamp: Optional[int]
    source = None
    source: Optional[Source]
    is_view = attr.ib(default=None, converter=default_if_none)
    is_view: Optional[bool]
    programmatic_descriptions = None
    programmatic_descriptions: Optional[List[ProgrammaticDescription]]


class TableSchema(AttrsSchema):

    class Meta:
        target = Table
        register_as_scheme = True