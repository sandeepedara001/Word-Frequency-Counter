from django import forms
from django.forms import ModelForm

from counter.models import website

class textField(ModelForm):
    class Meta:
        model = website
        fields = ['url']
