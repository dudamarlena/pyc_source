# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/user_pages/lib.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 4454 bytes
from mediagoblin import mg_globals
from mediagoblin.db.base import Session
from mediagoblin.db.models import CollectionItem, Report, TextComment, MediaEntry
from mediagoblin.tools.mail import send_email
from mediagoblin.tools.pluginapi import hook_runall
from mediagoblin.tools.template import render_template
from mediagoblin.tools.translate import pass_to_ugettext as _

def send_comment_email(user, comment, media, request):
    """
    Sends comment email to user when a comment is made on their media.

    Args:
    - user: the user object to whom the email is sent
    - comment: the comment object referencing user's media
    - media: the media object the comment is about
    - request: the request
    """
    comment_url = request.urlgen('mediagoblin.user_pages.media_home.view_comment', comment=comment.id, user=media.get_actor.username, media=media.slug_or_id, qualified=True) + '#comment'
    comment_author = comment.get_actor.username
    rendered_email = render_template(request, 'mediagoblin/user_pages/comment_email.txt', {'username': user.username,  'comment_author': comment_author, 
     'comment_content': comment.content, 
     'comment_url': comment_url})
    send_email(mg_globals.app_config['email_sender_address'], [
     user.email], '{instance_title} - {comment_author} '.format(comment_author=comment_author, instance_title=mg_globals.app_config['html_title']) + _('commented on your post'), rendered_email)


def add_media_to_collection(collection, media, note=None, commit=True):
    collection_item = CollectionItem()
    collection_item.collection = collection.id
    collection_item.get_object = media
    if note:
        collection_item.note = note
    Session.add(collection_item)
    collection.num_items = collection.num_items + 1
    Session.add(collection)
    Session.add(media)
    hook_runall('collection_add_media', collection_item=collection_item)
    if commit:
        Session.commit()


def build_report_object(report_form, media_entry=None, comment=None):
    """
    This function is used to convert a form object (from a User filing a
        report) into a Report.

    :param report_form          A MediaReportForm or a CommentReportForm object
                                  with valid information from a POST request.
    :param media_entry          A MediaEntry object. The MediaEntry being repo-
                                  -rted by a Report.
    :param comment              A Comment object. The Comment being
                                  reported by a Report.

    :returns                A Report object if a valid MediaReportForm is
                              passed as kwarg media_entry. This Report has
                              not been saved.
    :returns                None if the form_dict is invalid.
    """
    report_object = Report()
    if report_form.validate() and comment is not None:
        report_object.obj = comment.comment()
        report_object.reported_user_id = TextComment.query.get(comment.id).get_actor.id
    else:
        if report_form.validate() and media_entry is not None:
            report_object.obj = media_entry
            report_object.reported_user_id = MediaEntry.query.get(media_entry.id).get_actor.id
        else:
            return
    report_object.report_content = report_form.report_reason.data
    report_object.reporter_id = report_form.reporter_id.data
    return report_object