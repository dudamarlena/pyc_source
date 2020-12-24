# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/source/ambition-edc/venv/lib/python3.7/site-packages/edc_selenium/mixins/selenium_model_form_mixin.py
# Compiled at: 2019-01-21 20:09:21
# Size of source mod 2**32: 5828 bytes
import sys
import django.apps as django_apps
from django.core.management.color import color_style
from model_mommy import mommy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.common.by import By
import selenium.webdriver.support as EC
from selenium.webdriver.support.ui import WebDriverWait
style = color_style()
SYSTEM_COLUMNS = [
 'created', 'modified', 'user_created', 'user_modified',
 'hostname_created', 'hostname_modified',
 'device_created', 'device_modified', 'revision', 'id',
 'subject_identifier_as_pk', 'subject_identifier_aka',
 'slug']

class SeleniumModelFormMixin:

    def fill_form(self, model=None, obj=None, exclude=None, values=None, save=None, save_value=None, verbose=None):
        """Fills a django modelform taking values from a given object.

        If not obj, tries to get the mommy receipe for the model.

        For example:
            self.fill_form(
                model=self.subject_screening_model,
                obj=obj, exclude=['subject_identifier', 'report_datetime'])
        """
        save = True if save is None else save
        save_value = save_value or 'Save'
        values = values or {}
        if not obj:
            sys.stdout.write(style.WARNING(f"Using mommy recipe. model={model}\n"))
            obj = (mommy.prepare_recipe)(model, **values)
        form_id = f"{model.split('.')[1]}_form"
        self.selenium.find_element_by_xpath(f"//form[@id='{form_id}']")
        fields = self.fields(model=model, exclude=exclude)
        for field in fields:
            element = None
            value = values.get(field.name) or getattr(obj, field.name)
            if verbose:
                sys.stdout.write(f"{field.name}={value}, {field.__class__.__name__}\n")
            if value:
                try:
                    if field.name.endswith('_datetime'):
                        pass
                    elif field.__class__.__name__ in ('ForeignKey', 'OneToOneField'):
                        select = Select(self.selenium.find_element_by_name(field.name))
                        select.select_by_value(str(value.id))
                        continue
                    else:
                        if field.__class__.__name__ in ('TextField', ):
                            element = self.selenium.find_element_by_xpath(f"//textarea[@name='{field.name}']")
                        else:
                            element = self.selenium.find_element_by_xpath(f"//input[@name='{field.name}']")
                except NoSuchElementException as e:
                    try:
                        sys.stdout.write(style.ERROR(f"{e}\n"))
                    finally:
                        e = None
                        del e

                else:
                    if element:
                        if verbose:
                            sys.stdout.write(f"{field.name}, {element.tag_name}, {element.get_attribute('class')})\n")
                        if field.name.endswith('_datetime'):
                            element = self.selenium.find_element_by_xpath(f"//input[@id='id_{field.name}_0']")
                            element.clear()
                            element.send_keys(value.strftime('%Y-%m-%d'))
                            element = self.selenium.find_element_by_xpath(f"//input[@id='id_{field.name}_1']")
                            element.clear()
                            element.send_keys(value.strftime('%H:%M'))
                    elif element.get_attribute('class') == 'vDateField':
                        element.clear()
                        element.send_keys(value.strftime('%Y-%m-%d'))
                    elif element.get_attribute('class') == 'radiolist':
                        for index in range(0, len(field.choices)):
                            try:
                                element = self.selenium.find_element_by_xpath(f"//input[@id='id_{field.name}_{index}']")
                            except NoSuchElementException as e:
                                try:
                                    sys.stdout.write(style.ERROR(f"{e}\n"))
                                    break
                                finally:
                                    e = None
                                    del e

                            else:
                                if element.get_attribute('value') == value:
                                    element.click()
                                    break

                    else:
                        try:
                            element.clear()
                        except InvalidElementStateException:
                            pass

                        element.send_keys(str(value))

        if save:
            element = self.selenium.find_element_by_xpath(f"//input[@value='{save_value}']")
            element.click()
        model_cls = django_apps.get_model(model)
        qs = model_cls.objects.all().order_by('modified').last()
        WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.ID, 'edc-body')))
        return qs

    def fields(self, model=None, exclude=None):
        """Returns all field classes that might be on the form.

        Use exclude to avoid unnecessarily attempting to find an element
        known not to be on the form for this case.
        """
        exclude = exclude or []
        model_cls = django_apps.get_model(model)
        fields = [f for f in model_cls._meta.fields if f.name not in SYSTEM_COLUMNS if f.editable if f.name not in exclude]
        return fields