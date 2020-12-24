# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/handlerMap.py
# Compiled at: 2012-01-05 21:29:21
from controllers import BaseControllers
from controllers import ShellControllers
from controllers import HalWebControllers
from controllers import cmsControllers
webapphandlers = [
 (
  '/Login', BaseControllers.LoginController),
 (
  '/Login/(.*)', BaseControllers.LoginController),
 (
  '/Logout', BaseControllers.LogoutController),
 (
  '/AddUser', BaseControllers.AddUserController),
 (
  '/WishList', BaseControllers.WishListController),
 (
  '/admin/Role', BaseControllers.RoleController),
 (
  '/admin/RoleAssociation', BaseControllers.RoleAssociationController),
 (
  '/Base/WishList', BaseControllers.WishListController),
 (
  '/Base/Invitation', BaseControllers.InvitationController),
 (
  '/admin/Shell', ShellControllers.FrontPageController),
 (
  '/admin/stat.do', ShellControllers.StatementController),
 (
  '/cms/contents', cmsControllers.CMSContentController.new_factory(op='my_contents')),
 (
  '/cms/content/(.*)', cmsControllers.CMSContentController),
 (
  '/cms/links', cmsControllers.CMSLinksController),
 (
  '/cms/tag/(.*)', cmsControllers.CMSPageController.new_factory(op='index')),
 (
  '/cms/(.*)', cmsControllers.CMSPageController.new_factory(op='view')),
 (
  '/cms/pages', cmsControllers.CMSPageController.new_factory(op='index', menu='pages')),
 (
  '/menu/(.*)', cmsControllers.MenuController.new_factory(op='view')),
 (
  '/menu', cmsControllers.MenuController),
 (
  '/', HalWebControllers.WelcomeController)]