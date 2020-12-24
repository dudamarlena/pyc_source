# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refinement.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 8540 bytes
import logging
logger = logging.getLogger(__name__)
import random
from mvc.models.properties import LabeledProperty, ListProperty, IntegerChoiceProperty, BoolProperty, ReadOnlyMixin
from mvc.models import TreeNode
from pyxrd.generic.models.event_context_manager import EventContextManager
from pyxrd.generic.models.properties import InheritableMixin
from pyxrd.generic.models import ChildModel
from .refinables.mixins import RefinementValue, RefinementGroup
from .refinables.wrapper import RefinableWrapper
from .refine_method_manager import RefineMethodManager
from .refiner import Refiner

class Refinement(ChildModel):
    __doc__ = '\n        A simple model that plugs onto the Mixture model. It provides\n        the functionality related to refinement of parameters.\n    '

    class Meta(ChildModel.Meta):
        store_id = 'Refinement'

    mixture = property(ChildModel.parent.fget, ChildModel.parent.fset)
    make_psp_plots = BoolProperty(default=False,
      text='Make parameter space plots',
      tabular=False,
      visible=True,
      persistent=True)
    refinables = ListProperty(default=None,
      text='Refinables',
      tabular=True,
      persistent=False,
      visible=True,
      data_type=RefinableWrapper,
      cast_to=None,
      widget_type='object_tree_view')
    refine_methods = None
    refine_method_index = IntegerChoiceProperty(default=0,
      text='Refinement method index',
      tabular=True,
      persistent=True,
      visible=True,
      choices={key:method.name for key, method in RefineMethodManager.get_all_methods().items()})

    @LabeledProperty(default=None,
      text='Refine options',
      persistent=False,
      visible=False,
      mix_with=(
     ReadOnlyMixin,))
    def refine_options(self):
        return self.get_refinement_method().get_options()

    @property
    def all_refine_options(self):
        return {method.index:method.get_options() for method in list(self.refine_methods.values())}

    def __init__(self, *args, **kwargs):
        my_kwargs = self.pop_kwargs(kwargs, 'refine_method_index', 'refine_method', 'refine_options')
        (super(Refinement, self).__init__)(*args, **kwargs)
        kwargs = my_kwargs
        self.refinables = TreeNode()
        self.update_refinement_treestore()
        try:
            self.refine_method_index = int(self.get_kwarg(kwargs, None, 'refine_method_index', 'refine_method'))
        except ValueError:
            self.refine_method_index = self.refine_method_index

        self.refine_methods = RefineMethodManager.initialize_methods(self.get_kwarg(kwargs, None, 'refine_options'))

    def get_refiner(self):
        """
            This returns a Refiner object which can be used to refine the
            selected properties using the selected algorithm.
            Just call 'refine(stop)' on the returned object, with stop a
            threading.Event or multiprocessing.Event which you can use to stop
            the refinement before completion.
            The Refiner object also has a RefineHistory and RefineStatus object
            that can be used to track the status and history of the refinement.
        """
        return Refiner(method=(self.get_refinement_method()),
          data_callback=(lambda : self.mixture.data_object),
          refinables=(self.refinables),
          event_cmgr=(EventContextManager(self.mixture.needs_update, self.mixture.data_changed)),
          metadata=dict(phases=(self.mixture.phases),
          num_specimens=(len(self.mixture.specimens))))

    def get_refinement_method(self):
        """
            Returns the actual refinement method by translating the 
            `refine_method` attribute
        """
        return self.refine_methods[self.refine_method_index]

    def auto_restrict(self):
        """
            Convenience function that restricts the selected properties 
            automatically by setting their minimum and maximum values.
        """
        with self.mixture.needs_update.hold():
            for node in self.refinables.iter_children():
                ref_prop = node.object
                if ref_prop.refine and ref_prop.refinable:
                    ref_prop.value_min = ref_prop.value * 0.8
                    ref_prop.value_max = ref_prop.value * 1.2

    def randomize(self):
        """
            Convenience function that randomize the selected properties.
            Respects the current minimum and maximum values.
            Executes an optimization after the randomization.
        """
        with self.mixture.data_changed.hold_and_emit():
            with self.mixture.needs_update.hold_and_emit():
                for node in self.refinables.iter_children():
                    ref_prop = node.object
                    if ref_prop.refine and ref_prop.refinable:
                        ref_prop.value = random.uniform(ref_prop.value_min, ref_prop.value_max)

    def update_refinement_treestore(self):
        """
            This creates a tree store with all refinable properties and their
            minimum, maximum and current value.
        """
        if self.parent is not None:
            self.refinables.clear()

            def add_property(parent_node, obj, prop, is_grouper):
                rp = RefinableWrapper(obj=obj, prop=prop, parent=(self.mixture), is_grouper=is_grouper)
                return parent_node.append(TreeNode(rp))

            def parse_attribute(obj, prop, root_node):
                if prop is not None:
                    if isinstance(prop, InheritableMixin):
                        value = prop.get_uninherited(obj)
                    else:
                        value = getattr(obj, prop.label)
                else:
                    value = obj
                if isinstance(value, RefinementValue):
                    new_node = add_property(root_node, value, prop, False)
                else:
                    if hasattr(value, '__iter__'):
                        for new_obj in value:
                            parse_attribute(new_obj, None, root_node)

                    else:
                        if isinstance(value, RefinementGroup):
                            if len(value.refinables) > 0:
                                new_node = add_property(root_node, value, prop, True)
                                for prop in value.refinables:
                                    parse_attribute(value, prop, new_node)

                        else:
                            new_node = add_property(root_node, obj, prop, False)

            for phase in self.mixture.project.phases:
                if phase in self.mixture.phase_matrix:
                    parse_attribute(phase, None, self.refinables)