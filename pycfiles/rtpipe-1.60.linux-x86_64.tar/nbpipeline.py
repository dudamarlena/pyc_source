# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/nbpipeline.py
# Compiled at: 2016-10-24 18:03:37
from ipywidgets import interact, FloatSlider, Text, Dropdown, Output, VBox, fixed
import pickle, os
from IPython.display import display, Javascript

class state:
    """ Jupyter notebook state attached to notebook name.
    Useful when running programatically and interactively and need to save parameters for next user.
    """

    def __init__(self, statedir):
        """ Initialize with directory to save state as files """
        self.statedir = statedir
        if not os.path.exists(self.statedir):
            os.mkdir(self.statedir)

    @property
    def objects(self):
        """ List names of stored objects """
        return os.listdir(self.statedir)

    def save(self, obj, label, format='text'):
        """ Save or update obj as pkl file with name label 

        format can be 'text' or 'pickle'.
        """
        objloc = ('{0}/{1}').format(self.statedir, label)
        with open(objloc, 'w') as (fp):
            if format == 'pickle':
                pickle.dump(obj, fp)
            elif format == 'text':
                fp.write(str(obj))
            else:
                print ('Format {0} not recognized. Please choose either pickle or text.').format(format)
        print ('Saving {0} to label {1}').format(obj, label)

    def load(self, label):
        """ Load obj with give label from hidden state directory """
        objloc = ('{0}/{1}').format(self.statedir, label)
        try:
            obj = pickle.load(open(objloc, 'r'))
        except (KeyError, IndexError, EOFError):
            obj = open(objloc, 'r').read()
            try:
                obj = float(obj)
            except ValueError:
                pass

        except IOError:
            obj = None

        return obj

    def setText(self, label, default='', description='Set Text', format='text'):
        """ Set text in a notebook pipeline (via interaction or with nbconvert) """
        obj = self.load(label)
        if obj == None:
            obj = default
            self.save(obj, label)
        textw = Text(value=obj, description=description)
        hndl = interact(self.save, obj=textw, label=fixed(label), format=fixed(format))
        return

    def setFloat(self, label, default=0, min=-20, max=20, description='Set Float', format='text'):
        """ Set float in a notebook pipeline (via interaction or with nbconvert) """
        obj = self.load(label)
        if obj == None:
            obj = default
            self.save(obj, label)
        floatw = FloatSlider(value=obj, min=min, max=max, description=description)
        hndl = interact(self.save, obj=floatw, label=fixed(label), format=fixed(format))
        return

    def setDropdown(self, label, default=None, options=[], description='Set Dropdown', format='text'):
        """ Set float in a notebook pipeline (via interaction or with nbconvert) """
        obj = self.load(label)
        if obj == None:
            obj = default
            self.save(obj, label)
        dropdownw = Dropdown(value=obj, options=options, description=description)
        hndl = interact(self.save, obj=dropdownw, label=fixed(label), format=fixed(format))
        return


def getnbname():
    """ Hack to get name of notebook as python obj 'nbname'. Does not work with 'run all' """
    display(Javascript('IPython.notebook.kernel.execute("nbname = " + "\'"+IPython.notebook.notebook_name+"\'");'))