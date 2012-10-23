from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
    
class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.CharField(max_length=100, required=False)
    password_new = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100, required=False)    
    password_old = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100, required=False) 
