from django import forms
from models import NicheModel

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)

class AccountForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.CharField(max_length=100, required=False)
    password_new = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100, required=False)    
    password_old = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100, required=False) 

class ArticlePackForm(forms.Form):
    packfile = forms.FileField(label='Select a file')
    description = forms.CharField(label='Article pack description')
    niche = forms.ModelChoiceField(queryset = NicheModel.objects.all(), label='Articles niche')

class BlogForm(forms.Form):
    address = forms.CharField(label='Blog address')
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password')
    niche = forms.ModelChoiceField(queryset = NicheModel.objects.all(), label='Blog niche')
