# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/tests/test_addons_settings.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.testing import INTEGRATION_TESTING
from collective.cover.controlpanel import ICoverSettings
from collective.nitf.controlpanel import INITFSettings
from collective.upload.interfaces import IUploadSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import unittest

class AddonsSettingsTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.nitf_settings = self.registry.forInterface(INITFSettings)
        self.wt = self.portal['portal_workflow']
        self.pm = self.portal['portal_membership']

    def test_collective_cover_available_tyles_settings(self):
        """ Tiles disponiveis no collective.cover
        """
        settings = self.registry.forInterface(ICoverSettings)
        expected = [
         'agenda',
         'audio',
         'audiogallery',
         'collective.cover.banner',
         'collective.cover.carousel',
         'collective.cover.collection',
         'collective.cover.list',
         'collective.cover.richtext',
         'standaloneheader',
         'video',
         'videogallery']
        available_tiles = settings.available_tiles
        available_tiles.sort()
        self.assertListEqual(available_tiles, expected)

    def test_collective_cover_content_type_settings(self):
        """ Tipos de conteudo buscaveis no cover
        """
        settings = self.registry.forInterface(ICoverSettings)
        allowed_types = [
         'collective.nitf.content',
         'collective.polls.poll',
         'Collection',
         'FormFolder',
         'Image',
         'Document',
         'Link']
        self.assertListEqual(settings.searchable_content_types, allowed_types)

    def test_collective_cover_styles_settings(self):
        """Tile styles available on collective.cover configuration."""
        settings = self.registry.forInterface(ICoverSettings)
        expected = {
         'Box Branco|box-branco',
         'Box Colorido|box-colorido',
         'Box Escuro|box-escuro',
         'Colunas Destacadas|colunas-destacadas',
         'Colunas Discretas|colunas-discretas',
         'Colunas Quadradas|colunas-quadradas',
         'Com Etiqueta|tile-etiqueta',
         'Com Multimidia|com-multimidia',
         'Degrade para destaque topo|topo-com-degrade',
         'Discreto|tile-discreto',
         'FAQ|tile-faq',
         'Foto destacada grande|foto-destacada-grande',
         'Foto Sobreposta Grande|foto-sobreposta-grande',
         'Foto Sobreposta Pequena|foto-sobreposta-pequena',
         'Foto Sobreposta|foto-sobreposta',
         'Fundo topo claro|fundo-topo-claro',
         'Fundo topo escuro|fundo-topo-escuro',
         'Linha destacada|linha-destacada',
         'Linha destaque topo|linha-destaquetopo',
         'Linha discreta|linha-discreta',
         'Linha recuada|linha-recuada',
         'Lista Blocos|lista-blocos',
         'Lista em Alta|tile-em-alta',
         'Noticia Destaque|tile-noticia-destaque',
         'Noticia Vinculada|tile-vinculada',
         'Tile Transparente|tile-transparente',
         'Titulo Fio Separador|fio-separador'}
        styles = list(settings.styles)
        self.assertItemsEqual(styles, expected)

    def test_collective_nitf_available_genres(self):
        """ Genres used portal wide.
        """
        available_genres = list(self.nitf_settings.available_genres)
        available_genres.sort()
        expected_genres = [
         'Analysis',
         'Archive material',
         'Current',
         'Exclusive',
         'From the Scene',
         'Interview',
         'Obituary',
         'Opinion',
         'Polls and Surveys',
         'Press Release',
         'Profile',
         'Retrospective',
         'Review',
         'Special Report',
         'Summary',
         'Wrap']
        self.assertListEqual(available_genres, expected_genres)

    def test_collective_nitf_available_sections(self):
        """ News sections defined.
        """
        available_sections = list(self.nitf_settings.available_sections)
        available_sections.sort()
        expected = [
         'Geral',
         'Notícias']
        self.assertListEqual(available_sections, expected)

    def test_collective_nitf_default_section(self):
        self.assertEqual(self.nitf_settings.default_section, 'Notícias')

    def test_collective_upload_settings(self):
        settings = self.registry.forInterface(IUploadSettings)
        self.assertEqual(settings.resize_max_width, 1024)
        self.assertEqual(settings.resize_max_height, 1024)
        self.assertEqual(settings.upload_extensions, 'gif|jpeg|jpg|png|pdf|doc|txt|docx')

    def test_sc_social_likes_settings(self):
        from sc.social.like.interfaces import ISocialLikeSettings
        settings = self.registry.forInterface(ISocialLikeSettings)
        types_expected = ('Audio', 'collective.cover.content', 'collective.nitf.content',
                          'collective.polls.poll', 'Document', 'Event', 'Image',
                          'sc.embedder')
        self.assertTupleEqual(settings.enabled_portal_types, types_expected)