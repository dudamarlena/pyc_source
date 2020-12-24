# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quincy/Code/valuehorizon-people/people/models.py
# Compiled at: 2015-04-29 12:49:12
from django.db import models
from countries.models import Country

class Person(models.Model):
    """
    Represents a person, such as John Doe, Joe Public, or Jiminy Cricket.
    """
    GENDER_CHOICES = (
     ('M', 'Male'),
     ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    TITLE_CHOICES = (
     ('DR', 'Dr.'),
     ('MR', 'Mr.'),
     ('MS', 'Ms.'),
     ('MRS', 'Mrs.'),
     ('SIR', 'Sir'),
     ('LORD', 'Lord'))
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, blank=True, help_text='Middle names, comma separated')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    profile = models.TextField(blank=True, help_text='Description of Person')
    is_deceased = models.BooleanField(default=False)
    nationality = models.ManyToManyField(Country, blank=True, null=True, related_name='nationalities')
    full_name = models.CharField(max_length=255, blank=True, editable=False)
    date_modified = models.DateTimeField(null=True, blank=True, editable=False, auto_now=True)
    date_created = models.DateTimeField(null=True, blank=True, editable=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'People'
        verbose_name = 'Person'
        ordering = ['last_name', 'first_name', 'date_of_birth']

    def __unicode__(self):
        return '%s' % unicode(self.full_name)

    def age(self):
        from datetime import date
        if self.date_of_birth != None:
            today = date.today()
            dob = self.date_of_birth
            if today.month > dob.month and today.day > dob.day:
                return today.year - dob.year
            return today.year - dob.year - 1
        else:
            return
        return

    def name(self):
        """
        Return the person's name. If we have special titles, use them, otherwise,
        don't include the title.
        """
        if self.title == 'DR' or self.title == 'SIR' or self.title == 'LORD':
            return str(self.get_title_display()) + ' ' + str(self.first_name) + ' ' + str(self.last_name)
        else:
            return str(self.first_name) + ' ' + str(self.last_name)

    def get_absolute_url(self):
        return ('person_profile', (), {'person_id': self.id})

    get_absolute_url = models.permalink(get_absolute_url)

    def save(self, *args, **kwargs):
        """
        If date of death is specified, set is_deceased to true
        """
        if self.date_of_death != None:
            self.is_deceased = True
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.other_names = self.other_names.strip()
        self.full_name = str(self.name())
        self.profile = self.profile.encode('ascii', 'ignore').encode('utf8')
        super(Person, self).save(*args, **kwargs)
        return