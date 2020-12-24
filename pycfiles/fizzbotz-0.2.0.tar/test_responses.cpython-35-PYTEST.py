# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/martensm/fizzbotz/tests/test_responses.py
# Compiled at: 2016-02-18 00:02:19
# Size of source mod 2**32: 3643 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, codecs, os.path as path, pytest, fizzbotz

def get_test_file(filename, extension):
    file_path = path.join(path.dirname(__file__), 'test_files', '{}.{}'.format(filename, extension))
    with codecs.open(file_path, 'r', 'utf-8') as (test_file):
        return test_file.read()[:-1]


@pytest.mark.asyncio
@pytest.mark.parametrize('filename, message_function', [
 (
  'bestoftwitchchat', fizzbotz.TwitchChat().get_bestoftwitchchat_pasta),
 (
  'twitchquotes', fizzbotz.TwitchChat().get_twitchquotes_pasta),
 (
  'twitchquotes_emotes', fizzbotz.TwitchChat().get_twitchquotes_pasta),
 (
  'twitchquotes_text_art', fizzbotz.TwitchChat().get_twitchquotes_pasta),
 (
  'twitchquotes_unicode', fizzbotz.TwitchChat().get_twitchquotes_pasta),
 (
  'joke_oneliner', fizzbotz.Joke().get_oneliner),
 (
  'joke_oneliner_quote', fizzbotz.Joke().get_oneliner),
 (
  'insult', fizzbotz.Insult().get)])
async def test_messages(filename, message_function):
    raw_html = get_test_file(filename, 'html')
    message = await message_function(from_html=raw_html)
    expected_message = get_test_file(filename, 'txt')
    if message != expected_message:
        pytest.fail("Didn't get expected result.\n\nExpected:\n{}\n\nReceived:\n{}".format(expected_message, message))


@pytest.mark.asyncio
@pytest.mark.parametrize('callback', [
 fizzbotz.Imgur(2).get,
 fizzbotz.Joke().get,
 fizzbotz.TwitchChat().get])
async def test_command_get(callback):
    await callback() is not None


@pytest.mark.asyncio
async def test_square():
    square_message = await fizzbotz.Square().get('ggsnipes/sgak')
    @py_assert2 = '```\nG G S N I P E S / S G A K\nG S N I P E S / S G A K A\nS N I P E S / S G A K A G\nN I P E S / S G A K A G S\nI P E S / S G A K A G S /\nP E S / S G A K A G S / S\nE S / S G A K A G S / S E\nS / S G A K A G S / S E P\n/ S G A K A G S / S E P I\nS G A K A G S / S E P I N\nG A K A G S / S E P I N S\nA K A G S / S E P I N S G\nK A G S / S E P I N S G G\n```'
    @py_assert1 = square_message == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (square_message, @py_assert2)) % {'py0': @pytest_ar._saferepr(square_message) if 'square_message' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(square_message) else 'square_message', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@pytest.mark.asyncio
@pytest.mark.parametrize('string_literal, exception', [
 (
  '', fizzbotz.EmptyStringError),
 (
  'This string is longer than the max allowed.', fizzbotz.StringLengthError)])
async def test_square_exceptions(string_literal, exception):
    with pytest.raises(exception):
        await fizzbotz.Square().get(string_literal)


@pytest.mark.asyncio
@pytest.mark.parametrize('dice', ['3d10', '3D10', '12', ''])
async def test_roll(dice):
    await fizzbotz.Roll().get(dice) is not None


@pytest.mark.asyncio
@pytest.mark.parametrize('dice', ['d10', '10d', '0', 'foo'])
async def test_roll_exception(dice):
    with pytest.raises(ValueError):
        await fizzbotz.Roll().get(dice)