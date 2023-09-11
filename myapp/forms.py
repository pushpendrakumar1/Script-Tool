from django import forms
from .models import TextProcessorInput

class TextProcessorForm(forms.ModelForm):
    class Meta:
        model = TextProcessorInput
        fields = ['input_text']
        # Add fields for variables here
