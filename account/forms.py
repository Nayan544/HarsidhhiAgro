from django import forms
from .models import AbstractUser,Vendor,ProductReview
from django.core.validators import MinLengthValidator



class Register(forms.Form):
    username = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control'}),
    )
    phone_number = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(
        max_length=100,
        validators=[MinLengthValidator(8)],
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )

class Login(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

class VendorForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone', 'address', 'message']


class ProductReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.HiddenInput())
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']