from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'style': 'width: 100%; margin-bottom: 10px;'}),
            'text': forms.Textarea(attrs={
                'style': 'width: 100%; margin-bottom: 10px;', 
                'rows': 3, 
                'placeholder': 'Ваш отзыв...'
            }),
        }