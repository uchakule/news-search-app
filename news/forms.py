from django import forms
from django.contrib.auth.models import User

class KeywordSearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search news...', 'class': 'form-control'})
    )

class UserForm(forms.ModelForm):
    """
    This function gives you userform of admin user only
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']    