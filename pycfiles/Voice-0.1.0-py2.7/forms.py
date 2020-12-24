# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/voice/forms.py
# Compiled at: 2011-09-23 13:52:46
from django import forms
from voice.models import Vote, Feature

class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        exclude = ('used_twitter', 'used_facebook')

    def clean(self):
        cleaned_data = self.cleaned_data
        feature_id = cleaned_data.get('feature')
        voter = cleaned_data.get('voter')
        vote = Vote.objects.filter(feature=feature_id, voter=voter)
        if vote.exists():
            error = '%s has already voted on this feature' % voter
            self._errors['feature'] = self._errors.get('feature', [])
            self._errors['feature'].append(error)
            raise forms.ValidationError(error)
        return cleaned_data


class FeatureForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'xxlarge', 'rows': 3}))
    voter = forms.EmailField()

    class Meta:
        model = Feature
        exclude = ('votes_needed', 'created', 'state')