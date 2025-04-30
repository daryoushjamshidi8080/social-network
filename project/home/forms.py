from django import forms


class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Search .. ',
            'class': 'form-control p-2'
        }
    ))
