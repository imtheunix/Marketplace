from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from .models import Robos, User

User = get_user_model()


class RobosForm(forms.ModelForm):
    class Meta:
        model = Robos
        fields = (
            'nome',
            'descricao',
            'robocode',
            'robopic',
            'preco',
        )
    def __init__(self, *args, **kwargs):
        super(RobosForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].label = "Descrição"
        self.fields['robocode'].label = "Código (Formatos: .py, .js etc...)"
        self.fields['robopic'].label = "Imagem do robô"
        self.fields['preco'].label = "Preço"



class ProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = {"username", "email", "descricao_user",
                  "profilepic", "comentario", }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {"username", "email", "descricao_user",
                  "profilepic", "comentario", }
        field_classes = {"username": UsernameField}
