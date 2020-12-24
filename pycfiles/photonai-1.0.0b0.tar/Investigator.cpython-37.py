# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/Investigator.py
# Compiled at: 2019-11-07 12:26:02
# Size of source mod 2**32: 5492 bytes
import os, webbrowser
from threading import Thread
from time import sleep as slp
from photonai.base.hyperpipe import Hyperpipe
from photonai.helper.helper import Singleton
import photonai.photonlogger.logger as logger
from photonai.investigator.app.main import application

class Investigator:
    __doc__ = '\n    Instantiates a Flask website that shows you the results of the hyperparameter search, the best configuration,\n    all of its performances etc.\n    '

    @staticmethod
    def __build_url(storage: str, name: str):
        """
        creates a localhost url for displaying a pipeline according to its source (working memory, file or mongodb)
        """
        url = 'http://localhost:7275/pipeline/' + storage + '/' + name
        return url

    @staticmethod
    def show(pipe: Hyperpipe):
        """
        Opens the PHOTON investigator and shows the hyperpipe's hyperparameter search performance from working space

        Parameters
        ----------
        * 'pipe' [Hyperpipe]:
            The Hyperpipe object that has performed hyperparameter search

        """
        assert isinstance(pipe, Hyperpipe), 'Investigator.show needs an object of type Hyperpipe'
        assert pipe is not None, 'Investigator.show needs an object of Hyperpipe, is None'
        assert pipe.results is not None, 'Investigator.show needs n Hyperpipe that is already optimized, so it can show the result tree'
        FlaskManager().set_pipe_object(pipe.name, pipe.results)
        Investigator.start_flask('a', pipe.name)

    @staticmethod
    def start_flask(storage, pipe_name):
        url = Investigator._Investigator__build_url(storage, pipe_name)
        logger.info('Your url is: ' + url)
        Investigator._Investigator__delayed_browser(url)
        FlaskManager().run_app()

    @staticmethod
    def load_from_db(mongo_connect_url: str, pipe_name: str):
        """
        Opens the PHOTON investigator and
        loads a hyperpipe's performance results from a MongoDB instance

        Parameters
        ---------
        * 'mongo_connect_url' [str]:
            The MongoDB connection string including the database name
        * 'pipe_name' [str]:
            The name of the pipeline to load
        """
        FlaskManager().set_mongo_db_url(mongo_connect_url)
        Investigator.start_flask('m', pipe_name)

    @staticmethod
    def load_many_from_db(mongo_connect_url: str, pipe_names: list):
        """
        Opens the PHOTON investigator and
        loads a hyperpipe performance results from a MongoDB instance

        Parameters
        ---------
        * 'mongo_connect_url' [str]:
            The MongoDB connection string including the database name
        * 'pipe_names' [list]:
            A list of the hyperpipe objects to load
        """
        FlaskManager().set_mongo_db_url(mongo_connect_url)
        for pipe in pipe_names:
            url = Investigator._Investigator__build_url('m', pipe)
            logger.info('Your url is: ' + url)

        FlaskManager().run_app()

    @staticmethod
    def load_from_file(name: str, file_url: str):
        """
        Opens the PHOTON investigator and loads the hyperpipe search results from the file path

        Parameters
        ----------
        * 'name' [str]:
            The name of the hyperpipe object that you want to load
        * 'file_url' [str]:
            The path to the file in which the hyperparameter search results are encoded.
        """
        assert os.path.isfile(file_url), 'File' + file_url + ' does not exist or is not a file. Please give absolute path.'
        FlaskManager().set_pipe_file(name, file_url)
        Investigator.start_flask('f', name)

    @staticmethod
    def __open_browser(url):
        slp(2)
        webbrowser.open(url)

    @staticmethod
    def __delayed_browser(url):
        thread = Thread(target=(Investigator._Investigator__open_browser), args=(url,))
        thread.start()
        thread.join()


@Singleton
class FlaskManager:

    def __init__(self):
        self.app = application

    def set_mongo_db_url(self, mongo_url):
        self.app.config['mongo_db_url'] = mongo_url

    def set_pipe_file(self, name, path):
        self.app.config['pipe_files'][name] = path

    def set_pipe_object(self, name, obj):
        self.app.config['pipe_objects'][name] = obj

    def run_app(self):
        try:
            self.app = application.run(host='0.0.0.0', port=7275)
        except OSError as exc:
            try:
                if exc.errno == 98:
                    pass
                else:
                    raise exc
            finally:
                exc = None
                del exc