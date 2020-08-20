from django import forms

class CountryForm(forms.Form):
    country = forms.CharField(initial="Enter a country...", max_length=100, required=False, label="")