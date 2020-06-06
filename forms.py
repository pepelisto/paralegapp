from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Caso, Usuario_t_caso, Usuario_T_estado, Tareas, Profile, Anotacion
from bootstrap_datepicker_plus import DatePickerInput

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username',  'first_name', 'last_name', 'email', 'password1', 'password2']

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['rol', 'numero', 'year', 'tribunal']

class ValueForm(forms.ModelForm):
    class Meta:
        model = Usuario_t_caso
        fields = ['monto']


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['nombre', 'desc', 'fecha_tarea', 'fecha_plazo', 'importancia', 'comentarios']
        widgets = {
            'fecha_plazo': DatePickerInput(format='%Y-%m-%d'),
            'fecha_tarea': DatePickerInput(format='%Y-%m-%d'),
        }

class PlazoForm(forms.ModelForm):
    class Meta:
        model = Usuario_T_estado
        fields = ['plazo']
        widgets = {
            'plazo': DatePickerInput(format='%Y-%m-%d'),
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Anotacion
        fields = ['comentario']

class HorasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['horas']