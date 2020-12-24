# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eeshangarg/python-zulip-api/zulip/integrations/bridge_with_matrix/test_matrix.py
# Compiled at: 2020-04-20 21:49:10
# Size of source mod 2**32: 6851 bytes
from .matrix_bridge import check_zulip_message_validity, zulip_to_matrix
from unittest import TestCase, mock
from subprocess import Popen, PIPE
import os, shutil
from contextlib import contextmanager
from tempfile import mkdtemp
script_file = 'matrix_bridge.py'
script_dir = os.path.dirname(__file__)
script = os.path.join(script_dir, script_file)
from typing import List, Iterator
sample_config_path = 'matrix_test.conf'
sample_config_text = '[matrix]\nhost = https://matrix.org\nusername = username\npassword = password\nroom_id = #zulip:matrix.org\n\n[zulip]\nemail = glitch-bot@chat.zulip.org\napi_key = aPiKeY\nsite = https://chat.zulip.org\nstream = test here\ntopic = matrix\n\n'

@contextmanager
def new_temp_dir() -> Iterator[str]:
    path = mkdtemp()
    yield path
    shutil.rmtree(path)


class MatrixBridgeScriptTests(TestCase):

    def output_from_script(self, options: List[str]) -> List[str]:
        popen = Popen((['python', script] + options), stdin=PIPE, stdout=PIPE, universal_newlines=True)
        return popen.communicate()[0].strip().split('\n')

    def test_no_args(self) -> None:
        output_lines = self.output_from_script([])
        expected_lines = [
         'Options required: -c or --config to run, OR --write-sample-config.',
         'usage: {} [-h]'.format(script_file)]
        for expected, output in zip(expected_lines, output_lines):
            self.assertIn(expected, output)

    def test_help_usage_and_description(self) -> None:
        output_lines = self.output_from_script(['-h'])
        usage = 'usage: {} [-h]'.format(script_file)
        description = 'Script to bridge'
        self.assertIn(usage, output_lines[0])
        blank_lines = [num for num, line in enumerate(output_lines) if line == '']
        self.assertTrue(blank_lines)
        self.assertTrue(len(output_lines) > blank_lines[0])
        self.assertIn(description, output_lines[(blank_lines[0] + 1)])

    def test_write_sample_config(self) -> None:
        with new_temp_dir() as (tempdir):
            path = os.path.join(tempdir, sample_config_path)
            output_lines = self.output_from_script(['--write-sample-config', path])
            self.assertEqual(output_lines, ["Wrote sample configuration to '{}'".format(path)])
            with open(path) as (sample_file):
                self.assertEqual(sample_file.read(), sample_config_text)

    def test_write_sample_config_from_zuliprc(self) -> None:
        zuliprc_template = ['[api]', 'email={email}', 'key={key}', 'site={site}']
        zulip_params = {'email':'foo@bar',  'key':'some_api_key', 
         'site':'https://some.chat.serverplace'}
        with new_temp_dir() as (tempdir):
            path = os.path.join(tempdir, sample_config_path)
            zuliprc_path = os.path.join(tempdir, 'zuliprc')
            with open(zuliprc_path, 'w') as (zuliprc_file):
                zuliprc_file.write(('\n'.join(zuliprc_template).format)(**zulip_params))
            output_lines = self.output_from_script(['--write-sample-config', path,
             '--from-zuliprc', zuliprc_path])
            self.assertEqual(output_lines, [
             "Wrote sample configuration to '{}' using zuliprc file '{}'".format(path, zuliprc_path)])
            with open(path) as (sample_file):
                sample_lines = [line.strip() for line in sample_file.readlines()]
                expected_lines = sample_config_text.split('\n')
                expected_lines[7] = 'email = {}'.format(zulip_params['email'])
                expected_lines[8] = 'api_key = {}'.format(zulip_params['key'])
                expected_lines[9] = 'site = {}'.format(zulip_params['site'])
                self.assertEqual(sample_lines, expected_lines[:-1])

    def test_detect_zuliprc_does_not_exist(self) -> None:
        with new_temp_dir() as (tempdir):
            path = os.path.join(tempdir, sample_config_path)
            zuliprc_path = os.path.join(tempdir, 'zuliprc')
            output_lines = self.output_from_script(['--write-sample-config', path,
             '--from-zuliprc', zuliprc_path])
            self.assertEqual(output_lines, [
             "Could not write sample config: Zuliprc file '{}' does not exist.".format(zuliprc_path)])


class MatrixBridgeZulipToMatrixTests(TestCase):
    valid_zulip_config = dict(stream='some stream',
      topic='some topic',
      email='some@email')
    valid_msg = dict(sender_email='John@Smith.smith',
      type='stream',
      display_recipient=(valid_zulip_config['stream']),
      subject=(valid_zulip_config['topic']))

    def test_zulip_message_validity_success(self) -> None:
        zulip_config = self.valid_zulip_config
        msg = self.valid_msg
        assert msg['sender_email'] != zulip_config['email']
        self.assertTrue(check_zulip_message_validity(msg, zulip_config))

    def test_zulip_message_validity_failure(self) -> None:
        zulip_config = self.valid_zulip_config
        msg_wrong_stream = dict((self.valid_msg), display_recipient='foo')
        self.assertFalse(check_zulip_message_validity(msg_wrong_stream, zulip_config))
        msg_wrong_topic = dict((self.valid_msg), subject='foo')
        self.assertFalse(check_zulip_message_validity(msg_wrong_topic, zulip_config))
        msg_not_stream = dict((self.valid_msg), type='private')
        self.assertFalse(check_zulip_message_validity(msg_not_stream, zulip_config))
        msg_from_bot = dict((self.valid_msg), sender_email=(zulip_config['email']))
        self.assertFalse(check_zulip_message_validity(msg_from_bot, zulip_config))

    def test_zulip_to_matrix(self) -> None:
        room = mock.MagicMock()
        zulip_config = self.valid_zulip_config
        send_msg = zulip_to_matrix(zulip_config, room)
        msg = dict((self.valid_msg), sender_full_name='John Smith')
        expected = {'hi':'{} hi', 
         '*hi*':'{} *hi*', 
         '**hi**':'{} **hi**'}
        for content in expected:
            send_msg(dict(msg, content=content))

        for (method, params, _), expect in zip(room.method_calls, expected.values()):
            self.assertEqual(method, 'send_text')
            self.assertEqual(params[0], expect.format('<JohnSmith>'))