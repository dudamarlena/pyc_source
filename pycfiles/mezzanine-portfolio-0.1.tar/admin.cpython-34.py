# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sf_www/mezzanine/personal/heroku/personal/portfolio/admin.py
# Compiled at: 2016-12-25 14:17:39
# Size of source mod 2**32: 2522 bytes
from copy import deepcopy
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from portfolio.models import PortfolioPost, PortfolioCategory, PortfolioImage
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin, BaseTranslationModelAdmin, TabularDynamicInlineAdmin
from mezzanine.twitter.admin import TweetableAdminMixin
from mezzanine.utils.static import static_lazy as static
portfoliopost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
portfoliopost_fieldsets[0][1]['fields'].insert(1, 'categories')
portfoliopost_fieldsets[0][1]['fields'].extend(['content'])
portfoliopost_list_display = ['title', 'user', 'status', 'admin_link']
if settings.BLOG_USE_FEATURED_IMAGE:
    portfoliopost_fieldsets[0][1]['fields'].insert(-2, 'featured_image')
    portfoliopost_list_display.insert(0, 'admin_thumb')
portfoliopost_fieldsets = list(portfoliopost_fieldsets)
portfoliopost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ('categories', )

class PortfolioImageInline(TabularDynamicInlineAdmin):
    model = PortfolioImage


class PortfolioPostAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    __doc__ = '\n    Admin class for Portfolio posts.\n    '

    class Media:
        css = {'all': (static('mezzanine/css/admin/gallery.css'),)}

    fieldsets = portfoliopost_fieldsets
    list_display = portfoliopost_list_display
    list_filter = portfoliopost_list_filter
    filter_horizontal = ('categories', )
    inlines = (PortfolioImageInline,)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class PortfolioCategoryAdmin(BaseTranslationModelAdmin):
    __doc__ = '\n    Admin class for Portfolio categories. Hides itself from the admin menu\n    unless explicitly specified.\n    '
    fieldsets = (
     (
      None, {'fields': ('title', )}),)

    def has_module_permission(self, request):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for name, items in settings.ADMIN_MENU_ORDER:
            if 'Portfolio.PortfolioCategory' in items:
                return True

        return False


admin.site.register(PortfolioPost, PortfolioPostAdmin)
admin.site.register(PortfolioCategory, PortfolioCategoryAdmin)