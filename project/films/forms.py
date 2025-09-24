from django import forms

from .models import Movie

class CommentForm(forms.Form):
    text = forms.CharField(max_length=500, label="Izoh", widget=forms.TextInput(
        attrs={
            "style": "width: 100%; border-radius: 20px; padding: 10px; margin: 10px;",
            "placeholder": "Izoh matni..."
        }
    ))


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ['views']
        labels = {
            "name": "Nomi",
            "description": "Tavsifi"
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "style": "width: 500px;",
                "placeholder": "Nomi",
            }),
            "description": forms.Textarea(attrs={
                "style": "width: 500px;",
                "placeholder": "Tavsifi",
            }),
        }