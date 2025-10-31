from django import forms
from .models import Application, Category  # Исправлено: Application вместо Aplication


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Исправлено: Application вместо Aplication
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError('Размер файла не должен превышать 2MB')
            return photo