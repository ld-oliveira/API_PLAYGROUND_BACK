from django import forms

class LoginForms(forms.Form):
    nome_login=forms.CharField(
        label="Login Name",
        required=True,
        max_length=70,
    )
    
    senha=forms.CharField(
        label="Senha",
        required=True,
        max_length=50,
        widget=forms.PasswordInput()
    )
    
class CadastroForms(forms.Form):
    nome_cad=forms.CharField(
        label="Login",
        required=True,
        max_length= 120,)
    
    email_cad=forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
    )
    
    senha_1=forms.CharField(
        label="Senha",
        required=True,
        max_length=50,
        widget=forms.PasswordInput()
    )
    
    senha_2=forms.CharField(
        label="Senha",
        required=True,
        max_length=50,
        widget=forms.PasswordInput()
    )
    