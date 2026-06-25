from django import forms
from .models import Comment 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your comment here...', 
                'rows': 3, 
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'
                }),
        }