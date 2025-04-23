from django import forms
from .models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter post body'}),
        }
