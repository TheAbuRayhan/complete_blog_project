from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from .models import UserBio
from .forms import SignupForm,LoginForm,UserProfileChange,UserBioForm
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import  UserProfileChange, ProfilePic
from django.contrib import messages
def AuthSignUp(request):
    form=SignupForm()
    if request.method=="POST":
        form= SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'congratulations!! you have become an Author.')
            return redirect('login')
    else:
        form= SignupForm()
    return render(request,'authentication/signup.html',context={'form':form})

def AuthLogIn(request):
    form=LoginForm()
    if request.method =="POST":
        form= LoginForm(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upassword=form.cleaned_data['password']
            user=authenticate(username=uname,password=upassword)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in succesfully')
                return redirect('index')
    return render(request,'authentication/login.html',context={'form':form})
def authlogout(request):
    logout(request)
    return redirect('index')
def profile(request):
    
    
    return render(request,'authentication/profile.html')


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
            messages.success(request,'Change Saved succesfully!')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'authentication/change_profile.html', context={'form':form})

@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
            messages.success(request,'Change Saved succesfully!')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'authentication/pass_change.html', context={'form':form, 'changed':changed})

@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            messages.success(request,'Change Saved succesfully!')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'authentication/pro_pic_add.html', context={'form':form})

@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Change Saved succesfully!')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'authentication/pro_pic_add.html', context={'form':form})
@login_required
def Userbio(request):
    form=UserBioForm()   
    if request.method == 'POST':
        form = UserBioForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.user=request.user
            a.save()
            messages.success(request,'Change Saved succesfully!')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'authentication/User_bio.html', context={'form':form})
@login_required
def ChangeUserbio(request):
    form=UserBioForm(instance=request.user.user_bio)   
    if request.method == 'POST':
        form = UserBioForm(request.POST, instance=request.user.user_bio)
        if form.is_valid():
            form.save()
            messages.success(request,'Change Saved succesfully!')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'authentication/User_bio.html', context={'form':form})
