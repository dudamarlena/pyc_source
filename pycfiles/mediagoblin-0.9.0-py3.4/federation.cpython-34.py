# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/federation.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 3383 bytes
from mediagoblin.db.models import Activity, Generator, User

def create_generator(request):
    """
    This creates a Generator object based on the Client associated with the
    OAuth credentials used. If the request has invalid OAuth credentials or
    no OAuth credentials None is returned.
    """
    if not hasattr(request, 'access_token'):
        return
    client = request.access_token.get_requesttoken.get_client
    generator = Generator.query.filter_by(name=client.application_name, object_type='client').first()
    if generator is None:
        generator = Generator(name=client.application_name, object_type='client')
        generator.save()
    return generator


def create_activity(verb, obj, actor, target=None, generator=None):
    """
    This will create an Activity object which for the obj if possible
    and save it. The verb should be one of the following:
        add, author, create, delete, dislike, favorite, follow
        like, post, share, unfollow, unfavorite, unlike, unshare,
        update, tag.

    If none of those fit you might not want/need to create an activity for
    the object. The list is in mediagoblin.db.models.Activity.VALID_VERBS
    """
    if verb not in Activity.VALID_VERBS:
        raise ValueError('A invalid verb type has been supplied.')
    if generator is None:
        generator = Generator.query.filter_by(name='GNU MediaGoblin').first()
        if generator is None:
            generator = Generator(name='GNU MediaGoblin', object_type='service')
            generator.save()
    obj.save(commit=False)
    activity = Activity(verb=verb)
    activity.object = obj
    if target is not None:
        activity.target = target
    activity.actor = actor.id if isinstance(actor, User) else actor
    activity.generator = generator.id
    activity.save()
    if activity.generate_content():
        activity.save()
    return activity