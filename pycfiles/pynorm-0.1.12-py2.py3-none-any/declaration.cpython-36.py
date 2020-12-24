# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/schema/declaration.py
# Compiled at: 2019-05-19 18:32:04
# Size of source mod 2**32: 7231 bytes
from norm.executable import NormExecutable
from norm.executable.schema.variable import VariableName
from norm.executable.schema.type import TypeName
from norm.models import Lambda, Status, PythonLambda
from typing import List
import logging
logger = logging.getLogger(__name__)

class ArgumentDeclaration(object):

    def __init__(self, variable_name, variable_type, optional=False):
        """
        The argument declaration
        :param variable_name: the name of the variable
        :type variable_name: VariableName
        :param variable_type: the type of the variable
        :type variable_type: TypeName
        :param optional: whether it is optional or not
        :type optional: bool
        """
        if not variable_type is not None:
            raise AssertionError
        elif not variable_type.lam is not None:
            raise AssertionError
        from norm.models import Variable
        self.var = Variable(variable_name.name, variable_type.lam, not optional)


class RenameArgument(object):

    def __init__(self, variable_original_name, variable_new_name):
        """
        Rename a variable
        :param variable_original_name: the original name
        :type variable_original_name: str
        :param variable_new_name: the new name
        :type variable_new_name: str
        """
        self.variable_original_name = variable_original_name
        self.variable_new_name = variable_new_name


class TypeDeclaration(NormExecutable):

    def __init__(self, type_name, argument_declarations=None, output_type_name=None):
        """
        The type declaration
        :param type_name: the type name
        :type type_name: TypeName
        :param argument_declarations: the list of argument declarations
        :type argument_declarations: List[ArgumentDeclaration]
        :param output_type_name: the type_name as output, default to boolean
        :type output_type_name: TypeName
        """
        super().__init__()
        self.type_name = type_name
        self.argument_declarations = argument_declarations
        self.output_type_name = output_type_name
        self._description = None

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        self.lam.description = value

    def compile(self, context):
        """
        Declare a type:
            * Create a type
            * Add new variable to a type # TODO
            * Modify description # TODO
            * Modify variables # TODO
        :return: the lambda
        :rtype: Lambda
        """
        lam = self.type_name.lam
        if self.output_type_name is not None:
            output_arg = ArgumentDeclaration(VariableName(None, Lambda.VAR_OUTPUT), self.output_type_name)
            if self.argument_declarations is None:
                self.argument_declarations = [
                 output_arg]
            else:
                self.argument_declarations.append(output_arg)
        else:
            if self.argument_declarations is None:
                variables = []
            else:
                variables = [var_declaration.var for var_declaration in self.argument_declarations]
        if lam is None:
            lam = Lambda(namespace=(context.context_namespace), name=(self.type_name.name))
            lam.description = self.description
            lam.variables = variables
            context.session.add(lam)
            from norm.config import cache
            cache[(context.context_namespace, self.type_name.name, None, None)] = lam
        elif not lam.status == Status.DRAFT:
            raise AssertionError
        if len(variables) > 0 and sorted((lam.variables), key=(lambda v: v.name)) != sorted(variables, key=(lambda v: v.name)):
            new_variables = {v.name:v.type_ for v in variables}
            current_variables = {v.name:v.type_ for v in lam.variables}
            lam.delete_variable([v.name for v in lam.variables if new_variables.get(v.name, None) != v.type_])
            lam.add_variable([v for v in variables if current_variables.get(v.name, None) != v.type_])
            if self.description:
                lam.description = self.description
        self.lam = lam
        return self


class AdditionalTypeDeclaration(TypeDeclaration):

    def __init__(self, type_name, argument_declarations):
        super().__init__(type_name, argument_declarations)

    def compile(self, context):
        lam = self.type_name.lam
        variables = [var_declaration.var for var_declaration in self.argument_declarations]
        if not lam.status == Status.DRAFT:
            raise AssertionError
        elif not sorted((lam.variables), key=(lambda v: v.name)) != sorted(variables, key=(lambda v: v.name)):
            raise AssertionError
        current_variables = {v.name:v.type_ for v in lam.variables}
        lam.add_variable([v for v in variables if v.name not in current_variables.keys()])
        lam.astype([v for v in variables if v.name in current_variables.keys() if current_variables.get(v.name) != v.type_])
        self.lam = lam
        return self


class RenameTypeDeclaration(TypeDeclaration):

    def __init__(self, type_name, rename_arguments):
        super().__init__(type_name)
        self.rename_arguments = rename_arguments

    def compile(self, context):
        lam = self.type_name.lam
        assert lam is not None
        variables = {rename.variable_original_name:rename.variable_new_name for rename in self.rename_arguments if rename.variable_original_name in lam}
        lam.rename_variable(variables)
        self.lam = lam
        return self


class CodeTypeDeclaration(TypeDeclaration):

    def __init__(self, type_name, code, description):
        super().__init__(type_name)
        self.code = code
        self._description = description

    def compile(self, context):
        lam = PythonLambda(context.context_namespace, self.type_name.name, self.description, self.code)
        context.session.add(lam)
        from norm.config import cache
        cache[(context.context_namespace, self.type_name.name, None, None)] = lam
        self.lam = lam
        return self