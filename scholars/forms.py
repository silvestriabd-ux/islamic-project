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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['biography'].widget.attrs.update({
            'rows': 6
        })

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Scholar.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                "This scholar already exists in the archive."
            )

        return name
