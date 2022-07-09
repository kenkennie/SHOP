from django import forms
from .models import Comment

class NewCommentForm(forms.ModelForm):


    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')

        # bootstrap styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)