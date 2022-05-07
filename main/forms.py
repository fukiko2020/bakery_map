from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Bakery, CustomUser, Review


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("bakery", "comment", "image")


class CreateBakeryForm(forms.ModelForm):
    class Meta:
        model = Bakery
        fields = ("name", "longitude", "latitude", "info")
