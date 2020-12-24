# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/__main__.py
# Compiled at: 2018-12-26 08:08:28
# Size of source mod 2**32: 903 bytes
import argparse, asyncio, logging, pykzee.PluginLoaderPlugin, pykzee.ConfigPlugin, pykzee.ManagedTree
logging.getLogger().setLevel(logging.DEBUG)
try:
    import coloredlogs
except ImportError:
    pass
else:
    coloredlogs.install(level='DEBUG')
parser = argparse.ArgumentParser()
parser.add_argument('--config', help='path to config directory', required=True)
options = parser.parse_args()

async def amain():
    shutdown = asyncio.Event()
    tree = pykzee.ManagedTree.ManagedTree()
    tree.addPlugin(pykzee.ConfigPlugin.ConfigPlugin, None, ('config', ), options.config)
    tree.addPlugin((pykzee.PluginLoaderPlugin.PluginLoaderPlugin),
      None,
      configPath=('config', 'plugins'),
      mountPath=('pluginloader', ))
    await shutdown.wait()


def main():
    asyncio.run(amain())


if __name__ == '__main__':
    main()