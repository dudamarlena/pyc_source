# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon_cli/__init__.py
# Compiled at: 2015-11-23 22:50:28
# Size of source mod 2**32: 5291 bytes
import os

def new():
    project_name = ''
    while not project_name:
        project_name = input('Enter name for project: ')

    os.makedirs(project_name + '/adapters')
    os.mkdir(project_name + '/plugins')
    print('Created directories')
    start_file = open(project_name + '/start.py', 'w')
    start_file.write("\nimport argparse\nfrom sheldon import Sheldon\n\nparser = argparse.ArgumentParser(description='Start bot')\nparser.add_argument('--config-prefix', type=str, default='SHELDON_',\n                    help='a str from which starting all config variables')\nparser.add_argument('--adapter', type=str, default='console',\n                    help='a str with name of adapter from adapters folder'\n                         'or PyPi')\nargs = parser.parse_args()\n\nbot = Sheldon({'config-prefix': args.config_prefix,\n               'adapter': args.adapter})\n\nbot.start()\n    ")
    start_file.close()
    print('Created start.py')
    plugin_file = open(project_name + '/plugins/hello.py', 'w')
    plugin_file.write('\n"""\n# Config (valid YAML document) must be at __doc__.\nname: hello     # Name of plugin, lowercase, match with\n                # file or package name.\ndescription: "Example plugin for testing bot."\nconfig:                          # Config variable that needed to set\n  SHELDON_HELLO_REPLY: \'Hi\'      # in environment.\n                                 # You must set default values after colon.\n"""\n\nimport sheldon\nimport sheldon.utils.logger\nimport schedule\n\n\n@sheldon.hooks.message([\'hello, bot\', \'hey, bot\'])\ndef hello_message(message, bot):\n    answer = sheldon.OutgoingMessage(text=bot.config.get(\'SHELDON_HELLO_REPLY\'),\n                                     attachments=[])\n    bot.send_message(answer)\n\n\n@sheldon.hooks.command(\'hello\')\ndef hello_command(message, bot):\n    answer = sheldon.OutgoingMessage(text=bot.config.get(\'SHELDON_HELLO_REPLY\'),\n                                     attachments=[])\n    bot.send_message(answer)\n\n\n@sheldon.hooks.interval(schedule.every(5).minutes)\ndef hello_interval(bot):\n    sheldon.utils.logger.info_message(\'Hello from hello module\')\n\n\n    ')
    plugin_file.close()
    print('Created plugin file')
    adapter_file = open(project_name + '/adapters/console.py', 'w')
    adapter_file.write('\n"""\n# Config (valid YAML document) must be at __doc__.\nname: console # Name of adapter, lowercase, match with\n              # file or package name.\ndescription: "Example adapter for testing bot."\nconfig:                         # Config variable that needed to set\n  SHELDON_CONSOLE_PROMPT: \'>>>\' # in environment.\n                                # You can set default values after colon.\n"""\nfrom os import getlogin\nfrom time import sleep\nfrom random import randint\nfrom sheldon.adapter import IncomingMessage, Attachment\n\n# Code running on adapter loading may be here\n\n\ndef get_messages(bot):\n    while True:\n        # Let plugin thread end\n        sleep(1)\n        text = input(\'Enter message: \')\n\n        attachments = []\n        # For our example, attachment will be looking like:\n        # \'[type]_[path]\'\n        received_attachments = input(\n            \'Enter a comma-separated attachments\'\n            \'(<type>_<path>):\'\n        ).split(\',\')\n\n        # If user don\'t enter attachment,\n        # message_attachments will be empty\n        if received_attachments[0]:\n            for attachment in received_attachments:\n                # Parse incoming attachment:\n                # attachment_data[0] will be attachment type\n                # attachment_data[1] will be attachment path\n                attachment_data = attachment.split(\'_\')\n                if len(attachment_data) < 2:\n                    print(\'Incorrect attachment "{}"\'.format(attachment))\n                    continue\n                attachments.append(Attachment(\n                    attachment_type=attachment_data[0],\n                    attachment_path=attachment_data[1:],\n                    attachment_id=randint(1, 1000000000)  # Fake id\n                ))\n\n        yield IncomingMessage(sender=User(username=getlogin()), text=text,\n                              attachments=attachments, variables={\n                                  # Fake message id\n                                  \'console_id\': randint(1, 1000000000)\n                              })\n\n\ndef send_message(message, bot):\n    print(\'BOT: \', message.text)\n    print(\'Channel: \', message.channel)\n    print(\'Attachments:\')\n    for attachment in message.attachments:\n        print(attachment.id)\n        print(attachment.type)\n        print(attachment.path)\n        print(attachment.text)\n\n\n# Adapter must have implementation of User class.\nclass User:\n    def __init__(self, username):\n        """\n        Create new User for console adapter\n\n        :param username: name in bash session\n        :return:\n        """\n        # Adapter object should have \'id\' and \'username\' params.\n        self.id = hash(username)\n        self.username = username\n\n\n    ')
    adapter_file.close()
    print('Created adapter file')
    plugins_file = open(project_name + '/installed_plugins.txt', 'w')
    plugins_file.write('plugins.hello\n')
    plugins_file.close()
    print('Created installed plugins file')
    print('Project created')