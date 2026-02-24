from django import forms
from .models import Scholar


class ScholarSubmissionForm(forms.ModelForm):
    class Meta:
        model = Scholar
        fields = [
            'name',
            'birth_year',
            'death_year',
            'madhhab',
            'birth_place',
            'biography',
            'teachers',
            'students',
            'famous_books',
            'notable_quotes',
        ]
