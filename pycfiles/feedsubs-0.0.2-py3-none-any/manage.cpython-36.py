# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/feedsubs/manage.py
# Compiled at: 2018-12-13 14:13:37
# Size of source mod 2**32: 1545 bytes
import os, sys

def main():
    if os.environ.get('DDTRACE_EXTRA_PATCH') == 'true':
        import ddtrace
        ddtrace.patch(requests=True, botocore=True, redis=True)
    try:
        from boto3.s3 import transfer
    except ImportError:
        pass
    else:

        def create_transfer_manager(*arg, **kwargs):
            return (transfer.TransferManager)(arg, **kwargs, **{'executor_cls': transfer.NonThreadedExecutor})

        transfer.create_transfer_manager = create_transfer_manager
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedsubs.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?") from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()