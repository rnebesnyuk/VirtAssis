from django.forms import CheckboxSelectMultiple, ModelForm, CharField, ModelMultipleChoiceField, SelectMultiple, TextInput, Textarea
from django.db import models

from .models import *


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["importance"].required = False


    class Meta:
        model = Note
        fields = ['name', 'description', 'importance']
        exclude = ['tags']
        widgets = {
            "description": Textarea(
                attrs={"cols": 30, "rows": 5},
            ),
        }


class EditNoteForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=SelectMultiple(attrs={'size': 5, 'class': 'wide-select'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields["tags"].required = False
        instance = kwargs.get('instance')
        if instance:
            self.fields['tags'].initial = instance.tags.all()

    def save(self, commit=True):
        note = super().save(commit=False)
        if commit:
            note.save()
            self.save_m2m()
        return note


    class Meta:
        model = Note
        fields = ['name', 'description', 'tags']
        exclude = ['tags']
        widgets = {
            "description": Textarea(
                attrs={"cols": 30, "rows": 5},
            ),
        }