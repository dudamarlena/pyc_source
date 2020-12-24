# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/annotation.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
from model import Model
from collection import Collection
import random

class Annotation(Model):

    def __init__(self, params=None):
        super(Annotation, self).__init__(params)
        self._callback_identifier = 'annotation'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'annotation/%d.json' % self.id
        else:
            return 'annotation.json'

    def get_annotation_crop_url(self, desired_zoom=None, max_size=None):
        if desired_zoom:
            return self.cropURL.replace('.jpg', '.png?zoom=%d' % desired_zoom)
        else:
            if max_size:
                return self.cropURL.replace('.jpg', '.png?max_size=%d' % max_size)
            return self.cropURL.replace('.jpg', '.png')

    def get_annotation_crop_tiled_translated(self, minx, maxx, miny, maxy, id_image, image_height, tile_size, translate):
        w_width = maxx - minx
        w_height = maxy - miny
        if translate:
            translate_x = random.randrange(-w_width / 2, w_width / 2)
            translate_y = random.randrange(-w_height / 2, w_height / 2)
            print 'translate_x: %d translate_y: %d' % (translate_x, translate_y)
            minx = minx + translate_x
            maxx = maxx + translate_x
            miny = miny + translate_y
            maxy = maxy + translate_y
        if w_width < tile_size:
            displace_x = tile_size - w_width
            minx = minx - displace_x / 2
            maxx = minx + tile_size
        if w_height < tile_size:
            displace_y = tile_size - w_height
            miny = miny - displace_y / 2
            maxy = miny + tile_size
        windowURL = 'imageinstance/%d/window-%d-%d-%d-%d.jpg' % (id_image, minx, image_height - maxy, maxx - minx, maxy - miny)
        return windowURL

    def get_annotation_alpha_crop_url(self, desired_zoom=None, max_size=None):
        if desired_zoom:
            return self.cropURL.replace('crop.jpg', 'alphamask.png?zoom=%d' % desired_zoom)
        else:
            if max_size:
                return self.cropURL.replace('crop.jpg', 'alphamask.png?max_size=%d' % max_size)
            return self.cropURL.replace('crop.jpg', 'alphamask.png')

    def get_annotation_mask_url(self, desired_zoom=None, max_size=None):
        if desired_zoom:
            return self.cropURL.replace('crop.jpg', 'mask.png?zoom=%d' % desired_zoom)
        else:
            if max_size:
                return self.cropURL.replace('crop.jpg', 'mask.png?max_size=%d' % max_size)
            return self.cropURL.replace('crop.jpg', 'mask.png')

    def __str__(self):
        return 'Annotation : ' + str(self.id)


class AnnotationUnion(Model):

    def __init__(self, params=None):
        super(AnnotationUnion, self).__init__(params)
        self._callback_identifier = 'annotationunion'

    def to_url(self):
        if self.buffer_length:
            return 'algoannotation/union.json?idUser=%d&idImage=%d&idTerm=%d&minIntersectionLength=%d&bufferLength=%d' % (self.id_user, self.id_image, self.id_term, self.min_intersection_length, self.buffer_length)
        else:
            return 'algoannotation/union.json?idUser=%d&idImage=%d&idTerm=%d&minIntersectionLength=%d' % (self.id_user, self.id_image, self.id_term, self.min_intersection_length)

    def __str__(self):
        return 'Annotation Union %d,%d,%d,%d ' % (self.id_user, self.id_image, self.id_term, self.min_intersection_length)


class AnnotationTerm(Model):

    def __init__(self, params=None):
        super(AnnotationTerm, self).__init__(params)
        self._callback_identifier = 'annotationterm'

    def to_url(self):
        if hasattr(self, 'annotation') and hasattr(self, 'term'):
            return 'annotation/%d/term/%d.json' % (self.annotation, self.term)
        if hasattr(self, 'annotation'):
            return 'annotation/%d/term.json' % self.annotation

    def __str__(self):
        return 'Annotation : ' + str(self.id)


class AlgoAnnotationTerm(AnnotationTerm):

    def __init__(self, params=None):
        super(AlgoAnnotationTerm, self).__init__(params)
        self._callback_identifier = 'algoannotationterm'


class AnnotationProperty(Model):

    def __init__(self, params=None):
        super(AnnotationProperty, self).__init__(params)
        self._callback_identifier = 'property'

    def to_url(self):
        if hasattr(self, 'domainIdent') and not hasattr(self, 'id'):
            return 'annotation/%d/property.json' % self.domainIdent
        if hasattr(self, 'domainIdent') and hasattr(self, 'id'):
            return 'annotation/%d/property/%d.json' % (self.domainIdent, self.id)

    def __str__(self):
        return 'Annotation Property %d,%d ' % (self.annotation, self.id)


class AnnotationPropertyCollection(Collection):

    def __init__(self, params=None):
        super(AnnotationPropertyCollection, self).__init__(AnnotationProperty, params)

    def to_url(self):
        if hasattr(self, 'annotation_id'):
            return 'annotation/%d/property.json' % self.annotation_id
        else:
            return
            return

    def __str__(self):
        return 'Annotation Properties'


class AnnotationCollection(Collection):

    def __init__(self, params=None):
        super(AnnotationCollection, self).__init__(Annotation, params)

    def to_url(self):
        if hasattr(self, 'project') and hasattr(self, 'term'):
            return 'term/' + str(self.term) + '/project/' + str(self.project) + '/annotation.json'
        else:
            if hasattr(self, 'project'):
                return 'project/' + str(self.project) + '/annotation.json'
            if hasattr(self, 'included') and hasattr(self, 'imageinstance'):
                return 'imageinstance/' + str(self.imageinstance) + '/annotation/' + 'included.json'
            if hasattr(self, 'user') and hasattr(self, 'imageinstance'):
                return 'user/' + str(self.user) + '/imageinstance/' + str(self.imageinstance) + '/annotation.json'
            if hasattr(self, 'imageinstance'):
                return 'imageinstance/' + str(self.imageinstance) + '/userannotation.json'
            return 'annotation.json'


class ReviewedAnnotationCollection(Collection):

    def __init__(self, params=None):
        super(ReviewedAnnotationCollection, self).__init__(Annotation, params)

    def to_url(self):
        if hasattr(self, 'project'):
            return 'project/' + str(self.project) + '/reviewedannotation.json'
        else:
            if hasattr(self, 'user') and hasattr(self, 'imageinstance'):
                return 'user/' + str(self.user) + '/imageinstance/' + str(self.imageinstance) + '/reviewedannotation.json'
            if hasattr(self, 'imageinstance'):
                return 'imageinstance/' + str(self.imageinstance) + '/reviewedannotation.json'
            return 'reviewedannotation.json'