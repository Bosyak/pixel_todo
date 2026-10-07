from django import forms
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    weekdays = forms.MultipleChoiceField(
        choices=Task.WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'pixel-checkbox'}),
        label='Дни недели',
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'difficulty', 'tags', 'weekdays',
            'duration_minutes', 'scheduled_time', 'repeat',
            'monster_sprite', 'is_group', 'shared_with',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'pixel-input'}),
            'description': forms.Textarea(
                attrs={'class': 'pixel-textarea', 'rows': 3}
            ),
            'difficulty': forms.Select(attrs={'class': 'pixel-select'}),
            'duration_minutes': forms.NumberInput(
                attrs={'class': 'pixel-input', 'min': 5, 'step': 5}
            ),
            'scheduled_time': forms.TimeInput(
                attrs={'class': 'pixel-input', 'type': 'time'}
            ),
            'repeat': forms.Select(attrs={'class': 'pixel-select'}),
            'monster_sprite': forms.Select(attrs={'class': 'pixel-select'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shared_with'].queryset = User.objects.exclude(pk=user.pk)
        if self.instance.pk and self.instance.weekdays:
            self.fields['weekdays'].initial = self.instance.weekdays
        self.fields['tags'].widget.attrs['class'] = 'pixel-select'
        self.fields['shared_with'].widget.attrs['class'] = 'pixel-select'
        self.fields['shared_with'].required = False
        self.fields['tags'].required = False

    def clean_weekdays(self):
        return [int(x) for x in self.cleaned_data.get('weekdays', [])]
