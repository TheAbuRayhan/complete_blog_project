from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField,UserChangeForm,PasswordChangeForm
from .models import UserProfile,UserBio
class SignupForm(UserCreationForm):
    password1= forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label='Confirm password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model= User
        fields= ['username','first_name','last_name','email']
        labels= {'first_name':'First name','last_name':'Last name','email':'Email'}#in templete page- you can write {{as_p}} or {{as_table}} or {{as_ul}}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username= UsernameField(label='*User Name',widget=forms.TextInput(attrs={'class':'form-control','autofocus':True}))
    password= forms.CharField(label='*Password',widget=forms.PasswordInput(attrs={'class':'form-control'}),strip=False)
    class Meta:
        fields=['username','password']
        labels={'username':'User Name','password':'Password'}


class UserProfileChange(UserChangeForm):
    class Meta:
        model= User
        fields= ['username','first_name','last_name','email']
        labels= {'first_name':'First name','last_name':'Last name','email':'Email'}#in templete page- you can write {{as_p}} or {{as_table}} or {{as_ul}}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)
        widgets={
            'profile_pic':forms.ClearableFileInput(attrs={'class':'form-control'})
        }
class UserBioForm(forms.ModelForm):
    class Meta:
        model = UserBio
        fields = ('user_profile_bio',)
        widgets={
            'user_profile_bio':forms.TextInput(attrs={'class':'form-control'})
        }
