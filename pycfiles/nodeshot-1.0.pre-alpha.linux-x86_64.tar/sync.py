# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/interop/sync/management/commands/sync.py
# Compiled at: 2014-09-24 10:02:20
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models import Q
from django.utils.module_loading import import_by_path
from nodeshot.core.layers.models import Layer
from optparse import make_option

class Command(BaseCommand):
    args = '<layer_slug layer_slug ...>'
    help = 'Synchronize external layers with the local database'
    option_list = BaseCommand.option_list + (
     make_option('--exclude', action='store', dest='exclude', default=[], help='Exclude specific layers from synchronization\n                 Supply a comma separated string of layer slugs\n                 e.g. --exclude=layer1-slug,layer2-slug,layer3-slug\n                 (works only if no layer has been specified)'),)

    def retrieve_layers(self, *args, **options):
        """
        Retrieve specified layers or all external layers if no layer specified.
        """
        queryset = Q()
        if len(args) < 1:
            all_layers = Layer.objects.published().external()
            if options['exclude']:
                exclude_list = options['exclude'].replace(' ', '').split(',')
                return all_layers.exclude(slug__in=exclude_list)
            self.verbose('no layer specified, will retrieve all layers!')
            return all_layers
        for layer_slug in args:
            queryset = queryset | Q(slug=layer_slug)
            try:
                layer = Layer.objects.get(slug=layer_slug)
                if not layer.is_external:
                    raise CommandError('Layer "%s" is not an external layer\n\r' % layer_slug)
                if not layer.is_published:
                    raise CommandError('Layer "%s" is not published. Why are you trying to work on an unpublished layer?\n\r' % layer_slug)
            except Layer.DoesNotExist:
                raise CommandError('Layer "%s" does not exist\n\r' % layer_slug)

        return Layer.objects.published().external().select_related().filter(queryset)

    def verbose(self, message):
        if self.verbosity == 2:
            self.stdout.write('%s\n\r' % message)

    def handle(self, *args, **options):
        """ execute sync command """
        self.verbosity = int(options.get('verbosity'))
        self.stdout.write('\r\n')
        layers = self.retrieve_layers(*args, **options)
        if len(layers) < 1:
            self.stdout.write('no layers to process\n\r')
            return
        else:
            self.verbose('going to process %d layers...' % len(layers))
            for layer in layers:
                try:
                    synchronizer_path = layer.external.synchronizer_path
                except (ObjectDoesNotExist, AttributeError):
                    self.stdout.write('External Layer %s does not have a synchronizer class specified\n\r' % layer.name)
                    continue

                if synchronizer_path == 'None':
                    self.stdout.write('External Layer %s does not have a synchronizer class specified\n\r' % layer.name)
                    continue
                if layer.external.config is None:
                    self.stdout.write('Layer %s does not have a config yet\n\r' % layer.name)
                    continue
                Synchronizer = import_by_path(synchronizer_path)
                self.stdout.write('imported module %s\r\n' % Synchronizer.__name__)
                try:
                    instance = Synchronizer(layer, verbosity=self.verbosity)
                    self.stdout.write('Processing layer "%s"\r\n' % layer.slug)
                    messages = instance.process()
                except ImproperlyConfigured as e:
                    self.stdout.write('Validation error: %s\r\n' % e)
                    continue

                for message in messages:
                    self.stdout.write('%s\n\r' % message)

            self.stdout.write('\r\n')
            return