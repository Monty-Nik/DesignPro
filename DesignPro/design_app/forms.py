from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, RoomPlan, Category
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q

# Валидатор для кириллицы, пробелов и дефисов
CYRILLIC_REGEX = '^[А-Яа-яёЁ\\s\\-]+$'
# Валидатор для латиницы и дефиса (для логина)
LATIN_REGEX = '^[a-zA-Z0-9\\-]+$'


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомная форма аутентификации для применения CSS-классов Bootstrap.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Логин'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации с кастомными полями и валидацией согласно ТЗ.
    """
    full_name = forms.CharField(
        label="ФИО",
        max_length=200,
        validators=[
            RegexValidator(
                regex=CYRILLIC_REGEX,
                message='ФИО должно содержать только кириллические буквы, пробелы и дефис.'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'})
    )

    username = forms.CharField(
        label="Логин",
        max_length=150,
        validators=[
            RegexValidator(
                regex=LATIN_REGEX,
                message='Логин должен содержать только латинские буквы, цифры и дефис.'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ivanov-ivan'})
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )

    agreement = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For standard UserCreationForm, the fields are usually:
        # 'username', 'password1', 'password2'

        # Update placeholders and classes for existing fields
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            })

        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Пароль'
            })

        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Подтверждение пароля'
            })

        # If you have email field
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Email'
            })


class RoomPlanForm(forms.ModelForm):
    """
    Форма создания заявки с валидацией файла.
    """

    class Meta:
        model = RoomPlan
        fields = ['title', 'description', 'category', 'plan_file']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Название (например, "Дизайн кухни")'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите ваши пожелания...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'plan_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название заявки',
            'description': 'Описание',
            'category': 'Категория',
            'plan_file': 'Файл плана или фото',
        }

    def clean_plan_file(self):
        file = self.cleaned_data.get('plan_file', False)

        if not file:
            # Поле обязательно (хотя `blank=True` в модели, форма требует)
            # В ТЗ сказано "все поля обязательны"
            raise ValidationError("Необходимо загрузить файл.")

        # Валидация размера (2MB)
        if file.size > 2 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 2 МБ.")

        # Валидация формата
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        ext = '.' + file.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise ValidationError(f"Недопустимый формат файла. Разрешены: {', '.join(valid_extensions)}")

        return file


class RoomPlanStatusForm(forms.ModelForm):
    """
    Форма для администратора/персонала для смены статуса заявки.
    Реализует условную валидацию согласно ТЗ.
    """

    class Meta:
        model = RoomPlan
        fields = ['status', 'design_image', 'admin_comment', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'design_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'admin_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Новый статус',
            'design_image': 'Файл дизайн-проекта',
            'admin_comment': 'Комментарий',
            'assigned_to': 'Назначить исполнителя (Дизайнер)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор исполнителей только дизайнерами и менеджерами
        self.fields['assigned_to'].queryset = User.objects.filter(
            Q(userprofile__user_type='DESIGNER') | Q(userprofile__user_type='MANAGER')
        ).distinct()

        # Сохраняем исходный статус
        self.initial_status = self.instance.status

    def clean(self):
        cleaned_data = super().clean()
        new_status = cleaned_data.get('status')
        design_image = cleaned_data.get('design_image')
        admin_comment = cleaned_data.get('admin_comment')

        # Запрет на изменение статуса, если он уже "В работе" или "Выполнено"
        if self.initial_status in ['IN_PROGRESS', 'COMPLETED'] and new_status != self.initial_status:
            raise ValidationError(f"Нельзя изменить статус, который уже '{self.instance.get_status_display()}'.")

        # Логика ТЗ:

        # 1. NEW -> COMPLETED
        if self.initial_status == 'NEW' and new_status == 'COMPLETED':
            if not design_image:
                self.add_error('design_image',
                               "Для смены статуса на 'Выполнено' необходимо прикрепить изображение дизайна.")

        # 2. NEW -> IN_PROGRESS
        if self.initial_status == 'NEW' and new_status == 'IN_PROGRESS':
            if not admin_comment:
                self.add_error('admin_comment',
                               "Для смены статуса на 'Принято в работу' необходимо оставить комментарий.")

        return cleaned_data

