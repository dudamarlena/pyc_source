# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/brew_util.py
# Compiled at: 2018-04-20 03:19:42
""" brew_exts defines generic extensions to Homebrew this file
builds on those abstraction and provides Galaxy specific functionality
not useful to the brew external commands.
"""
from ..deps import brew_exts
DEFAULT_TAP = 'homebrew/science'

class HomebrewRecipe(object):

    def __init__(self, recipe, version, tap):
        self.recipe = recipe
        self.version = version
        self.tap = tap


def requirements_to_recipes(requirements):
    return filter(None, map(requirement_to_recipe, requirements))


def requirement_to_recipe(requirement):
    if requirement.type != 'package':
        return None
    else:
        recipe_name = requirement.name
        recipe_version = requirement.version
        return HomebrewRecipe(recipe_name, recipe_version, tap=DEFAULT_TAP)


def requirements_to_recipe_contexts(requirements, brew_context):

    def to_recipe_context(homebrew_recipe):
        return brew_exts.RecipeContext(homebrew_recipe.recipe, homebrew_recipe.version, brew_context)

    return map(to_recipe_context, requirements_to_recipes(requirements))