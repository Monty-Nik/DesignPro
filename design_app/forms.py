from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import RoomPlan


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Применяем класс Bootstrap 'form-control' ко всем полям
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Применяем класс Bootstrap 'form-control' ко всем полям
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class RoomPlanForm(forms.ModelForm):
    class Meta:
        model = RoomPlan
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Дизайн гостиной в квартире'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите помещение, ваши пожелания по стилю, бюджету...',
                'rows': 4
            }),
        }
        labels = {
            'title': 'Название проекта',
            'description': 'Описание помещения',

        }