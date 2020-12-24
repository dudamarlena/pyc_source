# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blake/code/vivint-selenium-docker/tests/test_utils.py
# Compiled at: 2017-11-07 18:40:48
# Size of source mod 2**32: 2477 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, random, pytest
from docker.errors import ImageNotFound
from selenium_docker.base import ContainerFactory
from selenium_docker.utils import *

@pytest.mark.parametrize('i', range(100))
def test_gen_uuid(i):
    @py_assert3 = gen_uuid(i)
    @py_assert5 = len(@py_assert3)
    @py_assert7 = @py_assert5 == i
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py8)s', ), (@py_assert5, i)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(gen_uuid) if 'gen_uuid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gen_uuid) else 'gen_uuid',  'py2':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = None


@pytest.mark.parametrize('i', ['a', 1.0, None, -1.0, {}, []])
def test_gen_uuid_types(i):
    @py_assert3 = gen_uuid(i)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 4
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(gen_uuid) if 'gen_uuid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gen_uuid) else 'gen_uuid',  'py2':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_gen_uuid_bools():
    @py_assert2 = True
    @py_assert4 = gen_uuid(@py_assert2)
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(gen_uuid) if 'gen_uuid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gen_uuid) else 'gen_uuid',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = False
    @py_assert4 = gen_uuid(@py_assert2)
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py1)s(%(py3)s)\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(gen_uuid) if 'gen_uuid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gen_uuid) else 'gen_uuid',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_in_container():
    @py_assert1 = in_container()
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s()\n}') % {'py0':@pytest_ar._saferepr(in_container) if 'in_container' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(in_container) else 'in_container',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


def test_in_container_via_factory(factory):
    output = factory.docker.containers.run('standalone-chrome-ffmpeg', 'ls -la /')
    if isinstance(output, bytes):
        output = output.decode('ascii')
    @py_assert0 = '.docker'
    @py_assert2 = @py_assert0 in output
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, output)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


@pytest.mark.parametrize('port', [
 ('4444/tcp', None),
 (
  '4444/tcp', random.randint(30000, 35000))])
def test_ip_port(port, factory):
    port_str, port_int = port
    spec = {'image':'standalone-chrome-ffmpeg', 
     'labels':{'browser': 'chrome'}, 
     'detach':True, 
     'ports':{port_str: port_int}, 
     'publish_all_ports':True}
    c = factory.start_container(spec)
    host, port = ip_port(c, port_str)
    @py_assert2 = '0.0.0.0'
    @py_assert1 = host == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (host, @py_assert2)) % {'py0':@pytest_ar._saferepr(host) if 'host' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(host) else 'host',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = []
    @py_assert5 = isinstance(port, int)
    @py_assert0 = @py_assert5
    if @py_assert5:
        @py_assert10 = 10000
        @py_assert9 = port > @py_assert10
        @py_assert0 = @py_assert9
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py2':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py3':@pytest_ar._saferepr(port) if 'port' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(port) else 'port',  'py4':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_assert1.append(@py_format7)
        if @py_assert5:
            @py_format12 = @pytest_ar._call_reprcompare(('>', ), (@py_assert9,), ('%(py8)s > %(py11)s', ), (port, @py_assert10)) % {'py8':@pytest_ar._saferepr(port) if 'port' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(port) else 'port',  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = '%(py13)s' % {'py13': @py_format12}
            @py_assert1.append(@py_format14)
        @py_format15 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert9 = @py_assert10 = None
    factory.stop_all_containers()


@pytest.mark.parametrize('bg', [True, False])
def test_load_docker_image(bg, factory):
    names = [
     'hello-world:latest', 'hello-world:linux']
    for img in names:
        try:
            factory.docker.images.remove(img, force=True, noprune=False)
        except ImageNotFound:
            pass

    images = factory.docker.images.list(name='hello-world')
    @py_assert1 = not images
    if not @py_assert1:
        @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(images) if 'images' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(images) else 'images'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None
    image = load_docker_image((factory.docker), 'hello-world', background=bg)
    if bg:
        gevent.wait([image], timeout=15.0)
        image = image.value
    @py_assert0 = 'hello-world:latest'
    @py_assert4 = image.tags
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.tags\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(image) if 'image' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(image) else 'image',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


@pytest.mark.parametrize('pack', [({}, ''),
 (
  {'one': 1}, '-metadata one="1"'),
 (
  {'one': None}, ''),
 (
  {'two':True, 
   'three':False},
  '-metadata two="True" -metadata three="False"'),
 (
  {'one': '""'}, '')])
def test_parse_metadata(pack):
    meta, expected = pack
    @py_assert4 = parse_metadata(meta)
    @py_assert1 = expected == @py_assert4
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(parse_metadata) if 'parse_metadata' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_metadata) else 'parse_metadata',  'py3':@pytest_ar._saferepr(meta) if 'meta' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(meta) else 'meta',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None