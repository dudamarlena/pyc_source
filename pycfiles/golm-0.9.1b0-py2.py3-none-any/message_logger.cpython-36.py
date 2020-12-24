# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/message_logger.py
# Compiled at: 2018-04-15 16:14:23
# Size of source mod 2**32: 771 bytes
from celery import shared_task

@shared_task
def on_message(uid, chat_id, message_text, dialog, from_user):
    from golm_admin.models import User, Chat, Message
    if chat_id is None:
        chat_id = uid
    user, was_created = User.objects.get_or_create(uid=uid, defaults={'uid': uid})
    if was_created:
        user.save()
    chat, was_created = Chat.objects.get_or_create(chat_id=chat_id, defaults={'chat_id':chat_id,  'user_uid':user})
    if was_created:
        chat.save()
    message = Message()
    message.chat = chat
    message.text = message_text
    message.is_from_user = from_user
    message.intent = dialog.context.get('intent', max_age=0)
    message.state = dialog.current_state_name
    message.save()