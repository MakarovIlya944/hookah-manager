from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Hooker

class HookerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Hooker
        fields = UserCreationForm.Meta.fields + ('Tabaccos',)

class HookerChangeForm(UserChangeForm):
    class Meta:
        model = Hooker
        fields = UserCreationForm.Meta.fields + ('Tabaccos',)