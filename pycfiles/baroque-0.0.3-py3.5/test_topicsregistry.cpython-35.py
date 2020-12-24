# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/datastructures/test_topicsregistry.py
# Compiled at: 2017-05-05 06:02:13
# Size of source mod 2**32: 7220 bytes
import pytest
from baroque.entities.event import Event
from baroque.entities.topic import Topic
from baroque.defaults.eventtypes import MetricEventType, GenericEventType
from baroque.defaults.reactors import ReactorFactory
from baroque.datastructures.registries import TopicsRegistry
from baroque.datastructures.bags import EventTypesBag

def test_register_failing():
    r = TopicsRegistry()
    with pytest.raises(AssertionError):
        r.register(None)
    with pytest.raises(AssertionError):
        r.register('not-a-topic')


def test_register():
    r = TopicsRegistry()
    t = Topic('test', [])
    r.register(t)
    assert r.count() == 1
    r.register(t)
    assert r.count() == 1
    t2 = Topic('test2', [])
    r.register(t2)
    assert r.count() == 2


def test_new():
    r = TopicsRegistry()
    topic = r.new('test', [GenericEventType(), MetricEventType()], description='this is a test topic', owner='me', tags=[
     'aaa', 'bbb', 'ccc'])
    assert isinstance(topic, Topic)
    assert topic.name == 'test'
    assert isinstance(topic.eventtypes, EventTypesBag)
    assert topic.description == 'this is a test topic'
    assert topic.owner == 'me'
    assert 'aaa' in topic.tags
    assert 'bbb' in topic.tags
    assert 'ccc' in topic.tags
    assert topic in r


def test_count():
    r = TopicsRegistry()
    t1 = Topic('test1', [])
    r.register(t1)
    assert r.count() == 1
    t2 = Topic('test2', [])
    t3 = Topic('test3', [])
    r.register(t2)
    r.register(t3)
    assert r.count() == 3


def test_remove():
    r = TopicsRegistry()
    t1 = Topic('test1', [])
    t2 = Topic('test2', [])
    r.register(t1)
    r.register(t2)
    assert len(r) == 2
    r.remove(t2)
    assert len(r) == 1
    assert t2 not in r


def test_remove_all():
    r = TopicsRegistry()
    t1 = Topic('test1', [])
    t2 = Topic('test2', [])
    r.register(t1)
    r.register(t2)
    assert len(r) == 2
    r.remove_all()
    assert len(r) == 0


def test_of():
    r = TopicsRegistry()
    t1 = Topic('test1', [], owner='me')
    t2 = Topic('test2', [], owner='you')
    t3 = Topic('test3', [], owner='me')
    assert len(r.of('me')) == 0
    assert len(r.of('you')) == 0
    r.register(t1)
    r.register(t2)
    r.register(t3)
    my_topics = r.of('me')
    your_topics = r.of('you')
    assert len(my_topics) == 2
    assert len(your_topics) == 1
    assert t1 in my_topics
    assert t3 in my_topics
    assert t2 in your_topics
    with pytest.raises(AssertionError):
        r.of(None)


def test_with_id():
    r = TopicsRegistry()
    t1 = Topic('test1', [])
    t2 = Topic('test2', [])
    t3 = Topic('test3', [])
    r.register(t1)
    r.register(t2)
    r.register(t3)
    id2 = t2.id
    result = r.with_id(id2)
    assert result == t2
    result = r.with_id('missing-id')
    assert result is None
    with pytest.raises(AssertionError):
        r.with_id(None)


def test_with_name():
    r = TopicsRegistry()
    t1 = Topic('test1', [])
    t2 = Topic('test2', [])
    t3 = Topic('test3', [])
    r.register(t1)
    r.register(t2)
    r.register(t3)
    result = r.with_name('test3')
    assert result == t3
    result = r.with_name('missing-name')
    assert result is None
    with pytest.raises(AssertionError):
        r.with_name(None)


def test_with_tags():
    r = TopicsRegistry()
    t1 = Topic('test1', [], tags=['aaa'])
    t2 = Topic('test2', [], tags=['bbb', 'ccc'])
    t3 = Topic('test3', [], tags=['aaa', 'ccc', 'ddd'])
    r.register(t1)
    r.register(t2)
    r.register(t3)
    results = r.with_tags(['aaa'])
    assert len(results) == 2
    assert t1 in results
    assert t3 in results
    results = r.with_tags(['aaa'])
    assert len(results) == 2
    assert t1 in results
    assert t3 in results
    results = r.with_tags(['missing-tag'])
    assert len(results) == 0
    with pytest.raises(AssertionError):
        r.with_tags(None)
    with pytest.raises(AssertionError):
        r.with_tags('string')
    with pytest.raises(AssertionError):
        r.with_tags(123)


def test_run():
    reg = TopicsRegistry()
    t = Topic('test-topic', [])
    r1 = ReactorFactory.stdout()
    with pytest.raises(AssertionError):
        reg.on_topic_run(None, r1)
    with pytest.raises(AssertionError):
        reg.on_topic_run(123, r1)
    with pytest.raises(AssertionError):
        reg.on_topic_run(t, None)
    with pytest.raises(AssertionError):
        reg.on_topic_run(t, 123)
    assert len(reg.topics) == 0
    reg.on_topic_run(t, r1)
    assert len(reg.topics) == 0
    r1 = ReactorFactory.stdout()
    reg.register(t)
    reg.on_topic_run(t, r1)
    reactors = reg.topics[t]
    assert len(reactors) == 1
    assert r1 in reactors
    r2 = ReactorFactory.stdout()
    reg.on_topic_run(t, r2)
    assert len(reg.topics) == 1
    reactors = reg.topics[t]
    assert len(reactors) == 2
    assert r2 in reactors
    reg = TopicsRegistry()
    reg.register(t)
    r3 = ReactorFactory.stdout()
    reg.on_topic_run(t, r3)
    assert len(reg.topics) == 1
    reactors = reg.topics[t]
    assert len(reactors) == 1
    assert r3 in reactors


def test_publish_on_topic():
    reg = TopicsRegistry()
    t = Topic('test', [GenericEventType(), MetricEventType()])
    evt = Event(MetricEventType())
    with pytest.raises(AssertionError):
        reg.publish_on_topic(None, t)
    with pytest.raises(AssertionError):
        reg.publish_on_topic(123, t)
    with pytest.raises(AssertionError):
        reg.publish_on_topic(evt, None)
    with pytest.raises(AssertionError):
        reg.publish_on_topic(evt, 123)

    class Box:

        def __init__(self):
            self.called = False

        def mark_called(self):
            self.called = True

    t = Topic('aaa', [GenericEventType()])
    evt = Event(MetricEventType())
    box = Box()
    r = ReactorFactory.call_function(box, 'mark_called')
    reg.register(t)
    reg.on_topic_run(t, r)
    reg.publish_on_topic(evt, t)
    assert not box.called
    reg = TopicsRegistry()
    t = Topic('aaa', [MetricEventType()])
    box = Box()
    r = ReactorFactory.call_function(box, 'mark_called')
    reg.register(t)
    reg.on_topic_run(t, r)
    evt = Event(MetricEventType())
    reg.publish_on_topic(evt, t)
    assert box.called


def test_magic_methods():
    r = TopicsRegistry()
    t1 = Topic('test1', [])
    r.register(t1)
    assert len(r) == 1
    assert t1 in r
    t2 = Topic('test2', [])
    assert t2 not in r
    r.register(Topic('test2', []))
    r.register(Topic('test3', []))
    for _ in r:
        pass


def test_print():
    print(TopicsRegistry())