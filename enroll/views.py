from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create your views here.

# signUp

def home(request):
    return render(request, 'enroll/home.html')

def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Acount Created Successfully!!!')
            fm = SignUpForm()
    else:
        fm = SignUpForm()

    return render(request, 'enroll/signup.html', {'form':fm})
 

# login

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/profile/')

        else:
            fm = AuthenticationForm()

        return render(request, 'enroll/userlogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')

# profile

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Profile Updated...')

        else:
            fm = EditUserProfileForm(instance=request.user)
        return render(request, 'enroll/profile.html', {'name':request.user, 'form':fm})

    else:
        return HttpResponseRedirect('/login/')
# logout

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# change password with old password

def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user = request.user, data = request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Changed Successfully')
                return HttpResponseRedirect('/profile/')

        else:
            fm = PasswordChangeForm(user=request.user)

        return render(request, 'enroll/changepass.html',{'form':fm})

    else:
        return HttpResponseRedirect('/login/')

