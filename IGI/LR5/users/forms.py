# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, 2009)), 
        label="Дата рождения"
    )
    
    phone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) 123-45-67'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('birth_date', 'phone')