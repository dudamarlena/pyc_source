# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/kytosd.py
# Compiled at: 2019-08-30 11:49:50
# Size of source mod 2**32: 4232 bytes
"""Start Kytos SDN Platform core."""
import asyncio, functools, signal
from concurrent.futures import ThreadPoolExecutor
import daemon
from IPython.terminal.embed import InteractiveShellEmbed
from IPython.terminal.prompts import Prompts, Token
from traitlets.config.loader import Config
from kytos.core import Controller
from kytos.core.config import KytosConfig
from kytos.core.metadata import __version__

class KytosPrompt(Prompts):
    __doc__ = 'Configure Kytos prompt for interactive shell.'

    def in_prompt_tokens(self):
        """Kytos IPython prompt."""
        return [
         (
          Token.Prompt, 'kytos $> ')]


def start_shell(controller=None):
    """Load Kytos interactive shell."""
    kytos_ascii = '\n      _          _\n     | |        | |\n     | | ___   _| |_ ___  ___\n     | |/ / | | | __/ _ \\/ __|\n     |   <| |_| | || (_) \\__ \\\n     |_|\\_\\__,  |\\__\\___/|___/\n            __/ |\n           |___/\n    '
    banner1 = f"\x1b[95m{kytos_ascii}\x1b[0m\n    Welcome to Kytos SDN Platform!\n\n    We are making a huge effort to make sure that this console will work fine\n    but for now it's still experimental.\n\n    Kytos website.: https://kytos.io/\n    Documentation.: https://docs.kytos.io/\n    OF Address....:"
    exit_msg = 'Stopping Kytos daemon... Bye, see you!'
    if controller:
        address = controller.server.server_address[0]
        port = controller.server.server_address[1]
        banner1 += f" tcp://{address}:{port}\n"
        api_port = controller.api_server.port
        banner1 += f"    WEB UI........: http://{address}:{api_port}/\n"
        banner1 += f"    Kytos Version.: {__version__}"
    banner1 += '\n'
    cfg = Config()
    cfg.TerminalInteractiveShell.autocall = 2
    cfg.TerminalInteractiveShell.show_rewritten_input = False
    cfg.TerminalInteractiveShell.confirm_exit = False
    cfg.HistoryAccessor.enabled = False
    ipshell = InteractiveShellEmbed(config=cfg, banner1=banner1,
      exit_msg=exit_msg)
    ipshell.prompts = KytosPrompt(ipshell)
    ipshell()


def main():
    """Read config and start Kytos in foreground or daemon mode."""
    config = KytosConfig().options['daemon']
    if config.foreground:
        async_main(config)
    else:
        with daemon.DaemonContext():
            async_main(config)


def async_main(config):
    """Start main Kytos Daemon with asyncio loop."""

    def stop_controller(controller):
        """Stop the controller before quitting."""
        loop = asyncio.get_event_loop()
        loop.remove_signal_handler(signal.SIGINT)
        loop.remove_signal_handler(signal.SIGTERM)
        controller.log.info('Stopping Kytos controller...')
        controller.stop()

    async def start_shell_async():
        _start_shell = functools.partial(start_shell, controller)
        data = await loop.run_in_executor(executor, _start_shell)
        executor.shutdown()
        stop_controller(controller)
        return data

    loop = asyncio.get_event_loop()
    controller = Controller(config)
    kill_handler = functools.partial(stop_controller, controller)
    loop.add_signal_handler(signal.SIGINT, kill_handler)
    loop.add_signal_handler(signal.SIGTERM, kill_handler)
    if controller.options.debug:
        loop.set_debug(True)
    loop.call_soon(controller.start)
    if controller.options.foreground:
        executor = ThreadPoolExecutor(max_workers=1)
        loop.create_task(start_shell_async())
    try:
        try:
            loop.run_forever()
        except SystemExit as exc:
            try:
                controller.log.error(exc)
                controller.log.info('Shutting down Kytos...')
            finally:
                exc = None
                del exc

    finally:
        loop.close()