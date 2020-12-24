# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/client/logger.py
# Compiled at: 2020-03-30 11:33:28
# Size of source mod 2**32: 2148 bytes
from colorama import Fore, Back
from datetime import datetime
from time import sleep

class Logger:
    PURPLE = '\x1b[95m'
    CYAN = '\x1b[96m'
    DARKCYAN = '\x1b[36m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    END = '\x1b[0m'

    def warn(self, text: str, ask: bool=False, error_code: int=None) -> str:
        now = datetime.now()
        CLOCK = f"{Fore.BLUE}[{Fore.RESET}{Fore.GREEN}{now.strftime('%H:%M:%S')}{Fore.RESET}{Fore.BLUE}]{Fore.RESET}{self.END} "
        if not error_code:
            if not ask:
                print(self.YELLOW + '[!]' + CLOCK + self.BOLD + Fore.YELLOW + text + Fore.RESET + self.END)
                sleep(0.3)
            else:
                return self.YELLOW + '[!]' + CLOCK + self.BOLD + Fore.YELLOW + text + Fore.RESET + self.END
        elif not ask:
            print(CLOCK + f"[{error_code}] " + text)
            sleep(0.3)
        else:
            return CLOCK + f"[{error_code}] " + text

    def error(self, text: str, error_code: str=None):
        now = datetime.now()
        CLOCK = f"{Fore.BLUE}[{Fore.RESET}{Fore.GREEN}{now.strftime('%H:%M:%S')}{Fore.RESET}{Fore.BLUE}]{Fore.RESET}{self.END} "
        if not error_code:
            print(self.RED + '[!]' + CLOCK + self.BOLD + Fore.RED + text + Fore.RESET + self.END)
        else:
            if text2:
                print(self.RED + '[!]' + CLOCK + self.BOLD + Fore.RED + text + Fore.RESET + self.END)
            else:
                print(CLOCK + f"[{error_code}] " + text)

    def info(self, text: str, bold: bool=False):
        now = datetime.now()
        CLOCK = f"{Fore.BLUE}[{Fore.RESET}{Fore.GREEN}{now.strftime('%H:%M:%S')}{Fore.RESET}{Fore.BLUE}]{Fore.RESET}{self.END} "
        if bold:
            print(self.BLUE + '[+]' + CLOCK + self.BOLD + Fore.WHITE + text + Fore.RESET + self.END)
            sleep(0.3)
        else:
            print(self.BLUE + '[+]' + CLOCK + Fore.WHITE + text + Fore.RESET + self.END)
            sleep(0.3)