from django import forms
from .models import Post, Comment


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter post body'}),
        }


class PostCreateForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter post body'
            }
        )
    )


class CommentCreateFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(
                attrs={

                    'class': 'form-control',
                    'rows': '4'

                })
        }
