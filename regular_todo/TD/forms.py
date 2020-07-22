from django import forms

class TDF(forms.Form):
    text = forms.CharField(max_length=40,
                           widget=forms.TextInput(
                               attrs={'id': 'newitem',
                                      'placeholder': 'enter',
                                      'name': 'newitem'}
                           ))