# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/committers.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import operator, six
from sentry.api.serializers import serialize
from sentry.models import Release, ReleaseCommit, Commit, CommitFileChange, Event, Group
from sentry.api.serializers.models.commit import CommitSerializer, get_users_for_commits
from sentry.utils import metrics
from sentry.utils.safe import get_path
from django.db.models import Q
from itertools import izip
from collections import defaultdict
from functools import reduce
PATH_SEPERATORS = frozenset(['/', '\\'])

def tokenize_path(path):
    for sep in PATH_SEPERATORS:
        if sep in path:
            return reversed(filter(lambda x: x != '', path.split(sep)))
    else:
        return iter([path])


def score_path_match_length(path_a, path_b):
    score = 0
    for a, b in izip(tokenize_path(path_a), tokenize_path(path_b)):
        if a.lower() != b.lower():
            break
        score += 1

    return score


def _get_frame_paths(event):
    data = event.data
    frames = get_path(data, 'stacktrace', 'frames', filter=True)
    if frames:
        return frames
    return get_path(data, 'exception', 'values', 0, 'stacktrace', 'frames', filter=True) or []


def _get_commits(releases):
    return list(Commit.objects.filter(releasecommit=ReleaseCommit.objects.filter(release__in=releases)).select_related('author'))


def _get_commit_file_changes(commits, path_name_set):
    filenames = {next(tokenize_path(path), None) for path in path_name_set}
    filenames = {path for path in filenames if path is not None if path is not None}
    if not len(filenames):
        return []
    path_query = reduce(operator.or_, (Q(filename__iendswith=path) for path in filenames))
    commit_file_change_matches = CommitFileChange.objects.filter(path_query, commit__in=commits)
    return list(commit_file_change_matches)


def _match_commits_path(commit_file_changes, path):
    matching_commits = {}
    best_score = 1
    for file_change in commit_file_changes:
        score = score_path_match_length(file_change.filename, path)
        if score > best_score:
            best_score = score
            matching_commits = {}
        if score == best_score:
            if score == 1 and len(list(tokenize_path(file_change.filename))) > 1:
                continue
            matching_commits[file_change.commit.id] = (
             file_change.commit, score)

    return matching_commits.values()


def _get_commits_committer(commits, author_id):
    result = serialize([ commit for commit, score in commits if commit.author.id == author_id ], serializer=CommitSerializer(exclude=['author']))
    for idx, row in enumerate(result):
        row['score'] = commits[idx][1]

    return result


def _get_committers(annotated_frames, commits):
    committers = defaultdict(int)
    limit = 5
    for annotated_frame in annotated_frames:
        if limit == 0:
            break
        for commit, score in annotated_frame['commits']:
            committers[commit.author.id] += limit
            limit -= 1
            if limit == 0:
                break

    sorted_committers = sorted(committers, key=committers.get)
    users_by_author = get_users_for_commits([ c for c, _ in commits ])
    user_dicts = [ {'author': users_by_author.get(six.text_type(author_id)), 'commits': [ (commit, score) for commit, score in commits if commit.author.id == author_id ]} for author_id in sorted_committers
                 ]
    return user_dicts


def get_previous_releases(project, start_version, limit=5):
    try:
        release_dates = Release.objects.filter(organization_id=project.organization_id, version=start_version, projects=project).values('date_released', 'date_added').get()
    except Release.DoesNotExist:
        return []

    start_date = release_dates['date_released'] or release_dates['date_added']
    return list(Release.objects.filter(projects=project, organization_id=project.organization_id).extra(select={'date': 'COALESCE(date_released, date_added)'}, where=[
     'COALESCE(date_released, date_added) <= %s'], params=[
     start_date]).extra(order_by=[
     '-date'])[:limit])


def get_event_file_committers(project, event, frame_limit=25):
    Event.objects.bind_nodes([event], 'data')
    group = Group.objects.get(id=event.group_id)
    first_release_version = group.get_first_release()
    if not first_release_version:
        raise Release.DoesNotExist
    releases = get_previous_releases(project, first_release_version)
    if not releases:
        raise Release.DoesNotExist
    commits = _get_commits(releases)
    if not commits:
        raise Commit.DoesNotExist
    frames = _get_frame_paths(event) or ()
    app_frames = [ frame for frame in frames if frame['in_app'] ][-frame_limit:]
    if not app_frames:
        app_frames = [ frame for frame in frames ][-frame_limit:]
    if event.platform == 'java':
        for frame in frames:
            if frame.get('filename') is None:
                continue
            if '/' not in frame.get('filename') and frame.get('module'):
                module = frame['module'].split('.')
                module[-1] = frame['filename']
                frame['filename'] = ('/').join(module)

    path_set = {f for f in (frame.get('filename') or frame.get('abs_path') for frame in app_frames) if f if f}
    file_changes = []
    if path_set:
        file_changes = _get_commit_file_changes(commits, path_set)
    commit_path_matches = {path:_match_commits_path(file_changes, path) for path in path_set}
    annotated_frames = [ {'frame': frame, 'commits': commit_path_matches.get(frame.get('filename') or frame.get('abs_path')) or []} for frame in app_frames
                       ]
    relevant_commits = list({match for match in commit_path_matches for match in commit_path_matches[match]})
    return _get_committers(annotated_frames, relevant_commits)


def get_serialized_event_file_committers(project, event, frame_limit=25):
    committers = get_event_file_committers(project, event, frame_limit=frame_limit)
    commits = [ commit for committer in committers for commit in committer['commits'] ]
    serialized_commits = serialize([ c for c, score in commits ], serializer=CommitSerializer(exclude=['author']))
    serialized_commits_by_id = {}
    for (commit, score), serialized_commit in zip(commits, serialized_commits):
        serialized_commit['score'] = score
        serialized_commits_by_id[commit.id] = serialized_commit

    for committer in committers:
        commit_ids = [ commit.id for commit, _ in committer['commits'] ]
        committer['commits'] = [ serialized_commits_by_id[commit_id] for commit_id in commit_ids ]

    metrics.incr('feature.owners.has-committers', instance='hit' if committers else 'miss', skip_internal=False)
    return committers