# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/backup.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import click
from sentry.runner.decorators import configuration

@click.command(name='import')
@click.argument('src', type=click.File('rb'))
@configuration
def import_(src):
    """Imports data from a Sentry export."""
    from django.core import serializers
    for obj in serializers.deserialize('json', src, stream=True, use_natural_keys=True):
        obj.save()


def sort_dependencies(app_list):
    """
    Similar to Django's except that we discard the important of natural keys
    when sorting dependencies (i.e. it works without them).
    """
    from django.db.models import get_model, get_models
    model_dependencies = []
    models = set()
    for app, model_list in app_list:
        if model_list is None:
            model_list = get_models(app)
        for model in model_list:
            models.add(model)
            if hasattr(model, 'natural_key'):
                deps = getattr(model.natural_key, 'dependencies', [])
                if deps:
                    deps = [ get_model(*d.split('.')) for d in deps ]
            else:
                deps = []
            for field in model._meta.fields:
                if hasattr(field.rel, 'to'):
                    rel_model = field.rel.to
                    if rel_model != model:
                        deps.append(rel_model)

            for field in model._meta.many_to_many:
                rel_model = field.rel.to
                if rel_model != model:
                    deps.append(rel_model)

            model_dependencies.append((model, deps))

    model_dependencies.reverse()
    model_list = []
    while model_dependencies:
        skipped = []
        changed = False
        while model_dependencies:
            model, deps = model_dependencies.pop()
            found = True
            for candidate in (d not in models or d in model_list for d in deps):
                if not candidate:
                    found = False

            if found:
                model_list.append(model)
                changed = True
            else:
                skipped.append((model, deps))

        if not changed:
            raise RuntimeError("Can't resolve dependencies for %s in serialized app list." % (', ').join('%s.%s' % (model._meta.app_label, model._meta.object_name) for model, deps in sorted(skipped, key=lambda obj: obj[0].__name__)))
        model_dependencies = skipped

    return model_list


@click.command()
@click.argument('dest', default='-', type=click.File('wb'))
@click.option('--silent', '-q', default=False, is_flag=True, help='Silence all debug output.')
@click.option('--indent', default=2, help='Number of spaces to indent for the JSON output. (default: 2)')
@click.option('--exclude', default=None, help='Models to exclude from export.', metavar='MODELS')
@configuration
def export(dest, silent, indent, exclude):
    """Exports core metadata for the Sentry installation."""
    if exclude is None:
        exclude = ()
    else:
        exclude = exclude.lower().split(',')
    from django.db.models import get_apps
    from django.core import serializers

    def yield_objects():
        app_list = [ (a, None) for a in get_apps() ]
        for model in sort_dependencies(app_list):
            if not getattr(model, '__core__', True) or model.__name__.lower() in exclude or model._meta.proxy:
                if not silent:
                    click.echo('>> Skipping model <%s>' % (model.__name__,), err=True)
                continue
            queryset = model._base_manager.order_by(model._meta.pk.name)
            for obj in queryset.iterator():
                yield obj

        return

    if not silent:
        click.echo('>> Beginning export', err=True)
    serializers.serialize('json', yield_objects(), indent=indent, stream=dest, use_natural_keys=True)
    return