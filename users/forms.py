from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Character


class RegisterForm(UserCreationForm):
    character_name = forms.CharField(
        max_length=50, label='Имя персонажа',
        widget=forms.TextInput(attrs={'class': 'pixel-input'}),
    )
    class_type = forms.ChoiceField(
        choices=Character.CLASS_CHOICES, label='Класс',
        widget=forms.Select(attrs={'class': 'pixel-select'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('username', 'password1', 'password2'):
            self.fields[f].widget.attrs['class'] = 'pixel-input'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Character.objects.create(
                user=user,
                name=self.cleaned_data['character_name'],
                class_type=self.cleaned_data['class_type'],
            )
        return user
