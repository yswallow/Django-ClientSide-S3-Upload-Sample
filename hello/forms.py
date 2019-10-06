from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from . import models

class ProfileChangeForm(forms.ModelForm):
    class Meta():
        model = models.Account
        exclude = []
        
    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)
        print(self.fields.keys)
        self.fields['username'].widget = forms.TextInput(attrs={
            'name': 'username',
            'placeholder': 'Username'})

        self.fields['full_name'].widget = forms.TextInput(attrs={
            'name': 'full-name',
            'placeholder': 'Full name'})
        
        self.fields['avatar_url'].widget = forms.HiddenInput(attrs={
            'id': 'avatar-url',
            'name': 'avatar-url',
            'value': '/static/default.png'})