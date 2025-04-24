from django import forms

class KeywordSearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search news...', 'class': 'form-control'})
    )