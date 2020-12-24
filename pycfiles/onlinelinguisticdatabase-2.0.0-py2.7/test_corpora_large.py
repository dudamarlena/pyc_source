# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_corpora_large.py
# Compiled at: 2016-09-19 13:27:02
import logging, os, simplejson as json
from time import sleep
from nose.tools import nottest
from sqlalchemy.sql import and_
from onlinelinguisticdatabase.tests import TestController, url, get_file_size, decompress_gzip_string
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import Corpus
from subprocess import call
from onlinelinguisticdatabase.lib.SQLAQueryBuilder import SQLAQueryBuilder
log = logging.getLogger(__name__)

class TestCorporaLargeController(TestController):
    """Test the ``CorporaController`` making use of large "lorem ipsum" datasets."""

    def tearDown(self):
        pass

    @nottest
    def test_aaa_initialize(self):
        """Initialize the database using pseudo-data generated from random lorem ipsum sentences.

        These are located in ``onlinelinguisticdatabase/tests/data/corpora``.
        The data contain morphologically analyzed sentences, their component
        morphemes, and syntactic categories.  The sentences have phrase
        structure trees in bracket notation.

        The test will try to load the lorem ipsum dataset from a MySQL/SQLite
        dump file in ``onlinelinguisticdatabase/tests/data/corpora``.  If the
        dump file corresponding to ``loremipsum_path`` does not exist, it will
        import the lorem ipsum data directly from the text files and create
        the dump file so that future tests can run more speedily.  The
        ``loremipsum100_path``, ``loremipsum1000_path``, ``loremipsum10000_path``
        and ``loremipsum30000_path`` files are available and contain 100, 1000
        and 10,000 sentences, respectively.

        Setting the ``via_request`` variable to ``True`` will cause all of the
        forms to be created via request, i.e., via
        ``self.app.post(url('forms))...``.  This is much slower but may be
        desirable since values for the morphological analysis attributes
        will be generated.

        .. note::

            In order to run ``mysqldump`` with the MySQL user listed in
            ``test.ini``, that user must have permission to lock and update
            tables (alter and file privileges may also be required ...)::

                mysql -u root -p<root_password>
                grant lock tables, update on old_test.* to 'old'@'localhost';

        .. warning::

            Loading the .txt or .sql files with the ``via_request`` option set to
            ``True`` will take a very long time.  This might be an argument for
            separating the interface and logic components of the controllers so
            that a "core" HTTP-less OLD application could be exposed.  This
            would facilitate the creation of models with system-generated data
            and validation but without the HTTP overhead...

        """
        loremipsum_path = self.loremipsum100_path
        via_request = True
        self._add_SEARCH_to_web_test_valid_methods()
        application_settings = h.generate_default_application_settings()
        Session.add(application_settings)
        Session.commit()

        def create_model(line, categories, via_request=False):
            """Create a model (form or syncat) using the string in ``line``."""
            model = 'Form'
            elements = unicode(line).split('\t')
            non_empty_elements = filter(None, elements)
            try:
                ol, mb, mg, ml, sc, sx = non_empty_elements
            except Exception:
                try:
                    ol, mb, mg, ml, sc = non_empty_elements
                    sx = ''
                except Exception:
                    try:
                        model = 'SyntacticCategory'
                        n, t = non_empty_elements
                    except Exception:
                        return categories

            if via_request:
                if model == 'SyntacticCategory':
                    params = self.syntactic_category_create_params.copy()
                    params.update({'name': n, 
                       'type': t})
                    params = json.dumps(params)
                    response = self.app.post(url('syntacticcategories'), params, self.json_headers, self.extra_environ_admin)
                    cat_id = json.loads(response.body)['id']
                    categories[n] = cat_id
                else:
                    params = self.form_create_params.copy()
                    params.update({'transcription': ol, 
                       'morpheme_break': mb, 
                       'morpheme_gloss': mg, 
                       'translations': [{'transcription': ml, 'grammaticality': ''}], 'syntax': sx, 
                       'syntactic_category': categories.get(sc, '')})
                    params = json.dumps(params)
                    self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)
            elif model == 'SyntacticCategory':
                syntactic_category = model.SyntacticCategory()
                syntactic_category.name = n
                syntactic_category.type = t
                Session.add(syntactic_category)
                categories[n] = syntactic_category.id
            else:
                form = model.Form()
                form.transcription = ol
                form.morpheme_break = mb
                form.morpheme_gloss = mg
                translation = model.Translation()
                translation.transcription = ml
                form.translations.append(translation)
                form.syntax = sx
                form.syntacticcategory_id = categories.get(sc, None)
                Session.add(form)
            return categories

        def add_loremipsum_to_db(loremipsum_path, via_request=False):
            """Add the contents of the file at ``loremipsum_path`` to the database."""
            categories = {}
            with open(loremipsum_path, 'r') as (f):
                i = 0
                for l in f:
                    if i % 100 == 0:
                        if not via_request:
                            Session.commit()
                        log.debug('%d lines processed' % i)
                    i = i + 1
                    categories = create_model(l.replace('\n', ''), categories, via_request)

                Session.commit()

        loremipsum_path_no_ext = os.path.splitext(loremipsum_path)[0]
        sqlalchemy_URL = self.config['sqlalchemy.url']
        sqlalchemy_URL_list = sqlalchemy_URL.split(':')
        olddump_script_path = os.path.join(self.test_scripts_path, 'olddump.sh')
        oldload_script_path = os.path.join(self.test_scripts_path, 'oldload.sh')
        RDBMS = sqlalchemy_URL_list[0]
        if RDBMS == 'mysql':
            mysql_dump_path = '%s_mysql.sql' % loremipsum_path_no_ext
            username = sqlalchemy_URL_list[1][2:]
            password = sqlalchemy_URL_list[2].split('@')[0]
            dbname = sqlalchemy_URL_list[3].split('/')[1]
            if os.path.exists(mysql_dump_path):
                log.debug('The lorem ipsum MySQL dump file exists.  Loading it...')
                h.clear_all_models(retain=[])
                shell_script = '#!/bin/sh\nmysql -u %s -p%s %s < %s' % (
                 username, password, dbname, mysql_dump_path)
                with open(oldload_script_path, 'w') as (f):
                    f.write(shell_script)
                os.chmod(oldload_script_path, 484)
                with open(os.devnull, 'w') as (f):
                    call([oldload_script_path], stdout=f, stderr=f)
                os.remove(oldload_script_path)
                log.debug('Loaded.')
            else:
                log.debug('Have to import the lorem ipsum dataset from the text file and create the MySQL dump file.')
                add_loremipsum_to_db(loremipsum_path, via_request=via_request)
                shell_script = '#!/bin/sh\nmysqldump -u %s -p%s --single-transaction --no-create-info --result-file=%s %s' % (
                 username, password, mysql_dump_path, dbname)
                with open(olddump_script_path, 'w') as (f):
                    f.write(shell_script)
                os.chmod(olddump_script_path, 484)
                with open(os.devnull, 'w') as (f):
                    call([olddump_script_path], stdout=f, stderr=f)
                os.remove(olddump_script_path)
                log.debug('Imported and dumped.')
        elif RDBMS == 'sqlite' and h.command_line_program_installed('sqlite3'):
            sqlite_dump_path = '%s_sqlite.sql' % loremipsum_path_no_ext
            sqlite_db = sqlalchemy_URL.split('/')[(-1)]
            dbpath = os.path.join(self.here, sqlite_db)
            if os.path.exists(sqlite_dump_path):
                log.debug('The lorem ipsum SQLite dump file exists.  Loading it...')
                h.clear_all_models(retain=[])
                shell_script = '#!/bin/sh\nsqlite3 %s < %s' % (
                 dbpath, sqlite_dump_path)
                with open(oldload_script_path, 'w') as (f):
                    f.write(shell_script)
                os.chmod(oldload_script_path, 484)
                with open(os.devnull, 'w') as (f):
                    call([oldload_script_path], stdout=f, stderr=f)
                os.remove(oldload_script_path)
                log.debug('Loaded.')
            else:
                log.debug('Have to import the lorem ipsum dataset from the text file and create the SQLite dump file.')
                add_loremipsum_to_db(loremipsum_path, via_request=via_request)
                shell_script = '#!/bin/sh\nsqlite3 %s ".dump" | grep -v "^CREATE" > %s' % (
                 dbpath, sqlite_dump_path)
                with open(olddump_script_path, 'w') as (f):
                    f.write(shell_script)
                os.chmod(olddump_script_path, 484)
                with open(os.devnull, 'w') as (f):
                    call([olddump_script_path], stdout=f, stderr=f)
                os.remove(olddump_script_path)
                log.debug('Imported and dumped.')
        forms = h.get_forms()
        log.debug('Lorem ipsum data loaded.  There are now %d forms in the db.' % len(forms))
        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        Session.commit()
        a_form = Session.query(model.Form).filter(model.Form.syntactic_category.has(model.SyntacticCategory.name == 'S')).first()
        a_form_id = a_form.id
        a_form.tags.append(restricted_tag)
        Session.commit()
        restricted_form = Session.query(model.Form).filter(model.Form.tags.any(model.Tag.name == 'restricted')).first()
        assert a_form_id == restricted_form.id

    @nottest
    def test_writetofile_all_sentences(self):
        """Tests file writing/retrieval of a corpus containing all sentences.

        That is, that ``PUT /corpora/id/writetofile`` and
        ``GET /corpora/id/servefile`` both work with a corpus defined by a form
        search model that returns all sentences.

        """
        restricted_form_id = Session.query(model.Form).filter(model.Form.tags.any(model.Tag.name == 'restricted')).first().id
        tgrep2_installed = h.command_line_program_installed('tgrep2')
        query = {'filter': ['Form', 'syntactic_category', 'name', '=', 'S']}
        params = json.dumps({'name': 'Get all sentences', 
           'description': 'Query to return all sentences in the database.', 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = json.dumps({'query': query, 
           'paginator': {'page': 1, 'items_per_page': 1}})
        response = self.app.post(url('/forms/search'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        sentence_count = resp['paginator']['count']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus of sentences', 
           'description': 'No ordering, no duplicates.', 
           'form_search': form_search_id})
        params = json.dumps(params)
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert new_corpus_count == original_corpus_count + 1
        assert resp['name'] == 'Corpus of sentences'
        assert resp['description'] == 'No ordering, no duplicates.'
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == ''
        assert len(corpus.forms) == sentence_count
        assert resp['form_search']['id'] == form_search_id
        tgrep2pattern = json.dumps({'tgrep2pattern': 'S < NP-SBJ'})
        if h.command_line_program_installed('tgrep2'):
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=tgrep2pattern, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
            tgrep2resp = json.loads(response.body)
            assert tgrep2resp['error'] == 'Corpus %d has not been written to file as a treebank.'
        sleep(1)
        params = json.dumps({'format': 'treebank'})
        response = self.app.put(url('/corpora/%d/writetofile' % corpus_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp2 = json.loads(response.body)
        corpus_dir_contents = os.listdir(corpus_dir)
        corpus_tbk_path = os.path.join(corpus_dir, 'corpus_%d.tbk' % corpus_id)
        corpus_tbk_mod_time = h.get_file_modification_time(corpus_tbk_path)
        corpus_tbk_gzipped_path = '%s.gz' % corpus_tbk_path
        corpus_tbk_file_length = h.get_file_length(corpus_tbk_path)
        corpus_tbk_t2c_path = os.path.join(corpus_dir, 'corpus_%d.tbk.t2c' % corpus_id)
        corpus_file_id = resp2['files'][0]['id']
        assert resp['id'] == resp2['id']
        assert resp['name'] == resp2['name']
        assert resp2['datetime_modified'] > resp['datetime_modified']
        assert os.path.exists(corpus_tbk_path)
        if tgrep2_installed:
            assert os.path.exists(corpus_tbk_t2c_path)
        else:
            assert not os.path.exists(corpus_tbk_t2c_path)
        assert os.path.exists(corpus_tbk_gzipped_path)
        assert get_file_size(corpus_tbk_path) > get_file_size(corpus_tbk_gzipped_path)
        assert sentence_count == corpus_tbk_file_length
        corpus_file_object = open(corpus_tbk_path, 'rb')
        corpus_file_content = corpus_file_object.read()
        response = self.app.get(url('/corpora/%d/servefile/%d' % (
         corpus_id, corpus_file_id)), params, status=403, headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp == h.unauthorized_msg
        response = self.app.get(url('/corpora/%d/servefile/%d' % (
         corpus_id, corpus_file_id)), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        unzipped_corpus_file_content = decompress_gzip_string(response.body)
        assert unzipped_corpus_file_content == corpus_file_content
        assert response.content_type == 'application/x-gzip'
        query = {'filter': ['and',
                    [
                     [
                      'Form', 'syntactic_category', 'name', '=', 'S'],
                     [
                      'or',
                      [['Form', 'id', '=', restricted_form_id],
                       [
                        'Form', 'id', 'regex', '[02468]$']]]]]}
        params = json.dumps({'name': 'Get even-numbered or restricted sentences', 
           'description': 'Query to return all sentences in the database that have even-numbered ids or are restricted.', 
           'search': query})
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        form_search_id = resp['id']
        params = json.dumps({'query': query, 
           'paginator': {'page': 1, 'items_per_page': 1}})
        response = self.app.post(url('/forms/search'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        sentence_count = resp['paginator']['count']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus of even-numbered sentences', 
           'description': 'No ordering, no duplicates.', 
           'form_search': form_search_id})
        params = json.dumps(params)
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.put(url('corpus', id=corpus_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert new_corpus_count == original_corpus_count
        assert resp['name'] == 'Corpus of even-numbered sentences'
        assert resp['description'] == 'No ordering, no duplicates.'
        assert corpus_dir_contents != []
        assert response.content_type == 'application/json'
        assert resp['content'] == ''
        assert len(corpus.forms) == sentence_count
        assert resp['form_search']['id'] == form_search_id
        sleep(1)
        params = json.dumps({'format': 'treebank'})
        response = self.app.put(url('/corpora/%d/writetofile' % corpus_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp2 = json.loads(response.body)
        corpus_dir_contents = os.listdir(corpus_dir)
        corpus_tbk_path = os.path.join(corpus_dir, 'corpus_%d.tbk' % corpus_id)
        old_corpus_tbk_mod_time = corpus_tbk_mod_time
        corpus_tbk_mod_time = h.get_file_modification_time(corpus_tbk_path)
        corpus_tbk_gzipped_path = '%s.gz' % corpus_tbk_path
        corpus_tbk_file_length = h.get_file_length(corpus_tbk_path)
        corpus_tbk_t2c_path = os.path.join(corpus_dir, 'corpus_%d.tbk.t2c' % corpus_id)
        corpus_file_id = resp2['files'][0]['id']
        assert old_corpus_tbk_mod_time < corpus_tbk_mod_time
        assert len(resp2['files']) == 1
        assert resp['id'] == resp2['id']
        assert resp['name'] == resp2['name']
        assert resp2['datetime_modified'] > resp['datetime_modified']
        assert os.path.exists(corpus_tbk_path)
        assert os.path.exists(corpus_tbk_gzipped_path)
        if tgrep2_installed:
            assert os.path.exists(corpus_tbk_t2c_path)
        else:
            assert not os.path.exists(corpus_tbk_t2c_path)
        assert get_file_size(corpus_tbk_path) > get_file_size(corpus_tbk_gzipped_path)
        assert sentence_count == corpus_tbk_file_length
        corpus_file_object = open(corpus_tbk_path, 'rb')
        corpus_file_content = corpus_file_object.read()
        response = self.app.get(url('/corpora/%d/servefile/%d' % (
         corpus_id, corpus_file_id)), params, status=403, headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp == h.unauthorized_msg
        response = self.app.get(url('/corpora/%d/servefile/%d' % (
         corpus_id, corpus_file_id)), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        unzipped_corpus_file_content = decompress_gzip_string(response.body)
        assert unzipped_corpus_file_content == corpus_file_content
        sleep(1)
        params = json.dumps({'format': 'treebank'})
        response = self.app.put(url('/corpora/%d/writetofile' % corpus_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        old_resp2 = resp2
        resp2 = json.loads(response.body)
        corpus_tbk_path = os.path.join(corpus_dir, 'corpus_%d.tbk' % corpus_id)
        old_corpus_tbk_mod_time = corpus_tbk_mod_time
        corpus_tbk_mod_time = h.get_file_modification_time(corpus_tbk_path)
        assert old_corpus_tbk_mod_time < corpus_tbk_mod_time
        assert len(resp2['files']) == 1
        assert resp2['datetime_modified'] > old_resp2['datetime_modified']
        assert os.path.exists(corpus_tbk_path)
        tgrep2pattern = 'S < NP-SBJ'
        query = {'paginator': {'page': 1, 'items_per_page': 10}, 'tgrep2pattern': tgrep2pattern}
        json_query = json.dumps(query)
        response = h.command_line_program_installed('tgrep2') or self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        if not resp['error'] == 'TGrep2 is not installed.':
            raise AssertionError
        else:
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            for f in resp['items']:
                assert '(S ' in f['syntax'] and '(NP-SBJ ' in f['syntax']

            tgrep2pattern = 'S < NP-SBJ << DT'
            query['tgrep2pattern'] = tgrep2pattern
            json_query = json.dumps(query)
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            for f in resp['items']:
                assert '(S ' in f['syntax'] and '(NP-SBJ ' in f['syntax'] and '(DT ' in f['syntax']

            tgrep2pattern = 'NP-SBJ < DT . VP'
            query['tgrep2pattern'] = tgrep2pattern
            json_query = json.dumps(query)
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            match_count = resp['paginator']['count']
            for f in resp['items']:
                assert '(NP-SBJ ' in f['syntax'] and '(DT ' in f['syntax'] and '(VP ' in f['syntax']

            response = self.app.request(url(controller='corpora', action='tgrep2', id=123456789), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=404)
            resp = json.loads(response.body)
            assert resp['error'] == 'There is no corpus with id 123456789'
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_view)
            resp = json.loads(response.body)
            restricted_match_count = resp['paginator']['count']
            assert isinstance(restricted_match_count, int) and restricted_match_count < match_count
            json_query = json_query[:-1]
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=json_query, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
            resp = json.loads(response.body)
            assert resp == h.JSONDecodeErrorResponse
            tgrep2pattern = json.dumps({'TGrep2pattern': 'NP-SBJ < DT . VP'})
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=tgrep2pattern, headers=self.json_headers, environ=self.extra_environ_admin, status=400)
            resp = json.loads(response.body)
            assert resp['errors']['tgrep2pattern'] == 'A tgrep2pattern attribute must be supplied and must have a unicode/string value'
            tgrep2pattern = json.dumps({'tgrep2pattern': ''})
            response = self.app.request(url(controller='corpora', action='tgrep2', id=corpus_id), method='SEARCH', body=tgrep2pattern, headers=self.json_headers, environ=self.extra_environ_admin)
            resp = json.loads(response.body)
            assert resp == []

    @nottest
    def test_search(self):
        """Tests that corpora search works correctly.

        """
        long_sentences = Session.query(model.Form).filter(and_(model.Form.syntactic_category.has(model.SyntacticCategory.name == 'S'), model.Form.transcription.op('regexp')('^([^ ]+ ){5}[^ ]+'))).all()
        long_sentence = long_sentences[0]
        len_long_sentences = len(long_sentences)
        long_sentence_ids = [ f.id for f in long_sentences ]
        long_sentences = (',').join(map(str, long_sentence_ids))
        restricted_tag = h.get_restricted_tag()
        long_sentence.tags.append(restricted_tag)
        Session.add(long_sentence)
        Session.commit()
        name = 'Sentences with 6 or more words.'
        params = self.corpus_create_params.copy()
        params.update({'name': name, 
           'content': long_sentences})
        params = json.dumps(params)
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert new_corpus_count == original_corpus_count + 1
        assert resp['name'] == name
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == long_sentences
        assert len(corpus.forms) == len_long_sentences
        query = json.dumps({'query': {'filter': ['Form', 'transcription', 'regex', '^[AEIOUaeiou]']}, 'paginator': {'page': 1, 'items_per_page': 10}})
        response = self.app.post(url('/corpora/%d/search' % corpus_id), query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        matches = resp['items']
        assert not set([ f['id'] for f in matches ]) - set(long_sentence_ids)
        assert not filter(lambda f: f['transcription'][0].lower() not in ('a', 'e', 'i', 'o', 'u'), matches)
        assert not filter(lambda f: len(f['transcription'].split(' ')) < 6, matches)
        query = json.dumps({'query': {'filter': ['Form', 'transcription', 'like', '%']}})
        response = self.app.post(url('/corpora/%d/search' % corpus_id), query, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        assert set([ f['id'] for f in resp ]) == set(long_sentence_ids)
        query = json.dumps({'query': {'filter': ['Form', 'transcription', 'like', '%']}})
        response = self.app.post(url('/corpora/%d/search' % corpus_id), query, self.json_headers, self.extra_environ_view)
        resp2 = json.loads(response.body)
        assert len(resp) > len(resp2)
        query = json.dumps({'query': {'filter': ['Form', 'transcription', 'like', '%']}})
        response = self.app.post(url('/corpora/123456789/search'), query, self.json_headers, self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'There is no corpus with id 123456789'
        query = json.dumps({'query': {'filter': ['Form', 'thingamafracasicle', 'like', '%']}})
        response = self.app.post(url('/corpora/%d/search' % corpus_id), query, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['Form.thingamafracasicle'] == 'There is no attribute thingamafracasicle of Form'
        response = self.app.get(url(controller='corpora', action='new_search'), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp == {'search_parameters': h.get_search_parameters(SQLAQueryBuilder('Form'))}

    @nottest
    def test_writetofile_content_specified(self):
        """Tests file writing/retrieval of a corpus whose forms are specified in the ``content`` attribute.

        """
        tgrep2_installed = h.command_line_program_installed('tgrep2')
        sentences = Session.query(model.Form).filter(model.Form.syntactic_category.has(model.SyntacticCategory.name == 'S')).all()
        len_sentences = len(sentences)
        sentences = (',').join(map(str, map(lambda f: f.id, sentences)))
        long_sentences = Session.query(model.Form).filter(and_(model.Form.syntactic_category.has(model.SyntacticCategory.name == 'S'), model.Form.transcription.op('regexp')('^([^ ]+ ){5}[^ ]+'))).all()
        len_long_sentences = len(long_sentences)
        long_sentences = (',').join(map(str, map(lambda f: f.id, long_sentences)))
        content = (',').join([sentences, long_sentences, long_sentences, long_sentences])
        anticipated_length = len_sentences + 3 * len_long_sentences
        name = 'Corpus of sentences with 6+ word sentences repeated'
        description = 'Ordered by content field; duplicates of words with more than 6 words.'
        params = self.corpus_create_params.copy()
        params.update({'name': name, 
           'description': description, 
           'content': content})
        params = json.dumps(params)
        original_corpus_count = Session.query(Corpus).count()
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        corpus_id = resp['id']
        new_corpus_count = Session.query(Corpus).count()
        corpus = Session.query(Corpus).get(corpus_id)
        corpus_dir = os.path.join(self.corpora_path, 'corpus_%d' % corpus_id)
        corpus_dir_contents = os.listdir(corpus_dir)
        assert new_corpus_count == original_corpus_count + 1
        assert resp['name'] == name
        assert resp['description'] == description
        assert corpus_dir_contents == []
        assert response.content_type == 'application/json'
        assert resp['content'] == content
        assert len(corpus.forms) == len_sentences
        sleep(1)
        params = json.dumps({'format': 'treebank'})
        response = self.app.put(url('/corpora/%d/writetofile' % corpus_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp2 = json.loads(response.body)
        corpus_dir_contents = os.listdir(corpus_dir)
        corpus_tbk_path = os.path.join(corpus_dir, 'corpus_%d.tbk' % corpus_id)
        corpus_tbk_gzipped_path = '%s.gz' % corpus_tbk_path
        corpus_tbk_gzipped_size = get_file_size(corpus_tbk_gzipped_path)
        corpus_tbk_file_length = h.get_file_length(corpus_tbk_path)
        corpus_tbk_t2c_path = os.path.join(corpus_dir, 'corpus_%d.tbk.t2c' % corpus_id)
        corpus_file_id = resp2['files'][0]['id']
        assert resp['id'] == resp2['id']
        assert resp['name'] == resp2['name']
        assert resp2['datetime_modified'] > resp['datetime_modified']
        assert os.path.exists(corpus_tbk_path)
        if tgrep2_installed:
            assert os.path.exists(corpus_tbk_t2c_path)
        else:
            assert not os.path.exists(corpus_tbk_t2c_path)
        assert os.path.exists(corpus_tbk_gzipped_path)
        assert get_file_size(corpus_tbk_path) > corpus_tbk_gzipped_size
        assert anticipated_length == corpus_tbk_file_length
        corpus_file_object = open(corpus_tbk_path, 'rb')
        corpus_file_content = corpus_file_object.read()
        response = self.app.get(url('/corpora/%d/servefile/%d' % (
         corpus_id, corpus_file_id)), status=403, headers=self.json_headers, extra_environ=self.extra_environ_contrib)
        resp = json.loads(response.body)
        assert resp == h.unauthorized_msg
        response = self.app.get(url('/corpora/%d/servefile/%d' % (
         corpus_id, corpus_file_id)), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert len(response.body) < len(corpus_file_content)
        unzipped_corpus_file_content = decompress_gzip_string(response.body)
        assert unzipped_corpus_file_content == corpus_file_content
        sleep(1)
        params = json.dumps({'format': 'transcriptions only'})
        response = self.app.put(url('/corpora/%d/writetofile' % corpus_id), params, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        old_resp2 = resp2
        resp2 = json.loads(response.body)
        corpus_dir_contents = os.listdir(corpus_dir)
        corpus_TO_path = os.path.join(corpus_dir, 'corpus_%d_transcriptions.txt' % corpus_id)
        corpus_TO_gzipped_path = '%s.gz' % corpus_TO_path
        corpus_TO_gzipped_size = get_file_size(corpus_TO_gzipped_path)
        corpus_TO_file_length = h.get_file_length(corpus_TO_path)
        if tgrep2_installed:
            assert len(corpus_dir_contents) == 5
        else:
            assert len(corpus_dir_contents) == 4
        assert resp2['datetime_modified'] > old_resp2['datetime_modified']
        assert os.path.exists(corpus_TO_path)
        assert os.path.exists(corpus_TO_gzipped_path)
        assert get_file_size(corpus_TO_path) > corpus_TO_gzipped_size
        assert anticipated_length == corpus_TO_file_length
        assert os.path.exists(corpus_TO_path)
        assert os.path.exists(corpus_TO_gzipped_path)
        assert os.path.exists(corpus_tbk_path)
        assert os.path.exists(corpus_tbk_gzipped_path)
        if tgrep2_installed:
            assert os.path.exists(corpus_tbk_t2c_path)
        else:
            assert not os.path.exists(corpus_tbk_t2c_path)
        corpus_file_ids = [ cf['id'] for cf in resp2['files'] ]
        self.app.delete(url('corpus', id=corpus_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert Session.query(model.Corpus).get(corpus_id) == None
        for corpus_file_id in corpus_file_ids:
            assert Session.query(model.CorpusFile).get(corpus_file_id) == None

        assert not os.path.exists(corpus_TO_path)
        assert not os.path.exists(corpus_TO_gzipped_path)
        assert not os.path.exists(corpus_tbk_path)
        assert not os.path.exists(corpus_tbk_t2c_path)
        assert not os.path.exists(corpus_tbk_gzipped_path)
        return

    @nottest
    def test_zzz_cleanup(self):
        """Clean up after the tests."""
        h.clear_all_tables()
        h.destroy_all_directories(directory_name='users', config_filename='test.ini')
        h.destroy_all_directories(directory_name='corpora', config_filename='test.ini')
        languages = h.get_language_objects('test.ini', self.config)
        administrator = h.generate_default_administrator()
        contributor = h.generate_default_contributor()
        viewer = h.generate_default_viewer()
        Session.add_all([administrator, contributor, viewer] + languages)
        Session.commit()