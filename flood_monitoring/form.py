# forms.py
from django import forms

class LocationForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter a location'}))
