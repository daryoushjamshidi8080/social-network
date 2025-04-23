from django import forms
from .models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('slug', 'body')
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter post body'}),
        }
