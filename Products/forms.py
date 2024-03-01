from django import forms
from django.contrib.auth.models import User
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text']
        widgets = {
            'title' : forms.Textarea(attrs={
                'class' : "form-control",
                "rows" : 1

            }),
            'text' : forms.Textarea(attrs={
                'class': "form-control",
                "rows": 3
            })
        }
