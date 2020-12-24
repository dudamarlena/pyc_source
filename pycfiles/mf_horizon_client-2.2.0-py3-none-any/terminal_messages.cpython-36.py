# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/utils/terminal_messages.py
# Compiled at: 2020-05-09 07:13:20
# Size of source mod 2**32: 481 bytes


def print_success(message: str):
    print(f"\n ✔ {message}")


def print_failure(message: str):
    print(f"\n ❌ {message}")


def print_server_error_details(error_message: str):
    print(f"\nServer Message:\n\n ==> {error_message}\n")


def print_expert_message(message: str):
    print(f"\n ⓘ  EXPERT {message}\n")


def print_update(message: str):
    print(f"\n ⓘ {message}\n")


def print_warning(message: str):
    print(f"\n ⓘ WARN: {message}\n")