# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/__init__.py
# Compiled at: 2012-08-16 08:17:09
__doc__ = "This is the botnee package. You can run unit tests by running \nthe package from the command line, e.g.:\n\n$ python botnee\n\nor in ipython:\n\n>>> run botnee/__init__.py\n\nThe package is structured as follows:\n------------------------------------\n::\n\n botnee\n    \\- botnee_config             Configuration file\n    \\- debug                     some debugging helpers\n    \\- doc_store                 DocStore class, which deals with the mongodb meta data collection\n    \\- engine                    Main entry point - connects to databases and loads files\n    \\- errors                    Custom error handlers\n    \\- filters                   Class to apply filters to retrieved results\n    \\- get_related               Functions to retrieve related content by id, index or free text\n    \\- json_io                   reading of JSON files and management of mongodb connection\n    \\- process                   main processing engine\n    |   \\- data_dict                 Wrapper around standard dict for data_dict variable\n    |   \\- meta_dict                 Wrapper around standard dict for meta_dict variable\n    |   \\- text                  text processing\n    |   \\- vector_space_model    TF-IDF etc\n    \\- rss_writer                Simple RSS writer that uses WebHelpers Rss201rev2Feed\n    \\- standard_document_io      reading of standard document files\n    \\- test\n    |   \\- test_corpus           unit testing for the Corpus class\n    |   \\- test_process          unit testing for the process module\n    |   \\- test_standard_document_io\n    |   \\- test_json_io\n    \\- timeoutLock               class for timeout locking\n    \\- timer                     useful timing functions\n    \\- web\n    |   \\- manage                django management interface for web interface to botnee\n    |   \\- settings              django settings file\n    |   \\- urls                  sets up active urls\n    |   \\- interface\n    |   |   \\- models            initial loading in of data structures\n    |   |   \\- tests             unit tests\n    |   |   \\- views             code to manage view interaction (form submission etc)\n    |   \\- templates             html templates (landing pages)\n\n\nExternal dependencies\n---------------------\n::\n\n    IPython \n      \\-Debugger \n        \\-Tracer (botnee.search,botnee.debug)\n    bidict (botnee.persistent_dict)\n      \\-bidict (botnee.process.meta_dict,botnee.doc_store,botnee.process.text,botnee.process.matrix_dict,botnee.process.vector_space_model,botnee.doc_manager_store,botnee.process.data_dict,botnee.corpus)\n      \\-inverted (botnee.corpus)\n    botnee \n      \\-START_TIME (botnee.engine)\n      \\-corpus \n      | \\-Corpus (botnee.engine)\n      \\-doc_manager_store \n      | \\-DocManagerStore (botnee.engine)\n      \\-doc_store \n      | \\-DocStore (botnee.process.text,botnee.engine,botnee.process.vector_space_model)\n      \\-engine \n      | \\-Engine (botnee.web.interface.models,botnee.get_related)\n      \\-get_related \n      | \\-GetRelated (botnee.web.interface.models)\n      \\-persistent_dict \n      | \\-PersistentDict (botnee.process.data_dict,botnee.process.meta_dict,botnee.process.matrix_dict)\n      \\-process \n      | \\-data_dict \n      | | \\-DataDict (botnee.process.text,botnee.corpus,botnee.engine,botnee.process.vector_space_model)\n      | \\-matrix_dict \n      | | \\-MatrixDict (botnee.get_related,botnee.engine,botnee.process.vector_space_model)\n      | \\-meta_dict \n      | | \\-MetaDict (botnee.process.text,botnee.corpus,botnee.get_related,botnee.engine,botnee.process.vector_space_model)\n      | \\-text \n      | | \\-process_docs (botnee.engine)\n      | | \\-process_raw_text (botnee.get_related)\n      | \\-time_dict \n      | | \\-TimeDict (botnee.process.text,botnee.corpus,botnee.get_related,botnee.engine,botnee.process.vector_space_model)\n      | \\-vector_space_model \n      |   \\-vector_space_model (botnee.get_related,botnee.engine)\n      \\-standard_document \n      | \\-StandardDocument (botnee.standard_document_io,botnee.doc_store,botnee.process.text,botnee.engine,botnee.doc_manager_store)\n      \\-timeout_lock \n      | \\-TimeoutLock (botnee.web.interface.views,botnee.engine)\n      \\-web \n        \\-interface \n          \\-models \n            \\-engine (botnee.web.interface.views)\n            \\-get_related (botnee.web.interface.views)\n    bson (botnee.doc_store,botnee.get_related,botnee.doc_manager_store)\n      \\-code \n        \\-Code (botnee.doc_store,botnee.doc_manager_store)\n    dateutil \n      \\-parser (botnee.standard_document_io)\n    django \n      \\-conf \n      | \\-urls \n      |   \\-defaults \n      |     \\-include (botnee.web.urls)\n      |     \\-patterns (botnee.web.urls)\n      |     \\-url (botnee.web.urls)\n      \\-contrib \n      | \\-admin (botnee.web.urls)\n      \\-core \n      | \\-management \n      |   \\-execute_manager (botnee.web.manage)\n      \\-db \n      | \\-models (botnee.web.interface.models)\n      \\-forms (botnee.web.interface.views)\n      \\-http \n      | \\-HttpResponse (botnee.web.interface.views)\n      \\-middleware \n      | \\-gzip \n      |   \\-GZipMiddleware (botnee.web.interface.views)\n      \\-shortcuts \n      | \\-render_to_response (botnee.web.interface.views)\n      \\-template (botnee.web.interface.views)\n      \\-test \n      | \\-TestCase (botnee.web.interface.tests)\n      \\-views \n        \\-decorators \n          \\-csrf \n            \\-csrf_exempt (botnee.web.interface.views)\n    itertools \n      \\-groupby (botnee.process.vector_space_model)\n    nltk (botnee.test.test_corpus)\n    numpy (botnee.doc_store,botnee.process.text,botnee.engine,botnee.process.matrix_dict,botnee.process.vector_space_model,botnee.search,botnee.persistent_dict,botnee.json_io,botnee.filter_results,botnee.process.data_dict,botnee.corpus,botnee.get_related,botnee.debug)\n    ordereddict (botnee.persistent_dict)\n      \\-OrderedDict (botnee.process.time_dict,botnee.standard_document,botnee.process.meta_dict,botnee.process.text,botnee.process.matrix_dict,botnee.process.vector_space_model,botnee.process.data_dict,botnee.corpus)\n    pp (botnee.engine)\n    psutil (botnee.engine)\n    pymongo (botnee.doc_store,botnee.doc_manager_store)\n    scipy (botnee.process.vector_space_model)\n      \\-sparse (botnee.doc_store,botnee.engine,botnee.process.matrix_dict,botnee.search,botnee.filter_results,botnee.process.data_dict,botnee.corpus,botnee.get_related,botnee.debug)\n    setproctitle \n      \\-setproctitle (botnee.web.manage,botnee)\n    time \n      \\-asctime (botnee.engine)\n      \\-localtime (botnee.engine)\n      \\-time (botnee.doc_store,botnee.web.interface.views,botnee.process.text,botnee.process.vector_space_model,botnee.engine,botnee.doc_manager_store,botnee.corpus,botnee.debug,botnee.test.test_corpus)\n    webhelpers \n      \\-feedgenerator \n        \\-Rss201rev2Feed (botnee.rss_writer)\n\n\nCopyright 2012 BMJGroup\n\nThe name comes from the phonetic version of 'botany' [bot-n-ee] \nsince botanical nomenclature is closely linked to plant taxonomy.\n\nVersion 0.1.2\n"
import datetime, logging
from setproctitle import setproctitle
setproctitle('botnee-main')
__all__ = [
 'botnee_config',
 'debug',
 'doc_store',
 'doc_manager_store',
 'engine',
 'errors',
 'filters',
 'get_related',
 'json_io',
 'persistent_dict',
 'process',
 'rss_writer',
 'standard_document',
 'standard_document_io',
 'taxonomy',
 'test',
 'test_harness',
 'timeout_lock',
 'timer',
 'web']
import botnee_config
START_TIME = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
LOG_FILE = botnee_config.LOG_DIRECTORY + 'botnee_' + START_TIME + '.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
str_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(str_format)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
for module in __all__:
    exec 'import ' + module